from ..utils.Database import Database
from ..branch.Branch import Branch
# from ..city.CityService import CityService
from ..city.City import City


class BranchService:
    @staticmethod
    def create(branch_name: str, address: str, city: City) -> Branch:  # "city_name: str"
        # id = CityService.get_by_name(city_name)
        id = city.get_id()
        Database.execute_and_commit(
            "INSERT INTO public.branch (name, address, city_id) VALUES(%s, %s, %s)", branch_name, address, id)

        # branch_id = Database.execute_and_fetchone("SELECT id FROM public.branch WHERE name = %s", branch_name)
        # return Branch(branch_id)
        return BranchService.get_by_name(branch_name)

    @staticmethod
    def get_by_name(branch_name: str) -> Branch:
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.branch WHERE name = %s", branch_name)

        if result is not None:
            return Branch(result[0])

    @staticmethod
    def get_by_id(branch_id: str) -> Branch:
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.branch WHERE id = %s", branch_id)

        if result is not None:
            return Branch(result[0])

    @staticmethod
    def get_all() -> Branch:
        result = Database.execute_and_fetchall(
            "SELECT id FROM public.branch")

        if result is not None:
            return [Branch(record[0]) for record in result]

    @staticmethod
    def get_by_city(city: City) -> Branch:
        id = city.get_id()
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.branch WHERE city_id = %s", id)

        if result is not None:
            return Branch(result[0])
