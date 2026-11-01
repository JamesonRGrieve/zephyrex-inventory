import frappe
from frappe.utils import flt


def require_login():
	if frappe.session.user == "Guest":
		frappe.throw("Please log in before moving items.")


def get_warehouse(warehouse_name):
	if not warehouse_name:
		frappe.throw("Warehouse is required.")

	warehouse = frappe.get_doc("Warehouse", warehouse_name)
	warehouse.check_permission("read")

	if warehouse.is_group:
		frappe.throw("Group warehouses cannot hold stock.")

	if warehouse.disabled:
		frappe.throw("Warehouse is disabled.")

	return warehouse


def validate_stock_move(item_code, from_warehouse, to_warehouse, qty):
	require_login()

	if not item_code:
		frappe.throw("Item Code is required.")

	quantity = flt(qty)

	if quantity <= 0:
		frappe.throw("Quantity must be greater than zero.")

	if not from_warehouse or not to_warehouse:
		frappe.throw("Both warehouses are required.")

	if from_warehouse == to_warehouse:
		frappe.throw("Source and destination must be different.")

	item = frappe.get_doc("Item", item_code)
	item.check_permission("read")

	if not item.is_stock_item:
		frappe.throw("Item is not a stock item.")

	if item.disabled:
		frappe.throw("Item is disabled.")

	source = get_warehouse(from_warehouse)
	destination = get_warehouse(to_warehouse)

	if source.company != destination.company:
		frappe.throw("Warehouses must belong to the same company.")

	return item, source, destination, quantity


def create_stock_transfer(item, source, destination, quantity, serial_no=None):
	row = {
		"item_code": item.name,
		"qty": quantity,
		"s_warehouse": source.name,
		"t_warehouse": destination.name,
	}

	if serial_no:
		if not frappe.db.get_single_value("Stock Settings", "use_serial_batch_fields"):
			frappe.throw("Enable Use Serial / Batch Fields in ERPNext Stock Settings.")

		row["serial_no"] = serial_no
		row["use_serial_batch_fields"] = 1

	stock_entry = frappe.get_doc(
		{
			"doctype": "Stock Entry",
			"stock_entry_type": "Material Transfer",
			"purpose": "Material Transfer",
			"company": source.company,
			"from_warehouse": source.name,
			"to_warehouse": destination.name,
			"items": [row],
		}
	)

	stock_entry.insert()
	stock_entry.submit()

	return {
		"success": True,
		"stock_entry": stock_entry.name,
		"item_code": item.name,
		"from_warehouse": source.name,
		"to_warehouse": destination.name,
		"qty": quantity,
		"serial_no": serial_no,
		"operator": frappe.session.user,
	}


def get_asset(asset_id):
	require_login()

	if not asset_id:
		frappe.throw("Asset ID is required.")

	asset = frappe.get_doc("Asset", asset_id)
	asset.check_permission("read")

	if asset.docstatus != 1:
		frappe.throw("Asset must be submitted first.")

	return asset


def create_asset_movement(asset, purpose, details):
	movement = frappe.get_doc(
		{
			"doctype": "Asset Movement",
			"purpose": purpose,
			"company": asset.company,
			"assets": [
				{
					"asset": asset.name,
					**details,
				}
			],
		}
	)

	movement.insert()
	movement.submit()

	return {
		"success": True,
		"asset_id": asset.name,
		"movement_id": movement.name,
		"purpose": purpose,
		"operator": frappe.session.user,
	}
