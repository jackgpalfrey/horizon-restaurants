"""Module for managing specific orders."""


class Order:
    """Class for managing an order."""

    def __init__(self, branch_id: str):
        """Don't call outside of OrderService."""
        self._branch_id = branch_id
