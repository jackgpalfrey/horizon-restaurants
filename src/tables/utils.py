# Author: Dina Hassanein (22066792)
"""Module with helpers and validation logic for tables."""
from src.utils.Database import Database


def validate_create_table(table_number: int, branch_id: str) -> bool:
    """Validate create table input."""
    check = Database.execute_and_fetchone(
        "SELECT id from public.table WHERE table_number = %s \
        AND branch_id = %s;", table_number, branch_id)

    return check is not None
