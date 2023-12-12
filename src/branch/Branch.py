# import ..utils.Database from database
from ..utils.Database import Database

class Branch:
    def __init__(self, branch_id: str )-> None:
        self._branch_id = branch_id

    def get_id(self) -> str:
        return self._branch_id