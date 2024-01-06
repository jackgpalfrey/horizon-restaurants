import pytest
from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.tables.Table import Table
from src.discounts.BranchDiscounts import BranchDiscounts
from src.discounts.Discount import Discounts
from src.user.UserService import UserService
from src.utils.Database import Database


@pytest.fixture(autouse=True, scope="module")
def before_and_after_test():
    Database.connect()
    Database.DEBUG_delete_all_tables("DANGEROUSLY DELETE ALL TABLES")
    Database.init()
    UserService.init()

    UserService.login("admin", "admin")

    yield

    Database.close()


def test_create_discount():
    city = CityService.create("Bristol")
    branch = BranchService.create(
        "Bristol", "15-29 Union St, Bristol BS1 2DF", city)
    branch_discounts = branch.discounts()
    discount = branch_discounts.create(2.0,"this is the discount description")
    assert isinstance(branch_discounts, BranchDiscounts)
    assert isinstance(discount, Discounts)


def test_get_discount_by_id():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_discounts = branch.discounts()
    discount = branch_discounts.create(2.0, "this is the discount description")
    got_discount = branch_discounts.get_by_id(discount._discount_id)
    assert isinstance(got_discount, Discounts)
    assert type(got_discount._discount_id) is str
    assert discount._discount_id == got_discount._discount_id


def test_get_multiplier():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_discounts = branch.discounts()
    discount = branch_discounts.create(2.0, "this is the discount description")
    assert isinstance(discount, Discounts)
    multiplier = discount.get_multiplier()
    assert multiplier == 2.0


def test_set_multiplier():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_discounts = branch.discounts()
    discount = branch_discounts.create(2.0, "this is the discount description")
    assert discount is not None
    discount.set_multiplier(4.0)
    assert isinstance(discount, Discounts)
    assert discount.get_multiplier() == 4.0 

def test_get_description():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_discounts = branch.discounts()
    discount = branch_discounts.create(3.0, "This is Discount A or somehting")
    assert isinstance(discount, Discounts)
    description = discount.get_description()
    assert description == "This is Discount A or somehting"

def test_set_description():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_discounts = branch.discounts()
    discount = branch_discounts.create(3.0, "This is Discount A or somehting")
    assert discount is not None
    discount.set_description("New Description")
    assert isinstance(discount, Discounts)
    assert discount.get_description() == "New Description"

def test_get_all():
    branch = BranchService.get_by_name("Bristol")
    assert branch is not None
    branch_discounts = branch.discounts()
    discounts = branch_discounts.get_all()
    assert isinstance(discounts, list)
    assert len(discounts) == 6
