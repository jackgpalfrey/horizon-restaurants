import pytest
from src.utils.Database import Database
from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.event.BranchEvents import BranchEvents
from src.event.Event import Event
from src.user.UserService import UserService


@pytest.fixture(autouse=True, scope="module")
def before_and_after_test():
    Database.connect()
    Database.init()

    yield

    Database.close()


def test_create_event():
    type = "external"
    city = CityService.create("Bristol")
    branch = BranchService.create("Bristol", "Unit 17 Horn Hill Rd, Hornhill Road, Worcester WR4 0SX", city)
    event = BranchEvents.create(type)
    assert isinstance(Event, Event)

