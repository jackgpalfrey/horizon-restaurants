# Author: Dina Hassanein (22066792)
import pytest
from src.city.CityService import CityService
from src.city.City import City
from src.utils.Database import Database
from src.city.utils import validate_city_name

city_name = "London"
store_name = "Manchester"
new_name = "Bournemouth"


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
    assert isinstance(got_city, City)
    assert isinstance(got_city._city_id, str)
    assert created_city._city_id == got_city._city_id


def test_get_all_cities():
    city = CityService.get_all()
    assert len(city) == 2
    for i in range(len(city)):
        assert isinstance(city[i], City)
    assert isinstance(city, list)


def test_get_city_name():
    created_city = CityService.create(store_name)
    name = created_city.get_name()
    assert name == store_name


def test_get_city_id():
    created_city = CityService.create("Essex")
    id = created_city.get_id()
    assert id == created_city._city_id


def test_set_city_name():
    created_city = CityService.create("Bath")
    created_city.set_name(new_name)
    assert created_city.get_name() == new_name


def test_creating_cities_for_branches():
    city = CityService.create("Bath")
    city = CityService.create("Reading")
    city = CityService.create("Oxford")
    city = CityService.create("Plymouth")
    city = CityService.create("Liverpool")
    assert isinstance(city, City)


def test_city_name_validation():
    assert validate_city_name("Test City") is True
    assert validate_city_name("Bristol") is True
    assert validate_city_name("Bristol City ") is False
    assert validate_city_name(" Bristol City") is False
    assert validate_city_name("Bristol  City") is False
    assert validate_city_name("Bristol City1") is False
    assert validate_city_name("Bristol City!") is False
