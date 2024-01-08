from src.api.utils.Result import OK
from src.user.UserService import UserService


def post():
    users = UserService.get_all(dont_auth=True)

    users_data = [{"username": u.get_username(),
                   "full_name": u.get_full_name()} for u in users]

    return OK({"users": users_data})
