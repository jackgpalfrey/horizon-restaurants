from ..utils.Database import Database
from ..city.City import City
from ..city.CityService import CityService
from ..user.User import User
from ..user.UserService import UserService
from ..user.Role import Role
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

        :raises Exception: If branch name is invalid the branch name is not set.
        """
        if not validate_branch_name(branch_name):
            # FIXME: Replace with correct error
            raise Exception("Invalid name")

        Database.execute_and_commit(
            "UPDATE public.branch SET name = %s WHERE id = %s", branch_name, self._branch_id)

    def set_address(self, branch_address: str) -> None:
        """
        Sets a new branch address using given parameter.

        :raises Exception: If branch address is invalid the address is not set.
        """
        if not validate_branch_address(branch_address):
            # FIXME: Replace with correct error
            raise Exception("Invalid address")

        Database.execute_and_commit(
            "UPDATE public.branch SET address = %s WHERE id = %s", branch_address, self._branch_id)

    def set_city(self, city: City) -> None:
        city_id = city.get_id()

        Database.execute_and_commit(
            "UPDATE public.branch SET city_id = %s WHERE id = %s", city_id, self._branch_id)

    def get_staff(self) -> list[User]:
        result = Database.execute_and_fetchall(
            "SELECT user_id FROM public.branchstaff WHERE branch_id = %s", self._branch_id)

        if result is not None:
            return [User(record[0]) for record in result]

    def get_manager(self) -> User | None:
        result = Database.execute_and_fetchone(
            "SELECT user_id FROM public.branchstaff INNER JOIN public.staff ON public.staff.id = public.branchstaff.user_id WHERE public.branchstaff.branch_id = %s AND public.staff.role_id = %s;", self._branch_id, MANAGER_ROLE_ID)

        if result is not None:
            user = UserService.get_by_id(result[0])
            return user

    def set_manager(self, user: User) -> None:
        role = user.get_role()
        role_id = role.get_id()
        if role_id != MANAGER_ROLE_ID:
            raise Exception("Given user is not with manager role.")
        else:
            manager_id = user.get_id()

            check_if_manager_assigned = Database.execute_and_fetchone(
                "SELECT user_id FROM public.branchstaff WHERE user_id = %s", manager_id)
            check_if_branch_has_manager = Database.execute_and_fetchone(
                "SELECT user_id FROM public.branchstaff WHERE branch_id = %s", self._branch_id)

            if check_if_branch_has_manager is not None:
                raise Exception("Given branch already assigned a manager.")
            else:
                if check_if_manager_assigned is not None:
                    # if manager already assigned, the entry will be deleted and a new one will be made with the given parameters.
                    Database.execute_and_commit(
                        "DELETE FROM public.branchstaff WHERE user_id = %s", manager_id)
                # if manager isn't already assigned, a new entry is made.
                Database.execute_and_commit(
                    "INSERT INTO public.branchstaff (user_id, branch_id) VALUES (%s, %s);", manager_id, self._branch_id)
