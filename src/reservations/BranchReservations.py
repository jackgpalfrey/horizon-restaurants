from datetime import datetime, timedelta
from .Reservation import Reservation
from ..tables.Table import Table
from ..user.ActiveUser import ActiveUser
from ..utils.Database import Database


class BranchReservations:
    def __init__(self, branch_id: str):
        self._branch_id = branch_id

    def create(self, table: Table, customer_name: str, reservation_date: datetime, start_time: datetime, guest_num: int) -> Reservation:

        ActiveUser.get().raise_without_permission("reservation.create")

        table_id = table._table_id

        # reference: https://blog.finxter.com/how-to-add-time-onto-a-datetime-object-in-python/

        start_time = datetime.strptime(start_time, '%H:%M')
        duration = timedelta(hours=2)
        end_time = start_time + duration
        start_time = start_time.strftime("%X")
        end_time = end_time.strftime("%X")

        cursor = Database.execute("INSERT INTO public.reservations(customer_name, reservation_date, start_time, end_time, guest_num, table_id, branch_id)VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                                  customer_name, reservation_date, start_time, end_time, guest_num, table_id, self._branch_id)
        Database.commit()
        result = cursor.fetchone()
        id = result[0]

        return Reservation(id)
