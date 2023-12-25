from .Table import Table
from ..user.ActiveUser import ActiveUser
from ..utils.Database import Database

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..branch.Branch import Branch


class BranchTables:
    def __init__(self, branch_id: str):
        self._branch_id = branch_id

    def create(self, table_number: int, table_capacity: int) -> Table:
        """
        Creates a new table using the given parameters.
        A record of the created table is added to the database.

        :raises AuthorizationError: If active user does not have permission to create tables.
        """

        # branch_id = branch.get_id()

        ActiveUser.get().raise_without_permission("table.create")

        Database.execute_and_commit(
            "INSERT INTO public.table (table_number, capacity, branch_id) VALUES(%s, %s, %s)", table_number, table_capacity, self._branch_id)
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.table WHERE table_number = %s AND branch_id=%s;", table_number, self._branch_id)

        return Table(result[0])

    def get_by_id(self, table_id: str) -> Table:
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.table WHERE id = %s", table_id)

        if result is not None:
            return Table(result[0])

    def get_by_number(self, table_number: int) -> Table | None:
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.table WHERE table_number = %s", table_number)

        if result is not None:
            return Table(result[0])

    def find_by_capacity(self, table_capacity: int) -> list[Table]:
        result = Database.execute_and_fetchall(
            "SELECT id FROM public.table WHERE capacity >= %s ORDER BY capacity", table_capacity)

        return [Table(record[0]) for record in result]

    def get_all(self) -> list[Table]:
        result = Database.execute_and_fetchall("SELECT id FROM public.table")

        return [Table(record[0]) for record in result]
