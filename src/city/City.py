# Author: Dina Hassanein (22066792)
"""Module for managing individual cities."""
from psycopg2.errors import UniqueViolation
from src.user.ActiveUser import ActiveUser
from src.utils.errors import AlreadyExistsError, InputError

from ..utils.Database import Database
from .utils import validate_city_name


class City:
    """Class for managing individual cities."""

    def __init__(self, city_id: str) -> None:
        """Don't call outside of CityService."""
        self._city_id = city_id

    def get_id(self) -> str:
        """Get cities ID."""
        return self._city_id

    def get_name(self) -> str:
        """Get cities name."""
        name = Database.execute_and_fetchone(
            "SELECT name FROM public.city WHERE id = %s", self._city_id)
        # The assert is to provide type narrowing as we know name is not None
        # Not entriely sure if this is a good approach and should probably come
        # back to it in the future. TODO: Check this is okay and if not fix
        assert name is not None
        return name[0]

    def set_name(self, city_name: str) -> None:
        """
        Set a new city name using given parameter.

        :raises InputError: If city name is invalid the city name is not set.
        """
        if not validate_city_name(city_name):
            raise InputError("Invalid name.")

        city_id = self.get_id()
        try:
            Database.execute_and_commit(
                "UPDATE public.city SET name = %s WHERE id = %s",
                city_name, city_id)
        except UniqueViolation:
            raise AlreadyExistsError(f"City '{city_name}' already exists")

    def delete(self) -> None:
        """
        Delete the city from the database.

        After calling you should immediately discard this object. Not doing so
        will cause errors.

        :raises PermissionError: If the current user does not have permission
        """
        # Could cause issues with references, might be best to switch to soft
        # deletion and a cron job
        sql = "DELETE FROM public.city WHERE id=%s;"

        ActiveUser.get().raise_without_permission("city.delete")

        Database.execute_and_commit(sql, self._city_id)
