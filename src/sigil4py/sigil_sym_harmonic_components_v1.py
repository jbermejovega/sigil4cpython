"""Exact finite Hodge harmonic components, optional SymPy backend.

Finite cochain complexes over R with standard positive-definite inner products.
This is not a general twisted/sheaf Hodge theorem.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class HarmonicComponent:
    degree: int
    dimension: int
    basis: tuple
    laplacian: object
    witness: str

def hodge_components(differentials, dimensions, *, witness=""):
    """Return degree-indexed harmonic spaces of a verified finite cochain complex.

    d[k]: C^k -> C^(k+1). All dimensions nonnegative.
    """
    from sympy import Matrix, zeros
    dims = tuple(dimensions)
    if not dims or any(type(n) is not int or n < 0 for n in dims):
        raise ValueError("INVALID_COCHAIN_DIMENSIONS")
    if len(differentials) != len(dims) - 1:
        raise ValueError("DIFFERENTIAL_COUNT_MISMATCH")
    ds = tuple(Matrix(d) for d in differentials)
    for k, d in enumerate(ds):
        if d.shape != (dims[k+1], dims[k]):
            raise ValueError("DIFFERENTIAL_PORT_MISMATCH")
    for k in range(len(ds)-1):
        if ds[k+1] * ds[k] != zeros(dims[k+2], dims[k]):
            raise ValueError("COCHAIN_SQUARE_NOT_ZERO")
    result = []
    for k, n in enumerate(dims):
        lap = zeros(n, n)
        if k > 0:
            lap += ds[k-1] * ds[k-1].T
        if k < len(ds):
            lap += ds[k].T * ds[k]
        basis = tuple(lap.nullspace())
        result.append(HarmonicComponent(k, len(basis), basis, lap, witness))
    return tuple(result)

def pentagon_cochains():
    """Oriented C5 graph: five vertices, five edges, no filled 2-cells."""
    from sympy import zeros
    d = zeros(5, 5)
    for edge in range(5):
        d[edge, edge] = -1
        d[edge, (edge+1)%5] = 1
    return (d,), (5, 5)
