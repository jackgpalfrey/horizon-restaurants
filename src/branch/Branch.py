# import ..utils.Database from database
from ..utils.Database import Database


class Branch:
    def __init__(self, branch_id: str) -> None:
        self._branch_id = branch_id

    # only the following method can directly return the variable's value because it was created
    # earlier, unlike the others which need to query the database to get the data
    def get_id(self) -> str:
        return self._branch_id

    def get_name(self) -> str:
        name, = Database.execute_and_fetchone(
            "SELECT name FROM public.branch WHERE id = %s", self._branch_id)
        return name

    def get_address(self) -> str:
        address, = Database.execute_and_fetchone(
            "SELECT address from public.branch WHERE id = %s", self._branch_id)
        return address
