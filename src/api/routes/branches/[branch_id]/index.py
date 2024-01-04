from src.api.utils.Result import OK, Error, Status
from src.branch.BranchService import BranchService


def post(branch_id: str = ""):
    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)

    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    branch_data = {
        "id": branch.get_id(),
        "name": branch.get_name(),
        "address": branch.get_address(),
        "city": branch.get_city().get_name(),
    }

    return OK(branch_data)
