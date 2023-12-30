"""Module with helpers and validation logic for reservations."""
import re

from ..tables.Table import Table

ITEM_NAME_MIN_LEN = 3  # INCLUSIVE
ITEM_NAME_MAX_LEN = 50  # INCLUSIVE
ITEM_NAME_REGEX = re.compile(r"^[a-zA-Z][a-zA-Z ]*[a-zA-Z]$")


def validate_item_name(name: str):
    """Validate inventory item name."""
    name = name.replace("  ", "!")

    ABOVE_MIN = len(name) >= ITEM_NAME_MIN_LEN
    BELOW_MAX = len(name) <= ITEM_NAME_MAX_LEN
    CORRECT_FORMAT = ITEM_NAME_REGEX.match(name) is not None

    return ABOVE_MIN and BELOW_MAX and CORRECT_FORMAT
