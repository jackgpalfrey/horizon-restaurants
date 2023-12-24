import pytest
from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.branch.Branch import Branch
from src.tables.Table import Table
from src.tables.BranchTables import BranchTables
from src.user.UserService import UserService
from src.utils.Database import Database
from src.utils.errors import InputError, AlreadyExistsError


@pytest.fixture(autouse=True, scope="module")
def before_and_after_test():
    Database.connect()
    Database.DEBUG_delete_all_tables("DANGEROUSLY DELETE ALL TABLES")
    Database.init()
    UserService.init()

    UserService.login("admin", "admin")

    yield

    Database.close()


def test_create_table():
    city = CityService.create("Bristol")
    branch = BranchService.create(
        "Bristol", "15-29 Union St, Bristol BS1 2DF", city)
    table = branch.tables()
    result = table.create(branch, 1, 4)
    assert isinstance(table, BranchTables)
    assert isinstance(result, Table)
