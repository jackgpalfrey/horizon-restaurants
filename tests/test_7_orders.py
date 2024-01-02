import pytest
from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.order.Order import Order
from src.order.OrderService import OrderService
from src.utils.Database import Database
from src.user.UserService import UserService


@pytest.fixture(autouse=True, scope="module")
def before_and_after_test():
    Database.connect()
    Database.DEBUG_delete_all_tables("DANGEROUSLY DELETE ALL TABLES")
    Database.init()
    UserService.init()

    UserService.login("admin", "admin")

    yield

    Database.close()


def test_can_create_order():
    city = CityService.create("Swagstol")
    branch = BranchService.create(
        "Swag Branch", "42 Swag Street, Swagstol SW49 9GY", city)
    order = OrderService.create(branch)
    assert isinstance(order, Order)
