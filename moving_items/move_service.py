from decimal import Decimal


class MoveService:
    def __init__(self, erp_client):
        self.erp = erp_client

    def move_item(
        self,
        item_code,
        source_warehouse,
        destination_warehouse,
        quantity,
        company
    ):
        qty = Decimal(str(quantity))

        if qty <= 0:
            raise ValueError(
                "Quantity must be greater than zero"
            )

        if source_warehouse == destination_warehouse:
            raise ValueError(
                "Source and destination cannot be the same"
            )

        item = self.erp.get_item(item_code)

        if item.get("is_stock_item") != 1:
            raise ValueError(
                "Item is not stock-managed"
            )

        available = Decimal(str(
            self.erp.get_stock_qty(
                item_code,
                source_warehouse
            )
        ))

        if available < qty:
            raise ValueError(
                "Insufficient stock at source warehouse"
            )

        entry_name = self.erp.create_transfer(
            item_code,
            source_warehouse,
            destination_warehouse,
            float(qty),
            company
        )

        self.erp.submit_transfer(entry_name)

        return {
            "success": True,
            "item_code": item_code,
            "source": source_warehouse,
            "destination": destination_warehouse,
            "quantity": float(qty),
            "stock_entry": entry_name
        }