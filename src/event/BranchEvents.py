"""Module for managing events"""
from .Event import Event
from ..utils.Database import Database
from datetime import datetime, timedelta


class BranchEvents:

    def __init__(self, branch_id: str):
        self._branch_id = branch_id

    def create(self, type: int) -> Event:
        Database.execute_and_commit(
            "INSERT INTO public.branch (branch_name, type) VALUES(%s, %s)", self._branch_id, type)

        return BranchEvents.get_by_name(BranchEvents)

    def get_by_id(self, event_id: str) -> Event | None:
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.events WHERE id = %s \
             AND branch_id = %s;", event_id, self._branch_id)

        if result is not None:
            return Event(result(0))

    def get_all(self) -> list[Event]:
        """Get all event bookings"""
        result = Database.execute_and_fetchall("SELECT id FROM public.events")

        return [Event(record[0]) for record in result]

    def get_by_time(self) -> list[Event]:
        """Get all event bookings"""
        result = Database.execute_and_fetchall("SELECT id FROM public.events")

        return [Event(record[0]) for record in result]
