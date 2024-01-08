# Author: Jack Palfrey (22032928)
"""
Module for managing ActiveUsers.

See ActiveUser class docstring for more details
"""
from typing import TYPE_CHECKING

from ..utils.errors import AuthenticationError

if TYPE_CHECKING:
    from .User import User


class ActiveUser:
    """
    Class for managing the Active User.

    ActiveUser is the potentially temporary system for handling user sign-in

    It's a simple class that allows you to:
    - get the currently signed in user with ActiveUser.get()
    - sign-in a user with ActiveUser.set()
    - logout with ActiveUser.clear()
    """

    _active_user: "User | None"

    @staticmethod
    def get() -> "User":
        """
        Get the currently signed in user.

        :raises AuthenticationError: If no user is logged in
        """
        if ActiveUser._active_user is None:
            raise AuthenticationError("No user is logged in")

        return ActiveUser._active_user

    @staticmethod
    def clear():
        """Logout user."""
        ActiveUser._active_user = None

    @staticmethod
    def set(user: "User") -> None:
        """Login with the given user."""
        ActiveUser._active_user = user
