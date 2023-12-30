"""Module for creating and accessing inventories."""
from .InventoryItem import InventoryItem


class BranchInventory:
    """Class for managing a specific branches inventory."""

    def __init__(self, branch_id: str):
        """Don't call outside of Branch."""
        self._branch_id = branch_id
