from ..utils.Database import Database
from .utils import validate_city_name


class City:
    def __init__(self, city_id: str) -> None:
        self._city_id = city_id

    def get_id(self) -> str:
        return self._city_id

    def get_name(self) -> str:
        name = Database.execute_and_fetchone(
            "SELECT name FROM public.city WHERE id = %s", self._city_id)
        return name[0]

    def set_name(self, city_name: str) -> None:
        """
        Sets a new city name using given parameter.

        :raises Exception: If city name is invalid the city name is not set.
        """
        if not validate_city_name(city_name):
            # FIXME: Replace with correct error
            raise Exception(
                "Invalid name.")

        city_id = self.get_id()
        Database.execute_and_commit(
            "UPDATE public.city SET name = %s WHERE id = %s", city_name, city_id)
