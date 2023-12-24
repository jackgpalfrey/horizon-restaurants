from .Table import Table
from ..utils.Database import Database


class BranchTables:
    def __init__(self, branch_id: str):
        self._branch_id = branch_id
