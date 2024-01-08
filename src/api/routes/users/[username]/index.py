from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_user
from src.user.UserService import UserService
from src.api.middleware.auth import auth_guard, auth_cleanup

guard = auth_guard
cleanup = auth_cleanup

def post(username: str):
    if username is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    user = UserService.get_by_username(username)

    if user is None:
        return Error(Status.NOT_FOUND, "User not found.")

    return OK(dictify_user(user))
