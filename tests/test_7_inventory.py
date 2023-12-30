import pytest
from src.branch.Branch import Branch
from src.branch.BranchService import BranchService
from src.city.City import City
from src.city.CityService import CityService
from src.user.UserService import UserService
from src.inventory.BranchInventory import BranchInventory
from src.inventory.InventoryItem import InventoryItem
from src.utils.Database import Database
from src.utils.errors import AuthorizationError


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
