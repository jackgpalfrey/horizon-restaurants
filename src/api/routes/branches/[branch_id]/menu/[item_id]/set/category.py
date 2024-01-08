from marshmallow import Schema, fields
from src.api.middleware.auth import auth_cleanup, auth_guard, perm_guard
from src.api.utils.Result import OK, Error, Status
from src.api.utils.dictify import dictify_inventory_item, dictify_menu_item
from src.branch.BranchService import BranchService
from src.utils.errors import AuthorizationError, InputError

guard = perm_guard("menu.item.update.name")
cleanup = auth_cleanup


class PostSchema(Schema):
    category_id = fields.String(required=True)


def post(body: dict, branch_id: str, item_id: str):
    category_id: str = body["category_id"]

    try:
        branch = BranchService.get_by_id(branch_id)
        if branch is None:
            return Error(Status.NOT_FOUND, "Branch not found")

        item = branch.menu().get_item_by_id(item_id)
        if item is None:
            return Error(Status.NOT_FOUND, "Item not found")

        category = branch.menu().get_category_by_id(category_id)
        if category is None:
            return Error(Status.NOT_FOUND, "Category not found")

        item.set_category(category)

    except AuthorizationError as e:
        return Error(Status.FORBIDDEN, e.message)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK(dictify_menu_item(item))
