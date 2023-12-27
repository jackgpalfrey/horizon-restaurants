import pytest
from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.tables.Table import Table
from src.reservations.Reservation import Reservation
from src.reservations.utils import validate_customer_name
from src.user.UserService import UserService
from src.utils.Database import Database
from src.utils.errors import InputError
from datetime import datetime

customer_name = "Glenn Juarez"
reservation_time = datetime.strptime(
    "2023-12-27 14:30", '%Y-%m-%d %H:%M')  # FORMAT YY/MM/DD HH:MM
guest_num = 4

new_customer_name = "Ellis Mcintyre"


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
        table, customer_name, reservation_time, guest_num)
    assert isinstance(reservation, Reservation)


def test_can_create_reservation_with_future_date():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    assert table is not None
    branch_reservation = branch.reservations()
    time = datetime.strptime(
        "2023-12-28 14:30", '%Y-%m-%d %H:%M')
    reservation = branch_reservation.create(
        table, "Bianca Mcgrath", time, guest_num)
    assert isinstance(reservation, Reservation)


def test_cant_create_reservation_with_past_date():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    assert table is not None
    branch_reservation = branch.reservations()
    time = datetime.strptime(
        "2023-12-25 14:30", '%Y-%m-%d %H:%M')
    with pytest.raises(InputError):
        branch_reservation.create(
            table, "Mark Raymond", time, guest_num)


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
    assert branch is not None
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    assert table is not None
    branch_reservation = branch.reservations()
    with pytest.raises(InputError):
        branch_reservation.create(
            table, "abc", reservation_time,  guest_num)


def test_can_create_reservation_with_bigger_capacity():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    assert table is not None
    branch_reservation = branch.reservations()
    branch_reservation.create(
        table, "Rosales Dennis", reservation_time, 2)


def test_cant_create_reservation_with_insufficient_capacity():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    assert table is not None
    branch_reservation = branch.reservations()
    with pytest.raises(InputError):
        branch_reservation.create(
            table, "Dennis Mccullough", reservation_time, 5)


def test_get_table():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    assert table is not None
    branch_reservation = branch.reservations()
    reservation = branch_reservation.create(
        table, "Rosales Mccullough", reservation_time, 4)
    got_table = reservation.get_table()
    assert isinstance(got_table, Table)
    assert got_table.get_table_number() == 1


def test_get_customer_name():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    assert table is not None
    branch_reservation = branch.reservations()
    reservation = branch_reservation.create(
        table, "Charlotte Chandler", reservation_time, 4)
    customer_name = reservation.get_customer_name()
    assert customer_name == "Charlotte Chandler"
    assert isinstance(customer_name, str)


def test_get_time():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    assert table is not None
    branch_reservation = branch.reservations()
    reservation = branch_reservation.create(
        table, "Zaara Carter", reservation_time, 4)
    time = reservation.get_time()
    assert time is not None
    assert time == reservation_time


def test_get_num_people():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    assert table is not None
    branch_reservation = branch.reservations()
    reservation = branch_reservation.create(
        table, "Jenna Davila", reservation_time, 4)
    guest_num = reservation.get_num_people()
    assert guest_num is not None
    assert guest_num == 4


def test_set_table():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    assert table is not None
    branch_reservation = branch.reservations()
    reservation = branch_reservation.create(
        table, "Ronald Robles", reservation_time, 4)
    new_table = branch_table.create(2, 6)
    assert new_table is not None
    reservation.set_table(new_table)
    got_table = reservation.get_table()
    assert isinstance(got_table, Table)
    assert got_table._table_id == new_table._table_id


def test_set_customer_name():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    assert table is not None
    branch_reservation = branch.reservations()
    reservation = branch_reservation.create(
        table, "Sally Owens", reservation_time, 4)
    reservation.set_customer_name(new_customer_name)
    customer = reservation.get_customer_name()
    assert isinstance(customer, str)
    assert customer == new_customer_name


def test_cant_set_invalid_customer_name():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    assert table is not None
    branch_reservation = branch.reservations()
    reservation = branch_reservation.create(
        table, "Michelle Ibarra", reservation_time, 4)
    with pytest.raises(InputError):
        reservation.set_customer_name("1Tyler ..7")


def test_set_time():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    assert table is not None
    branch_reservation = branch.reservations()
    reservation = branch_reservation.create(
        table, "Hannah Carter", reservation_time, 4)
    time = datetime.strptime(
        "2023-12-29 17:30", '%Y-%m-%d %H:%M')
    reservation.set_time(time)
    got_time = reservation.get_time()
    assert got_time is not None
    assert time == got_time


def test_cant_set_invalid_time():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    assert table is not None
    branch_reservation = branch.reservations()
    reservation = branch_reservation.create(
        table, "Aisha Howard", reservation_time, 4)
    time = datetime.strptime(
        "2023-12-22 11:30", '%Y-%m-%d %H:%M')
    with pytest.raises(InputError):
        reservation.set_time(time)


def test_set_guest_num():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    assert table is not None
    branch_reservation = branch.reservations()
    reservation = branch_reservation.create(
        table, "Kyran Fuller", reservation_time, 4)
    reservation.set_num_people(3)
    customer_num = reservation.get_num_people()
    assert customer_num == 3
    assert isinstance(customer_num, int)


def test_set_invalid_guest_num():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    assert table is not None
    branch_reservation = branch.reservations()
    reservation = branch_reservation.create(
        table, "Ophelia Pineda", reservation_time, 4)
    with pytest.raises(InputError):
        reservation.set_num_people(8)


def test_get_by_id():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_table = branch.tables()
    table = branch_table.get_by_number(1)
    assert table is not None
    branch_reservation = branch.reservations()
    reservation = branch_reservation.create(
        table, "Tony Barrett", reservation_time, 4)
    got_reservation = branch_reservation.get_by_id(reservation._reservation_id)
    assert isinstance(got_reservation, Reservation)
    assert got_reservation._reservation_id == reservation._reservation_id
