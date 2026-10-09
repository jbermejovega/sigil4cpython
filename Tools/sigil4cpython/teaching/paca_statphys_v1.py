# SPDX-License-Identifier: MIT
"""PACA QORE/NUKLEA: source-only Ising teaching model, independent of CPython internals."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from itertools import product
from math import exp, isfinite, log
from random import Random


@dataclass(frozen=True)
class Ring:
    """Distinct sites joined by a periodic nearest-neighbor relation."""
    sites: tuple[str, ...]
    coupling: int = 1
    field: int = 0
    context: str = "PACA_GUAPA"

    def __post_init__(self):
        if type(self.sites) is not tuple:
            raise ValueError("sites must be an immutable tuple")
        if not 3 <= len(self.sites) <= 12 or len(set(self.sites)) != len(self.sites):
            raise ValueError("3..12 uniquely named sites required")
        if any(not isinstance(s, str) or not s for s in self.sites):
            raise ValueError("nonempty site IDs required")
        if type(self.coupling) is not int or type(self.field) is not int:
            raise ValueError("integer J/h required")
        if abs(self.coupling) > 1000 or abs(self.field) > 1000:
            raise ValueError("J/h must be bounded")
        if not isinstance(self.context, str) or not self.context:
            raise ValueError("context required")

    @property
    def edges(self) -> tuple[tuple[str, str], ...]:
        return tuple((site, self.sites[(i + 1) % len(self.sites)])
                     for i, site in enumerate(self.sites))


def energy(ring: Ring, spins: tuple[int, ...]) -> int:
    if len(spins) != len(ring.sites) or any(type(s) is not int or s not in (-1, 1)
                                           for s in spins):
        raise ValueError("spin assignment incompatible with sites")
    return -ring.coupling * sum(spins[i] * spins[(i + 1) % len(spins)]
                               for i in range(len(spins))) - ring.field * sum(spins)


@dataclass(frozen=True)
class Exchange:
    """Formal resource account; not measured physical heat or work."""
    epoch: int
    site: str
    parent: str
    occurrence: str
    before_energy: int
    after_energy: int
    exchange_into_system: int
    accepted: bool
    probability: float
    witness: str
    pacapdg: str = "ADMIT_SOURCE_PLAN"
    uap: str = "UNJUDGED"

    @property
    def balanced(self) -> bool:
        return self.before_energy + self.exchange_into_system == self.after_energy


def metropolis_probability(delta_energy: int, beta: float) -> float:
    if type(delta_energy) is not int or type(beta) not in (float, int):
        raise ValueError("typed delta/beta required")
    if not isfinite(beta) or not 0 <= beta <= 10000:
        raise ValueError("finite nonnegative beta required")
    return 1.0 if delta_energy <= 0 else exp(-float(beta) * delta_energy)


def trajectory(ring: Ring, *, beta: float, steps: int, seed: int,
               initial: tuple[int, ...] | None = None) -> tuple[tuple[int, ...], tuple[Exchange, ...]]:
    if type(steps) is not int or not 0 <= steps <= 10000 or type(seed) is not int:
        raise ValueError("bounded step count and integer seed required")
    metropolis_probability(0, beta)
    if initial is not None and type(initial) is not tuple:
        raise ValueError("initial spin assignment must be a tuple")
    spins = tuple([1] * len(ring.sites) if initial is None else initial)
    energy(ring, spins)
    rng = Random(seed)
    trace: list[Exchange] = []
    run_source = (ring.context, ring.sites, ring.coupling, ring.field,
                  float(beta), spins, seed)
    run_id = sha256(repr(run_source).encode("utf-8")).hexdigest()[:16]
    parent = f"{ring.context}:RUN:{run_id}:GENESIS:0"
    for epoch in range(1, steps + 1):
        i = rng.randrange(len(spins))
        candidate = spins[:i] + (-spins[i],) + spins[i + 1:]
        before = energy(ring, spins)
        delta = energy(ring, candidate) - before
        p = metropolis_probability(delta, beta)
        accepted = rng.random() < p
        if accepted:
            spins = candidate
        after = energy(ring, spins)
        occurrence = f"{ring.context}:RUN:{run_id}:EPOCH:{epoch}"
        record = Exchange(epoch, ring.sites[i], parent, occurrence, before,
                          after, after - before, accepted, p,
                          f"SIMULATED:{seed}:{epoch}")
        if not record.balanced:
            raise AssertionError("UAP4 resource ledger failed")
        trace.append(record)
        parent = occurrence
    return spins, tuple(trace)


def exact_equilibrium(ring: Ring, beta: float) -> dict[str, float]:
    """Enumerate finite Gibbs equilibrium using log-sum-exp; no MC estimate."""
    metropolis_probability(0, beta)
    states = tuple(product((-1, 1), repeat=len(ring.sites)))
    energies = tuple(energy(ring, s) for s in states)
    a = tuple(-float(beta) * e for e in energies)
    m = max(a)
    weights = tuple(exp(x - m) for x in a)
    z = sum(weights)
    mean_e = sum(w * e for w, e in zip(weights, energies)) / z
    mean_m = sum(w * sum(s) for w, s in zip(weights, states)) / z
    var_e = sum(w * (e - mean_e) ** 2 for w, e in zip(weights, energies)) / z
    var_m = sum(w * (sum(s) - mean_m) ** 2 for w, s in zip(weights, states)) / z
    return {
        "n": len(ring.sites), "beta": float(beta), "log_partition": m + log(z),
        "mean_energy": mean_e, "mean_magnetization": mean_m,
        "heat_capacity_kB1": beta * beta * var_e,
        "susceptibility_kB1": beta * var_m,
    }


def source_receipt(ring: Ring, spins: tuple[int, ...], trace: tuple[Exchange, ...]) -> dict:
    """Presentation-only receipt, no external effects."""
    return {
        "contract": "SIGIL_PACA_UAP4_EQUIVALENT_EXCHANGE_TEACHING_V1",
        "state": list(spins), "energy": energy(ring, spins),
        "sites": list(ring.sites), "edges": [list(x) for x in ring.edges],
        "trace": [asdict(e) for e in trace], "uap": "UNJUDGED",
        "external_effect": False, "safe_to_ship": False,
    }
