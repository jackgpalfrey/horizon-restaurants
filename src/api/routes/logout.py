from flask import session
from src.api.guards.auth import auth_guard
from src.api.utils.Result import OK

guard = auth_guard

def post():
    session.clear()

    return OK({})
