# Author: Jack Palfrey (22032928)
"""Module for handling all users."""
from typing import TYPE_CHECKING

from psycopg2.errors import UniqueViolation

from ..utils.Database import Database
from ..utils.errors import AlreadyExistsError, AuthenticationError, InputError
from .ActiveUser import ActiveUser
from .Role import Role
from .User import User
from .utils import (
    hash_password,
    validate_full_name,
    validate_password,
    validate_username,
)

if TYPE_CHECKING:
    from ..branch.Branch import Branch


class UserService:
    """Static class for managing all users."""

    _active_user: User | None = None

    @staticmethod
    def init():
        """
        Create the admin user if it doesn't exist, and loads all roles.

        Loads roles from src/config/roles/
        """
        print("Initializing UserService...")

        admin_user = UserService.get_by_username("admin", dont_auth=True)
        if admin_user is None:
            UserService.create("admin", "admin", "Administrator", role_id=99)

        ActiveUser.clear()  # Makes sure the active user is None
        Role.load_roles()

    @staticmethod
    def create(username: str,
               password: str,
               full_name: str,
               branch: "Branch | None" = None,
               role_id: int = 0) -> User:
        """
        Create a new user with the given details.

        See the validation rules in ./utils.py

        :raises AlreadyExistsError: If the given username is already in use
        :raises InputError: If any of the parameters are invalid
        :raises PermissionError: If the current user does not have permission
        """
        sql = """
        INSERT INTO public.staff (username, password, full_name, role_id)
        VALUES (%s, %s, %s, %s) RETURNING id;
        """

        # Creating an admin account is handle immediately at initialisation
        # so does not require permission checks and validation.
        if username != "admin":
            UserService._validate_create_user(username, password, full_name)
            ActiveUser.get().raise_without_permission("account.create")

        hashed_password = hash_password(password)

        try:
            cursor = Database.execute(
                sql, username, hashed_password, full_name, role_id)
        except UniqueViolation:
            raise AlreadyExistsError(f"User {username} already exists")

        Database.commit()
        result = cursor.fetchone()
        assert result is not None
        user = User(result[0])

        if branch is not None:
            user.set_branch(branch)

        return user

    @staticmethod
    def get_by_username(username: str, dont_auth: bool = False) -> User | None:
        """
        Get a user with a given username, returns None if no user exists.

        :raises PermissionError: If the current user does not have permission
        """
        if not dont_auth:
            IS_ACTIVE_USER = ActiveUser.get().get_username() == username
            permission = "account.view.self" if IS_ACTIVE_USER\
                else "account.view.all"
            ActiveUser.get().raise_without_permission(permission)

        sql = "SELECT id FROM public.staff WHERE username=%s"
        result = Database.execute_and_fetchone(sql, username)

        if result is None:
            return None

        id = result[0]
        return User(id)

    @staticmethod
    def get_by_id(id: str, dont_auth: bool = False) -> User | None:
        """
        Get a user with a given id, returns None if no user exists with id.

        :raises PermissionError: If the current user does not have permission.
        """
        if not dont_auth:
            IS_ACTIVE_USER = ActiveUser.get().get_id() == id
            permission = "account.view.self" if IS_ACTIVE_USER\
                else "account.view.all"
            ActiveUser.get().raise_without_permission(permission)

        sql = "SELECT id FROM public.staff WHERE id=%s;"
        result = Database.execute_and_fetchone(sql, id)

        if result is None:
            return None

        id = result[0]
        return User(id)

    @staticmethod
    def get_all(dont_auth: bool = False) -> list[User]:
        """
        Get a list of all users. Returns an empty list if none exist.

        :raises PermissionError: If the current user does not have permission.
        """
        if not dont_auth:
            ActiveUser.get().raise_without_permission("account.view.all")

        sql = "SELECT id FROM public.staff;"
        result = Database.execute_and_fetchall(sql)

        return [User(record[0]) for record in result]

    @staticmethod
    def get_all_at_branch(branch: "Branch",
                          dont_auth: bool = False) -> list[User]:
        """
        Get a list of all users at a given branch.

        Returns an empty list if no users exist at that branch.

        :raises PermissionError: If the current user does not have permission
        """
        if not dont_auth:
            ActiveUser.get().raise_without_permission("account.view.all")

        sql = "SELECT user_id FROM public.branchstaff WHERE branch_id=%s;"
        result = Database.execute_and_fetchall(sql, branch.get_id())

        return [User(record[0]) for record in result]

    @staticmethod
    def login(username: str, password: str) -> User:
        """
        Validate credentials and then sets the user as the active user.

        :raises AuthenticationError: If the username or password is incorrect
        """
        user = UserService.get_by_username(username, dont_auth=True)

        if (user is None) or (not user.check_is_password_correct(password)):
            raise AuthenticationError("Username or password incorrect")

        ActiveUser.set(user)
        return user

    @staticmethod
    def logout() -> None:
        """Set the active user to None."""
        ActiveUser.clear()

    @staticmethod
    def _validate_create_user(username: str, password: str, full_name: str):
        """
        Validate given username, password and full name.

        Validation logic can be found under .utils.py

        :raises InputError: If any of the parameters are invalid
        """
        if not validate_username(username):
            raise InputError(
                "Invalid username. Must be between 3 and 15 characters, start\
                with a letter, and only contain letters, numbers, and hyphens")

        if not validate_password(password):
            raise InputError(
                "Invalid password. Must be between 8 and 100 characters,\
                contain at least one uppercase letter, one lowercase letter,\
                one number, and one special character")

        if not validate_full_name(full_name):
            raise InputError(
                "Invalid full name. Must be between 2 and 50 characters, start\
                and end with a letter, and only contain letters and spaces")
