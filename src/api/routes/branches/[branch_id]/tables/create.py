from flask import render_template
from marshmallow import Schema, fields

from src.api.middleware.auth import auth_cleanup, auth_guard, perm_guard
from src.api.utils.Result import Error, OK, Status
from src.api.utils.dictify import dictify_table
from src.branch.BranchService import BranchService
from src.utils.errors import AlreadyExistsError, InputError

guard = perm_guard("table.create")
cleanup = auth_cleanup


class PostSchema(Schema):
    table_number = fields.Int(required=True)
    capacity = fields.Int(required=True)


def post(body: dict, branch_id: str):
    table_number = body["table_number"]
    capacity = body["capacity"]

    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)
    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    try:
        table = branch.tables().create(table_number, capacity)
    except AlreadyExistsError as e:
        return Error(Status.CONFLICT, e.message)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK(dictify_table(table))


def get(branch_id: str):
    return render_template("table-create.html")
