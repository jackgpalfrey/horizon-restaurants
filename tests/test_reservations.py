import pytest
from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.tables.Table import Table
from src.reservations.Reservation import Reservation
from src.reservations.utils import validate_customer_name
from src.user.UserService import UserService
from src.utils.Database import Database
from src.utils.errors import InputError

customer_name = "Glenn Juarez"
reservation_date = "2023-12-27"  # FORMAT YY/MM/DD
start_time = "21:50"  # FORMAT HH:MM
guest_num = 4


@pytest.fixture(autouse=True, scope="module")
def before_and_after_test():
    Database.connect()
    Database.DEBUG_delete_all_tables("DANGEROUSLY DELETE ALL TABLES")
    Database.init()
    UserService.init()

    UserService.login("admin", "admin")

    yield

    Database.close()


def test_create_reservation():
    city = CityService.create("Bristol")
    branch = BranchService.create(
        "Bristol", "15-29 Union St, Bristol BS1 2DF", city)
    branch_table = branch.tables()
    table = branch_table.create(1, 4)
    branch_reservation = branch.reservations()
    reservation = branch_reservation.create(
        table, customer_name, reservation_date, start_time, guest_num)
    assert isinstance(reservation, Reservation)


def test_can_create_reservation_with_future_date():
    branch = BranchService.get_by_name("Bristol")
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    branch_reservation = branch.reservations()
    reservation = branch_reservation.create(
        table, "Bianca Mcgrath", "2023-12-28", start_time, guest_num)
    assert isinstance(reservation, Reservation)


def test_cant_create_reservation_with_past_date():
    branch = BranchService.get_by_name("Bristol")
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    branch_reservation = branch.reservations()
    with pytest.raises(InputError):
        branch_reservation.create(
            table, "Mark Raymond", "2023-12-25", start_time, guest_num)


def test_customer_name_validation():
    assert validate_customer_name("Dennis Mccullough") == True
    assert validate_customer_name("Dennis Rosales Mccullough") == True
    assert validate_customer_name("Dennis Rosales Mccullough ") == False
    assert validate_customer_name(" Dennis Rosales Mccullough") == False
    assert validate_customer_name("Dennis Rosales  Mccullough") == False
    assert validate_customer_name("1234") == False
    assert validate_customer_name("1 1 1!") == False
    assert validate_customer_name("Dennis1 Rosales2 Mccullough3") == False
    assert validate_customer_name("1Dennis 2Rosales 3Mccullough") == False


def test_cant_create_reservation_with_invalid_customer_name():
    branch = BranchService.get_by_name("Bristol")
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    branch_reservation = branch.reservations()
    with pytest.raises(InputError):
        branch_reservation.create(
            table, "abc", reservation_date, start_time, guest_num)


def test_can_create_reservation_with_bigger_capacity():
    branch = BranchService.get_by_name("Bristol")
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    branch_reservation = branch.reservations()
    branch_reservation.create(
        table, "Rosales Dennis", reservation_date, start_time, 2)


def test_cant_create_reservation_with_insufficient_capacity():
    branch = BranchService.get_by_name("Bristol")
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    branch_reservation = branch.reservations()
    with pytest.raises(InputError):
        branch_reservation.create(
            table, "Dennis Mccullough", reservation_date, start_time, 5)


def test_get_table():
    branch = BranchService.get_by_name("Bristol")
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    branch_reservation = branch.reservations()
    reservation = branch_reservation.create(
        table, "Rosales Mccullough", reservation_date, start_time, 4)
    got_table = reservation.get_table()
    assert isinstance(got_table, Table)
    assert got_table.get_table_number() == 1


def test_get_customer_name():
    branch = BranchService.get_by_name("Bristol")
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    branch_reservation = branch.reservations()
    reservation = branch_reservation.create(
        table, "Charlotte Chandler", reservation_date, start_time, 4)
    customer_name = reservation.get_customer_name()
    assert customer_name == "Charlotte Chandler"
    assert isinstance(customer_name, str)
