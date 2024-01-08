# Author: Evan Duwat
"""Module for managing events."""
from datetime import datetime

from ..utils.Database import Database
from .Event import Event


class BranchEvents:
    """Class for managing events at a specifc branch."""

    def __init__(self, branch_id: str):
        """Don't call outside of Branch."""
        self._branch_id = branch_id

    def create(self,
               start_time: datetime,
               end_time: datetime,
               type: int,
               phone_number: str,
               email: str,
               address: str) -> Event:
        """Create a new event."""
        cursor = Database.execute(
            "INSERT INTO public.events \
            (branch_id, start_time, end_time, type, \
            phone_number, email, address) \
            VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id",
            self._branch_id, start_time, end_time, type,
            phone_number, email, address)

        Database.commit()
        result = cursor.fetchone()
        assert result is not None

        return Event(result[0])

    def get_by_id(self, event_id: str) -> Event | None:
        """Get a event by it's id."""
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.events WHERE id = %s \
             AND branch_id = %s;", event_id, self._branch_id)

        if result is not None:
            return Event(result[0])

    def get_all(self) -> list[Event]:
        """Get all event bookings."""
        result = Database.execute_and_fetchall("SELECT id FROM public.events \
        WHERE branch_id = %s", self._branch_id)

        return [Event(record[0]) for record in result]

    def get_by_time(self, time: datetime) -> Event | None:
        """Get event by time."""
        result = Database.execute_and_fetchone(
            "SELECT start_time FROM public.events WHERE id = %s \
            AND branch_id = %s \
            AND end_time > %s AND start_time < %s",
            self._branch_id, time, time)

        if result is not None:
            return Event(result[0])
