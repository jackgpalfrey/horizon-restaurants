import pytest
from src.branch.Branch import Branch
from src.branch.BranchService import BranchService
from src.city.City import City
from src.city.CityService import CityService
from src.user.UserService import UserService
from src.inventory.BranchInventory import BranchInventory
from src.inventory.InventoryItem import InventoryItem
from src.utils.Database import Database
from src.utils.errors import (
    AuthorizationError,
    AlreadyExistsError,
    InputError,
)


@pytest.fixture(autouse=True, scope="module")
def before_and_after_test():
    Database.connect()
    Database.DEBUG_delete_all_tables("DANGEROUSLY DELETE ALL TABLES")
    Database.init()
    UserService.init()

    UserService.login("admin", "admin")

    yield

    Database.close()


name = "Tomatoe"
quantity = 50
threshold = 20


def test_create_item():
    UserService.create("kitchen-staff1", "myPassword0!",
                       "Kitchen Staff", role_id=2)
    UserService.create("frontend-staff1", "myPassword0!",
                       "Frontend Staff", role_id=1)
    UserService.logout()
    UserService.login("kitchen-staff1", "myPassword0!")
    global branch
    city = CityService.create("Bristol")
    assert isinstance(city, City)
    branch = BranchService.create(
        "Bristol", "15-29 Union St, Bristol BS1 2DF", city)
    assert isinstance(branch, Branch)
    branch_inventory = branch.inventory()
    assert isinstance(branch_inventory, BranchInventory)
    item = branch_inventory.create_new_item(name, quantity, threshold)
    assert isinstance(item, InventoryItem)
    assert item is not None


def test_cant_create_item_with_duplicate_name():
    assert branch is not None
    branch_inventory = branch.inventory()
    with pytest.raises(AlreadyExistsError):
        branch_inventory.create_new_item("Tomatoe", 12, 8)


def test_get_item_name():
    assert branch is not None
    branch_inventory = branch.inventory()
    item = branch_inventory.create_new_item("Potatoe", 60, 35)
    assert item is not None
    item_name = item.get_name()
    assert item_name == "Potatoe"
    assert isinstance(item_name, str)


def test_get_item_quantity():
    assert branch is not None
    branch_inventory = branch.inventory()
    item = branch_inventory.create_new_item("Onion", 40, 10)
    assert item is not None
    item_quantity = item.get_quantity()
    assert item_quantity == 40
    assert isinstance(item_quantity, int)


def test_get_item_threshold():
    assert branch is not None
    branch_inventory = branch.inventory()
    item = branch_inventory.create_new_item("Pasta", 30, 7)
    assert item is not None
    item_threshold = item.get_threshold()
    assert item_threshold == 7
    assert isinstance(item_threshold, int)


def test_get_all_items():
    assert branch is not None
    branch_inventory = branch.inventory()
    items = branch_inventory.get_all()
    assert isinstance(items, list)
    assert len(items) == 4

    assert items[0].get_name() == name
    assert items[1].get_name() == "Potatoe"
    assert items[2].get_name() == "Onion"
    assert items[3].get_name() == "Pasta"


def test_get_item_by_name():
    assert branch is not None
    branch_inventory = branch.inventory()
    item = branch_inventory.create_new_item("Meat", 50, 10)
    got_item = branch_inventory.get_by_name("Meat")
    assert isinstance(got_item, InventoryItem)
    assert got_item.get_name() == "Meat"
    assert got_item._item_id == item._item_id


def test_set_item_name():
    assert branch is not None
    branch_inventory = branch.inventory()
    item = branch_inventory.get_by_name("Potatoe")
    assert item is not None
    item.set_name("Sweet Potatoe")
    got_name = item.get_name()
    assert got_name == "Sweet Potatoe"
    assert isinstance(got_name, str)


def test_cant_set_invalid_item_name():
    assert branch is not None
    branch_inventory = branch.inventory()
    item = branch_inventory.get_by_name("Sweet Potatoe")
    assert item is not None
    with pytest.raises(InputError):
        item.set_name("12239Invalid123")


def test_cant_set_duplicate_item_name():
    assert branch is not None
    branch_inventory = branch.inventory()
    item = branch_inventory.get_by_name("Sweet Potatoe")
    assert item is not None
    with pytest.raises(AlreadyExistsError):
        item.set_name("Meat")


def test_set_item_quantity():
    assert branch is not None
    branch_inventory = branch.inventory()
    item = branch_inventory.get_by_name("Meat")
    assert item is not None
    item.set_quantity(7)
    got_quantity = item.get_quantity()
    assert isinstance(got_quantity, int)
    assert got_quantity == 7


def test_set_item_threshold():
    assert branch is not None
    branch_inventory = branch.inventory()
    item = branch_inventory.get_by_name("Meat")
    assert item is not None
    item.set_threshold(10)
    got_threshold = item.get_threshold()
    assert isinstance(got_threshold, int)
    assert got_threshold == 10


def test_add_quantity():
    assert branch is not None
    branch_inventory = branch.inventory()
    item = branch_inventory.get_by_name("Meat")
    assert item is not None
    item.add_quantity(10)
    got_quantity = item.get_quantity()
    assert isinstance(got_quantity, int)
    assert got_quantity == 17


def test_subtract_quantity():
    assert branch is not None
    branch_inventory = branch.inventory()
    item = branch_inventory.get_by_name("Meat")
    assert item is not None
    assert item.get_quantity() == 17
    item.subtract_quantity(10)
    got_quantity = item.get_quantity()
    assert isinstance(got_quantity, int)
    assert got_quantity == 7


def test_cant_subtract_quantity_over_current_quantity():
    assert branch is not None
    branch_inventory = branch.inventory()
    item = branch_inventory.get_by_name("Meat")
    assert item is not None
    assert item.get_quantity() == 7
    with pytest.raises(InputError):
        item.subtract_quantity(15)


def test_cant_update_item_with_wrong_role():
    UserService.logout()
    UserService.login("frontend-staff1", "myPassword0!")
    assert branch is not None
    branch_inventory = branch.inventory()
    item = branch_inventory.get_by_name("Sweet Potatoe")
    assert item is not None
    with pytest.raises(AuthorizationError):
        item.set_name("Potatoe")
        item.set_quantity(40)
        item.set_threshold(6)
        item.add_quantity(8)
        item.subtract_quantity(2)
