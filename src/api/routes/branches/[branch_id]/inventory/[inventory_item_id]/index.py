from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_inventory_item
from src.branch.BranchService import BranchService


def post(branch_id: str = "", inventory_item_id: str = ""):
    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)
    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    item = branch.inventory().get_by_id(inventory_item_id)
    if item is None:
        return Error(Status.NOT_FOUND, "Item not found.")

    return OK(dictify_inventory_item(item))
