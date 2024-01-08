# Author: Dina Hassanein (22066792)
import pytest
from src.branch.Branch import Branch
from src.branch.BranchService import BranchService
from src.branch.utils import validate_branch_name
from src.city.CityService import CityService
from src.tables.BranchTables import BranchTables
from src.user.User import User
from src.user.UserService import UserService
from src.utils.Database import Database
from src.utils.errors import AlreadyExistsError, InputError

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
    assert isinstance(got_branch, Branch)
    assert isinstance(got_branch._branch_id, str)
    assert created_branch._branch_id == got_branch._branch_id


def test_get_all_branches():
    branch = BranchService.get_all()
    assert len(branch) == 2
    assert isinstance(branch, list)


def test_cannot_create_duplicate_branch():
    city = CityService.create("Nottingham")
    with pytest.raises(AlreadyExistsError):
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
    assert city is not None
    got_branch = BranchService.get_by_city(city)
    assert got_branch is not None
    query = Database.execute_and_fetchone(
        "SELECT city_id FROM branch WHERE id = %s", got_branch[0]._branch_id)
    assert query is not None
    id = query[0]
    city_id = city.get_id()
    assert city_id == id


def test_get_city():
    city = CityService.get_by_name("Leeds")
    assert city is not None
    created_branch = BranchService.create(
        "Plymouth Branch", "12a Oxford Rd, Manchester M1 5QA", city)
    branch_city_id = created_branch.get_city().get_id()
    city_id = city.get_id()
    assert branch_city_id == city_id


def test_set_city():
    city = CityService.get_by_name("Cambridge")
    assert city is not None
    created_branch = BranchService.create(
        "Lancaster Branch", "67 Broadmead, Bristol BS1 3DX", city)
    new_city = CityService.create("Lancaster")
    created_branch.set_city(new_city)
    city_id = created_branch.get_city().get_id()
    assert city_id == new_city.get_id()


def test_branch_name_validation():
    assert validate_branch_name("Test Branch") is True
    assert validate_branch_name("South Bristol Branch") is True
    assert validate_branch_name("South Bristol Branch ") is False
    assert validate_branch_name(" South Bristol Branch") is False
    assert validate_branch_name("South Bristol  Branch") is False
    assert validate_branch_name("South Bristol Branch1") is False
    assert validate_branch_name("South Bristol Branch!") is False


def test_get_staff():
    branch = BranchService.get_by_name("Bristol Branch")
    assert branch is not None
    branch2 = BranchService.get_by_name("Bath Branch")
    assert branch2 is not None
    user = UserService.create(
        "manager", "myPassword0!", "Test User One", branch, role_id=4)
    user = UserService.create(
        "front-end1", "myPassword0!", "Test User Two", branch, role_id=1)
    user = UserService.create(
        "manager1", "myPassword0!", "Test User Three", branch2, role_id=4)
    users = branch.get_staff()
    users2 = branch2.get_staff()
    assert isinstance(branch, Branch)
    assert isinstance(user, User)
    assert isinstance(users, list)
    assert len(users) == 2
    assert len(users2) == 1


def test_get_branch_by_user():
    city = CityService.create("Derby")
    branch = BranchService.create(
        "Derby Branch", "4 Eastgate Rd, Bristol BS5 6XX", city)
    user = UserService.create(
        "front-end2", "myPassword0!", "Test User Four", role_id=4)
    user.set_branch(branch)
    got_branch = BranchService.get_branch_by_user(user)
    assert isinstance(got_branch, Branch)
    assert branch._branch_id == got_branch._branch_id


def test_get_manager():
    branch = BranchService.get_by_name("Bristol Branch")
    assert branch is not None
    manager = branch.get_manager()
    assert manager is not None
    manager_role = manager.get_role()
    manager_role_id = manager_role.get_id()
    assert isinstance(manager, User)
    assert manager_role_id == 4


def test_set_manager():
    branch = BranchService.get_by_name("Plymouth Branch")
    assert branch is not None
    manager = UserService.create(
        "manager2", "myPassword0!", "Test User Five", role_id=4)
    assert manager is not None
    assert isinstance(manager, User)
    branch.set_manager(manager)
    new_manager = branch.get_manager()
    assert new_manager is not None
    manager_id = manager.get_id()
    new_manager_id = new_manager.get_id()
    assert manager_id == new_manager_id
    assert isinstance(new_manager, User)


def test_cant_assign_same_manager():
    branch = BranchService.get_by_name("Bristol Branch")
    branch2 = BranchService.get_by_name("Bath Branch")
    assert branch is not None
    assert branch2 is not None
    manager = branch2.get_manager()
    assert manager is not None
    with pytest.raises(AlreadyExistsError):
        branch.set_manager(manager)


def test_cant_set_manager_with_wrong_role():
    branch = BranchService.get_by_name("Bath Branch")
    assert branch is not None
    user = UserService.create(
        "front-end3", "myPassword0!", "Test User Six", role_id=1)
    assert user is not None
    with pytest.raises(InputError):
        branch.set_manager(user)


def test_set_manager_with_assigned_branch():
    # Lancaster branch not assigned a manager
    branch = BranchService.get_by_name("Lancaster Branch")
    assert branch is not None
    branch2 = BranchService.get_by_name("Bath Branch")
    assert branch2 is not None
    manager = branch2.get_manager()
    assert manager is not None
    manager_id = manager.get_id()
    branch.set_manager(manager)
    new_manager = branch.get_manager()
    assert new_manager is not None
    new_manager_id = new_manager.get_id()
    assert manager_id == new_manager_id
    assert isinstance(new_manager, User)
    assert branch2.get_manager() is None


def test_create_instance_BranchTables():
    city = CityService.create("Plymouth")
    table = BranchService.create(
        "Test Branch", "15-29 Union St, Bristol BS1 2DF", city).tables()
    assert isinstance(table, BranchTables)
