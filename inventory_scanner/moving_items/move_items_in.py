import frappe

from .common import (
	create_stock_transfer,
	validate_stock_move,
)


@frappe.whitelist()
def move_items_in(to_warehouse, item_code, from_warehouse, qty=1):
	item, source, destination, quantity = validate_stock_move(item_code, from_warehouse, to_warehouse, qty)

	if item.has_serial_no or item.has_batch_no:
		frappe.throw("Use the serial/batch movement workflow for serialized or batched items.")

	result = create_stock_transfer(item, source, destination, quantity)

	result["message"] = "Items moved in successfully"
	return result
