import re
from datetime import datetime

CUSTOMER_NAME_MIN_LEN = 5  # INCLUSIVE
CUSTOMER_NAME_MAX_LEN = 50  # INCLUSIVE
CUSTOMER_NAME_REGEX = re.compile(r"^[a-zA-Z][a-zA-Z ]*[a-zA-Z]$")


def validate_reservation_date(reservation_date: datetime):
    current_date = datetime.today().date()
    reservation_date = datetime.date(reservation_date)

    VALID_DATE = reservation_date >= current_date

    return VALID_DATE


def validate_customer_name(customer_name: str):
    customer_name = customer_name.replace("  ", "!")

    ABOVE_MIN = len(customer_name) >= CUSTOMER_NAME_MIN_LEN
    BELOW_MAX = len(customer_name) <= CUSTOMER_NAME_MAX_LEN
    CORRECT_FORMAT = CUSTOMER_NAME_REGEX.match(customer_name) is not None

    return ABOVE_MIN and BELOW_MAX and CORRECT_FORMAT
