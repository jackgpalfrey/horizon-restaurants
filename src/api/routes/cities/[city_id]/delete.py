from src.api.middleware.auth import auth_cleanup, auth_guard
from src.api.utils.Result import OK, Error, Status

from src.city.CityService import CityService
from src.utils.errors import AlreadyExistsError, InputError

guard = auth_guard
cleanup = auth_cleanup


def post(city_id: str):
    try:
        city = CityService.get_by_id(city_id)
        if city is None:
            return Error(Status.NOT_FOUND, "City not found")

        city.delete()
    except AlreadyExistsError as e:
        return Error(Status.CONFLICT, e.message)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK({})
