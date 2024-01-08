from src.api.middleware.auth import auth_cleanup, auth_guard
from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_city
from marshmallow import Schema, fields

from src.city.CityService import CityService
from src.utils.errors import AlreadyExistsError, InputError

guard = auth_guard
cleanup = auth_cleanup


class PostSchema(Schema):
    name = fields.String(required=True)


def post(body: dict):
    name = body["name"]

    try:
        city = CityService.create(name)
    except AlreadyExistsError as e:
        return Error(Status.CONFLICT, e.message)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK(dictify_city(city))
