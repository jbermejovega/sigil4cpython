import pytest
s=pytest.importorskip("sympy")
from sigil4py.sigil_sym_harmonic_components_v1 import (
    hodge_components, pentagon_cochains)

def test_pentagon_betti():
    ds,dims=pentagon_cochains()
    hs=hodge_components(ds,dims,witness="C5")
    assert [h.dimension for h in hs]==[1,1]

def test_exact_laplacian():
    ds,dims=pentagon_cochains()
    hs=hodge_components(ds,dims)
    assert all(h.laplacian * b == s.zeros(dims[h.degree],1)
               for h in hs for b in h.basis)

def test_invalid_cochain():
    with pytest.raises(ValueError):
        hodge_components((s.eye(2),s.eye(2)),(2,2,2))

def test_empty_topology():
    hs=hodge_components((),(3,))
    assert hs[0].dimension==3
