from flask import render_template
from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_discount
from src.branch.BranchService import BranchService


def post(branch_id: str = ""):
    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)
    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    discounts = branch.discounts().get_all()

    discounts_data = [dictify_discount(d) for d in discounts]

    return OK({"discounts": discounts_data})


def get(branch_id: str = ""):
    return render_template("discounts.html", branch_id=branch_id)
