import pytest
from src.city.CityService import CityService
from src.city.City import City
from src.utils.Database import Database

city_name = "London"


@pytest.fixture(autouse=True, scope="module")
def before_and_after_test():
    Database.connect()
    Database.DEBUG_delete_all_tables("DANGEROUSLY DELETE ALL TABLES")
    Database.init()

    yield

    Database.close()


def test_create_city():
    city = CityService.create(city_name)
    assert isinstance(city, City)


def test_get_city_by_name():
    city = CityService.get_by_name(city_name)
    assert isinstance(city, City)


def test_get_city_by_id():
    created_city = CityService.create("Cardiff")
    got_city = CityService.get_by_id(created_city._city_id)
    assert type(got_city) == City
    assert type(got_city._city_id) == str
    assert created_city._city_id == got_city._city_id


def test_get_all_cities():
    city = CityService.get_all()
    assert len(city) == 2
    assert type(city) == list
