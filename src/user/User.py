from .ActiveUser import ActiveUser
from .Role import Role
from .utils import hash_password, check_password, validate_full_name, validate_password
from src.utils.errors import AuthorizationError, InputError
from ..utils.Database import Database


class User:
    def __init__(self, user_id: str) -> None:
        """Should not be called directly outside of the UserService class"""

        self._user_id = user_id

    def get_id(self):
        return self._user_id

    def get_username(self) -> str:
        sql = "SELECT username FROM public.staff WHERE id=%s;"

        return Database.execute_and_fetchone(sql, self.get_id())[0]

    def get_full_name(self) -> str:
        sql = "SELECT full_name FROM public.staff WHERE id=%s;"

        return Database.execute_and_fetchone(sql, self._user_id)[0]

    def check_is_password_correct(self, password: str) -> bool:
        sql = "SELECT password FROM public.staff WHERE id=%s;"

        result = Database.execute_and_fetchone(sql, self._user_id)
        correct_hashed_password = result[0]

        return check_password(password, correct_hashed_password)

    def check_has_password_expired(self) -> bool:
        sql = "SELECT is_password_expired FROM public.staff WHERE id=%s;"

        return Database.execute_and_fetchone(sql, self._user_id)[0]

    def get_role(self) -> Role:
        return Role.get_by_id(self._get_role_id())

    def _get_role_id(self) -> int:
        sql = "SELECT role_id FROM public.staff WHERE id=%s;"

        return Database.execute_and_fetchone(sql, self._user_id)[0]

    def check_permission(self, permission: str) -> bool:
        role = self.get_role()
        return role.check_permission(permission)

    def raise_without_permission(self, permission: str) -> None:
        """
        :raises AuthorizationError: If the user does not have the given permission
        """
        if not self.check_permission(permission):
            raise AuthorizationError(
                "You do not have permission to perform this action")

    def set_password(self, old: str, new: str) -> None:
        """
        Sets the user's password to the given value, if the old password is correct
        Also unexpires the password

        :raises AuthorizationError: If the old password is incorrect
        :raises InputError: If the new password is invalid
        :raises PermissionError: If the current user does not have permission to update the password
        """

        if not self.check_is_password_correct(old):
            raise AuthorizationError("Incorrect password")

        if not validate_password(new):
            raise InputError("Invalid password")

        self.set_password_dont_validate(new)

    def set_password_dont_validate(self, new: str) -> None:
        """
        Sets password without checking the old password or validating the new password but still checks permissions
        Also unexpires the password. 

        :raises PermissionError: If the current user does not have permission to update the password
        """

        sql = "UPDATE public.staff SET password=%s, is_password_expired=FALSE WHERE id=%s;"

        active_user = ActiveUser.get()
        THIS_IS_ACTIVE_USER = active_user.get_id() == self._user_id

        permission = "account.update-password.all" if THIS_IS_ACTIVE_USER else "account.update.self"
        active_user.raise_without_permission(permission)

        hashed_password = hash_password(new)

        Database.execute_and_commit(sql, hashed_password, self._user_id)

    def set_full_name(self, full_name: str) -> None:
        """
        Sets the user's full name to the given value

        :raises InputError: If the new full name is invalid
        :raises PermissionError: If the current user does not have permission to update the full name
        """
        sql = "UPDATE public.staff SET full_name=%s WHERE id=%s;"

        active_user = ActiveUser.get()
        THIS_IS_ACTIVE_USER = active_user.get_id() == self._user_id

        permission = "account.update.all" if THIS_IS_ACTIVE_USER else "account.update.self"
        active_user.raise_without_permission(permission)

        if not validate_full_name(full_name):
            raise InputError("Invalid full name")

        Database.execute_and_commit(sql, full_name, self._user_id)

    def set_role(self, role: Role) -> None:
        """
        Sets the user's role to the given value

        :raises PermissionError: If the current user does not have permission to update the role
        """

        sql = "UPDATE public.staff SET role_id=%s WHERE id=%s;"

        ActiveUser.get().raise_without_permission("account.update-role.all")

        Database.execute_and_commit(sql, role.get_id(), self._user_id)

    def expire_password(self) -> None:
        sql = "UPDATE public.staff SET is_password_expired=TRUE WHERE id=%s;"

        Database.execute_and_commit(sql, self._user_id)

    def delete(self) -> None:
        """
        Deletes the user from the database. After calling you should immediately discard this object.
        Not doing so will cause errors.

        :raises PermissionError: If the current user does not have permission to delete the user
        """

        # Could cause issues with references, might be best to switch to soft deletion and a cron job
        sql = "DELETE FROM public.staff WHERE id=%s;"

        ActiveUser.get().raise_without_permission("account.delete.all")

        Database.execute_and_commit(sql, self._user_id)
