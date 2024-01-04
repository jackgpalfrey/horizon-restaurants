from src.api.utils.Result import OK
from src.branch.BranchService import BranchService


def post():
    branches = BranchService.get_all()

    branch_data = [{"branch_id": b.get_id(),
                    "name": b.get_name(),
                    "city": b.get_city().get_name()} for b in branches]

    return OK({"branches": branch_data})
