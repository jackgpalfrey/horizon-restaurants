from __future__ import annotations
import os
import yaml

ROLE_DIR_PATH = "src/config/roles"


class Role:
    _roles: dict[int, Role] = {}

    _role_id: int
    _name: str
    _permissions: dict[str, bool]

    @classmethod
    def load_roles(cls):
        os.scandir(ROLE_DIR_PATH)
        for entry in os.scandir(ROLE_DIR_PATH):
            if entry.is_file():
                Role._load_role_file(entry.path)

    @classmethod
    def _load_role_file(cls, path: str):
        print("Loading role file:", path, end="... ")

        with open(path, "r") as f:
            data = yaml.safe_load(f)

        id = data["id"]
        name = data["name"]
        permissions = data["permissions"]

        role = Role(id, name, permissions)
        cls._roles[id] = role

        print("Loaded", name)

    @classmethod
    def get_by_id(cls, id: int) -> Role | None:
        return cls._roles.get(id, None)

        raise ValueError(f"Role with id {id} does not exist")

    def __init__(self, id: int, name: str, permissions: list[str]):
        self._role_id = id
        self._name = name
        self._permissions = {}

        self._add_permission_list(permissions)

    def check_permission(self, permission: str) -> bool:
        return self._permissions.get(permission, False)

    def get_name(self) -> str:
        return self._name

    def get_id(self) -> int:
        return self._role_id

    def _add_permission_list(self, permissions: list[str]):
        for permission in permissions:
            self._add_permission(permission)

    def _add_permission(self, permission: str):
        self._permissions[permission] = True
