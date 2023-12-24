from .Table import Table
from ..user.ActiveUser import ActiveUser
from ..utils.Database import Database

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..branch.Branch import Branch


class BranchTables:
    def __init__(self, branch_id: str):
        self._branch_id = branch_id

    def create(self, branch: "Branch", table_number: int, table_capacity: int) -> Table:

        branch_id = branch.get_id()

        Database.execute_and_commit(
            "INSERT INTO public.table (table_number, capacity, branch_id) VALUES(%s, %s, %s)", table_number, table_capacity, branch_id)
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.table WHERE table_number = %s AND branch_id=%s;", table_number, branch_id)

        return Table(result[0])

    def get_by_id(self, table_id: str) -> Table:
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.table WHERE id = %s", table_id)

        if result is not None:
            return Table(result[0])
