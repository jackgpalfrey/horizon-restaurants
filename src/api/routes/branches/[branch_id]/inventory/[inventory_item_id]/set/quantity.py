from marshmallow import Schema, fields
from src.api.middleware.auth import auth_cleanup, auth_guard
from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_inventory_item
from src.branch.BranchService import BranchService
from src.utils.errors import AuthorizationError, InputError

guard = auth_guard
cleanup = auth_cleanup


class PostSchema(Schema):
    quantity = fields.Int()
    delta = fields.Int()


def post(body: dict, branch_id: str, inventory_item_id: str):
    quantity: int | None = body.get("quantity", None)
    delta: int | None = body.get("delta", None)

    try:
        branch = BranchService.get_by_id(branch_id)
        if branch is None:
            return Error(Status.NOT_FOUND, "Branch not found")

        item = branch.inventory().get_by_id(inventory_item_id)
        if item is None:
            return Error(Status.NOT_FOUND, "Item not found")

        if quantity is not None:
            item.set_quantity(quantity)
        elif delta is not None:
            if delta > 0:
                item.add_quantity(delta)
            else:
                item.subtract_quantity(delta * -1)
        else:
            return Error(Status.BAD_REQUEST,
                         "Must include either quantity or delta fields")
    except AuthorizationError as e:
        return Error(Status.FORBIDDEN, e.message)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK(dictify_inventory_item(item))
