import pytest
from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.tables.BranchTables import BranchTables
from src.tables.Table import Table
from src.user.UserService import UserService
from src.utils.Database import Database
from src.reservations.Reservation import Reservation
from datetime import datetime, timedelta


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
    result = table.create(1, 4)
    assert isinstance(table, BranchTables)
    assert isinstance(result, Table)


def test_get_table_by_id():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_tables = branch.tables()
    table = branch_tables.create(2, 2)
    got_table = branch_tables.get_by_id(table._table_id)
    assert isinstance(got_table, Table)
    assert type(got_table._table_id) is str
    assert table._table_id == got_table._table_id


def test_get_table_by_number():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_tables = branch.tables()
    got_table = branch_tables.get_by_number(2)
    assert isinstance(got_table, Table)
    assert got_table.get_table_number() == 2


def test_find_table_by_capacity():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_tables = branch.tables()
    branch_tables.create(3, 6)
    branch_tables.create(4, 8)
    branch_tables.create(5, 2)
    got_table = branch_tables.find_by_capacity(2)
    assert type(got_table) is list
    assert len(got_table) == 5
    for i in range(len(got_table)):
        assert isinstance(got_table[i], Table)
    assert got_table[0].get_capacity() == 2
    assert got_table[4].get_capacity() == 8


def test_get_all_tables():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_tables = branch.tables()
    tables = branch_tables.get_all()
    assert len(tables) == 5
    for i in range(len(tables)):
        assert isinstance(tables[i], Table)
    assert type(tables) is list


def test_get_table_number():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_tables = branch.tables()
    table = branch_tables.create(6, 2)
    table_number = table.get_table_number()
    assert table_number == 6


def test_get_table_capacity():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_tables = branch.tables()
    table = branch_tables.create(7, 6)
    capacity = table.get_capacity()
    assert capacity == 6


def test_set_table_capacity():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_tables = branch.tables()
    table = branch_tables.get_by_number(4)
    assert table is not None
    table.set_capacity(2)
    assert isinstance(table, Table)
    assert table.get_capacity() == 2


def test_delete_table():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_tables = branch.tables()
    table = branch_tables.get_by_number(1)
    assert table is not None
    table.delete()
    assert branch_tables.get_by_number(1) is None


def check_table_is_reserved():
    branch = BranchService.get_by_name("Bristol")
    branch_tables = branch.tables()
    table = branch_tables.get_by_number(2)
    branch_reservations = branch.reservations()
    time = datetime.now()
    reservation = branch_reservations.create(table, "Hannah Carter", time, 2)
    check = table.check_is_reserved(time)
    assert isinstance(reservation, Reservation)
    assert type(check) == bool
    assert check == True


def check_table_is_not_reserved():
    branch = BranchService.get_by_name("Bristol")
    branch_tables = branch.tables()
    table = branch_tables.get_by_number(2)
    branch_reservations = branch.reservations()
    time = datetime.now()
    reservation = branch_reservations.create(table, "Hannah Carter", time, 2)
    check_time = time + timedelta(hours=4)
    check = table.check_is_reserved(check_time)
    assert isinstance(reservation, Reservation)
    assert type(check) == bool
    assert check == False
