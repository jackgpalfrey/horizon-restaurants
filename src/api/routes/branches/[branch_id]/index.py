from flask import redirect, render_template
from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_branch
from src.branch.BranchService import BranchService


def post(branch_id: str = ""):
    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)

    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    return OK(dictify_branch(branch))


def get(branch_id: str = ""):
    return redirect("inventory")
