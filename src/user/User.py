from .Role import Role
from .utils import hash_password, check_password, validate_full_name, validate_password
from src.utils.errors import AuthorizationError, InputError
from ..utils.Database import Database


class User:
    def __init__(self, user_id: str) -> None:
        self._user_id = user_id

    def get_username(self) -> str:
        sql = "SELECT username FROM public.user WHERE id=%s;"

        result = Database.execute_and_fetchone(sql, self._user_id)
        return result[0]

    def get_full_name(self) -> str:
        sql = "SELECT full_name FROM public.user WHERE id=%s;"

        result = Database.execute_and_fetchone(sql, self._user_id)
        return result[0]

    def check_is_password_correct(self, password: str) -> bool:
        sql = "SELECT password FROM public.user WHERE id=%s;"

        result = Database.execute_and_fetchone(sql, self._user_id)
        correct_hashed_password = result[0]

        return check_password(password, correct_hashed_password)

    def check_has_password_expired(self) -> bool:
        sql = "SELECT is_password_expired FROM public.user WHERE id=%s;"

        result = Database.execute_and_fetchone(sql, self._user_id)
        return result[0]

    def get_role(self) -> Role:
        return Role.get_by_id(self._get_role_id())

    def _get_role_id(self) -> int:
        sql = "SELECT role_id FROM public.user WHERE id=%s;"

        result = Database.execute_and_fetchone(sql, self._user_id)
        return result[0]

    def check_permission(self, permission: str) -> bool:
        role = self.get_role()
        return role.check_permission(permission)

    def raise_without_permission(self, permission: str) -> None:
        if not self.check_permission(permission):
            raise AuthorizationError(
                "You do not have permission to perform this action")

    def set_password(self, old: str, new: str) -> None:
        if not self.check_is_password_correct(old):
            raise AuthorizationError("Incorrect password")

        if not validate_password(new):
            raise InputError("Invalid password")

        self.set_password_dont_validate(new)

    def set_password_dont_validate(self, new: str) -> None:
        sql = "UPDATE public.user SET password=%s, is_password_expired=FALSE WHERE id=%s;"

        hashed_password = hash_password(new)

        Database.execute_and_commit(sql, hashed_password, self._user_id)

    def set_full_name(self, full_name: str) -> None:
        sql = "UPDATE public.user SET full_name=%s WHERE id=%s;"

        if not validate_full_name(full_name):
            raise InputError("Invalid full name")

        Database.execute_and_commit(sql, full_name, self._user_id)

    def set_role(self, role: Role) -> None:
        sql = "UPDATE public.user SET role_id=%s WHERE id=%s;"

        Database.execute_and_commit(sql, role.get_id(), self._user_id)

    def expire_password(self) -> None:
        sql = "UPDATE public.user SET is_password_expired=TRUE WHERE id=%s;"

        Database.execute_and_commit(sql, self._user_id)

    def delete(self) -> None:
        # FIXME: Could cause issues with references, might be best to switch to soft deletion and a cron job
        sql = """
        DELETE FROM public.user WHERE id=%s;
        """

        Database.execute_and_commit(sql, self._user_id)
