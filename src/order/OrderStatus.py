# Author: Jack Palfrey (22032928)
"""Module with enum for OrderStatus."""
from enum import auto, Enum


class OrderStatus(Enum):
    """Status or order."""

    NOT_PLACED = auto()
    CANCELLED = auto()
    PLACED = auto()
    COMPLETED = auto()
