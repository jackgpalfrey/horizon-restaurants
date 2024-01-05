from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_simple_branch
from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.user.UserService import UserService


def post(city_id: str = ""):
    if city_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    city = CityService.get_by_id(city_id)
    if city is None:
        return Error(Status.NOT_FOUND, "City not found.")

    branches = BranchService.get_by_city(city)

    branches_data = [dictify_simple_branch(b) for b in branches]

    return OK({"branches": branches_data})
