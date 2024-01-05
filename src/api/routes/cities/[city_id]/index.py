from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_city
from src.city.CityService import CityService


def post(city_id: str = ""):
    if city_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    city = CityService.get_by_id(city_id)

    if city is None:
        return Error(Status.NOT_FOUND, "City not found.")

    return OK(dictify_city(city))
