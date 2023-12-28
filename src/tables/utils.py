from src.utils.Database import Database
from src.utils.errors import AlreadyExistsError


def validate_create_table(table_number: int, branch_id: str) -> bool:

    check = Database.execute_and_fetchone(
        "SELECT id from public.table WHERE table_number = %s AND branch_id = %s;", table_number, branch_id)

    if check is not None:
        return True
    return False
