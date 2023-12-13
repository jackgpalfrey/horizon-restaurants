from ..utils.Database import Database


class City:
    def __init__(self, city_id: str) -> None:
        self._city_id = city_id

    def get_id(self) -> str:
        return self._city_id

    def get_name(self) -> str:
        name, = Database.execute_and_fetchone(
            "SELECT name FROM public.city WHERE id = %s", self._city_id)
        return name

    def set_name(self, city_name: str) -> None:
        city_id = self.get_id()
        Database.execute_and_commit(
            "UPDATE public.city SET name = %s WHERE id = %s", city_name, city_id)
