import pytest
from src.city.CityService import CityService
from src.city.City import City
from src.utils.Database import Database

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
    # print("!!!!!")
    # print(city)
    # print("!!!!!")
    # assert False
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


def test_get_city_name():
    created_city = CityService.create("Manchester")
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
    city = CityService.create("city1")
    city = CityService.create("city2")
    city = CityService.create("city3")
    city = CityService.create("city4")
    assert isinstance(city, City)
