from ..tables.Table import Table
from ..user.ActiveUser import ActiveUser
from ..utils.Database import Database
from .utils import validate_reservation_date, validate_customer_name, validate_guest_num
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

    def get_time(self) -> datetime:
        time = Database.execute_and_fetchone(
            "SELECT reservation_time FROM public.reservations WHERE id = %s", self._reservation_id)

        return time[0]

    def get_num_people(self) -> int:
        guest_num = Database.execute_and_fetchone(
            "SELECT guest_num FROM public.reservations WHERE id = %s", self._reservation_id)

        return guest_num[0]

    def set_table(self, table: Table) -> None:

        ActiveUser.get().raise_without_permission("reservation.update")

        reservation_time = self.get_time()

        if table.check_is_reserved(reservation_time) is True:
            raise InputError("This table is already reserved.")

        Database.execute_and_commit(
            "UPDATE public.reservations SET table_id = %s WHERE id = %s", table._table_id, self._reservation_id)

    def set_customer_name(self, customer_name: str) -> None:

        ActiveUser.get().raise_without_permission("reservation.update")

        if not validate_customer_name(customer_name):
            raise InputError("Invalid customer name.")

        Database.execute_and_commit(
            "UPDATE public.reservations SET customer_name = %s WHERE id = %s", customer_name, self._reservation_id)

    def set_time(self, reservation_time: datetime) -> None:

        ActiveUser.get().raise_without_permission("reservation.update")

        table = self.get_table()

        if table.check_is_reserved(reservation_time) is True:
            raise InputError("This table is already reserved.")

        if not validate_reservation_date(reservation_time):
            raise InputError(
                "Invalid reservation date. The reservation must be booked today or at a future date.")

        Database.execute_and_commit(
            "UPDATE public.reservations SET reservation_time = %s WHERE id = %s", reservation_time, self._reservation_id)

    def set_num_people(self, guest_num: int) -> None:

        ActiveUser.get().raise_without_permission("reservation.update")

        table = self.get_table()

        if not validate_guest_num(table, guest_num):
            raise InputError("Customer number exceeds table capacity.")

        Database.execute_and_commit(
            "UPDATE public.reservations SET guest_num = %s WHERE id = %s", guest_num, self._reservation_id)
