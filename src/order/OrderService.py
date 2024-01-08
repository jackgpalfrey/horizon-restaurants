"""Module for managing orders."""
from src.events.Event import Event
from ..branch.Branch import Branch
from ..user.ActiveUser import ActiveUser
from ..utils.Database import Database
from .OrderStatus import OrderStatus
from .Order import Order


class OrderService:
    """Static class for managing orders."""

    @staticmethod
    def create(branch: Branch) -> Order:
        """Create a new order."""
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

    @staticmethod
    def get_by_id(order_id: str) -> Order | None:
        """Get an order by it's id."""
        sql = "SELECT id FROM public.order WHERE id=%s"
        result = Database.execute_and_fetchone(sql, order_id)

        if result is not None:
            return Order(result[0])

    @staticmethod
    def get_by_event(event: Event) -> Order | None:
        """Get associated order."""
        sql = "SELECT order_id FROM public.events WHERE id=%s"
        result = Database.execute_and_fetchone(sql, event.get_id())

        if result is not None and result[0] is not None:
            return Order(result[0])

    @staticmethod
    def get_all_from_branch(branch: Branch) -> list[Order]:
        """Get all orders at a specific branch."""
        branch_id = branch.get_id()

        sql = "SELECT id FROM public.order WHERE branch_id=%s"
        result = Database.execute_and_fetchall(sql, branch_id)

        return [Order(record[0]) for record in result]

    @staticmethod
    def get_all_open_from_branch(branch: Branch) -> list[Order]:
        """Get all open orders at a specific branch."""
        branch_id = branch.get_id()

        sql = "SELECT id FROM public.order WHERE branch_id=%s AND status!=%s"
        result = Database.execute_and_fetchall(sql,
                                               branch_id,
                                               OrderStatus.COMPLETED.value)

        return [Order(record[0]) for record in result]

    @staticmethod
    def get_all_placed_from_branch(branch: Branch) -> list[Order]:
        """Get all open placed orders at a specific branch."""
        branch_id = branch.get_id()

        sql = "SELECT id FROM public.order WHERE branch_id=%s AND status=%s"
        result = Database.execute_and_fetchall(sql, branch_id,
                                               OrderStatus.PLACED.value)

        return [Order(record[0]) for record in result]

    @staticmethod
    def get_by_order_number(branch: Branch,
                            order_number: int) -> Order | None:
        """Get the open order with an order number."""
        branch_id = branch.get_id()

        sql = "SELECT id FROM public.order \
        WHERE branch_id=%s AND status!=%s AND number=%s"

        result = Database.execute_and_fetchone(sql, branch_id,
                                               OrderStatus.COMPLETED.value,
                                               order_number)

        if result is not None:
            return Order(result[0])
