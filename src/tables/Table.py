from ..utils.Database import Database
from ..user.ActiveUser import ActiveUser
from datetime import datetime, timedelta


class Table:
    def __init__(self, table_id: str):
        self._table_id = table_id

    def get_table_number(self) -> str:
        table_number = Database.execute_and_fetchone(
            "SELECT table_number FROM public.table WHERE id = %s", self._table_id)
        return table_number[0]

    def get_capacity(self) -> int:
        capacity = Database.execute_and_fetchone(
            "SELECT capacity FROM public.table WHERE id = %s", self._table_id)
        return capacity[0]

    def set_capacity(self, table_capacity: int) -> None:
        """
        Updates the table capicity to the given capacity.

        :raises AuthorizationError: If active user does not have permission to update tables.
        """

        ActiveUser.get().raise_without_permission("table.update")

        Database.execute_and_commit(
            "UPDATE public.table SET capacity = %s WHERE id = %s", table_capacity, self._table_id)

    def delete(self) -> None:
        """
        Deletes the table record from the database.

        :raises AuthorizationError: If active user does not have permission to delete tables.
        """

        ActiveUser.get().raise_without_permission("table.delete")

        Database.execute_and_commit(
            "DELETE FROM public.table WHERE id = %s", self._table_id)

    def check_is_reserved(self, reservation_time: datetime) -> bool:

        duration = timedelta(hours=2)
        end_time = reservation_time + duration

        check = Database.execute_and_fetchone(
            "SELECT id FROM public.reservations WHERE table_id = %s AND end_time > %s AND reservation_time < %s;", self._table_id, reservation_time, end_time)

        if check is not None:
            return True
        return False
