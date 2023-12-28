"""Module for managing a specific branches menu."""
from src.menu.MenuItem import MenuItem
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

    def create_item(self, name: str, desc: str, price: float,
                    img_url: str | None, category: MenuCategory) -> MenuItem:
        """Create a new item."""
        sql = "INSERT INTO public.menuitem \
        (name, description, price, image_url, category_id, branch_id) \
        VALUES (%s,%s,%s,%s,%s,%s) RETURNING id;"

        cursor = Database.execute(sql, name, desc, price, img_url,
                                  category.get_id(), self._branch_id)

        Database.commit()
        result = cursor.fetchone()
        assert result is not None
        return MenuItem(result[0])

    def get_item_by_id(self, id: str) -> MenuItem | None:
        """Get an item by id."""
        sql = "SELECT id FROM public.menuitem WHERE branch_id=%s AND id=%s;"
        result = Database.execute_and_fetchone(sql, self._branch_id, id)

        if result is not None:
            return MenuItem(result[0])

    def get_all_items(self) -> list[MenuItem]:
        """Get all items in menu."""
        sql = "SELECT id FROM public.menuitem WHERE branch_id=%s;"
        result = Database.execute_and_fetchall(sql, self._branch_id)

        return [MenuItem(record[0]) for record in result]

    def get_all_items_categorised(self) -> dict[str, list[MenuItem]]:
        """Get all items as dict with category name key and list as value."""
        sql = "SELECT id, category_id FROM public.menuitem WHERE branch_id=%s"
        result = Database.execute_and_fetchall(sql, self._branch_id)

        items: dict[str, list[MenuItem]] = {}

        def add_item(category_name: str, item: MenuItem):
            if category_name in items:
                items[category_name].append(item)
            else:
                items[category_name] = [item]

        for item in result:
            item_id, category_id = item
            print(item_id)
            category_name = MenuCategory(category_id).get_name()
            assert category_name is not None
            add_item(category_name, MenuItem(item_id))

        return items

    def get_items_by_category(self, category: MenuCategory) -> list[MenuItem]:
        """Get items in a specific category."""
        category_id = category.get_id()
        sql = "SELECT id FROM public.menuitem \
        WHERE branch_id=%s AND category_id=%s"

        result = Database.execute_and_fetchall(
            sql, self._branch_id, category_id)

        return [MenuItem(record[0]) for record in result]
