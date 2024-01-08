from src.api.middleware.auth import auth_cleanup, auth_guard, perm_guard
from src.api.utils.Result import OK, Error, Status
from src.branch.BranchService import BranchService
from src.utils.errors import AuthorizationError, InputError

guard = perm_guard("discounts.delete")
cleanup = auth_cleanup


def post(branch_id: str, discount_id: str):
    try:
        branch = BranchService.get_by_id(branch_id)
        if branch is None:
            return Error(Status.NOT_FOUND, "Branch not found")

        discount = branch.discounts().get_by_id(discount_id)
        if discount is None:
            return Error(Status.NOT_FOUND, "Discount not found")

        discount.delete()
    except AuthorizationError as e:
        return Error(Status.FORBIDDEN, e.message)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK({})
