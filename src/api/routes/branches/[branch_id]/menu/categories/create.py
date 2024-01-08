from flask import render_template
from marshmallow import Schema, fields

from src.api.middleware.auth import auth_cleanup, auth_guard, perm_guard
from src.api.utils.Result import Error, OK, Status
from src.api.utils.dictify import dictify_inventory_item, dictify_menu_category, dictify_menu_item
from src.branch.BranchService import BranchService
from src.utils.errors import AlreadyExistsError, AuthorizationError, InputError

guard = perm_guard("menu.category.create")
cleanup = auth_cleanup


class PostSchema(Schema):
    name = fields.String(required=True)


def post(body: dict, branch_id: str):
    name = body["name"]

    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)
    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    try:
        category = branch.menu().create_category(name)
    except AuthorizationError as e:
        return Error(Status.FORBIDDEN, e.message)
    except AlreadyExistsError as e:
        return Error(Status.CONFLICT, e.message)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK(dictify_menu_category(category))
