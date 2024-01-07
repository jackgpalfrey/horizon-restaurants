from flask import render_template
from src.api.utils.Result import OK
from src.api.utils.dictify import dictify_simple_branch
from src.branch.BranchService import BranchService


def post():
    branches = BranchService.get_all()

    branches_data = [dictify_simple_branch(b) for b in branches]

    return OK({"branches": branches_data})


def get():
    return render_template("select-branch.html")
