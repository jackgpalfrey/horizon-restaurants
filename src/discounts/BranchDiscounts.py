"""Module for managing discounts in a branch."""
from ..user.ActiveUser import ActiveUser
from ..utils.Database import Database
from .Discount import Discounts


class BranchDiscounts:
    """Class for managing discounts in a branch."""

    def __init__(self, branch_id: str):
        """Don't call outside of Branch."""
        self._branch_id = branch_id

    def create(self, multiplier: float, description: str) -> Discounts:
        """Create a new discount."""
        ActiveUser.get().raise_without_permission("discounts.create")

        cursor = Database.execute(
            "INSERT INTO public.discounts \
            (multiplier, description, branch_id) \
            VALUES(%s, %s, %s) RETURNING id;",
            multiplier, description, self._branch_id)

        Database.commit()
        result = cursor.fetchone()

        assert result is not None
        return Discounts(result[0])

    def get_by_id(self, discount_id: str) -> Discounts | None:
        """Get a discount by its id."""
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.discounts WHERE id=%s AND branch_id=%s",
            discount_id, self._branch_id)

        if result is not None:
            return Discounts(result[0])

    def get_all(self) -> list[Discounts]:
        """Get all discounts."""
        result = Database.execute_and_fetchall(
            "SELECT id FROM public.discounts")

        return [Discounts(record[0]) for record in result]
