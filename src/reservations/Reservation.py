"""Module for handling specific reservations."""
from ..tables.Table import Table
from ..user.ActiveUser import ActiveUser
from ..utils.Database import Database
from src.utils.errors import InputError, AlreadyExistsError
from datetime import datetime
from .utils import (
    validate_reservation_date,
    validate_customer_name,
    validate_guest_num
)


class Reservation:
    """Class to manage a specific reservation."""

    def __init__(self, reservation_id: str):
        """Don't call outside of BranchReservations."""
        self._reservation_id = reservation_id

    def get_table(self) -> Table:
        """Get reservations table."""
        result = Database.execute_and_fetchone(
            "SELECT table_id FROM public.reservations WHERE id = %s",
            self._reservation_id)

        return Table(result[0])

    def get_customer_name(self) -> str:
        """Get reservations customer name."""
        customer_name = Database.execute_and_fetchone(
            "SELECT customer_name FROM public.reservations WHERE id = %s",
            self._reservation_id)

        if customer_name is not None:
            return customer_name[0]

    def get_time(self) -> datetime:
        """Get reservations time."""
        time = Database.execute_and_fetchone(
            "SELECT reservation_time FROM public.reservations WHERE id = %s",
            self._reservation_id)

        if time is not None:
            return time[0]

    def get_num_people(self) -> int:
        """Get reservations customer number."""
        guest_num = Database.execute_and_fetchone(
            "SELECT guest_num FROM public.reservations WHERE id = %s",
            self._reservation_id)

        if guest_num is not None:
            return guest_num[0]

    def set_table(self, table: Table) -> None:
        """
        Update the reservation's table.

        :raises AuthorizationError: If active user does not have permission.
        :raises AlreadyExistsError: If table given already has a reservation booked.
        """
        ActiveUser.get().raise_without_permission("reservation.update")

        reservation_time = self.get_time()

        if table.check_is_reserved(reservation_time) is True:
            raise AlreadyExistsError("This table is already reserved.")

        Database.execute_and_commit(
            "UPDATE public.reservations SET table_id = %s WHERE id = %s",
            table._table_id, self._reservation_id)

    def set_customer_name(self, customer_name: str) -> None:
        """
        Update the reservation's customer name.

        :raises AuthorizationError: If active user does not have permission.
        :raises InputError: If customer name given is invalid.
        """
        ActiveUser.get().raise_without_permission("reservation.update")

        if not validate_customer_name(customer_name):
            raise InputError("Invalid customer name.")

        Database.execute_and_commit(
            "UPDATE public.reservations SET customer_name = %s WHERE id = %s",
            customer_name, self._reservation_id)

    def set_time(self, reservation_time: datetime) -> None:
        """
        Update the reservation's time.

        :raises AuthorizationError: If active user does not have permission.
        :raises InputError: If table already has a reservation booked.
        :raises InputError: If reservation date given is invalid.
        """
        ActiveUser.get().raise_without_permission("reservation.update")

        table = self.get_table()

        if table.check_is_reserved(reservation_time) is True:
            raise InputError("This table is already reserved.")

        if not validate_reservation_date(reservation_time):
            raise InputError(
                "The reservation must be booked today or at a future date.")

        Database.execute_and_commit(
            "UPDATE public.reservations SET reservation_time = %s WHERE id = %s",
            reservation_time, self._reservation_id)

    def set_num_people(self, guest_num: int) -> None:
        """
        Update the reservation's guest number.

        :raises AuthorizationError: If active user does not have permission.
        :raises InputError: If guest number given is invalid to table.
        """
        ActiveUser.get().raise_without_permission("reservation.update")

        table = self.get_table()

        if not validate_guest_num(table, guest_num):
            raise InputError("Customer number exceeds table capacity.")

        Database.execute_and_commit(
            "UPDATE public.reservations SET guest_num = %s WHERE id = %s",
            guest_num, self._reservation_id)

    def delete(self):
        """
        Deletes the reservation record from the database.

        :raises AuthorizationError: If active user does not have permission.
        """

        ActiveUser.get().raise_without_permission("reservation.delete")

        Database.execute_and_commit(
            "DELETE FROM public.reservations WHERE id = %s",
            self._reservation_id)
