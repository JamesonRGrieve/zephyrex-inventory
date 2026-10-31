
import frappe

from .common import (
    validate_stock_move,
    create_stock_transfer,
)


@frappe.whitelist()
def move_serial(
    item_code,
    serial_no,
    from_warehouse,
    to_warehouse
):
    if not serial_no:
        frappe.throw("Serial Number is required.")

    item, source, destination, quantity = validate_stock_move(
        item_code,
        from_warehouse,
        to_warehouse,
        1
    )

    if not item.has_serial_no:
        frappe.throw(
            "This item does not have serial tracking enabled."
        )

    if item.has_batch_no:
        frappe.throw(
            "Items using both serial and batch tracking "
            "need a separate bundle workflow."
        )

    serial = frappe.get_doc("Serial No", serial_no)
    serial.check_permission("read")

    if serial.item_code != item.name:
        frappe.throw(
            "Serial Number does not match the Item Code."
        )

    if serial.warehouse != source.name:
        frappe.throw(
            "Serial Number is not in the source warehouse."
        )

    result = create_stock_transfer(
        item,
        source,
        destination,
        quantity,
        serial_no=serial.name
    )

    result["message"] = "Serial item moved successfully"
    return result
