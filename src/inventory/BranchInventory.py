# Author: Dina Hassanein (22066792)
"""Module for creating and accessing inventories."""
from .InventoryItem import InventoryItem
from ..utils.Database import Database
from ..user.ActiveUser import ActiveUser
from src.utils.errors import AlreadyExistsError, InputError
from .utils import validate_item_name


class BranchInventory:
    """Class for managing a specific branches inventory."""

    def __init__(self, branch_id: str):
        """Don't call outside of Branch."""
        self._branch_id = branch_id

    def create(self, name: str, quantity: int,
               threshold: int) -> InventoryItem:
        """
        Create a new inventory item using the given parameters.

        A record of the created item is added to the database.

        :raises AuthorizationError: If active user does not have permission.
        """
        ActiveUser.get().raise_without_permission("inventory.create")

        if not validate_item_name(name):
            raise InputError("Invalid item name.")

        check = Database.execute_and_fetchone("SELECT id from public.inventory\
                                               WHERE name = %s", name)
        if check is not None:
            raise AlreadyExistsError("An item with this name already exists.")

        sql = "INSERT INTO public.inventory (name, quantity, threshold,\
              branch_id) VALUES(%s, %s, %s, %s) RETURNING id"

        cursor = Database.execute(
            sql, name, quantity, threshold, self._branch_id)
        Database.commit()
        result = cursor.fetchone()
        assert result is not None
        id = result[0]

        return InventoryItem(id)

    def get_by_name(self, name: str) -> InventoryItem | None:
        """
        Get an inventory item by its name.

        Note: This is not limited to this branch.
        """
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.inventory WHERE name = %s \
            AND branch_id = %s;", name, self._branch_id)

        if result is not None:
            return InventoryItem(result[0])

    def get_all(self) -> list[InventoryItem]:
        """Get all inventory items at the branch."""
        result = Database.execute_and_fetchall(
            "SELECT id FROM public.inventory WHERE branch_id = %s;",
            self._branch_id)

        return [InventoryItem(record[0]) for record in result]
