import pytest

from src.utils.Database import Database
from src.UserService import UserService
from src.User import User
from src.utils.errors import AlreadyExistsError


@pytest.fixture(autouse=True)
def before_and_after_test():
    Database.connect()
    Database.init()
    UserService.init()

    yield

    Database.close()


def test_can_create_user():
    user = UserService.create("test", "test", "Test User")
    assert user is not None
    assert isinstance(user, User)


def test_can_get_user():
    user = UserService.get_by_username("test")
    assert user is not None
    assert isinstance(user, User)


def test_cant_create_duplicate_username():
    with pytest.raises(AlreadyExistsError):
        UserService.create("test", "test", "Test User")


def test_can_delete_user():
    user = UserService.get_by_username("test")
    user.delete()

    user = UserService.get_by_username("test")
    assert user is None
