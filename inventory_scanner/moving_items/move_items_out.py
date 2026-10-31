
import frappe

from .common import (
    validate_stock_move,
    create_stock_transfer,
)


@frappe.whitelist()
def move_items_out(
    from_warehouse,
    item_code,
    to_warehouse,
    qty=1
):
    item, source, destination, quantity = validate_stock_move(
        item_code,
        from_warehouse,
        to_warehouse,
        qty
    )

    if item.has_serial_no or item.has_batch_no:
        frappe.throw(
            "Use the serial/batch movement workflow "
            "for serialized or batched items."
        )

    result = create_stock_transfer(
        item,
        source,
        destination,
        quantity
    )

    result["message"] = "Items moved out successfully"
    return result
