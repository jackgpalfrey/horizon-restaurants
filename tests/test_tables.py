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


def test_get_table_by_id():
    branch = BranchService.get_by_name("Bristol")
    branch_tables = branch.tables()
    table = branch_tables.create(branch, 2, 2)
    got_table = branch_tables.get_by_id(table._table_id)
    assert type(got_table) == Table
    assert type(got_table._table_id) == str
    assert table._table_id == got_table._table_id


def test_get_table_by_number():
    branch = BranchService.get_by_name("Bristol")
    branch_tables = branch.tables()
    got_table = branch_tables.get_by_number(2)
    assert isinstance(got_table, Table)


def test_find_table_by_capacity():
    branch = BranchService.get_by_name("Bristol")
    branch_tables = branch.tables()
    got_table = branch_tables.find_by_capacity(2)
    assert type(got_table) == list
    assert len(got_table) == 1
    for i in range(len(got_table)):
        assert isinstance(got_table[i], Table)
    assert got_table[0].get_capacity() == 2


def test_get_all_tables():
    branch = BranchService.get_by_name("Bristol")
    branch_tables = branch.tables()
    tables = branch_tables.get_all()
    assert len(tables) == 2
    for i in range(len(tables)):
        assert isinstance(tables[i], Table)
    assert type(tables) == list


def test_get_table_number():
    branch = BranchService.get_by_name("Bristol")
    branch_tables = branch.tables()
    table = branch_tables.create(branch, 3, 2)
    table_number = table.get_table_number()
    assert table_number == 3
    assert table_number == table.get_table_number()


def test_get_table_capacity():
    branch = BranchService.get_by_name("Bristol")
    branch_tables = branch.tables()
    table = branch_tables.create(branch, 4, 6)
    capacity = table.get_capacity()
    assert capacity == 6
    assert capacity == table.get_capacity()
