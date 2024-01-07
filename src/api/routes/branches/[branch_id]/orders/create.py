from flask import jsonify, redirect, render_template
from marshmallow import Schema, fields

from src.api.middleware.auth import auth_cleanup, auth_guard, perm_guard
from src.api.utils.Result import Error, OK, Status
from src.api.utils.dictify import dictify_inventory_item
from src.branch.BranchService import BranchService
from src.order.OrderService import OrderService
from src.utils.errors import AlreadyExistsError, AuthorizationError, InputError

guard = perm_guard("order.create")
cleanup = auth_cleanup


def post(branch_id: str):

    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)
    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    try:
        order = OrderService.create(branch)
    except AuthorizationError as e:
        return Error(Status.FORBIDDEN, e.message)
    except AlreadyExistsError as e:
        return Error(Status.CONFLICT, e.message)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK({"id": order.get_id()})


def get(branch_id: str):
    result = post(branch_id)[0].get_json()
    if not result["success"]:
        return result

    return redirect(result["data"]["id"])
