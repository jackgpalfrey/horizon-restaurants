from src.api.middleware.auth import auth_cleanup, auth_guard
from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_user
from marshmallow import Schema, fields

from src.user.UserService import UserService
from src.utils.errors import AlreadyExistsError, AuthorizationError, InputError

guard = auth_guard
cleanup = auth_cleanup


class PostSchema(Schema):
    username = fields.String(required=True)
    full_name = fields.String(required=True)
    password = fields.String(required=True)
    role_id = fields.Int(required=True)


def post(body: dict):
    username = body["username"]
    full_name = body["full_name"]
    password = body["password"]
    role_id = body["role_id"]
    print(role_id, flush=True)

    try:
        user = UserService.create(username, password, full_name, None, role_id)
    except AuthorizationError as e:
        return Error(Status.FORBIDDEN, e.message)
    except AlreadyExistsError as e:
        return Error(Status.CONFLICT, e.message)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK(dictify_user(user))
