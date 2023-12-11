from src.utils.enum import Enum, iota


def test_iota():
    class TestEnum(Enum):
        A = iota(True)
        B = iota()
        C = iota()

    assert TestEnum.A.value == 0
    assert TestEnum.B.value == 1
    assert TestEnum.C.value == 2
