"""PACA GUAPA UAP4: pure-Python typed exchange and teaching kernel."""
from dataclasses import dataclass
from fractions import Fraction

SCHEMA = "SIGIL_PACA_GUAPA_UAP4_KRONE_V1"

@dataclass(frozen=True)
class Exchange:
    source: str
    target: str
    resource_in: Fraction
    resource_out: Fraction
    context: str
    witness: str = ""
    boundary: str = "CLOPEN"

def evaluate(exchange: Exchange) -> dict:
    if not isinstance(exchange, Exchange):
        return {"verdict": "REJECT", "reason": "EXCHANGE_TYPE_REQUIRED"}
    if not exchange.source or not exchange.target or not exchange.context:
        return {"verdict": "REJECT", "reason": "MISSING_TYPED_PORT"}
    if exchange.resource_in < 0 or exchange.resource_out < 0:
        return {"verdict": "REJECT", "reason": "NEGATIVE_RESOURCE"}
    if exchange.boundary != "CLOPEN":
        return {"verdict": "HOLD_QUNO", "reason": "BOUNDARY_NOT_ADMITTED"}
    balanced = exchange.resource_in == exchange.resource_out
    return {"schema_id": SCHEMA,
            "verdict": "ADMIT_SOURCE_PLAN" if balanced and exchange.witness else "HOLD_QUNO",
            "balanced": balanced,
            "delta": str(exchange.resource_out - exchange.resource_in),
            "source": exchange.source, "target": exchange.target,
            "context": exchange.context, "witness": exchange.witness,
            "no_identity_transport": True, "safe_replay": True}

def ising_ring_partition(n: int, beta, coupling, field=0):
    """Exact symbolic finite-size Ising partition sum for a periodic 1D ring."""
    if type(n) is not int or not 1 <= n <= 12:
        raise ValueError("FINITE_SPIN_COUNT_REQUIRED")
    try:
        from sympy import S, exp, sympify
    except ImportError as exc:
        raise RuntimeError("SYMPY_OPTIONAL_DEPENDENCY_MISSING") from exc
    beta, coupling, field = map(sympify, (beta, coupling, field))
    result = S.Zero
    for mask in range(1 << n):
        spins = [1 if mask & (1 << i) else -1 for i in range(n)]
        interaction = sum(spins[i] * spins[(i + 1) % n] for i in range(n))
        magnetization = sum(spins)
        result += exp(beta * (coupling * interaction + field * magnetization))
    return result
