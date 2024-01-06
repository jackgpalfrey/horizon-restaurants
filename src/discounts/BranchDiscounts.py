from ..user.ActiveUser import ActiveUser
from ..utils.Database import Database
from .Discount import Discounts

class BranchDiscounts:

    def __init__(self, branch_id: str):
        self._branch_id = branch_id

    def create(self, multiplier: float, description: str) -> Discounts:
        ActiveUser.get().raise_without_permission("discounts.create")

        Database.execute_and_commit(
            "INSERT INTO public.discounts (multiplier, description, branch_id) \
            VALUES(%s, %s, %s)", multiplier, description, self._branch_id)
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.discounts \
            WHERE branch_id=%s;",
            self._branch_id)

        assert result is not None
        return Discounts(result[0])

    def get_by_id(self, discount_id: str) -> Discounts:
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.discounts WHERE id = %s", discount_id)

        if result is not None:
            return Discounts(result[0])    

    def get_all(self) -> list[Discounts]:
        result = Database.execute_and_fetchall("SELECT id FROM public.discounts")

        return [Discounts(record[0]) for record in result]