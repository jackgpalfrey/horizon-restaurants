# Testing branch and branchservice here
import pytest
from src.branch.BranchService import BranchService
from src.branch.Branch import Branch
from src.utils.Database import Database

# this pytest thingy does the connect, init and the yield means it runs the tests then it continues its thing where it does the close too
# by the tests i mean the tests you wrote yourself starting from test_create_branch function.. and so on.

branch_name = "Bristol Branch"
address = "Bristol City"
# created_branch = BranchService.create("new branch", "aiosfhaf")
# branch_id = Database.execute_and_fetchone("SELECT id FROM public.branch WHERE name = %s", "new branch")


@pytest.fixture(autouse=True, scope="module")
def before_and_after_test():
    Database.connect()
    Database.DEBUG_delete_all_tables("DANGEROUSLY DELETE ALL TABLES")
    Database.init()

    yield

    Database.close()


def test_create_branch():
    branch = BranchService.create(branch_name, address)
    assert isinstance(branch, Branch)


def test_get_branch_by_name():
    branch = BranchService.get_by_name(branch_name)
    assert isinstance(branch, Branch)


def test_get_branch_by_id():
    created_branch = BranchService.create("branch", "aiosfhaf")
    got_branch = BranchService.get_by_id(created_branch._branch_id)
    assert type(got_branch) == Branch
    assert type(got_branch._branch_id) == str
    assert created_branch._branch_id == got_branch._branch_id


def test_cannot_create_duplicate_branch():
    with pytest.raises(Exception):
        BranchService.create(branch_name, address)

    Database.connection.rollback()


def test_get_branch_id():
    created_branch = BranchService.create("branch2", "aiosfhaf")
    id = created_branch.get_id()
    assert id == created_branch._branch_id

# def test_get_branch_name():
#     created_branch = BranchService.create("new branch", "aiosfhaf")
