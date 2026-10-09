from fractions import Fraction
import pytest
from sigil4py.paca_guapa_uap4_krone import Exchange, evaluate, ising_ring_partition

def test_equal_exchange():
    e = Exchange("A","B",Fraction(2),Fraction(2),"G","W")
    assert evaluate(e)["verdict"] == "ADMIT_SOURCE_PLAN"

def test_unequal_hold():
    e = Exchange("A","B",Fraction(1),Fraction(2),"G","W")
    assert evaluate(e)["verdict"] == "HOLD_QUNO"

def test_no_witness_hold():
    assert evaluate(Exchange("A","B",Fraction(1),Fraction(1),"G"))["verdict"] == "HOLD_QUNO"

def test_ising_two_spin_ring():
    s = pytest.importorskip("sympy")
    b, j = s.symbols("beta J", real=True)
    z = ising_ring_partition(2,b,j)
    assert s.simplify(z - 4*s.cosh(2*b*j)) == 0

def test_ising_reject_unbounded():
    with pytest.raises(ValueError):
        ising_ring_partition(13,1,1)
