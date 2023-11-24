from src.arithmetic import add, subtract



def test_add_two_1():
    assert add(1,1) == 2

def test_add_two_negatives():
    assert add(-2,-2) == -4

def test_add_two_zeros():
    assert add(0,0) == 0

def test_subtract_two_1():
    assert subtract(1,1) == 2

def test_subtract_two_negatives():
    assert subtract(-2,-2) == -4

def test_subtract_two_zeros():
    assert subtract(0,0) == 0