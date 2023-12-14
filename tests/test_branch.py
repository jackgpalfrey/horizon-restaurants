# Testing branch and branchservice here
import pytest
from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.branch.Branch import Branch
from src.utils.Database import Database

# this pytest thingy does the connect, init and the yield means it runs the tests then it continues its thing where it does the close too
# by the tests i mean the tests you wrote yourself starting from test_create_branch function.. and so on.

branch_name = "Bristol Branch"
branch_address = "Bristol City"
store_name = "branch3"
store_address = "aiosfhaf"
new_name = "Manchester Branch"
new_address = "Manchester City"
# created_branch = BranchService.create("new branch", "aiosfhaf")
# branch_id = Database.execute_and_fetchone("SELECT id FROM public.branch WHERE name = %s", "new branch")


@pytest.fixture(autouse=True, scope="module")
def before_and_after_test():
    Database.connect()
    # Database.DEBUG_delete_all_tables("DANGEROUSLY DELETE ALL TABLES")
    Database.init()

    yield

    Database.close()


def test_create_branch():
    city = CityService.get_by_name("London")
    branch = BranchService.create(branch_name, branch_address, city)
    assert isinstance(branch, Branch)


def test_get_branch_by_name():
    branch = BranchService.get_by_name(branch_name)
    assert isinstance(branch, Branch)


def test_get_branch_by_id():
    city = CityService.get_by_name("Manchester")
    created_branch = BranchService.create("branch", "aiosfhaf", city)
    got_branch = BranchService.get_by_id(created_branch._branch_id)
    assert type(got_branch) == Branch
    assert type(got_branch._branch_id) == str
    assert created_branch._branch_id == got_branch._branch_id


def test_get_all_branches():
    branch = BranchService.get_all()
    assert len(branch) == 2
    assert type(branch) == list


def test_cannot_create_duplicate_branch():
    city = CityService.get_by_name("Essex")
    with pytest.raises(Exception):
        BranchService.create(branch_name, branch_address, city)

    # Database.connection.rollback()


def test_get_branch_id():
    city = CityService.get_by_name("Cardiff")
    created_branch = BranchService.create("branch2", "aiosfhaf", city)
    id = created_branch.get_id()
    assert id == created_branch._branch_id


def test_get_branch_name():
    city = CityService.get_by_name("city1")
    created_branch = BranchService.create("branch3", "aiosfhaf", city)
    name = created_branch.get_name()
    assert name == store_name


def test_get_branch_address():
    city = CityService.get_by_name("city2")
    created_branch = BranchService.create("branch4", "aiosfhaf", city)
    address = created_branch.get_address()
    assert address == store_address


def test_set_branch_name():
    city = CityService.get_by_name("city3")
    created_branch = BranchService.create("branch5", "aiosfhaf", city)
    created_branch.set_branch_name(new_name)
    assert created_branch.get_name() == new_name


def test_set_branch_address():
    city = CityService.get_by_name("city4")
    created_branch = BranchService.create("branch6", "aiosfhaf", city)
    created_branch.set_address(new_address)
    assert created_branch.get_address() == new_address
