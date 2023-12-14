# import ..utils.Database from database
from ..utils.Database import Database
from ..city.City import City
from ..city.CityService import CityService


class Branch:
    def __init__(self, branch_id: str) -> None:
        self._branch_id = branch_id

    # only the following method can directly return the variable's value because it was created
    # earlier, unlike the others which need to query the database to get the data
    def get_id(self) -> str:
        return self._branch_id

    def get_name(self) -> str:
        name, = Database.execute_and_fetchone(
            "SELECT name FROM public.branch WHERE id = %s", self._branch_id)
        return name

    def get_address(self) -> str:
        address, = Database.execute_and_fetchone(
            "SELECT address from public.branch WHERE id = %s", self._branch_id)
        return address

    def set_branch_name(self, branch_name: str) -> None:
        branch_id = self.get_id()
        Database.execute_and_commit(
            "UPDATE public.branch SET name = %s WHERE id = %s", branch_name, branch_id)

    def set_address(self, branch_address: str) -> None:
        branch_id = self.get_id()
        Database.execute_and_commit(
            "UPDATE public.branch SET address = %s WHERE id = %s", branch_address, branch_id)

    def get_city(self) -> City:
        city_id, = Database.execute_and_fetchone(
            "SELECT city_id FROM public.branch WHERE id = %s", self._branch_id)
        city = CityService.get_by_id(city_id)
        return city

    def set_city(self, city: City) -> None:
        branch_id = self.get_id()
        city_id = city.get_id()
        Database.execute_and_commit(
            "UPDATE public.branch SET city_id = %s WHERE id = %s", city_id, branch_id)
