from psycopg2.errors import UniqueViolation

from .Role import Role
from ..utils.errors import AlreadyExistsError, AuthenticationError
from .User import User
from ..utils.Database import Database
from .password_utils import hash_password


class UserService:
    _roles: dict[int, Role] = []

    @staticmethod
    def init():
        print("Initializing UserService...")
        admin_user = UserService.get_by_username("admin")
        if admin_user is None:
            UserService.create("admin", "admin", "Administrator")

        Role.load_roles()

    @staticmethod
    def create(username: str, password: str, fullname: str) -> User:
        sql = """
        INSERT INTO public.user (username, password, full_name) 
        VALUES (%s, %s, %s);
        """

        hashed_password = hash_password(password)

        try:
            Database.execute_and_commit(
                sql, username, hashed_password, fullname)
        except UniqueViolation:
            # FIXME: Should be replaced with Database.rollback() when implemented
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
