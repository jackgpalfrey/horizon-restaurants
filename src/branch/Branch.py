"""Module for Branch Managment."""
from typing import Any
from src.menu.BranchMenu import BranchMenu

from src.utils.errors import AlreadyExistsError, InputError

from ..city.City import City
from ..tables.BranchTables import BranchTables
from ..reservations.BranchReservations import BranchReservations
from ..inventory.BranchInventory import BranchInventory
from ..user.User import User
from ..utils.Database import Database
from .utils import validate_branch_address, validate_branch_name


MANAGER_ROLE_ID = 4


class Branch:
    """Manage Branch."""

    def __init__(self, branch_id: str):
        """Do not call outside of BranchService."""
        self._branch_id = branch_id

    def tables(self):
        """Access table managment methods."""
        return BranchTables(self._branch_id)

    def menu(self):
        """Access menu management methods."""
        return BranchMenu(self._branch_id)

    def reservations(self):
        """Access reservation managment methods."""
        return BranchReservations(self._branch_id)

    def inventory(self):
        """Access inventory managment methods."""
        return BranchInventory(self._branch_id)

    def get_id(self) -> str:
        """Get ID of branch."""
        return self._branch_id

    def get_name(self) -> str:
        """Get name of branch."""
        name: Any = Database.execute_and_fetchone(
            "SELECT name FROM public.branch WHERE id = %s", self._branch_id)
        return name[0]

    def get_address(self) -> str:
        """Get address of branch."""
        address: Any = Database.execute_and_fetchone(
            "SELECT address from public.branch WHERE id = %s", self._branch_id)
        return address[0]

    def get_city(self) -> City:
        """Get city of branch."""
        city_id: Any = Database.execute_and_fetchone(
            "SELECT city_id FROM public.branch WHERE id = %s", self._branch_id)

        return City(city_id[0])

    def set_branch_name(self, branch_name: str) -> None:
        """
        Set a new branch name using given parameter.

        :raises InputError: If branch name is invalid
        """
        if not validate_branch_name(branch_name):
            raise InputError("Invalid branch name")

        Database.execute_and_commit(
            "UPDATE public.branch SET name = %s WHERE id = %s",
            branch_name, self._branch_id)

    def set_address(self, branch_address: str) -> None:
        """
        Set a new branch address using given parameter.

        :raises InputError: If branch address is invalid.
        """
        if not validate_branch_address(branch_address):
            raise InputError("Invalid address")

        Database.execute_and_commit(
            "UPDATE public.branch SET address = %s WHERE id = %s",
            branch_address, self._branch_id)

    def set_city(self, city: City) -> None:
        """Set city."""
        city_id = city.get_id()

        Database.execute_and_commit(
            "UPDATE public.branch SET city_id = %s WHERE id = %s",
            city_id, self._branch_id)

    def get_staff(self) -> list[User]:
        """Get a list of all Users who work at this branch."""
        result = Database.execute_and_fetchall(
            "SELECT user_id FROM public.branchstaff WHERE branch_id = %s",
            self._branch_id)

        return [User(record[0]) for record in result]

    def get_manager(self) -> User | None:
        """Get manager of branch."""
        sql = """SELECT user_id FROM public.branchstaff\
        INNER JOIN public.staff ON public.staff.id= public.branchstaff.user_id\
        WHERE public.branchstaff.branch_id = %s\
        AND public.staff.role_id = %s;"""

        result = Database.execute_and_fetchone(
            sql, self._branch_id, MANAGER_ROLE_ID)

        if result is not None:
            return User(result[0])

    def set_manager(self, user: User) -> None:
        """
        Assign manager to branch and performs necessary checks.

        Checks if manager already assigned to a branch and deletes the entry
        if it exists, a new entry is made using the given parameters.
        Checks if branch given has a manager, if that is the case, no entry is
        made because each branch can only have one manager.

        :raises InputError: If given user role is not manager role
        :raises AlreadyExistsError: If given branch already assigned a manager.
        """
        role = user.get_role()
        role_id = role.get_id()

        if role_id != MANAGER_ROLE_ID:
            raise InputError("Given user is not with manager role.")

        manager = self.get_manager()
        if manager is not None:
            raise AlreadyExistsError("Branch already assigned a manager.")

        manager_id = user.get_id()
        manager_assigned = Database.execute_and_fetchone(
            "SELECT user_id FROM public.branchstaff WHERE user_id = %s",
            manager_id)

        if manager_assigned is not None:
            # if manager already assigned, the entry will be deleted to remove
            # link between user and any other branches. Each user can work at
            # only one branch.
            Database.execute_and_commit(
                "DELETE FROM public.branchstaff WHERE user_id =%s", manager_id)

        Database.execute_and_commit(
            "INSERT INTO public.branchstaff (user_id, branch_id)\
            VALUES (%s, %s);", manager_id, self._branch_id)
