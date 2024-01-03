import pytest
from src.branch.Branch import Branch
from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.menu.MenuItem import MenuItem
from src.order.Order import Order
from src.order.OrderService import OrderService
from src.order.OrderStatus import OrderStatus
from src.tables.Table import Table
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
    order.set_status(OrderStatus.PLACED)
    assert order.get_status() == OrderStatus.PLACED
    order.set_status(OrderStatus.NOT_PLACED)
    assert order.get_status() == OrderStatus.NOT_PLACED
    order.complete()
    assert order.get_status() == OrderStatus.COMPLETED
    order.cancel()
    assert order.get_status() == OrderStatus.CANCELLED


def test_assign_staff():
    assert order is not None
    assert branch is not None
    assert order.get_assigned_staff() is None
    user = UserService.create("test", "myPassw0rd!", "Test Account", branch)
    order.assign_staff(user)
    assignee = order.get_assigned_staff()
    assert isinstance(assignee, User)
    assert assignee.get_id() == user.get_id()
    order.assign_staff(None)
    assert order.get_assigned_staff() is None


def test_priority():
    assert order is not None
    assert order.get_priority() == 0
    order.set_priority(5)
    assert order.get_priority() == 5


def test_customer_name():
    assert order is not None
    assert order.get_customer_name() is None
    order.set_customer_name("Joe Mama")
    assert order.get_customer_name() == "Joe Mama"


def test_table():
    assert order is not None
    assert branch is not None
    assert order.get_table() is None

    table = branch.tables().create(5, 5)
    order.set_table(table)
    got_table = order.get_table()
    assert isinstance(got_table, Table)
    assert got_table.get_id() == table.get_id()


def test_items():
    assert order is not None
    assert branch is not None

    all = order.get_all_items()
    assert type(all) is list
    assert len(all) == 0

    menu = branch.menu()
    category = menu.create_category("Category")
    item = menu.create_item("item", "my description", 3.56, None, category)

    order.add_item(item)
    all = order.get_all_items()
    assert len(all) == 1
    record = all[0]
    assert type(record) is tuple
    assert isinstance(record[0], MenuItem)
    assert type(record[1]) is int
    assert record[0].get_id() == item.get_id()
    assert record[1] == 1

    order.add_item(item)
    all = order.get_all_items()
    assert len(all) == 1
    assert all[0][1] == 2

    other_item = menu.create_item("other item", "my description", 3.55,
                                  None, category)

    order.add_item(other_item)
    all = order.get_all_items()
    assert len(all) == 2
    assert all[0][1] == 2
    record = all[1]
    assert isinstance(record[0], MenuItem)
    assert record[0].get_id() == other_item.get_id()
    assert record[1] == 1


def test_place():
    assert order is not None
    order.place()
    assert order.get_status() == OrderStatus.PLACED
