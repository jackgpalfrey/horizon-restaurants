from flask import render_template

from src.api.middleware.auth import auth_cleanup, perm_guard
from src.api.utils.Result import Error, OK, Status
from src.api.utils.dictify import dictify_inventory_item
from src.branch.BranchService import BranchService

guard = perm_guard("inventory.view")
cleanup = auth_cleanup


def post(branch_id: str = ""):
    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)
    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    inventory = branch.inventory().get_all()

    inventory_data = [dictify_inventory_item(i) for i in inventory]

    return OK({"inventory": inventory_data})


def get(branch_id: str = ""):
    return render_template("inventory.html", branch_id=branch_id)
