from flask import render_template
from marshmallow import Schema, fields

from src.api.middleware.auth import auth_cleanup, auth_guard, perm_guard
from src.api.utils.Result import Error, OK, Status
from src.api.utils.dictify import dictify_discount, dictify_table
from src.branch.BranchService import BranchService
from src.utils.errors import AlreadyExistsError, InputError

guard = perm_guard("discount.create")
cleanup = auth_cleanup


class PostSchema(Schema):
    description = fields.String(required=True)
    multiplier = fields.Float(required=True)


def post(body: dict, branch_id: str):
    description = body["description"]
    multiplier = body["multiplier"]

    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)
    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    try:
        discount = branch.discounts().create(multiplier, description)
    except AlreadyExistsError as e:
        return Error(Status.CONFLICT, e.message)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK(dictify_discount(discount))


def get(branch_id: str):
    return render_template("discount-create.html")
