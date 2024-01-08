from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_reservation
from src.branch.BranchService import BranchService


def post(branch_id: str = ""):
    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)
    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    reservations = branch.reservations().get_all()

    users_data = [dictify_reservation(r) for r in reservations]

    return OK({"reservations": users_data})
