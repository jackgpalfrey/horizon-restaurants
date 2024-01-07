from src.branch.Branch import Branch
from src.branch.BranchService import BranchService
from src.city.City import City
from src.inventory.InventoryItem import InventoryItem
from src.menu.MenuCategory import MenuCategory
from src.menu.MenuItem import MenuItem
from src.order.Order import Order
from src.reservations.Reservation import Reservation
from src.tables.Table import Table
from src.user.User import User


def dictify_city(obj: City):
    return {
        "id": obj.get_id(),
        "name": obj.get_name()
    }


def dictify_branch(obj: Branch):
    city = obj.get_city()
    return {
        "id": obj.get_id(),
        "name": obj.get_name(),
        "address": obj.get_address(),
        "city": {
            "id": city.get_id(),
            "name": city.get_name()
        }
    }


def dictify_simple_branch(obj: Branch):
    return {
        "id": obj.get_id(),
        "name": obj.get_name()
    }


def dictify_user(obj: User):
    branch = BranchService.get_branch_by_user(obj)

    branch_data = None
    if branch is not None:
        branch_data = dictify_simple_branch(branch)

    role = obj.get_role()
    return {
        "username": obj.get_username(),
        "full_name": obj.get_full_name(),
        "branch": branch_data,
        "role": {
            "id": role.get_id(),
            "name": role.get_name(),
        }
    }


def dictify_table(obj: Table):
    return {
        "number": obj.get_table_number(),
        "capacity": obj.get_capacity()
    }


def dictify_inventory_item(obj: InventoryItem):
    quantity = obj.get_quantity()
    threshold = obj.get_threshold()
    too_low = quantity < threshold
    return {
        "id": obj.get_id(),
        "name": obj.get_name(),
        "quantity": quantity,
        "threshold": threshold,
        "is_too_low": too_low
    }


def dictify_reservation(obj: Reservation):
    return {
        "table_number": obj.get_table().get_table_number(),
        "num_people": obj.get_num_people(),
        "customer_name": obj.get_customer_name(),
        "time": obj.get_time().__str__()
    }


def dictify_simple_order(obj: Order):
    return {
        "order_number": obj.get_number(),
        "customer_name": obj.get_customer_name(),
        "num_items": len(obj.get_all_items()),

    }

def dictify_menu_category(obj: MenuCategory):
    return {
        "id": obj.get_id(),
        "name": obj.get_name()
    }

def dictify_menu_item(obj: MenuItem):
    raw_category = obj.get_category()
    category = dictify_menu_category(
        raw_category) if raw_category is not None else None

    return {
        "id": obj.get_id(),
        "name": obj.get_name(),
        "description": obj.get_description(),
        "price": obj.get_price(),
        "image_url": obj.get_image_url(),
        "is_available": obj.get_is_available(),
        "category": category,
    }
