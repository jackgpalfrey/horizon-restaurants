"""Module for managing orders."""
from ..branch.Branch import Branch
from ..user.ActiveUser import ActiveUser
from ..utils.Database import Database
from .Order import Order


class OrderService:
    """Static class for managing orders."""

    @staticmethod
    def create(branch: Branch) -> Order:
        """Create a new branch."""
        ActiveUser.get().raise_without_permission("order.create")

        branch_id = branch.get_id()
        number = 0

        sql = "INSERT INTO public.order (number, branch_id) \
        VALUES (%s,%s) RETURNING id;"

        cursor = Database.execute(sql, number, branch_id)
        Database.commit()
        result = cursor.fetchone()
        assert result is not None
        return Order(result[0])
