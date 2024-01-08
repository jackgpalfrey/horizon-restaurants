# Author: Evan Duwat
"""Module for managing individual events."""
from ..utils.Database import Database
from src.user.ActiveUser import ActiveUser
from datetime import datetime


class Event:
    """Class for managing events."""

    def __init__(self, event_id: str):
        """Don't call outside of BranchEvents."""
        self._event_id = event_id

    def get_id(self) -> str:
        """Get event ID."""
        event_id = Database.execute_and_fetchone(
            "SELECT id FROM public.events WHERE id = %d", self._event_id)
        assert event_id is not None

        return event_id[0]

    def get_event_type(self) -> str:
        """Get event type."""
        event_type = Database.execute_and_fetchone(
            "SELECT type FROM public.events WHERE id = %s", self._event_id)
        assert event_type is not None

        return event_type[0]

    def get_phone_number(self) -> str:
        """Get the phone number of whoever booked event."""
        phone_number = Database.execute_and_fetchone(
            "SELECT phone_number FROM public.events WHERE id = %s",
            self._event_id)
        assert phone_number is not None

        return phone_number[0]

    def get_email(self) -> str:
        """Get the phone number of customer."""
        email = Database.execute_and_fetchone(
            "SELECT email FROM public.events WHERE id = %s", self._event_id)
        assert email is not None

        return email[0]

    def get_start_time(self) -> datetime:
        """Get the time for the event."""
        start_time = Database.execute_and_fetchone(
            "SELECT start_time FROM public.events WHERE id = %s",
            self._event_id)
        assert start_time is not None

        return start_time[0]

    def get_end_time(self) -> datetime:
        """Get the time for the event."""
        end_time = Database.execute_and_fetchone(
            "SELECT end_time FROM public.events WHERE id = %s", self._event_id)
        assert end_time is not None

        return end_time[0]

    def set_type(self, event_type: int) -> None:
        """Set type of event."""
        ActiveUser.get().raise_without_permission("events.update.type")

        sql = "UPDATE public.events SET type = %s WHERE id = %s"
        Database.execute_and_commit(sql, event_type, self._event_id)

    def set_email(self, email: str) -> None:
        """Set user email for event."""
        ActiveUser.get().raise_without_permission("events.update.email")

        sql = "UPDATE public.events SET email = %s WHERE id = %s"
        Database.execute_and_commit(sql, email, self._event_id)

    def set_phone(self, phone: str) -> None:
        """Set user phone number for event."""
        ActiveUser.get().raise_without_permission("events.update.phone_number")

        sql = "UPDATE public.events SET phone_number = %s WHERE id = %s"
        Database.execute_and_commit(sql, phone, self._event_id)

    def set_start_time(self, start_time: datetime) -> None:
        """Set the start time for event."""
        ActiveUser.get().raise_without_permission("events.update.time.start")

        sql = "UPDATE public.events SET start_time = %s WHERE id = %s"
        Database.execute_and_commit(sql, start_time, self._event_id)

    def set_end_time(self, end_time: datetime) -> None:
        """Set the end time for event."""
        ActiveUser.get().raise_without_permission("events.update.time.end")

        sql = "UPDATE public.events SET end_time = %s WHERE id = %s"
        Database.execute_and_commit(sql, end_time, self._event_id)
