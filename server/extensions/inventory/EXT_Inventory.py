"""inventory extension definition."""

from typing import ClassVar, List, Type

from zephyrex.extensions.AbstractExtensionProvider import (
    AbstractStaticExtension,
)


class InventoryExtension(AbstractStaticExtension):
    name: ClassVar[str] = "inventory"
    description: ClassVar[str] = "Parts and asset tracking on top of ERPNext."
    extension_dependencies: ClassVar[List[str]] = []

    @classmethod
    def models(cls) -> List[Type]:
        from zephyrex.extensions.inventory.BLL_Inventory import ALL_MODELS

        return list(ALL_MODELS)
