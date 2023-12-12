import bcrypt


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
