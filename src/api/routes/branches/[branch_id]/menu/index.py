from flask import render_template

from src.api.middleware.auth import auth_cleanup, perm_guard
from src.api.utils.Result import Error, OK, Status
from src.api.utils.dictify import dictify_inventory_item, dictify_menu_item
from src.branch.BranchService import BranchService

guard = perm_guard("menu.view")
cleanup = auth_cleanup


def post(branch_id: str = ""):
    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)
    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    menu = branch.menu().get_all_items()

    inventory_data = [dictify_menu_item(i) for i in menu]

    return OK({"menu": inventory_data})


def get(branch_id: str = ""):
    return render_template("menu.html", branch_id=branch_id)
