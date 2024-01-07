from marshmallow import Schema, fields
from src.api.middleware.auth import auth_cleanup, perm_guard
from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_inventory_item
from src.branch.BranchService import BranchService
from src.utils.errors import AuthorizationError, InputError

guard = perm_guard("inventory.update.threshold")
cleanup = auth_cleanup


class PostSchema(Schema):
    threshold = fields.Int(required=True)


def post(body: dict, branch_id: str, inventory_item_id: str):
    threshold: int = body["threshold"]

    try:
        branch = BranchService.get_by_id(branch_id)
        if branch is None:
            return Error(Status.NOT_FOUND, "Branch not found")

        item = branch.inventory().get_by_id(inventory_item_id)
        if item is None:
            return Error(Status.NOT_FOUND, "Item not found")

        item.set_threshold(threshold)
    except AuthorizationError as e:
        return Error(Status.FORBIDDEN, e.message)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK(dictify_inventory_item(item))
