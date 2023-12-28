import pytest
from src.branch.Branch import Branch
from src.branch.BranchService import BranchService
from src.city.City import City
from src.city.CityService import CityService
from src.menu.BranchMenu import BranchMenu
from src.menu.MenuCategory import MenuCategory
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


def test_can_delete_category():
    assert menu is not None
    category = menu.get_category_by_name("New Category")
    assert isinstance(category, MenuCategory)
    category.delete()
    assert menu.get_category_by_name("New Category") is None
