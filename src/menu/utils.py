# Author: Jack Palfrey (22032928)
"""Module with validation logic for menu items."""
import re

MENU_NAME_MIN_LEN = 3  # INCLUSIVE
MENU_NAME_MAX_LEN = 50  # INCLUSIVE
MENU_NAME_REGEX = re.compile(r"^[a-zA-Z][a-zA-Z ]*[a-zA-Z]$")

MENU_DESC_MIN_LEN = 10  # INCLUSIVE
MENU_DESC_MAX_LEN = 200  # INCLUSIVE
MENU_DESC_REGEX = re.compile(r"^[a-zA-Z][a-zA-Z0-9,. ]*[a-zA-Z].$")


def validate_menu_name(name: str) -> bool:
    """Validate given menu item or category name name."""
    name = name.replace("  ", "!")

    ABOVE_MIN = len(name) >= MENU_NAME_MIN_LEN
    BELOW_MAX = len(name) <= MENU_NAME_MAX_LEN
    CORRECT_FORMAT = MENU_NAME_REGEX.match(name) is not None

    return ABOVE_MIN and BELOW_MAX and CORRECT_FORMAT


def validate_menu_description(desc: str) -> bool:
    """Validate given item description."""
    desc = desc.replace("  ", "!")

    ABOVE_MIN = len(desc) >= MENU_DESC_MIN_LEN
    BELOW_MAX = len(desc) <= MENU_DESC_MAX_LEN
    CORRECT_FORMAT = MENU_DESC_REGEX.match(desc) is not None

    return ABOVE_MIN and BELOW_MAX and CORRECT_FORMAT
