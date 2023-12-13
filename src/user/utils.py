import bcrypt
import re

USERNAME_MIN_LEN = 2  # INCLUSIVE
USERNAME_MAX_LEN = 15  # INCLUSIVE
USERNAME_REGEX = re.compile(r"^[a-z][a-z0-9-]*$")

PASSWORD_MIN_LEN = 8   # INCLUSIVE
PASSWORD_MAX_LEN = 100  # INCLUSIVE
PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[a-zA-Z\d@$!%*#?&]*$")


FULL_NAME_MIN_LEN = 2  # INCLUSIVE
FULL_NAME_MAX_LEN = 50  # INCLUSIVE
FULL_NAME_REGEX = re.compile(r"^[a-zA-Z][a-zA-Z ]*[a-zA-Z]$")


def hash_password(password: str) -> str:
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()

    hash_bytes = bcrypt.hashpw(bytes, salt)
    hash_str = str(hash_bytes, "utf-8")
    return hash_str


def check_password(password: str, hashed_password: str) -> bool:
    bytes = password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(bytes, hashed_bytes)


def validate_username(username: str) -> bool:
    MIN_LENGTH = 3
    MAX_LENGTH = 15
    REGEX = re.compile(r"^[a-z][a-z0-9-]*$")

    ABOVE_MIN = MIN_LENGTH <= len(username)
    BELOW_MAX = len(username) <= MAX_LENGTH
    CORRECT_FORMAT = REGEX.match(username) is not None

    return ABOVE_MIN and BELOW_MAX and CORRECT_FORMAT


def validate_username(username: str) -> bool:
    ABOVE_MIN = len(username) >= USERNAME_MIN_LEN
    BELOW_MAX = len(username) <= USERNAME_MAX_LEN
    CORRECT_FORMAT = USERNAME_REGEX.match(username) is not None

    return ABOVE_MIN and BELOW_MAX and CORRECT_FORMAT


def validate_password(password: str):
    ABOVE_MIN = len(password) >= PASSWORD_MIN_LEN
    BELOW_MAX = len(password) <= PASSWORD_MAX_LEN
    CORRECT_FORMAT = PASSWORD_REGEX.match(password) is not None

    return ABOVE_MIN and BELOW_MAX and CORRECT_FORMAT


def validate_full_name(full_name: str):
    # Hacky solution to block two or more spaces sequentially. If anyone's better at regex than me
    # please fix
    full_name = full_name.replace("  ", "!")

    ABOVE_MIN = len(full_name) >= FULL_NAME_MIN_LEN
    BELOW_MAX = len(full_name) <= FULL_NAME_MAX_LEN
    CORRECT_FORMAT = FULL_NAME_REGEX.match(full_name) is not None

    return ABOVE_MIN and BELOW_MAX and CORRECT_FORMAT
