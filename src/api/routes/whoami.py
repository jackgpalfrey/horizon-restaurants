from src.api.middleware.auth import auth_cleanup, auth_guard
from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_user
from marshmallow import Schema, fields
from src.user.ActiveUser import ActiveUser

from src.user.UserService import UserService
from src.utils.errors import AlreadyExistsError, AuthorizationError, InputError

guard = auth_guard
cleanup = auth_cleanup


def post():
    user = ActiveUser.get()

    if user is None:
        return Error(Status.UNAUTHORIZED, "Not logged in")

    return OK(dictify_user(user))
