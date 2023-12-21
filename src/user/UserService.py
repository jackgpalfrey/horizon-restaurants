from psycopg2.errors import UniqueViolation

from ..utils.errors import AlreadyExistsError, AuthenticationError, InputError
from ..utils.Database import Database

from .utils import hash_password, validate_username, validate_password, validate_full_name
from .Role import Role
from .User import User
from .ActiveUser import ActiveUser

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..branch.Branch import Branch


class UserService:
    _roles: dict[int, Role] = []
    _active_user: User | None = None

    @staticmethod
    def init():
        """
        Creates the admin user if it doesn't exist, and loads all roles from src/config/roles/
        """

        print("Initializing UserService...")

        admin_user = UserService.get_by_username("admin", dont_auth=True)
        if admin_user is None:
            UserService.create("admin", "admin", "Administrator", role_id=99)

        ActiveUser.clear()  # Makes sure the active user is None
        Role.load_roles()

    @staticmethod
    def create(username: str, password: str, full_name: str, branch: "Branch" = None, role_id: int = 0) -> User:
        """
        Create a new user with the given username, password, full name, and optional role id

        :param username: The username of the new user (see ./utils.py for validation rules)
        :param password: The password of the new user (see ./utils.py for validation rules)
        :param full_name: The full name of the new user (see ./utils.py for validation rules)
        :param role_id: The role id of the new user (defaults to 0)

        :raises AlreadyExistsError: If a user with the given username already exists
        :raises InputError: If any of the parameters are invalid
        :raises PermissionError: If the current user does not have permission to create users

        :returns: The newly created user
        """

        sql = """
        INSERT INTO public.user (username, password, full_name, role_id, branch_id) 
        VALUES (%s, %s, %s, %s, %s);
        """

        if username != "admin":
            UserService._validate_create_user(username, password, full_name)
            ActiveUser.get().raise_without_permission("account.create")

        hashed_password = hash_password(password)

        branch_id = branch.get_id() if branch is not None else None

        try:
            Database.execute_and_commit(
                sql, username, hashed_password, full_name, role_id, branch_id)
        except UniqueViolation:
            raise AlreadyExistsError(f"User {username} already exists")

        return UserService.get_by_username(username, dont_auth=True)

    @staticmethod
    def get_by_username(username: str, dont_auth: bool = False) -> User | None:
        """
        Gets a user with a given username, returns None if no user exists with that username

        :raises PermissionError: If the current user does not have permission to view the user
        """

        if not dont_auth:
            IS_ACTIVE_USER = ActiveUser.get().get_username() == username
            permission = "account.view.self" if IS_ACTIVE_USER else "account.view.all"
            ActiveUser.get().raise_without_permission(permission)

        sql = "SELECT id FROM public.user WHERE username=%s"
        result = Database.execute_and_fetchone(sql, username)

        if result is None:
            return None

        id = result[0]
        return User(id)

    @staticmethod
    def get_by_id(id: str, dont_auth: bool = False) -> User | None:
        """
        Gets a user with a given id, returns None if no user exists with that id

        :raises PermissionError: If the current user does not have permission to view the user
        """

        if not dont_auth:
            IS_ACTIVE_USER = ActiveUser.get().get_id() == id
            permission = "account.view.self" if IS_ACTIVE_USER else "account.view.all"
            ActiveUser.get().raise_without_permission(permission)

        sql = "SELECT id FROM public.user WHERE id=%s;"
        result = Database.execute_and_fetchone(sql, id)

        if result is None:
            return None

        id = result[0]
        return User(id)

    @staticmethod
    def get_all(dont_auth: bool = False) -> list[User]:
        """
        Get a list of all users as User classes. Returns an empty list if no users exist

        :raises PermissionError: If the current user does not have permission to view all users
        """

        if not dont_auth:
            ActiveUser.get().raise_without_permission("account.view.all")

        sql = "SELECT id FROM public.user;"
        result = Database.execute_and_fetchall(sql)

        return [User(record[0]) for record in result]

    @staticmethod
    def login(username: str, password: str) -> User:
        """
        Validates credentials and then sets the user as the active user. 

        :raises AuthenticationError: If the username or password is incorrect
        """

        user = UserService.get_by_username(username, dont_auth=True)

        USER_DOSENT_EXIST = user is None
        INCORRECT_PASSWORD = not user.check_is_password_correct(password)

        if USER_DOSENT_EXIST or INCORRECT_PASSWORD:
            raise AuthenticationError("Username or password incorrect")

        ActiveUser.set(user)
        return user

    @staticmethod
    def logout() -> None:
        """
        Sets the active user to None
        """
        ActiveUser.clear()

    @staticmethod
    def _validate_create_user(username: str, password: str, full_name: str):
        """
        Checks the parameters for UserService.create() to make sure they are valid based on the validation rules in ./utils.py

        :raises InputError: If any of the parameters are invalid
        """

        if not validate_username(username):
            raise InputError(
                "Invalid username. Must be between 3 and 15 characters, start with a letter, and only contain letters, numbers, and hyphens")

        if not validate_password(password):
            raise InputError(
                "Invalid password. Must be between 8 and 100 characters, contain at least one uppercase letter, one lowercase letter, one number, and one special character")

        if not validate_full_name(full_name):
            raise InputError(
                "Invalid full name. Must be between 2 and 50 characters, start and end with a letter, and only contain letters and spaces")
