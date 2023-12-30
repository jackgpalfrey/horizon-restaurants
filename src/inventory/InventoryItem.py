"""Module for handling specific inventories."""
from ..utils.Database import Database


class InventoryItem:
    """Class to manage a specific reservation."""

    def __init__(self, item_id: str):
        """Don't call outside of BranchInventory."""
        self._item_id = item_id

    def get_name(self) -> str:
        """Get inventory item's name."""
        result = Database.execute_and_fetchone(
            "SELECT name FROM public.inventory WHERE id = %s",
            self._item_id)

        assert result is not None
        return result[0]
