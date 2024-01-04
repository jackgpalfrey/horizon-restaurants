from src.api.middleware.auth import auth_cleanup, auth_guard
from src.api.utils.Result import OK, Error, Status
from src.branch.BranchService import BranchService
from marshmallow import Schema, fields

from src.city.CityService import CityService
from src.utils.errors import AlreadyExistsError, InputError

guard = auth_guard
cleanup = auth_cleanup


class PostSchema(Schema):
    name = fields.String(required=True)
    address = fields.String(required=True)
    city_id = fields.String(required=True)


def post(body: dict):
    name = body["name"]
    address = body["address"]
    city_id = body["city_id"]

    city = CityService.get_by_id(city_id)
    if city is None:
        return Error(Status.NOT_FOUND, "City not found.")

    try:
        branch = BranchService.create(name, address, city)
    except AlreadyExistsError as e:
        return Error(Status.CONFLICT, e.message)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    branch_data = {
        "id": branch.get_id(),
        "name": branch.get_name(),
        "address": branch.get_address(),
        "city": branch.get_city().get_name(),
    }

    return OK(branch_data)
