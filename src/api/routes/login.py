from flask import render_template, session
from marshmallow import Schema, fields
from src.api.middleware.auth import auth_cleanup

from src.api.utils.Result import Error, OK, Status
from src.api.utils.dictify import dictify_user
from src.user.ActiveUser import ActiveUser
from src.user.UserService import UserService
from src.utils.errors import AuthenticationError

cleanup = auth_cleanup


class PostSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


def post(body: dict):
    username: str = body["username"]
    password: str = body["password"]

    print(session.get("user_id"), flush=True)

    try:
        UserService.login(username, password)
    except AuthenticationError:
        return Error(Status.UNAUTHORIZED,
                     "Incorrect credentials")

    user = ActiveUser.get()
    user_id = user.get_id()

    session["user_id"] = user_id

    return OK(dictify_user(user))


def get():
    return render_template('login.html', logged_in='user_id' in session)
