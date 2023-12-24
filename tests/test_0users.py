import pytest
from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.user.ActiveUser import ActiveUser
from src.user.Role import Role
from src.user.User import User
from src.user.UserService import UserService
from src.user.utils import (
    validate_full_name,
    validate_password,
    validate_username
)
from src.utils.Database import Database
from src.utils.errors import (
    AlreadyExistsError,
    AuthenticationError,
    AuthorizationError,
    InputError,
)


usernames = ["test", "test1", "test2"]
full_names = ["Test User", "Test User Two", "Test User Three"]
password = "myPassword0!"

new_password = "newPassw0rd!"
newest_password = "evenNewerPassw0rd!"
new_full_name = "New Full Name"
user: User | None = None


@pytest.fixture(autouse=True, scope="module")
def before_and_after_test():
    Database.connect()
    Database.DEBUG_delete_all_tables("DANGEROUSLY DELETE ALL TABLES")
    Database.init()
    UserService.init()
    Role._load_role_file("tests/roles/test-default.yml")
    Role._load_role_file("tests/roles/test-other.yml")
    Role._load_role_file("tests/roles/test-extends.yml")
    Role._load_role_file("tests/roles/test-implicit-wildcards.yml")
    Role._load_role_file("tests/roles/test-explicit-wildcard.yml")
    Role._load_role_file("tests/roles/test-negation.yml")
    Role._load_role_file("tests/roles/test-multi-extends.yml")

    UserService.login("admin", "admin")

    yield

    Database.close()


def test_username_validation():
    assert validate_username("test") is True
    assert validate_username("test123") is True
    assert validate_username("test-123") is True
    assert validate_username("Test") is False
    assert validate_username("123test") is False
    assert validate_username("test_123") is False
    assert validate_username("t") is False
    assert validate_username("te") is True
    assert validate_username("strlongerthan15c") is False
    assert validate_username("strequalto15chr") is True


def test_password_validation():
    assert validate_password("mypassword") is False
    assert validate_password("myPassword") is False
    assert validate_password("myPassword0") is False
    assert validate_password("myPassword0!") is True
    assert validate_password("myPas0!") is False
    assert validate_password("myPass0!") is True
    long_pass = "Mysuperduperlongpasswordthatshouldnotbe@llowedbecauseits\
longerthanthe100characterslimitbyjustasingle!"
    assert validate_password(long_pass) is False
    assert validate_password(long_pass[:-1]) is True


def test_full_name_validation():
    assert validate_full_name("Test User") is True
    assert validate_full_name("First Middle Last") is True
    assert validate_full_name("First Middle Last ") is False
    assert validate_full_name(" First Middle Last") is False
    assert validate_full_name("First Middle  Last") is False
    assert validate_full_name("First Middle Last1") is False
    assert validate_full_name("First Middle Last!") is False


def test_can_create_user():
    user = UserService.create(usernames[0], password, full_names[0])
    assert user is not None
    assert isinstance(user, User)


def test_can_get_user():
    user = UserService.get_by_username(usernames[0])
    assert user is not None
    assert isinstance(user, User)
    assert user.get_full_name() == full_names[0]


def test_cant_create_duplicate_username():
    with pytest.raises(AlreadyExistsError):
        UserService.create(usernames[0], password, full_names[1])


def test_can_create_duplicate_password_and_full_name():
    user = UserService.create(usernames[1], password, full_names[0])
    assert user is not None
    assert isinstance(user, User)


def test_can_get_user_by_username():
    global user
    user = UserService.get_by_username(usernames[0])
    assert user is not None
    assert isinstance(user, User)


def test_can_get_users_username():
    assert user is not None
    assert user.get_username() == usernames[0]


def test_can_get_users_full_name():
    assert user is not None
    assert user.get_full_name() == full_names[0]


def test_cant_create_invalid_username():
    with pytest.raises(InputError):
        UserService.create("invalid!", password, full_names[0])


def test_cant_create_invalid_password():
    with pytest.raises(InputError):
        UserService.create("invalid", "inval", full_names[0])


def test_cant_create_invalid_full_name():
    with pytest.raises(InputError):
        UserService.create("invalid", password, "invalid!")


def test_check_is_password_correct():
    assert user is not None
    assert user.check_is_password_correct(password) is True
    assert user.check_is_password_correct("notThePassw0rd!") is False


def test_password_is_expired_after_creation():
    assert user is not None
    assert user.check_has_password_expired() is True


def test_can_set_password_without_validation():
    assert user is not None
    user.set_password_dont_validate(new_password)
    assert user.check_is_password_correct(new_password) is True


def test_cant_set_password_with_incorrect_old_password():
    assert user is not None
    with pytest.raises(AuthorizationError):
        user.set_password("inc0rrectPassw0rd!", newest_password)


def test_user_role_defaults_to_zero():
    assert user is not None
    assert user.get_role().get_id() == 0


def test_user_check_permission():
    assert user is not None
    assert user.check_permission("test.one") is True
    assert user.check_permission("test") is False


def test_raise_without_permission():
    assert user is not None
    with pytest.raises(AuthorizationError):
        user.raise_without_permission("test")


def test_cant_set_password_with_invalid_new_password():
    assert user is not None
    with pytest.raises(InputError):
        user.set_password(new_password, "invalid")


def test_can_set_password_with_correct_old_password():
    assert user is not None
    user.set_password(new_password, newest_password)
    assert user.check_is_password_correct(newest_password) is True


