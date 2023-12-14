from __future__ import annotations
import os
import yaml

ROLE_DIR_PATH = "src/config/roles"


class Role:
    _roles: dict[int, Role] = {}

    @classmethod
    def load_roles(cls):
        """
        Loads all roles from src/config/roles/

        :raises FileNotFoundError: If the role directory does not exist
        """

        files = os.scandir(ROLE_DIR_PATH)
        sorted_files = sorted(files, key=lambda entry: entry.name)

        for file in sorted_files:
            if file.is_file():
                Role._load_role_file(file.path)
            else:
                print("Skipping directory:", file.name)

    @classmethod
    def _load_role_file(cls, path: str):
        """
        Loads a yaml file at the given path as a role

        :raises FileNotFoundError: If the role file does not exist
        :raises KeyError: If the role file is missing any required fields
        """

        print("Loading role file:", path, end="... ")

        with open(path, "r") as f:
            data = yaml.safe_load(f)

        id = data["id"]
        name = data["name"]
        permissions = data["permissions"]
        extends = data.get("extends", None)

        if extends is not None:
            cls._handle_extends(extends, permissions)

        role = Role(id, name, permissions)
        cls._roles[id] = role

        print("Loaded", name)

    @classmethod
    def _handle_extends(cls, extends: list[int] | int, permissions: list[str]):
        if type(extends) is list:
            for role_id in extends:
                parent_role = cls.get_by_id(role_id)
                permissions += parent_role.get_all_permissions()

        else:
            parent_role = cls.get_by_id(extends)
            permissions += parent_role.get_all_permissions()

    @classmethod
    def get_by_id(cls, id: int) -> Role | None:
        return cls._roles.get(id, None)

    # ---------------------------------- Instance Methods ----------------------------------

    def __init__(self, id: int, name: str, permissions: list[str]):
        self._role_id = id
        self._name = name
        self._permissions: dict[str: bool] = {}

        self._add_permission_list(permissions)

    def check_permission(self, permission: str) -> bool:
        """
        Checks if this role has the given permission

        Supports implicit wildcards, e.g. "account.create" will come back True if this role has "account"
        Supports explicit wildcards, i.e. any permission check will come back True if this role has the ".*" permission
        Supports negation with the ~ prefix, e.g. "account.create" will come back False if this role has "account" but also "~account.create"
        """

        split_permission = permission.split(".")

        return self._check_split_permission(split_permission)

    def _check_split_permission(self, split_permission: list[str]) -> bool:
        """
        Recursively checks if this role has the given permission to support implicit wildcards
        """

        # Base Case
        if len(split_permission) == 1:
            HAS_PERMISSION = self._check_exact_permission(split_permission[0])

            if HAS_PERMISSION is not None:
                return HAS_PERMISSION

            return self._check_exact_permission(".*") or False

        permission_str = ".".join(split_permission)
        permission_value = self._check_exact_permission(permission_str)

        if permission_value is None:
            return self._check_split_permission(split_permission[:-1])

        return permission_value

    def get_name(self) -> str:
        return self._name

    def get_id(self) -> int:
        return self._role_id

    def get_all_permissions(self) -> list[str]:
        return list(self._permissions.keys())

    def _check_exact_permission(self, permission: str) -> bool | None:
        """
        Checks if this role has the given permission exactly. Does not support wildcards
        """
        perm = self._permissions.get(permission, None)
        print(permission, perm)
        return perm

    def _add_permission_list(self, permissions: list[str]):
        """Adds a list of permissions to this role"""

        for permission in permissions:
            self._add_permission(permission)

    def _add_permission(self, permission: str):
        """
        Adds a permission to this role
        Supports negation with the ~ operator
        """

        if permission.startswith("~"):
            self._permissions[permission[1:]] = False
        else:
            self._permissions[permission] = True
