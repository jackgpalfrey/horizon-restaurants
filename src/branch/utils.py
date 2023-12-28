"""Module containing helpers and validation logic for branch"""
import re

BRANCH_NAME_MIN_LEN = 3  # INCLUSIVE
BRANCH_NAME_MAX_LEN = 50  # INCLUSIVE
BRANCH_NAME_REGEX = re.compile(r"^[a-zA-Z][a-zA-Z ]*[a-zA-Z]$")

ADDRESS_MIN_LEN = 20  # INCLUSIVE
ADDRESS_MAX_LEN = 80  # INCLUSIVE
ADDRESS_REGEX = re.compile(
    r"^.*,?.*, ?[A-z- ]+ [A-Z]{1,2}[0-9]{1,2} [0-9][A-Z]{2}$")


def validate_branch_name(branch_name: str):
    """Validate branch name."""
    branch_name = branch_name.replace("  ", "!")

    ABOVE_MIN = len(branch_name) >= BRANCH_NAME_MIN_LEN
    BELOW_MAX = len(branch_name) <= BRANCH_NAME_MAX_LEN
    CORRECT_FORMAT = BRANCH_NAME_REGEX.match(branch_name) is not None

    return ABOVE_MIN and BELOW_MAX and CORRECT_FORMAT


def validate_branch_address(address: str):
    """Validate branch address."""
    address = address.replace("  ", "!")

    ABOVE_MIN = len(address) >= ADDRESS_MIN_LEN
    BELOW_MAX = len(address) <= ADDRESS_MAX_LEN
    CORRECT_FORMAT = ADDRESS_REGEX.match(address) is not None

    return ABOVE_MIN and BELOW_MAX and CORRECT_FORMAT
