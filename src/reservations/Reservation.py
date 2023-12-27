from ..tables.Table import Table
from ..tables.BranchTables import BranchTables
from ..utils.Database import Database


class Reservation:
    def __init__(self, reservation_id: str):
        self._reservation_id = reservation_id

    def get_table(self) -> Table:
        result = Database.execute_and_fetchone(
            "SELECT table_id FROM public.reservations WHERE id = %s", self._reservation_id)

        return Table(result[0])

    def get_customer_name(self) -> str:
        customer_name = Database.execute_and_fetchone(
            "SELECT customer_name FROM public.reservations WHERE id = %s", self._reservation_id)

        return customer_name[0]
