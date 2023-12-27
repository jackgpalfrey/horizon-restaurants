from datetime import datetime, timedelta
from .Reservation import Reservation
from .utils import validate_reservation_date, validate_customer_name, validate_guest_num
from ..tables.Table import Table
from ..user.ActiveUser import ActiveUser
from ..utils.Database import Database
from src.utils.errors import InputError


class BranchReservations:
    def __init__(self, branch_id: str):
        self._branch_id = branch_id

    def create(self, table: Table, customer_name: str, reservation_time: datetime, guest_num: int) -> Reservation:

        ActiveUser.get().raise_without_permission("reservation.create")

        table_id = table._table_id

        # reference: https://www.digitalocean.com/community/tutorials/python-string-to-datetime-strptime

        BranchReservations._validate_create_reservation(
            table, customer_name, reservation_time, guest_num)

        # reference: https://blog.finxter.com/how-to-add-time-onto-a-datetime-object-in-python/

        duration = timedelta(hours=2)
        end_time = reservation_time + duration

        cursor = Database.execute("INSERT INTO public.reservations(customer_name, reservation_time, end_time, guest_num, table_id, branch_id)VALUES(%s, %s, %s, %s, %s, %s) RETURNING id",
                                  customer_name, reservation_time, end_time, guest_num, table_id, self._branch_id)
        Database.commit()
        result = cursor.fetchone()
        id = result[0]

        return Reservation(id)

    def _validate_create_reservation(table: Table, customer_name: str, reservation_date: datetime, guest_num: int) -> None:
        """
        Validates given date, guest number, and customer name based on validation logic
        in ./utils.py Called in the create() method for reservations.

        :raises InputError: If reservation date, customer name, or guest number is invalid.
        :raises AlreadyExistsError: If customer name provided already has a reservation booked.
        """

        if not validate_reservation_date(reservation_date):
            raise InputError(
                "Invalid reservation date. The reservation must be booked today or at a future date.")

        if not validate_customer_name(customer_name):
            raise InputError("Invalid customer name.")

        if not validate_guest_num(table, guest_num):
            raise InputError("Customer number exceeds table capacity.")

    def get_by_id(self, reservation_id: str) -> Reservation:
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.reservations WHERE id = %s", reservation_id)

        if result is not None:
            return Reservation(result[0])
