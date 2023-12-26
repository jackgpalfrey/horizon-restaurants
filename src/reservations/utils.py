import re
from datetime import datetime


def validate_reservation_date(reservation_date: datetime):
    current_date = datetime.today().date()
    reservation_date = datetime.date(reservation_date)

    VALID_DATE = reservation_date >= current_date

    return VALID_DATE
