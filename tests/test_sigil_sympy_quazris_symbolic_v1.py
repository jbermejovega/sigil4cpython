import pytest
sympy = pytest.importorskip("sympy")
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
p = Path(__file__).resolve().parents[1] / "src/sigil4py/sigil_sympy_quazris_symbolic_v1.py"
s = spec_from_file_location("sigil_sympy", p)
m = module_from_spec(s)
s.loader.exec_module(m)

def test_occurrence_not_symbol_identity():
    x = sympy.Symbol("x", real=True)
    a = m.QuazrisSymbol(x, "o1", "G", "W")
    b = m.QuazrisSymbol(x, "o2", "G", "W")
    assert a.symbol == b.symbol and a.occurrence != b.occurrence

def test_witness_hold():
    x = sympy.Symbol("x")
    assert m.bind_symbol(m.QuazrisSymbol(x, "o1", "G"))["verdict"] == "HOLD_QUNO"

def test_reflection_shapes():
    r, psi, reflected, residual = m.symbolic_reflection()
    assert r.shape == (5, 5) and psi.shape == (5, 1)
    assert reflected.shape == residual.shape == (5, 1)

def test_invalid_network_size():
    with pytest.raises(ValueError):
        m.symbolic_reflection(0)
