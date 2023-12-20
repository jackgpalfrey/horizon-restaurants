import pytest

from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.menu.BranchMenu import BranchMenu
from src.utils.Database import Database

branch_address = "15-29 Union St, Bristol BS1 2DF"


@pytest.fixture(autouse=True, scope="module")
def before_and_after_test():
    Database.connect()
    Database.DEBUG_delete_all_tables("DANGEROUSLY DELETE ALL TABLES")
    Database.init()

    yield

    Database.close()


def test_can_get_menu():
    city = CityService.create("Bristol")
    branch = BranchService.create("My Branch", branch_address, city)
    menu = branch.menu()
    assert isinstance(menu, BranchMenu)
    assert menu._branch_id == branch._branch_id
