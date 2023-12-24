from ..utils.Database import Database


class Table:
    def __init__(self, table_id: str):
        self._table_id = table_id

    def get_capacity(self) -> int:
        capacity = Database.execute_and_fetchone(
            "SELECT capacity FROM public.table WHERE id = %s", self._table_id)
        return capacity[0]
