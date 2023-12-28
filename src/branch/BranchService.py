"""Module for creating and accessing branches."""
from psycopg2.errors import UniqueViolation

from src.utils.errors import InputError
from src.utils.errors import AlreadyExistsError

from ..user.User import User
from ..city.City import City
from ..utils.Database import Database
from .Branch import Branch
from .utils import validate_branch_address, validate_branch_name


class BranchService:
    """Static Class For Managing Branches."""

    @staticmethod
    def create(branch_name: str, address: str, city: City) -> Branch:
        """
        Create a new branch using the given parameters.

        A record of the created branch is added to the database.

        :raises InputError: If branch name or address inputs are invalid.
        :raises AlreadyExistsError: If a branch with given name already exists.
        """
        BranchService._validate_create_branch(branch_name, address)

        city_id = city.get_id()

        try:
            cursor = Database.execute(
                "INSERT INTO public.branch (name, address, city_id)\
                VALUES (%s, %s, %s) RETURNING id",
                branch_name, address, city_id)
        except UniqueViolation:
            raise AlreadyExistsError(f"Branch {branch_name} already exists")

        Database.commit()
        result = cursor.fetchone()
        assert result is not None

        return Branch(result[0])

    @staticmethod
    def get_by_name(branch_name: str) -> Branch | None:
        """Get a branch by name."""
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.branch WHERE name = %s", branch_name)

        if result is not None:
            return Branch(result[0])

    @staticmethod
    def get_by_id(branch_id: str) -> Branch | None:
        """Get a branch by ID."""
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.branch WHERE id = %s", branch_id)

        if result is not None:
            return Branch(result[0])

    @staticmethod
    def get_branch_by_user(user: User) -> Branch | None:
        result = Database.execute_and_fetchone(
            "SELECT branch_id FROM public.branchstaff WHERE user_id=%s;", user._user_id)

        return Branch(result[0])

    @staticmethod
    def get_by_city(city: City) -> list[Branch]:
        """Get a list of all branches in a given city."""
        id = city.get_id()
        result = Database.execute_and_fetchall(
            "SELECT id FROM public.branch WHERE city_id = %s", id)

        return [Branch(record[0]) for record in result]

    @staticmethod
    def get_all() -> list[Branch]:
        """Get a list of all branches."""
        result = Database.execute_and_fetchall("SELECT id FROM public.branch")

        return [Branch(record[0]) for record in result]

    @staticmethod
    def _validate_create_branch(branch_name: str, address: str) -> None:
        """
        Validate given name and address based on validation in ./utils.py.

        Using length and character checking.
        Called in the create() method for branch.

        :raises InputError: If branch name or address inputs are invalid.
        """
        if not validate_branch_name(branch_name):
            raise InputError("Invalid name.")

        if not validate_branch_address(address):
            raise InputError("Invalid address.")
