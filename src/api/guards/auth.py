from flask import session

from src.api.utils.Result import Error, Status
def auth_guard():
    if session.get("user_id", None) is None:
        return Error(Status.UNAUTHORIZED, "Not Authenticated.")
