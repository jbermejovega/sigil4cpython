# KRONE — PACA GUAPA UAP4 Statistical Physics Teaching Toolkit V1

Status: **release candidate, not published release**.
Authorial SIGIL educational facet: Jara Juana Bermejo Vega.
This is a new original educational implementation, not a copy of Fullmetal Alchemist.

## UAP4 exchange
A typed resource exchange records source, target, rational resource amounts,
context, boundary and witness. A balanced numerical exchange is only a
*source plan*, not proof of physical or economic equivalence.

## PACA core
- NUKLEA: pure Python dataclasses and exact rational resource accounting.
- QORE: optional SymPy exact partition functions.
- KORE: witnessed contextual decisions and replay-safe teaching outcomes.
- PACA.IO GAME: optional gameplay projection, not implemented here.
- KOKOMPI: optional parallel runtime, not executed here.

## Lesson: 1D Ising ring
Hamiltonian H = -J sum_i s_i s_(i+1) - h sum_i s_i, with periodic boundary.
Z = sum_{s_i = ±1} exp(-beta H).
Use the finite enumerator to explore symmetry, partition functions, energy
and magnetization. The n=2 ring counts two directed nearest-neighbour bonds,
as specified by the periodic sum; it is not the single-bond two-spin model.

Example:
```python
from sympy import symbols
from sigil4py.paca_guapa_uap4_krone import ising_ring_partition
beta, J = symbols("beta J")
print(ising_ring_partition(3, beta, J))
```

## Educational art license policy
Original lesson text and artwork require an explicit author-selected license.
The repository pyproject declares Apache-2.0 for its software, but that
does not automatically assign a license to newly authored art. Keep
third-party attribution, source references and review of all redistributed
assets. Do not ship images or code from external providers without rights review.

## Safe-to-ship gate
A 'safe to ship' label requires installation tests, CPython compatibility,
dependency audit, license audit, provenance, reproducible results and
explicit release authorization. Until then: HOLD_QUNO.
