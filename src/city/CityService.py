# Author: Dina Hassanein (22066792)
"""Module for managing all cities."""
from src.utils.errors import InputError

from ..utils.Database import Database
from .City import City
from .utils import validate_city_name


class CityService:
    """Static class for managing cities."""

    @staticmethod
    def create(city_name: str) -> City:
        """
        Create a new city using the given parameter.

        A record of the created city is added to the database.

        :raises InputError: If city name input is invalid.
        """
        CityService._validate_create_city(city_name)

        cursor = Database.execute(
            "INSERT INTO public.city (name) VALUES(%s) RETURNING id",
            city_name)

        Database.commit()
        result = cursor.fetchone()

        assert result is not None  # TODO: See City.py todo
        return City(result[0])

    @staticmethod
    def get_by_name(city_name: str) -> City | None:
        """Get city by name."""
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.city WHERE name = %s", city_name)

        if result is not None:
            return City(result[0])

    @staticmethod
    def get_by_id(city_id: str) -> City | None:
        """Get city by ID."""
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.city WHERE id = %s", city_id)

        if result is not None:
            return City(result[0])

    @staticmethod
    def get_all() -> list[City]:
        """Get all cities."""
        result = Database.execute_and_fetchall("SELECT id FROM public.city")

        return [City(record[0]) for record in result]

    @staticmethod
    def _validate_create_city(city_name: str):
        """
        Validate given name based on validation logic in ./utils.py.

        Uses length and character checking.
        Called in the create() method for city.

        :raises InputError: If city name input is invalid.
        """
        if not validate_city_name(city_name):
            raise InputError("Invalid name.")
