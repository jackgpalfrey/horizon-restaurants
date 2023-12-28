"""Module for managing a specific branches menu."""
from .MenuCategory import MenuCategory
from ..utils.Database import Database


class BranchMenu:
    """Class for manaing a specific branches menu."""

    def __init__(self, branch_id: str) -> None:
        """Don't call outside of Branch."""
        self._branch_id = branch_id

    def create_category(self, name: str) -> MenuCategory:
        """Create a new category."""
        sql = "INSERT INTO public.menucategory (name, branch_id) \
        VALUES (%s,%s) RETURNING id;"

        cursor = Database.execute(sql, name, self._branch_id)
        Database.commit()
        result = cursor.fetchone()
        assert result is not None

        return MenuCategory(result[0])

    def get_category_by_id(self, id: str) -> MenuCategory | None:
        """Get a category by it's id."""
        sql = "SELECT id FROM public.menucategory WHERE id=%s"
        result = Database.execute_and_fetchone(sql, id)

        if result is not None:
            return MenuCategory(result[0])

    def get_category_by_name(self, name: str) -> MenuCategory | None:
        """Get a category by it's id."""
        sql = "SELECT id FROM public.menucategory WHERE name=%s"
        result = Database.execute_and_fetchone(sql, name)

        if result is not None:
            return MenuCategory(result[0])
