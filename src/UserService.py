import bcrypt

from src.utils.errors import AlreadyExistsError

from .User import User
from .utils.Database import Database
from psycopg2.errors import UniqueViolation


class UserService:
    @staticmethod
    def init():
        print("Initializing UserService...")
        admin_user = UserService.get_by_username("admin")
        if admin_user is None:
            UserService.create("admin", "admin", "Administrator")

    @staticmethod
    def create(username: str, password: str, fullname: str) -> User:
        sql = """
        INSERT INTO public.user (username, password, full_name) 
        VALUES (%s, %s, %s);
        """

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        try:
            Database.execute_and_commit(
                sql, username, hashed_password, fullname)
        except UniqueViolation:
            raise AlreadyExistsError(f"User {username} already exists")

        return UserService.get_by_username(username)

    @staticmethod
    def get_by_username(username: str) -> User | None:
        sql = """
        SELECT * FROM public.user WHERE username=%s;
        """

        result = Database.execute_and_fetchone(sql, username)
        if result is None:
            return None

        id = result[0]
        return User(id)
