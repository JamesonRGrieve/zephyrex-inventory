import unittest
from unittest.mock import Mock
from moving_items.move_service import MoveService


class TestMoveService(unittest.TestCase):

    def setUp(self):
        self.erp = Mock()

        self.erp.get_item.return_value = {
            "is_stock_item": 1
        }

        self.erp.get_stock_qty.return_value = 10

        self.erp.create_transfer.return_value = (
            "MAT-STE-00001"
        )

        self.service = MoveService(self.erp)

    def test_successful_move(self):
        result = self.service.move_item(
            "ITEM-001",
            "Shelf-A",
            "Box-B",
            1,
            "Test Company"
        )

        self.assertTrue(result["success"])

        self.erp.submit_transfer.assert_called_once_with(
            "MAT-STE-00001"
        )

    def test_same_warehouse(self):
        with self.assertRaises(ValueError):
            self.service.move_item(
                "ITEM-001",
                "Shelf-A",
                "Shelf-A",
                1,
                "Test Company"
            )

    def test_insufficient_stock(self):
        self.erp.get_stock_qty.return_value = 0

        with self.assertRaises(ValueError):
            self.service.move_item(
                "ITEM-001",
                "Shelf-A",
                "Box-B",
                1,
                "Test Company"
            )


if __name__ == "__main__":
    unittest.main()