from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_user
from src.branch.BranchService import BranchService
from src.user.UserService import UserService


def post(branch_id: str = ""):
    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)
    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    users = UserService.get_all_at_branch(branch, dont_auth=True)

    users_data = [dictify_user(u) for u in users]

    return OK({"users": users_data})
