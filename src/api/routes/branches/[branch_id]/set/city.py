from marshmallow import Schema, fields
from src.api.middleware.auth import auth_cleanup, auth_guard
from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_branch
from src.branch.BranchService import BranchService
from src.city.CityService import CityService
from src.utils.errors import InputError

guard = auth_guard
cleanup = auth_cleanup


class PostSchema(Schema):
    city_id = fields.String(required=True)


def post(body: dict, branch_id: str):
    city_id: str = body["city_id"]

    city = CityService.get_by_id(city_id)
    if city is None:
        return Error(Status.NOT_FOUND, "City not found")

    try:
        branch = BranchService.get_by_id(branch_id)
        if branch is None:
            return Error(Status.NOT_FOUND, "Branch not found")

        branch.set_city(city)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK(dictify_branch(branch))
