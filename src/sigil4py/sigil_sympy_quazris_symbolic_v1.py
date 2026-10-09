"""SIGIL SymPy QUAZRIS symbolic adapter. SymPy is an optional dependency."""
from dataclasses import dataclass

SCHEMA = "SIGIL_SYMPY_PLURAL_SYMBOLIC_TYPE_V1"

@dataclass(frozen=True)
class QuazrisSymbol:
    symbol: object
    occurrence: str
    context: str
    witness: str = ""

def bind_symbol(value: QuazrisSymbol) -> dict:
    if not isinstance(value, QuazrisSymbol):
        return {"verdict": "REJECT", "reason": "QUAZRIS_SYMBOL_REQUIRED"}
    if not value.occurrence or not value.context:
        return {"verdict": "REJECT", "reason": "CONTEXT_AND_OCCURRENCE_REQUIRED"}
    try:
        from sympy import Symbol, srepr
    except ImportError:
        return {"verdict": "HOLD_QUNO", "reason": "SYMPY_NOT_INSTALLED"}
    if not isinstance(value.symbol, Symbol):
        return {"verdict": "REJECT", "reason": "SYMPY_SYMBOL_REQUIRED"}
    return {"schema_id": SCHEMA, "verdict": "ADMIT_SOURCE_PLAN" if value.witness else "HOLD_QUNO",
            "symbol": srepr(value.symbol), "occurrence": value.occurrence,
            "context": value.context, "witness": value.witness,
            "identity_preserved": True, "safe_replay": True}

def symbolic_reflection(n: int = 5):
    """Return (R, psi, R*psi, (I-R)*psi), without claiming a fixed point."""
    if type(n) is not int or not 1 <= n <= 64:
        raise ValueError("FINITE_NETWORK_SIZE_REQUIRED")
    from sympy import Identity, MatrixSymbol
    r = MatrixSymbol("R", n, n)
    psi = MatrixSymbol("psi", n, 1)
    return r, psi, r * psi, (Identity(n) - r) * psi
