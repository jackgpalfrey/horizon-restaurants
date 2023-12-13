from ..utils.Database import Database
from ..city.City import City


class CityService:
    @staticmethod
    def create(city_name: str) -> City:
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
