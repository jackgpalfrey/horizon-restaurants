"""Module with validation logic for cities."""
import re

CITY_NAME_MIN_LEN = 3  # INCLUSIVE
CITY_NAME_MAX_LEN = 50  # INCLUSIVE
CITY_NAME_REGEX = re.compile(r"^[a-zA-Z][a-zA-Z ]*[a-zA-Z]$")


def validate_city_name(city_name: str):
    """Validate given city name."""
    city_name = city_name.replace("  ", "!")

    ABOVE_MIN = len(city_name) >= CITY_NAME_MIN_LEN
    BELOW_MAX = len(city_name) <= CITY_NAME_MAX_LEN
    CORRECT_FORMAT = CITY_NAME_REGEX.match(city_name) is not None

    return ABOVE_MIN and BELOW_MAX and CORRECT_FORMAT
