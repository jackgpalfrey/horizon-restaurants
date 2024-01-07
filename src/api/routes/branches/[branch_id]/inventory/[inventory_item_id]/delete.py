from src.api.middleware.auth import auth_cleanup, auth_guard, perm_guard
from src.api.utils.Result import OK, Error, Status
from src.branch.BranchService import BranchService
from src.utils.errors import AuthorizationError, InputError

guard = perm_guard("inventory.delete")
cleanup = auth_cleanup

def post(branch_id: str, inventory_item_id: str):
    try:
        branch = BranchService.get_by_id(branch_id)
        if branch is None:
            return Error(Status.NOT_FOUND, "Branch not found")

        item = branch.inventory().get_by_id(inventory_item_id)
        if item is None:
            return Error(Status.NOT_FOUND, "Item not found")

        item.delete()
    except AuthorizationError as e:
        return Error(Status.FORBIDDEN, e.message)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK({})
