from extensions.inventory.EXT_Inventory import InventoryExtension


def test_extension_name():
    assert InventoryExtension.name == "inventory"

    print(f"\nExtension Name: {InventoryExtension.name}")

def test_no_models_yet():
    assert InventoryExtension.models() == []

    print(f"\nExtension Name: {InventoryExtension.models}")
