"""Module for managing individual menu items."""


from src.utils.Database import Database


class MenuItem:
    """Class for managing individual menu items."""

    def __init__(self, item_id: str):
        """Don't call outside of BranchMenu."""
        self._item_id = item_id

    def get_id(self):
        """Get item ID."""
        return self._item_id

    def get_name(self) -> str | None:
        """Get item name."""
        sql = "SELECT name FROM public.menuitem WHERE id=%s;"
        result = Database.execute_and_fetchone(sql, self._item_id)

        if result is not None:
            return result[0]
