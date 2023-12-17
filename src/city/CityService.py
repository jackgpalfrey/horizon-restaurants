from ..utils.Database import Database
from .City import City
from .utils import validate_city_name


class CityService:
    @staticmethod
    def create(city_name: str) -> City:

        CityService._validate_create_city(city_name)

        Database.execute_and_commit(
            "INSERT INTO public.city (name) VALUES(%s)", city_name)
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.city WHERE name = %s", city_name)
        return City(result[0])

    @staticmethod
    def get_by_name(city_name: str) -> City:
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.city WHERE name = %s", city_name)

        if result is not None:
            return City(result[0])

    @staticmethod
    def get_by_id(city_id: str) -> City:
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.city WHERE id = %s", city_id)

        if result is not None:
            return City(result[0])

    @staticmethod
    def get_all() -> City:
        result = Database.execute_and_fetchall(
            "SELECT id FROM public.city")

        if result is not None:
            return [City(record[0]) for record in result]

    @staticmethod
    def _validate_create_city(city_name: str):

        if not validate_city_name(city_name):
            # FIXME: Replace with correct error
            raise Exception(
                "Invalid name.")
