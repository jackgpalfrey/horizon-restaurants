from src.branch.Branch import Branch
from src.branch.BranchService import BranchService
from src.city.City import City
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
