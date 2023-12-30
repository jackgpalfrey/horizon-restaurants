"""Module for handling specific inventories."""


class InventoryItem:
    """Class to manage a specific reservation."""

    def __init__(self, item_id: str):
        """Don't call outside of BranchInventory."""
        self._item_id = item_id
