"""Module for managing specific orders."""


from src.branch.Branch import Branch
from src.order.OrderStatus import OrderStatus
from src.tables.Table import Table
from src.user.User import User
from src.utils.Database import Database
from src.utils.errors import InputError


class Order:
    """Class for managing an order."""

    def __init__(self, order_id: str):
        """Don't call outside of OrderService."""
        self._order_id = order_id

    def get_branch(self) -> Branch:
        """Get branch that order is in."""
        sql = "SELECT branch_id FROM public.order WHERE id=%s"
        result = Database.execute_and_fetchone(sql, self._order_id)
        assert result is not None
        return result[0]

    def get_number(self) -> int:
        """Get order's number."""
        sql = "SELECT number FROM public.order WHERE id=%s"
        result = Database.execute_and_fetchone(sql, self._order_id)
        assert result is not None
        return result[0]

    def get_status(self) -> OrderStatus:
        """Get order's status."""
        sql = "SELECT status FROM public.order WHERE id=%s"
        result = Database.execute_and_fetchone(sql, self._order_id)

        assert result is not None
        return OrderStatus(result[0])

    def get_priority(self) -> int:
        """Get order's priority."""
        sql = "SELECT priority FROM public.order WHERE id=%s"
        result = Database.execute_and_fetchone(sql, self._order_id)

        assert result is not None
        return result[0]

    def get_assigned_staff(self) -> User | None:
        """Get staff member assigned to this order."""
        sql = "SELECT assigned_staff FROM public.order WHERE id=%s"
        result = Database.execute_and_fetchone(sql, self._order_id)

        if result is not None and result[0] is not None:
            return User(result[0])

    def get_customer_name(self) -> str | None:
        """Get customers name."""
        sql = "SELECT customer_name FROM public.order WHERE id=%s"
        result = Database.execute_and_fetchone(sql, self._order_id)

        assert result is not None
        return result[0]

    def get_table(self) -> Table | None:
        """Get table associated with order."""
        sql = "SELECT table_id FROM public.order WHERE id=%s"
        result = Database.execute_and_fetchone(sql, self._order_id)

        if result is not None and result[0] is not None:
            return Table(result[0])

    def set_status(self, status: OrderStatus) -> None:
        """Set order status."""
        sql = "UPDATE public.order SET status = %s WHERE id = %s"
        Database.execute_and_commit(sql, status.value, self._order_id)

    def assign_staff(self, user: User | None) -> None:
        """Assign given staff to order."""
        sql = "UPDATE public.order SET assigned_staff=%s WHERE id=%s"

        id = None
        if user is not None:
            id = user.get_id()

        Database.execute_and_commit(sql, id, self._order_id)

    def cancel(self) -> None:
        """Cancel order."""
        self.set_status(OrderStatus.CANCELLED)

    def place(self) -> None:
        """Place order."""
        self.set_status(OrderStatus.PLACED)

    def complete(self) -> None:
        """Complete order."""
        self.set_status(OrderStatus.COMPLETED)

    def set_priority(self, priority: int) -> None:
        """Set priority."""
        sql = "UPDATE public.order SET priority=%s WHERE id=%s"
        Database.execute_and_commit(sql, priority, self._order_id)

    def set_customer_name(self, name: str) -> None:
        """Set customer name."""
        sql = "UPDATE public.order SET customer_name=%s WHERE id=%s"
        Database.execute_and_commit(sql, name, self._order_id)

    def set_table(self, table: Table) -> None:
        """Set table."""
        sql = "UPDATE public.order SET table_id = %s WHERE id=%s"
        Database.execute_and_commit(sql, table.get_id(), self._order_id)
