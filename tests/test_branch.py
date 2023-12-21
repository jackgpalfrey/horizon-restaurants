import pytest
from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.branch.Branch import Branch
from src.user.UserService import UserService
from src.user.User import User
from src.utils.Database import Database
from src.branch.utils import validate_branch_name, validate_branch_address

branch_name = "Bristol Branch"
branch_address = "15-29 Union St, Bristol BS1 2DF"
save_name = "Oxford Branch"
save_address = "116-118 Lower Borough Walls, Bath BA1 1QU"
new_name = "Manchester Branch"
new_address = "12a Oxford Rd, Manchester M1 5QA"


@pytest.fixture(autouse=True, scope="module")
def before_and_after_test():
    Database.connect()
    Database.DEBUG_delete_all_tables("DANGEROUSLY DELETE ALL TABLES")
    Database.init()
    UserService.init()

    UserService.login("admin", "admin")

    yield

    Database.close()


def test_create_branch():
    city = CityService.create("Bristol")
    branch = BranchService.create(branch_name, branch_address, city)
    assert isinstance(branch, Branch)


def test_get_branch_by_name():
    branch = BranchService.get_by_name(branch_name)
    assert isinstance(branch, Branch)


def test_get_branch_by_id():
    city = CityService.create("Leicester")
    created_branch = BranchService.create(
        "Reading Branch", "Unit 17 Horn Hill Rd, Hornhill Road, Worcester WR4 0SX", city)
    got_branch = BranchService.get_by_id(created_branch._branch_id)
    assert type(got_branch) == Branch
    assert type(got_branch._branch_id) == str
    assert created_branch._branch_id == got_branch._branch_id


def test_get_all_branches():
    branch = BranchService.get_all()
    assert len(branch) == 2
    assert type(branch) == list


def test_cannot_create_duplicate_branch():
    city = CityService.create("Nottingham")
    # FIXME: Replace with correct error
    with pytest.raises(Exception):
        BranchService.create(branch_name, branch_address, city)


def test_get_branch_id():
    city = CityService.create("Cambridge")
    created_branch = BranchService.create(
        "Cardiff Branch", "Blackpole Rd, Worcester WR3 8HP", city)
    id = created_branch.get_id()
    assert id == created_branch._branch_id


def test_get_branch_name():
    city = CityService.create("Exeter")
    created_branch = BranchService.create(
        "Oxford Branch", "Netherton Rd, Ross-on-Wye HR9 7QJ", city)
    name = created_branch.get_name()
    assert name == save_name


def test_get_branch_address():
    city = CityService.create("Norwich")
    created_branch = BranchService.create(
        "Essex Branch", "116-118 Lower Borough Walls, Bath BA1 1QU", city)
    address = created_branch.get_address()
    assert address == save_address


def test_set_branch_name():
    city = CityService.create("Leeds")
    created_branch = BranchService.create(
        "Manchester", "10 Straits Parade, Fishponds, Bristol BS16 2LA", city)
    created_branch.set_branch_name(new_name)
    assert created_branch.get_name() == new_name


def test_set_branch_address():
    city = CityService.create("Lichfield")
    created_branch = BranchService.create(
        "Bath Branch", "4 Eastgate Rd, Bristol BS5 6XX", city)
    created_branch.set_address(new_address)
    assert created_branch.get_address() == new_address


def test_get_by_city():
    city = CityService.get_by_name("Norwich")
    got_branch = BranchService.get_by_city(city)
    query = Database.execute_and_fetchone(
        "SELECT city_id FROM branch WHERE id = %s", got_branch._branch_id)
    id = query[0]
    city_id = city.get_id()
    assert city_id == id


def test_get_city():
    city = CityService.get_by_name("Leeds")
    created_branch = BranchService.create(
        "Plymouth Branch", "12a Oxford Rd, Manchester M1 5QA", city)
    branch_city_id = created_branch.get_city().get_id()
    city_id = city.get_id()
    assert branch_city_id == city_id


def test_set_city():
    city = CityService.get_by_name("Cambridge")
    created_branch = BranchService.create(
        "Lancaster Branch", "67 Broadmead, Bristol BS1 3DX", city)
    new_city = CityService.create("Lancaster")
    created_branch.set_city(new_city)
    city_id = created_branch.get_city().get_id()
    assert city_id == new_city.get_id()


def test_branch_name_validation():
    assert validate_branch_name("Test Branch") == True
    assert validate_branch_name("South Bristol Branch") == True
    assert validate_branch_name("South Bristol Branch ") == False
    assert validate_branch_name(" South Bristol Branch") == False
    assert validate_branch_name("South Bristol  Branch") == False
    assert validate_branch_name("South Bristol Branch1") == False
    assert validate_branch_name("South Bristol Branch!") == False


def test_get_staff():
    branch = BranchService.get_by_name("Bristol Branch")
    user = UserService.create(
        "manager", "myPassword0!", "Test User One", branch, role_id=4)
    user = UserService.create(
        "front-end1", "myPassword0!", "Test User Two", branch, role_id=1)
    user = UserService.create(
        "front-end2", "myPassword0!", "Test User Three", branch, role_id=1)
    users = branch.get_staff()
    assert isinstance(branch, Branch)
    assert isinstance(user, User)
    assert type(users) == list
    assert len(users) == 3
