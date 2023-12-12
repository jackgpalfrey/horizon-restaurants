# Testing branch and branchservice here
import pytest
from src.branch.BranchService import BranchService
from src.branch.Branch import Branch
from src.utils.Database import Database

# this pytest thingy does the connect, init and the yield means it runs the tests then it continues its thing where it does the close too
# by the tests i mean the tests you wrote yourself starting from test_create_branch function.. and so on.

branch_name = "Bristol Branch"
address = "Bristol City"

@pytest.fixture(autouse=True)
def before_and_after_test():
    Database.connect()
    Database.init()

    yield

    Database.close()

def test_create_branch():
    branch = BranchService.create(branch_name, address)
    assert isinstance(branch,Branch)