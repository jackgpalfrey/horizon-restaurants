from typing import TYPE_CHECKING

from ..utils.errors import AuthenticationError

if TYPE_CHECKING:
    from .User import User


class ActiveUser:
    _active_user: "User"

    @staticmethod
    def get() -> "User":
        if ActiveUser._active_user is None:
            raise AuthenticationError("No user is logged in")

        return ActiveUser._active_user

    @staticmethod
    def clear():
        ActiveUser._active_user = None

    @staticmethod
    def set(user: "User") -> None:
        ActiveUser._active_user = user
