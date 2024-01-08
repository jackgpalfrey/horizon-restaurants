from marshmallow import Schema, fields
from src.api.middleware.auth import auth_cleanup, auth_guard
from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_branch
from src.branch.BranchService import BranchService

guard = auth_guard
cleanup = auth_cleanup


class PostSchema(Schema):
    name = fields.String(required=True)


def post(body: dict, branch_id: str):
    name: str = body["name"]

    try:
        branch = BranchService.get_by_id(branch_id)
        if branch is None:
            return Error(Status.NOT_FOUND, "Branch not found")

        branch.set_branch_name(name)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK(dictify_branch(branch))
