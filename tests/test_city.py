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
