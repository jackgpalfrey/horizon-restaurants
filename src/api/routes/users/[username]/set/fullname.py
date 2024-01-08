from marshmallow import Schema, fields
from src.api.middleware.auth import auth_cleanup, auth_guard
from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_user
from src.user.UserService import UserService
from src.utils.errors import AuthorizationError, InputError

guard = auth_guard
cleanup = auth_cleanup


class PostSchema(Schema):
    full_name = fields.String(required=True)


def post(body: dict, username: str):
    full_name: str = body["full_name"]

    try:
        user = UserService.get_by_username(username)
        if user is None:
            return Error(Status.NOT_FOUND, "User not found")

        user.set_full_name(full_name)
    except AuthorizationError as e:
        return Error(Status.FORBIDDEN, e.message)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK(dictify_user(user))
