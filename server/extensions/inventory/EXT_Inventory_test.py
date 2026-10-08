from zephyrex.extensions.inventory.EXT_Inventory import InventoryExtension


def test_extension_name():
    assert InventoryExtension.name == "inventory"


def test_no_models_yet():
    assert InventoryExtension.models() == []
