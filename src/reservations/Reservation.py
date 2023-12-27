from ..tables.Table import Table
from ..user.ActiveUser import ActiveUser
from ..utils.Database import Database
from .utils import validate_reservation_date
from src.utils.errors import InputError
from datetime import datetime


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

    def get_time(self) -> str:
        time = Database.execute_and_fetchone(
            "SELECT reservation_time FROM public.reservations WHERE id = %s", self._reservation_id)

        return time[0]
