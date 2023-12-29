"""Module for managing individual menu items."""

from src.menu.utils import validate_menu_description, validate_menu_name
from src.user.ActiveUser import ActiveUser
from src.utils.Database import Database
from src.menu.MenuCategory import MenuCategory
from decimal import Decimal

from src.utils.errors import InputError


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

    def get_description(self) -> str | None:
        """Get item description."""
        sql = "SELECT description FROM public.menuitem WHERE id=%s;"
        result = Database.execute_and_fetchone(sql, self._item_id)

        if result is not None:
            return result[0]

    def get_price(self) -> float | None:
        """Get item price."""
        sql = "SELECT price FROM public.menuitem WHERE id=%s;"
        result = Database.execute_and_fetchone(sql, self._item_id)

        if result is not None:
            decimal: Decimal = result[0]
            return float(decimal)

    def get_image_url(self) -> str | None:
        """Get item image url."""
        sql = "SELECT image_url FROM public.menuitem WHERE id=%s;"
        result = Database.execute_and_fetchone(sql, self._item_id)

        if result is not None:
            return result[0]

    def get_category(self) -> MenuCategory | None:
        """Get menu items category."""
        sql = "SELECT category_id FROM public.menuitem WHERE id=%s;"
        result = Database.execute_and_fetchone(sql, self._item_id)

        if result is not None:
            return MenuCategory(result[0])

    def get_is_available(self) -> bool:
        """Get if the item is available or not."""
        sql = "SELECT is_available FROM public.menuitem WHERE id=%s;"
        result = Database.execute_and_fetchone(sql, self._item_id)

        return result is not None and result[0]

    def set_name(self, name: str) -> None:
        """Set name of item."""
        ActiveUser.get().raise_without_permission("menu.item.update.name")

        if not validate_menu_name(name):
            raise InputError("Invalid item name")

        sql = "UPDATE public.menuitem SET name = %s WHERE id = %s"
        Database.execute_and_commit(sql, name, self._item_id)

    def set_description(self, desc: str) -> None:
        """Set description of item."""
        ActiveUser.get().raise_without_permission("menu.item.update.desc")

        if not validate_menu_description(desc):
            raise InputError("Invalid item description")

        sql = "UPDATE public.menuitem SET description = %s WHERE id = %s"
        Database.execute_and_commit(sql, desc, self._item_id)

    def set_price(self, price: float) -> None:
        """Set price of item in £."""
        ActiveUser.get().raise_without_permission("menu.item.update.price")
        sql = "UPDATE public.menuitem SET price = %s WHERE id = %s"
        Database.execute_and_commit(sql, price, self._item_id)

    def set_image_url(self, url: str) -> None:
        """Set url of items cover image."""
        ActiveUser.get().raise_without_permission("menu.item.update.image")
        sql = "UPDATE public.menuitem SET image_url = %s WHERE id = %s"
        Database.execute_and_commit(sql, url, self._item_id)

    def set_category(self, category: MenuCategory) -> None:
        """Set category of item."""
        ActiveUser.get().raise_without_permission("menu.item.update.category")
        sql = "UPDATE public.menuitem SET category_id = %s WHERE id = %s"
        Database.execute_and_commit(sql, category.get_id(), self._item_id)

    def set_availability(self, is_available: bool) -> None:
        """Set availability of item."""
        ActiveUser.get().raise_without_permission("menu.item.update.available")
        sql = "UPDATE public.menuitem SET is_available = %s WHERE id = %s"
        Database.execute_and_commit(sql, is_available, self._item_id)

    def delete(self):
        """Delete item."""
        ActiveUser.get().raise_without_permission("menu.item.delete")
        sql = "DELETE FROM public.menuitem WHERE id=%s"
        Database.execute_and_commit(sql, self._item_id)
