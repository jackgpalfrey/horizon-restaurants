from flask import render_template

from src.api.middleware.auth import auth_cleanup, perm_guard
from src.api.utils.Result import Error, OK, Status
from src.api.utils.dictify import dictify_simple_order
from src.branch.BranchService import BranchService
from src.order.OrderService import OrderService

guard = perm_guard("order.view")
cleanup = auth_cleanup


def post(branch_id: str = ""):
    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)
    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    orders = OrderService.get_all_placed_from_branch(branch)

    inventory_data = [dictify_simple_order(o) for o in orders]

    return OK({"inventory": inventory_data})


def get(branch_id: str = ""):
    return render_template("orders.html", branch_id=branch_id)
