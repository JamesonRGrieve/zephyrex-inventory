
import frappe


@frappe.whitelist()
def move_serial(item_code, serial_no, from_warehouse, to_warehouse):
    """Move one serialized stock item to another warehouse."""

    if not all([item_code, serial_no, from_warehouse, to_warehouse]):
        frappe.throw("All fields are required.")

    if from_warehouse == to_warehouse:
        frappe.throw("Source and destination cannot be the same.")

    item = frappe.get_doc("Item", item_code)
    serial = frappe.get_doc("Serial No", serial_no)

    if not item.has_serial_no:
        frappe.throw("The item does not use serial numbers.")

    if serial.item_code != item_code:
        frappe.throw("Serial number does not match this item.")

    if serial.warehouse != from_warehouse:
        frappe.throw("Serial number is not in the source warehouse.")

    for name in (from_warehouse, to_warehouse):
        warehouse = frappe.get_doc("Warehouse", name)

        if warehouse.is_group:
            frappe.throw("Group warehouses cannot hold stock.")

    company = frappe.db.get_value(
        "Warehouse", from_warehouse, "company"
    )

    if company != frappe.db.get_value(
        "Warehouse", to_warehouse, "company"
    ):
        frappe.throw("Warehouses must belong to the same company.")

    # Uses ERPNext's legacy serial field compatibility mode.
    if not frappe.db.get_single_value(
        "Stock Settings", "use_serial_batch_fields"
    ):
        frappe.throw(
            "Enable Use Serial / Batch Fields in Stock Settings "
            "before using this transfer."
        )

    stock_entry = frappe.get_doc({
        "doctype": "Stock Entry",
        "stock_entry_type": "Material Transfer",
        "purpose": "Material Transfer",
        "company": company,
        "items": [{
            "item_code": item_code,
            "qty": 1,
            "s_warehouse": from_warehouse,
            "t_warehouse": to_warehouse,
            "serial_no": serial_no,
            "use_serial_batch_fields": 1
        }]
    })

    stock_entry.insert()
    stock_entry.submit()

    return {
        "success": True,
        "message": "Serial item moved successfully",
        "stock_entry": stock_entry.name,
        "item_code": item_code,
        "serial_no": serial_no,
        "from_warehouse": from_warehouse,
        "to_warehouse": to_warehouse
    }
