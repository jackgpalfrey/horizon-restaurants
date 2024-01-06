from src.api.middleware.auth import auth_cleanup, auth_guard
from src.api.utils.Result import OK, Error, Status
from src.user.UserService import UserService
from src.utils.errors import AuthorizationError

guard = auth_guard
cleanup = auth_cleanup


def post(username: str):
    try:
        user = UserService.get_by_username(username)
        if user is None:
            return Error(Status.NOT_FOUND, "User not found")

        user.delete()
    except AuthorizationError as e:
        return Error(Status.FORBIDDEN, e.message)

    return OK({})
