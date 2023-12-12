import pytest
from src.user.Role import Role

from src.utils.Database import Database
from src.user.UserService import UserService
from src.user.User import User
from src.utils.errors import AlreadyExistsError, AuthorizationError


username = "myTestUser"
password = "password"
full_name = "My Test User"

new_password = "newpassword"
newest_password = "evennewerpassword"

new_full_name = "New Full Name"
user: User = None


@pytest.fixture(autouse=True)
def before_and_after_test():
    Database.connect()
    Database.init()
    UserService.init()
    Role._load_role_file("tests/roles/test-default.yml")
    Role._load_role_file("tests/roles/test-other.yml")

    yield

    Database.close()


def test_can_create_user():
    user = UserService.create(username, password, full_name)
    assert user is not None
    assert isinstance(user, User)


def test_can_get_user():
    user = UserService.get_by_username(username)
    assert user is not None
    assert isinstance(user, User)


def test_cant_create_duplicate_username():
    with pytest.raises(AlreadyExistsError):
        UserService.create(username, "test", "Test User")


def test_can_create_duplicate_password_and_full_name():
    user = UserService.create("test", password, full_name)
    assert user is not None
    assert isinstance(user, User)


def test_can_get_user_by_username():
    global user
    user = UserService.get_by_username(username)
    assert user is not None
    assert isinstance(user, User)


def test_can_get_users_username():
    assert user.get_username() == username


def test_can_get_users_full_name():
    assert user.get_full_name() == full_name


def test_check_is_password_correct():
    assert user.check_is_password_correct(password) == True
    assert user.check_is_password_correct("not the password") == False


def test_password_is_expired_after_creation():
    assert user.check_has_password_expired() == True


def test_can_set_password_without_validation():
    user.set_password_dont_validate(new_password)
    assert user.check_is_password_correct(new_password) == True


def test_cant_set_password_with_incorrect_old_password():
    with pytest.raises(AuthorizationError):
        user.set_password("not the password", newest_password)


def test_user_role_defaults_to_zero():
    print(Role._roles)
    print(user._get_role_id())
    assert user.get_role().get_id() == 0


def test_user_check_permission():
    assert user.check_permission("test.one") == True
    assert user.check_permission("test") == False


def test_raise_without_permission():
    with pytest.raises(AuthorizationError):
        user.raise_without_permission("test")


def test_can_set_password_with_correct_old_password():
    user.set_password(new_password, newest_password)
    assert user.check_is_password_correct(newest_password) == True


def test_password_unexpired_after_setting_new_password():
    assert user.check_has_password_expired() == False


def test_can_set_full_name():
    user.set_full_name(new_full_name)
    assert user.get_full_name() == new_full_name


def test_can_set_role():
    role = Role.get_by_id(1)
    user.set_role(role)
    assert user.get_role().get_id() == 1
    assert user.check_permission("test.one") == False
    assert user.check_permission("other.one") == True


def test_can_expire_password():
    user.expire_password()
    assert user.check_has_password_expired() == True


def test_can_delete_user():
    user = UserService.get_by_username("test")
    user.delete()

    user = UserService.get_by_username("test")
    assert user is None
