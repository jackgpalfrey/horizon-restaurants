"""Module for managing an individual Role."""
from typing import TYPE_CHECKING

from src.utils.errors import AuthorizationError, InputError

from ..utils.Database import Database
from .ActiveUser import ActiveUser
from .Role import Role
from .utils import (
    check_password,
    hash_password,
    validate_full_name,
    validate_password
)

if TYPE_CHECKING:
    from ..branch.Branch import Branch

MANAGER_ROLE_ID = 4


class User:
    """Class for managing specific users."""

    def __init__(self, user_id: str) -> None:
        """Don't call directly outside of the UserService class."""
        self._user_id = user_id

    def get_id(self):
        """Get ID of user."""
        return self._user_id

    def get_username(self) -> str:
        """Get username of user."""
        sql = "SELECT username FROM public.staff WHERE id=%s;"

        result = Database.execute_and_fetchone(sql, self.get_id())
        assert result is not None
        return result[0]

    def get_full_name(self) -> str:
        """Get fullname of user."""
        sql = "SELECT full_name FROM public.staff WHERE id=%s;"

        result = Database.execute_and_fetchone(sql, self._user_id)
        assert result is not None
        return result[0]

    def check_is_password_correct(self, password: str) -> bool:
        """Check if a given password matches the one in the database."""
        sql = "SELECT password FROM public.staff WHERE id=%s;"

        result = Database.execute_and_fetchone(sql, self._user_id)
        assert result is not None
        correct_hashed_password = result[0]

        return check_password(password, correct_hashed_password)

    def check_has_password_expired(self) -> bool:
        """Check if the password of the user has expired."""
        sql = "SELECT is_password_expired FROM public.staff WHERE id=%s;"

        result = Database.execute_and_fetchone(sql, self._user_id)
        assert result is not None
        return result[0]

    def get_role(self) -> Role:
        """Get role of user."""
        role = Role.get_by_id(self._get_role_id())
        assert role is not None
        return role

    def _get_role_id(self) -> int:
        sql = "SELECT role_id FROM public.staff WHERE id=%s;"

        result = Database.execute_and_fetchone(sql, self._user_id)
        assert result is not None
        return result[0]

    def check_permission(self, permission: str) -> bool:
        """Check if user has permission."""
        role = self.get_role()
        return role.check_permission(permission)

    def raise_without_permission(self, permission: str) -> None:
        """
        Check if user has permission and raises error if not.

        :raises AuthorizationError: If the user doesn't have the permission
        """
        if not self.check_permission(permission):
            raise AuthorizationError(
                "You do not have permission to perform this action")

    def set_password(self, old: str, new: str) -> None:
        """
        Set the user's password as given, if the old password is correct.

        Also unexpires the password

        :raises AuthorizationError: If the old password is incorrect.
        :raises InputError: If the new password is invalid.
        :raises PermissionError: If the current user does not have permission.
        """
        if not self.check_is_password_correct(old):
            raise AuthorizationError("Incorrect password")

        if not validate_password(new):
            raise InputError("Invalid password")

        self.set_password_dont_validate(new)

    def set_password_dont_validate(self, new: str) -> None:
        """
        Set password without perform checks or validation.

        Dosen't check the old password or validate the new password
        but still checks permissions. Also unexpires the password.

        :raises PermissionError: If the current user does not have permission
        """
        sql = "UPDATE public.staff SET password=%s, is_password_expired=FALSE\
        WHERE id=%s;"

        active_user = ActiveUser.get()
        THIS_IS_ACTIVE_USER = active_user.get_id() == self._user_id

        permission = "account.update-password.all" if THIS_IS_ACTIVE_USER\
            else "account.update.self"
        active_user.raise_without_permission(permission)

        hashed_password = hash_password(new)

        Database.execute_and_commit(sql, hashed_password, self._user_id)

    def set_full_name(self, full_name: str) -> None:
        """
        Set the user's full name to the given value.

        :raises InputError: If the new full name is invalid
        :raises PermissionError: If the current user does not have permission
        """
        sql = "UPDATE public.staff SET full_name=%s WHERE id=%s;"

        active_user = ActiveUser.get()
        THIS_IS_ACTIVE_USER = active_user.get_id() == self._user_id

        permission = "account.update.all" if THIS_IS_ACTIVE_USER\
            else "account.update.self"
        active_user.raise_without_permission(permission)

        if not validate_full_name(full_name):
            raise InputError("Invalid full name")

        Database.execute_and_commit(sql, full_name, self._user_id)

    def set_role(self, role: Role) -> None:
        """
        Set the user's role to the given value.

        :raises PermissionError: If the current user does not have permission
        """
        sql = "UPDATE public.staff SET role_id=%s WHERE id=%s;"

        ActiveUser.get().raise_without_permission("account.update-role.all")

        Database.execute_and_commit(sql, role.get_id(), self._user_id)

    def expire_password(self) -> None:
        """Expire users password so they have to reset it after next login."""
        sql = "UPDATE public.staff SET is_password_expired=TRUE WHERE id=%s;"

        Database.execute_and_commit(sql, self._user_id)

    def delete(self) -> None:
        """
        Delete the user from the database.

        After calling you should immediately discard this object. Not doing so
        will cause errors.

        :raises PermissionError: If the current user does not have permission
        """
        # Could cause issues with references, might be best to switch to soft
        # deletion and a cron job
        sql = "DELETE FROM public.staff WHERE id=%s;"

        ActiveUser.get().raise_without_permission("account.delete.all")

        Database.execute_and_commit(sql, self._user_id)

    def set_branch(self, branch: "Branch") -> None:
        """
        Assign user to branch.

        If user already assigned, branch_id associated with user is updated.
        Otherwise, a new entry is made to assign the user to a branch.

        :raises PermissionError: If the current user does not have permission.
        """
        role = self.get_role()
        role_id = role.get_id()

        sql_check = "SELECT user_id FROM public.branchstaff WHERE user_id = %s"

        check = Database.execute_and_fetchone(sql_check, self._user_id)
        branch_id = branch.get_id()

        ActiveUser.get().raise_without_permission("branch.update")

        if check is not None and role_id != MANAGER_ROLE_ID:
            sql = "UPDATE public.branchstaff SET branch_id=%s WHERE user_id=%s"
        else:
            sql = "INSERT INTO public.branchstaff (branch_id, user_id)\
            VALUES (%s, %s);"

        Database.execute_and_commit(sql, branch_id, self._user_id)
