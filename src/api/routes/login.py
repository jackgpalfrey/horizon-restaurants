from marshmallow import Schema, fields

from src.api.utils.Result import Error, OK, Status
from src.user.ActiveUser import ActiveUser
from src.user.UserService import UserService
from src.utils.errors import AuthenticationError


class PostSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


def post(body: dict):
    username: str = body["username"]
    password: str = body["password"]

    try:
        UserService.login(username, password)
    except AuthenticationError:
        return Error(Status.UNAUTHORIZED,
                     "Incorrect credentials")

    user = ActiveUser.get()
    return OK({
        "user_id": user.get_id(),
        "role_id": user.get_role().get_id()
    })
