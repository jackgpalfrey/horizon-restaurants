import pytest
from src.branch.Branch import Branch
from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.order.Order import Order
from src.order.OrderService import OrderService
from src.order.OrderStatus import OrderStatus
from src.user.Role import Role
from src.user.User import User
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


order: Order | None = None
branch: Branch | None = None


def test_can_create_order():
    global order
    global branch
    city = CityService.create("Swagstol")
    branch = BranchService.create(
        "Swag Branch", "42 Swag Street, Swagstol SW49 9GY", city)
    order = OrderService.create(branch)
    assert isinstance(order, Order)


def test_order_number():
    assert order is not None
    assert order.get_number() == 0


def test_status():
    assert order is not None
    assert order.get_status() == OrderStatus.NOT_PLACED


def test_assign_staff():
    assert order is not None
    assert branch is not None
    assert order.get_assigned_staff() is None
    user = UserService.create("test", "myPassw0rd!", "Test Account", branch)
    order.assign_staff(user)
    assignee = order.get_assigned_staff()
    assert isinstance(assignee, User)
    assert assignee.get_id() == user.get_id()
