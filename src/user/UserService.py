from psycopg2.errors import UniqueViolation

from .Role import Role
from ..utils.errors import AlreadyExistsError, AuthenticationError, InputError
from .User import User
from ..utils.Database import Database
from .utils import hash_password, validate_username, validate_password, validate_full_name


class UserService:
    _roles: dict[int, Role] = []
    _active_user: User | None = None

    @staticmethod
    def init():
        print("Initializing UserService...")
        admin_user = UserService.get_by_username("admin")
        if admin_user is None:
            UserService.create("admin", "admin", "Administrator")

        Role.load_roles()

    @staticmethod
    def create(username: str, password: str, full_name: str) -> User:
        sql = """
        INSERT INTO public.user (username, password, full_name) 
        VALUES (%s, %s, %s);
        """

        if username != "admin":
            UserService._validate_create_user(username, password, full_name)

        hashed_password = hash_password(password)

        try:
            Database.execute_and_commit(
                sql, username, hashed_password, full_name)
        except UniqueViolation:
            # FIXME: hotfix-1 fixes this
            Database.connection.rollback()
            raise AlreadyExistsError(f"User {username} already exists")

        return UserService.get_by_username(username)

    @staticmethod
    def get_by_username(username: str) -> User | None:
        sql = """
        SELECT id FROM public.user WHERE username=%s;
        """

        result = Database.execute_and_fetchone(sql, username)
        if result is None:
            return None

        id = result[0]
        return User(id)

    @staticmethod
    def get_by_id(username: str) -> User | None:
        sql = """
        SELECT id FROM public.user WHERE id=%s;
        """

        result = Database.execute_and_fetchone(sql, username)
        if result is None:
            return None

        id = result[0]
        return User(id)

    @staticmethod
    def get_all() -> list[User]:
        sql = """
        SELECT id FROM public.user;
        """

        result = Database.execute_and_fetchall(sql)
        return [User(record[0]) for record in result]

    @staticmethod
    def get_active() -> User:
        user = UserService._active_user

        if user is None:
            raise AuthenticationError("No user is logged in")

        return user

    @staticmethod
    def login(username: str, password: str) -> User:
        user = UserService.get_by_username(username)

        USER_DOSENT_EXIST = user is None
        INCORRECT_PASSWORD = not user.check_is_password_correct(password)

        if USER_DOSENT_EXIST or INCORRECT_PASSWORD:
            raise AuthenticationError("Username or password incorrect")

        UserService._set_active(user)
        return user

    @staticmethod
    def logout() -> None:
        UserService._set_active(None)

    @staticmethod
    def _set_active(user: User) -> None:
        UserService._active_user = user

    @staticmethod
    def _validate_create_user(username: str, password: str, full_name: str):
        if not validate_username(username):
            raise InputError(
                "Invalid username. Must be between 3 and 15 characters, start with a letter, and only contain letters, numbers, and hyphens")

        if not validate_password(password):
            raise InputError(
                "Invalid password. Must be between 8 and 100 characters, contain at least one uppercase letter, one lowercase letter, one number, and one special character")

        if not validate_full_name(full_name):
            raise InputError(
                "Invalid full name. Must be between 2 and 50 characters, start and end with a letter, and only contain letters and spaces")
