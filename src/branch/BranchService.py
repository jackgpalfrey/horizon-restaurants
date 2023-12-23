from psycopg2.errors import UniqueViolation
from ..utils.Database import Database
from ..city.City import City
from .Branch import Branch
from .utils import validate_branch_name, validate_branch_address
from src.utils.errors import InputError
from src.utils.errors import AlreadyExistsError


class BranchService:
    @staticmethod
    def create(branch_name: str, address: str, city: City) -> Branch:
        """
        Creates a new branch using the given parameters.
        A record of the created branch is added to the database.

        :raises Exception: If branch name or address inputs are invalid the branch is not created.
        """

        BranchService._validate_create_branch(branch_name, address)

        city_id = city.get_id()

        try:
            Database.execute_and_commit(
                "INSERT INTO public.branch (name, address, city_id) VALUES(%s, %s, %s)", branch_name, address, city_id)
        except UniqueViolation:
            raise AlreadyExistsError(f"Branch {branch_name} already exists")

        return BranchService.get_by_name(branch_name)

    @staticmethod
    def get_by_name(branch_name: str) -> Branch | None:
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
    def get_by_city(city: City) -> list[Branch]:
        id = city.get_id()
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.branch WHERE city_id = %s", id)

        if result is not None:
            return Branch(result[0])

    @staticmethod
    def get_all() -> list[Branch]:
        result = Database.execute_and_fetchall("SELECT id FROM public.branch")

        if result is not None:
            return [Branch(record[0]) for record in result]

    @staticmethod
    def _validate_create_branch(branch_name: str, address: str) -> None:
        """
        Validates given name and address based on validation logic in ./utils.py
        through length and character checking. Called in the create() method for branch.

        :raises InputError: If branch name or address inputs are invalid.
        """
        if not validate_branch_name(branch_name):
            raise InputError("Invalid name.")

        if not validate_branch_address(address):
            raise InputError("Invalid address.")
