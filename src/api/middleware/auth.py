from flask import session

from src.api.utils.Result import Error, Status
from src.user.ActiveUser import ActiveUser
from src.user.User import User


def auth_guard():
    user_id: str | None = session.get("user_id", None)

    if user_id is None:
        return Error(Status.UNAUTHORIZED, "Not Authenticated.")

    ActiveUser.set(User(user_id))


def perm_guard(permission: str):
    def internal_perm_guard():
        auth_guard()
        ActiveUser.get().raise_without_permission(permission)

    return internal_perm_guard


def auth_cleanup():
    ActiveUser.clear()