def test_password_unexpired_after_setting_new_password():
    assert user is not None
    assert user.check_has_password_expired() is False


def test_can_set_full_name():
    assert user is not None
    user.set_full_name(new_full_name)
    assert user.get_full_name() == new_full_name


def test_cant_set_invalid_full_name():
    assert user is not None
    with pytest.raises(InputError):
        user.set_full_name("invalid!")


def test_can_set_role():
    assert user is not None
    role = Role.get_by_id(1)
    assert role is not None
    user.set_role(role)
    assert user.get_role().get_id() == 1
    assert user.check_permission("test.one") is False
    assert user.check_permission("other.one") is True


def test_roles_can_be_extended():
    assert user is not None
    role = Role.get_by_id(2)
    assert role is not None
    user.set_role(role)
    assert user.get_role().get_id() == 2
    assert user.check_permission("test.one") is True
    assert user.check_permission("extend.one") is True


def test_implicit_wildcard_permission():
    assert user is not None
    role = Role.get_by_id(3)
    assert role is not None
    user.set_role(role)
    assert user.get_role().get_id() == 3
    assert user.check_permission("expltest.one") is True
    assert user.check_permission("expltest.two") is True
    assert user.check_permission("expltest.three") is True
    assert user.check_permission("expltes.four") is False


def test_explicit_wildcard_permission():
    assert user is not None
    role = Role.get_by_id(4)
    assert role is not None
    user.set_role(role)
    assert user.get_role().get_id() == 4
    assert user.check_permission("my.permission") is True
    assert user.check_permission("your.permission") is True
    assert user.check_permission("your.other.permission") is True


def test_permission_negation():
    assert user is not None
    role = Role.get_by_id(5)
    assert role is not None
    user.set_role(role)
    assert user.get_role().get_id() == 5
    assert user.check_permission("test.one") is True
    assert user.check_permission("permission.good") is True
    assert user.check_permission("permission.bad") is False


def test_multiple_extends():
    assert user is not None
    role = Role.get_by_id(6)
    assert role is not None
    user.set_role(role)
    assert user.get_role().get_id() == 6
    assert user.check_permission("test.one") is True
    assert user.check_permission("test.two") is True
    assert user.check_permission("other.one") is True
    assert user.check_permission("other.two") is True
    assert user.check_permission("permission.cool") is True
    assert user.check_permission("random.one") is False


def test_can_expire_password():
    assert user is not None
    user.expire_password()
    assert user.check_has_password_expired() is True


def test_get_by_id():
    created_user = UserService.create("idtest", password, "ID Test")
    user = UserService.get_by_id(created_user._user_id)
    assert isinstance(user, User)
    assert user._user_id == created_user._user_id
    assert user.get_username() == "idtest"
    assert user.get_full_name() == "ID Test"


def test_get_all():
    users = UserService.get_all()
    assert len(users) == 4


def test_get_all_at_branch():
    city = CityService.create("Lancaster")
    branch = BranchService.create(
        "Lancaster Branch", "67 Broadmead, Lancaster BS1 3DX", city)
    UserService.create(
        "manageruser", "myPassword0!", "TestUser One", branch, role_id=4)
    UserService.create(
        "frontenduser", "myPassword0!", "TestUser Two", branch, role_id=1)
    UserService.create(
        "kitchenuser", "myPassword0!", "TestUser Three", branch, role_id=2)
    UserService.create(
        "chefuser", "myPassword0!", "TestUser Four", branch, role_id=3)
    users = UserService.get_all_at_branch(branch)
    assert isinstance(users, list)
    assert len(users) == 4


def test_login_to_admin_account():
    user = UserService.login("admin", "admin")
    assert user is not None
    assert isinstance(user, User)
    assert user.get_username() == "admin"
    assert user.get_full_name() == "Administrator"


def test_get_active_user():
    user = ActiveUser.get()
    assert user is not None
    assert isinstance(user, User)
    assert user.get_username() == "admin"
    assert user.get_full_name() == "Administrator"


def test_can_delete_user():
    UserService.create(usernames[2], password, full_names[2])
    user = UserService.get_by_username(usernames[2])
    assert user is not None
    user.delete()

    user = UserService.get_by_username(usernames[2])
    assert user is None


def test_set_branch():
    city = CityService.create("Derby")
    branch = BranchService.create(
        "Derby Branch", "4 Eastgate Rd, Bristol BS5 6XX", city)
    user = UserService.create(
        "manager2", "myPassword0!", "Test User Six", role_id=4)
    user.set_branch(branch)
    staff = branch.get_staff()
    assert isinstance(staff, list)
    assert len(staff) == 1


def test_logout():
    user = UserService.logout()
    assert user is None

    with pytest.raises(AuthenticationError):
        ActiveUser.get()


def test_cant_update_when_logged_out():
    assert user is not None
    with pytest.raises(AuthenticationError):
        user.set_password(newest_password, new_password)

    with pytest.raises(AuthenticationError):
        user.set_full_name(new_full_name)


def test_cant_update_any_when_non_admin_role():
    assert user is not None
    UserService.login(usernames[1], password)

    with pytest.raises(AuthorizationError):
        user.set_password(new_password, password)

    with pytest.raises(AuthorizationError):
        user.set_full_name(full_names[0])

    with pytest.raises(AuthorizationError):
        role = Role.get_by_id(1)
        assert role is not None
        user.set_role(role)
