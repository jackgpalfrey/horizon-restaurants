from ..utils.Database import Database
from ..city.City import City
from ..city.CityService import CityService
from ..user.User import User
from ..user.UserService import UserService
from ..user.Role import Role
from src.utils.errors import InputError, AlreadyExistsError
from .utils import validate_branch_name, validate_branch_address

MANAGER_ROLE_ID = 4


class Branch:
    def __init__(self, branch_id: str):
        self._branch_id = branch_id

    def get_id(self) -> str:
        return self._branch_id

    def get_name(self) -> str:
        name = Database.execute_and_fetchone(
            "SELECT name FROM public.branch WHERE id = %s", self._branch_id)
        return name[0]

    def get_address(self) -> str:
        address = Database.execute_and_fetchone(
            "SELECT address from public.branch WHERE id = %s", self._branch_id)
        return address[0]

    def get_city(self) -> City:
        city_id = Database.execute_and_fetchone(
            "SELECT city_id FROM public.branch WHERE id = %s", self._branch_id)
        city = CityService.get_by_id(city_id[0])
        return city

    def set_branch_name(self, branch_name: str) -> None:
        """
        Sets a new branch name using given parameter.

        :raises InputError: If branch name is invalid the branch name is not set.
        """
        if not validate_branch_name(branch_name):
            raise InputError("Invalid branch name")

        Database.execute_and_commit(
            "UPDATE public.branch SET name = %s WHERE id = %s", branch_name, self._branch_id)

    def set_address(self, branch_address: str) -> None:
        """
        Sets a new branch address using given parameter.

        :raises InputError: If branch address is invalid the address is not set.
        """
        if not validate_branch_address(branch_address):
            raise InputError("Invalid address")

        Database.execute_and_commit(
            "UPDATE public.branch SET address = %s WHERE id = %s", branch_address, self._branch_id)

    def set_city(self, city: City) -> None:
        city_id = city.get_id()

        Database.execute_and_commit(
            "UPDATE public.branch SET city_id = %s WHERE id = %s", city_id, self._branch_id)

    def get_staff(self) -> list[User]:
        result = Database.execute_and_fetchall(
            "SELECT user_id FROM public.branchstaff WHERE branch_id = %s", self._branch_id)

        return [User(record[0]) for record in result]

    def get_manager(self) -> User | None:
        result = Database.execute_and_fetchone(
            "SELECT user_id FROM public.branchstaff INNER JOIN public.staff ON public.staff.id = public.branchstaff.user_id WHERE public.branchstaff.branch_id = %s AND public.staff.role_id = %s;", self._branch_id, MANAGER_ROLE_ID)

        if result is not None:
            return UserService.get_by_id(result[0])

    def set_manager(self, user: User) -> None:
        """
        Assigns manager to branch and performs necessary checks to ensure user can be assigned.
        Checks if manager already assigned to a branch and deletes the entry if it exists, a new
        entry is made using the given parameters. Checks if branch given has a manager, if that
        is the case, no entry is made because each branch can only have one manager.

        :raises InputError: If given user role is not manager role
        :raises AlreadyExistsError: If given branch already assigned a manager.
        """
        role = user.get_role()
        role_id = role.get_id()
        if role_id != MANAGER_ROLE_ID:
            raise InputError("Given user is not with manager role.")
        manager_id = user.get_id()
        branch_manager_id = self.get_manager().get_id(
        ) if self.get_manager() is not None else None
        manager_assigned = Database.execute_and_fetchone(
            "SELECT user_id FROM public.branchstaff WHERE user_id = %s", manager_id)
        branch_has_manager = Database.execute_and_fetchone(
            "SELECT user_id FROM public.branchstaff WHERE user_id = %s AND branch_id = %s", branch_manager_id, self._branch_id)

        if branch_has_manager is not None:
            raise AlreadyExistsError(
                "Given branch already assigned a manager.")
        if manager_assigned is not None:
            # if manager already assigned, the entry will be deleted to remove link between user and any other branches. Each user can work at only one branch.
            Database.execute_and_commit(
                "DELETE FROM public.branchstaff WHERE user_id = %s", manager_id)
        Database.execute_and_commit(
            "INSERT INTO public.branchstaff (user_id, branch_id) VALUES (%s, %s);", manager_id, self._branch_id)
