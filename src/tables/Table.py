from ..utils.Database import Database


class Table:
    def __init__(self, table_id: str):
        self._table_id = table_id

    def get_table_number(self) -> str:
        table_number = Database.execute_and_fetchone(
            "SELECT table_number FROM public.table WHERE id = %s", self._table_id)
        return table_number[0]

    def get_capacity(self) -> int:
        capacity = Database.execute_and_fetchone(
            "SELECT capacity FROM public.table WHERE id = %s", self._table_id)
        return capacity[0]

    def set_capacity(self, table_capacity: int) -> None:

        Database.execute_and_commit(
            "UPDATE public.table SET capacity = %s WHERE id = %s", table_capacity, self._table_id)
