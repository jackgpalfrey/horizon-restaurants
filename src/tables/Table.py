# Author: Dina Hassanein (22066792)
"""Module for handling specific tables."""
from datetime import datetime, timedelta

from ..user.ActiveUser import ActiveUser
from ..utils.Database import Database


class Table:
    """Class to manage a specific table."""

    def __init__(self, table_id: str):
        """Don't call outside of BranchTables."""
        self._table_id = table_id

    def get_id(self):
        """Get table id."""
        return self._table_id

    def get_table_number(self) -> str:
        """Get tables number."""
        table_number = Database.execute_and_fetchone(
            "SELECT table_number FROM public.table WHERE id = %s",
            self._table_id)
        assert table_number is not None

        return table_number[0]

    def get_capacity(self) -> int:
        """Get tables number of seats."""
        capacity = Database.execute_and_fetchone(
            "SELECT capacity FROM public.table WHERE id = %s", self._table_id)
        assert capacity is not None

        return capacity[0]

    def set_capacity(self, table_capacity: int) -> None:
        """
        Update the table capicity to the given capacity.

        :raises AuthorizationError: If active user does not have permission.
        """
        ActiveUser.get().raise_without_permission("table.update")

        Database.execute_and_commit(
            "UPDATE public.table SET capacity = %s WHERE id = %s",
            table_capacity, self._table_id)

    def delete(self) -> None:
        """
        Delete the table record from the database.

        :raises AuthorizationError: If active user does not have permission.
        """
        ActiveUser.get().raise_without_permission("table.delete")

        Database.execute_and_commit(
            "DELETE FROM public.table WHERE id = %s", self._table_id)

    def check_is_reserved(self, reservation_time: datetime) -> bool:
        """Check if the table is reserved during the range of time given."""
        duration = timedelta(hours=2)
        end_time = reservation_time + duration

        check = Database.execute_and_fetchone(
            "SELECT id FROM public.reservations WHERE table_id = %s \
            AND end_time > %s AND reservation_time < %s;",
            self._table_id, reservation_time, end_time)

        return check is not None
