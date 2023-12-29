"""Module for creating and accessing reservations."""
from datetime import datetime, timedelta

from src.utils.errors import InputError
from src.utils.errors import AlreadyExistsError

from ..tables.Table import Table
from ..user.ActiveUser import ActiveUser
from ..utils.Database import Database
from .Reservation import Reservation
from .utils import (
    validate_customer_name,
    validate_guest_num,
    validate_reservation_date
)


class BranchReservations:
    """Class for managing a specific branches reservations."""

    def __init__(self, branch_id: str):
        """Don't call outside of Branch."""
        self._branch_id = branch_id

    def create(self, table: Table, customer_name: str,
               reservation_time: datetime, guest_num: int) -> Reservation:
        """
        Create a new reservation using the given parameters.

        A record of the created reservation is added to the database.
        :raises AuthorizationError: If active user does not have permission.
        :raises AuthorizationError: If active user does not have permission to
        create reservation at a different branch from the one they're assigned.
        """
        user = ActiveUser.get()
        user.raise_without_permission("reservation.create")

        check_user_branch = Database.execute_and_fetchone(
            "SELECT branch_id FROM public.branchstaff WHERE user_id=%s;",
            user._user_id)

        USER_BRANCH_DOESNT_EXIST = check_user_branch is None

        if USER_BRANCH_DOESNT_EXIST or check_user_branch[0] != self._branch_id:
            user.raise_without_permission("allbranches.reservation.create")

        if table.check_is_reserved(reservation_time):
            raise AlreadyExistsError("This table is already reserved.")

        BranchReservations._validate_create_reservation(
            table, customer_name, reservation_time, guest_num)

        # reference:
        # https://blog.finxter.com/how-to-add-time-onto-a-datetime-object-in-python/
        duration = timedelta(hours=2)
        end_time = reservation_time + duration

        table_id = table._table_id

        sql = "INSERT INTO public.reservations(customer_name, \
        reservation_time, end_time, guest_num, table_id, branch_id)\
        VALUES(%s, %s, %s, %s, %s, %s) RETURNING id"

        cursor = Database.execute(sql, customer_name, reservation_time,
                                  end_time, guest_num, table_id,
                                  self._branch_id)
        Database.commit()
        result = cursor.fetchone()
        assert result is not None
        id = result[0]

        return Reservation(id)

    def get_by_id(self, reservation_id: str) -> Reservation | None:
        """
        Get a reservation by its ID.

        Note: This is not limited to this branch.
        """
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.reservations WHERE id = %s \
            AND branch_id = %s;", reservation_id, self._branch_id)

        if result is not None:
            return Reservation(result[0])

    def get_by_table(self, table: Table) -> list[Reservation]:
        """Get a reservation by it's table."""
        result = Database.execute_and_fetchall(
            "SELECT id FROM public.reservations WHERE table_id = %s \
            AND branch_id = %s;", table._table_id, self._branch_id)

        return [Reservation(record[0]) for record in result]

    def get_by_customer_name(self, customer_name: str) -> Reservation | None:
        """Get a reservation by it's customer name."""
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.reservations WHERE customer_name = %s \
            AND branch_id = %s;", customer_name, self._branch_id)

        if result is not None:
            return Reservation(result[0])

    def get_all(self) -> list[Reservation]:
        """Get all reservations at the branch."""
        result = Database.execute_and_fetchall(
            "SELECT id FROM public.reservations WHERE branch_id = %s;",
            self._branch_id)

        return [Reservation(record[0]) for record in result]

    @staticmethod
    def _validate_create_reservation(table: Table,
                                     customer_name: str,
                                     reservation_date: datetime,
                                     guest_num: int) -> None:
        """
        Validate given date, guest number, and customer name.

        Based on logic in ./utils.py.
        Called in the create() method for reservations.

        :raises InputError: If any of the given values are invalid.
        """
        if not validate_reservation_date(reservation_date):
            raise InputError(
                "The reservation must be booked today or at a future date.")

        if not validate_customer_name(customer_name):
            raise InputError("Invalid customer name.")

        if not validate_guest_num(table, guest_num):
            raise InputError("Customer number exceeds table capacity.")
