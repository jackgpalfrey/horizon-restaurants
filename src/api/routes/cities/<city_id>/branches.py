from src.api.utils.Result import OK, Error, Status
from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.user.UserService import UserService


def post(city_id: str = ""):
    if city_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    city = CityService.get_by_id(city_id)
    if city is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    branches = BranchService.get_by_city(city)

    branch_data = [{"id": b.get_id(),
                   "name": b.get_name()} for b in branches]

    return OK({"branches": branch_data})

