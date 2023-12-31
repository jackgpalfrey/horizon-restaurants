from .Event import Event
from ..utils.Database import Database


class BranchEvents:

    def __init__(self, branch_id: str):
        self._branch_id = branch_id

    def create(self, type: int) -> Event:
        Database.execute_and_commit(
            "INSERT INTO public.branch (branch_name, type) VALUES(%s, %s)", self._branch_id, type)

        return BranchEvents.get_by_name(BranchEvents)

    def get_by_id(self,id: str) -> Event:
        sql = "SELECT id from public.event where id = %s"
        Database.execute_and_fetchone(sql, id)





