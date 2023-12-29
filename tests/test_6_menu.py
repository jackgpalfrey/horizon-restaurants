import pytest
from src.branch.Branch import Branch
from src.branch.BranchService import BranchService
from src.city.City import City
from src.city.CityService import CityService
from src.menu.BranchMenu import BranchMenu
from src.menu.MenuCategory import MenuCategory
from src.menu.MenuItem import MenuItem
from src.utils.Database import Database
from src.user.UserService import UserService


@pytest.fixture(autouse=True, scope="module")
def before_and_after_test():
    Database.connect()
    Database.DEBUG_delete_all_tables("DANGEROUSLY DELETE ALL TABLES")
    Database.init()
    UserService.init()

    UserService.login("admin", "admin")

    yield

    Database.close()


addr = "15-29 Union St, Bristol BS1 2DF"
branch: Branch | None = None
menu: BranchMenu | None = None
catname = "My Category"


def test_can_get_menu_class():
    global branch
    global menu
    city = CityService.create("Bristol")
    assert isinstance(city, City)
    branch = BranchService.create("Test Branch", addr, city)
    assert isinstance(branch, Branch)
    menu = branch.menu()
    assert isinstance(menu, BranchMenu)


def test_can_create_category():
    assert menu is not None
    category = menu.create_category(catname)
    assert isinstance(category, MenuCategory)
    assert category.get_name() == catname


def test_can_set_category_name():
    assert menu is not None
    category = menu.get_category_by_name(catname)
    assert isinstance(category, MenuCategory)
    category.set_name("New Category")
    new_category = menu.get_category_by_name("New Category")
    assert isinstance(new_category, MenuCategory)
    assert category.get_id() == new_category.get_id()
    assert new_category.get_name() == "New Category"


def test_can_delete_category():
    assert menu is not None
    category = menu.get_category_by_name("New Category")
    assert isinstance(category, MenuCategory)
    category.delete()
    assert menu.get_category_by_name("New Category") is None


def test_can_create_item():
    assert menu is not None
    category = menu.create_category(catname)
    assert isinstance(category, MenuCategory)
    item = menu.create_item("Item", "My Test Item", 3.96, None, category)
    assert isinstance(item, MenuItem)

    menu.create_item("Other Item", "My Other Test Item", 4, None, category)
    category = menu.create_category("Other Category")
    menu.create_item("Third Item", "My Thrid Test Item", 2, None, category)


def test_can_get_all_items():
    assert menu is not None
    items = menu.get_all_items()
    assert type(items) is list
    for item in items:
        assert isinstance(item, MenuItem)

    assert items[0].get_name() == "Item"
    assert items[1].get_name() == "Other Item"
    assert items[2].get_name() == "Third Item"


def test_can_get_all_items_categorised():
    assert menu is not None
    items = menu.get_all_items_categorised()
    assert type(items) is dict
    cat1 = items[catname]
    assert type(cat1) is list
    assert isinstance(cat1[0], MenuItem)
    assert cat1[0].get_name() == "Item"
    assert isinstance(cat1[1], MenuItem)
    assert cat1[1].get_name() == "Other Item"
    cat2 = items["Other Category"]
    assert type(cat2) is list
    assert isinstance(cat2[0], MenuItem)
    assert cat2[0].get_name() == "Third Item"


def test_can_get_by_category():
    assert menu is not None
    category = menu.get_category_by_name(catname)
    assert isinstance(category, MenuCategory)
    items = menu.get_items_by_category(category)
    assert type(items) is list
    assert len(items) == 2
    assert isinstance(items[0], MenuItem)
    assert items[0].get_name() == "Item"
    assert isinstance(items[1], MenuItem)
    assert items[1].get_name() == "Other Item"

    category = menu.get_category_by_name("Other Category")
    assert category is not None
    items = menu.get_items_by_category(category)
    assert type(items) is list
    assert len(items) == 1
    assert isinstance(items[0], MenuItem)
    assert items[0].get_name() == "Third Item"


item: MenuItem | None = None


def test_item_name():
    global item
    assert menu is not None
    category = menu.create_category("Burgers")
    item = menu.create_item("Burger", "A big, expensive burger",
                            10.56, None, category)

    assert item.get_name() == "Burger"
    item.set_name("Hamburguesa")
    assert item.get_name() == "Hamburguesa"


def test_item_description():
    assert item is not None
    assert item.get_description() == "A big, expensive burger"
    item.set_description("A spanish burger")
    assert item.get_description() == "A spanish burger"


def test_item_price():
    assert item is not None
    assert item.get_price() == 10.56
    item.set_price(3.29)
    assert item.get_price() == 3.29


def test_item_image_url():
    assert item is not None
    assert item.get_image_url() is None
    url = "https://www.thestreet.com/.image/t_share/MTg5NTQ2MzM0NDk0MTQwMDAx/bk-ice-cream-burger-.jpg"
    item.set_image_url(url)
    assert item.get_image_url() == url


def test_item_category():
    assert menu is not None
    assert item is not None
    new_category = menu.create_category("Spanish Food")
    old_category = item.get_category()
    assert old_category is not None
    assert old_category.get_name() == "Burgers"
    item.set_category(new_category)
    got_category = item.get_category()
    assert isinstance(got_category, MenuCategory)
    assert got_category.get_id() == new_category.get_id()
    assert got_category.get_name() == "Spanish Food"


def test_item_availability():
    assert item is not None
    assert item.get_is_available() is True
    item.set_availability(False)
    assert item.get_is_available() is False


def test_can_delete_item():
    global item
    assert menu is not None
    assert item is not None
    id = item.get_id()
    item.delete()
    item = None
    assert menu.get_item_by_id(id) is None
