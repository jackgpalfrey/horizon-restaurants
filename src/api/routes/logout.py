from flask import session
from src.api.middleware.auth import auth_guard, auth_cleanup
from src.api.utils.Result import OK

guard = auth_guard
cleanup = auth_cleanup

def post():
    session.clear()

    return OK({})
