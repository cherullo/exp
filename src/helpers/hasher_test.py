import pytest
from helpers import Hasher

STR1 = 'Shikamaru'
STR2 = 'Neji'
STR3 = 'Tsunade'

def test_initial_value():
    assert Hasher().value == 1

def test_int():
    for i in range(-2, 3):
        assert Hasher(i).value != 0 

def test_float():    
    for f in range(-2, 3):
        assert Hasher(float(f)).value != 0 

# __eq__ works against other Hasher
def test_eq_hasher():
    assert Hasher(7) == Hasher(7)
    assert Hasher(STR1) != Hasher(STR2)
    assert Hasher(STR2) == Hasher(STR2)

# __eq__ works against int
def test_eq_int():
    hash: int = Hasher(STR1).value
    assert Hasher(STR1) == hash

# Ordered works
def test_ordered_works():
    h1 = Hasher().ordered(STR1, STR2)
    h2 = Hasher().ordered(STR2, STR1)
    assert h1 != 0
    assert h2 != 0
    assert h1 != h2

# Constructor is ordered
def test_init_is_ordered():
    assert Hasher(STR1, STR2) == Hasher().ordered(STR1, STR2)

# Unordered works
# Ordered works
def test_unordered_works():
    h1 = Hasher().unordered(STR1, STR2, STR3)
    h2 = Hasher().unordered(STR3, STR2, STR1)
    assert h1 != 0
    assert h2 != 0
    assert h1 == h2

def test_unordered_works_2():
    h1 = Hasher().ordered(1).unordered(STR1, STR2, STR3).ordered(9)
    h2 = Hasher().ordered(1).unordered(STR3, STR2, STR1).ordered(9)
    assert h1 != 0
    assert h2 != 0
    assert h1 == h2

# Accepts lists
def test_accepts_lists():
    alist = [STR1, STR2, STR3]
    assert Hasher(STR1, STR2, STR3) == Hasher(*alist)
    assert Hasher(STR1, STR2, STR3) == Hasher().ordered(*alist)
    assert Hasher().unordered(STR2, STR1, STR3) == Hasher().unordered(*alist)

if __name__ == '__main__':
    x = lambda x : print (f'{x} = {Hasher(x)}')
    x(1)
    x(STR1)
    x(STR2)