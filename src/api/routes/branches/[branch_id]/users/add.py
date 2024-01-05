from marshmallow import Schema, fields
from src.api.middleware.auth import auth_cleanup, auth_guard
from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_user
from src.branch.BranchService import BranchService
from src.user.UserService import UserService
from src.utils.errors import AuthorizationError

guard = auth_guard
cleanup = auth_cleanup


class PostSchema(Schema):
    username = fields.String(required=True)


def post(body, branch_id: str = ""):
    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)
    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    username: str = body["username"]

    try:
        user = UserService.get_by_username(username)

        if user is None:
            return Error(Status.NOT_FOUND, "User not found.")

        user.set_branch(branch)

    except AuthorizationError as e:
        return Error(Status.FORBIDDEN, e.message)

    users = UserService.get_all_at_branch(branch)
    users_data = [dictify_user(u) for u in users]

    return OK({"users": users_data})
