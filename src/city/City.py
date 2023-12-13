from ..utils.Database import Database


class City:
    def __init__(self, city_id: str) -> None:
        self._city_id = city_id

    def get_name(self) -> str:
        name, = Database.execute_and_fetchone(
            "SELECT name FROM public.city WHERE id = %s", self._city_id)
        return name
