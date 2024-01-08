from marshmallow import Schema, fields
from src.api.middleware.auth import auth_cleanup, auth_guard
from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_user
from src.user.Role import Role
from src.user.UserService import UserService
from src.utils.errors import AuthorizationError, InputError

guard = auth_guard
cleanup = auth_cleanup


class PostSchema(Schema):
    role_id = fields.Int(required=True)


def post(body: dict, username: str):
    role_id: int = body["role_id"]

    role = Role.get_by_id(role_id)
    if role is None:
        return Error(Status.NOT_FOUND,
                     "Role not found, add to src/config/roles")

    try:
        user = UserService.get_by_username(username)
        if user is None:
            return Error(Status.NOT_FOUND, "User not found")

        user.set_role(role)
    except AuthorizationError as e:
        return Error(Status.FORBIDDEN, e.message)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK(dictify_user(user))
