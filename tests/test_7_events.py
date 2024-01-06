from datetime import datetime, timedelta
import pytest
from src.user.UserService import UserService
from src.utils.Database import Database
from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.events.BranchEvents import BranchEvents
from src.events.Event import Event


@pytest.fixture(autouse=True, scope="module")
def before_and_after_test():
    Database.connect()
    Database.DEBUG_delete_all_tables("DANGEROUSLY DELETE ALL TABLES")
    Database.init()
    UserService.init()
    UserService.login("admin", "admin")

    yield

    Database.close()


events: BranchEvents | None = None


def test_create_event():
    global events
    city = CityService.create("Bristol")
    branch = BranchService.create(
        "Bristol", "Unit 17 Horn Hill Rd, Hornhill Road, Worcester WR4 0SX", city)
    assert branch is not None
    events = branch.events()
    assert isinstance(events, BranchEvents)
    event = events.create(datetime.now(), datetime.now(
    ) + timedelta(hours=4), 0, "010101", "joe@email.com", "10 Bristol")
    assert isinstance(event, Event)


event: Event | None = None


def test_get_all():
    global event
    assert events is not None
    all = events.get_all()
    assert type(all) is list
    assert len(all) == 1
    assert isinstance(all[0], Event)
    event = all[0]


def test_type():
    assert event is not None
    assert event.get_event_type() == 0
    event.set_type(1)
    assert event.get_event_type() == 1


def test_start_time():
    assert event is not None
    assert type(event.get_start_time()) == datetime
    new_dt = datetime.now()
    event.set_start_time(new_dt)
    assert event.get_start_time().timestamp() == new_dt.timestamp()


def test_end_time():
    assert event is not None
    assert type(event.get_end_time()) == datetime
    new_dt = datetime.now()
    event.set_end_time(new_dt)
    assert event.get_end_time().timestamp() == new_dt.timestamp()
