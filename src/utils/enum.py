from enum import Enum

current = -1


def iota(reset: bool = False):
    """
    Similar to iota in Go, this function returns an incrementing integer.
    :param reset: If True, the counter will be reset to 0.

    :usage:
    class TestEnum(Enum):
        A = iota(True)
        B = iota()
        C = iota()

    TestEnum.A.value == 0
    TestEnum.B.value == 1
    TestEnum.C.value == 2
    """

    global current
    if reset:
        current = -1
    current += 1
    return current
