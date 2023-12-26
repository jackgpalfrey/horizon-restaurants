import pytest
from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.reservations.Reservation import Reservation
from src.user.UserService import UserService
from src.utils.Database import Database

customer_name = "Glenn Juarez"
reservation_date = "2023-12-26"  # FORMAT YY/MM/DD
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
