# PACA GUAPA · UAP4 · Statistical Physics Teaching Toolkit V1

**Public compatibility carrier:** `jbermejovega/sigil4cpython`  
**Project primitive:** `SIGIL_PACA_UAP4_EQUIVALENT_EXCHANGE_TEACHING_V1`  
**Origin conceptual author:** Jara Juana Bermejo Vega (JJBV)  
**Integration mode:** source-only, isolated `Tools/sigil4cpython/teaching/`.  
**Release state:** `RELEASE_CANDIDATE / HOLD_QUNO` — not a signed, tagged or upstream CPython release.

## Lesson goal (1–2 sessions)

Learn statistical physics from a finite Ising ring while inspecting how a symbolic design/game language can preserve the identity of a physical site, the occurrence of each proposed move, an energy-accounting trace, and the independence of a public CPython interface.

**Physics kernel (not a new physical law).** For \(s_i\in\{-1,+1\}\), distinct sites \(i\in\{0,\ldots,N-1\}\), integer coupling \(J\), field \(h\), and periodic indices,

\[
H(\mathbf s)=-J\sum_i s_i s_{i+1}-h\sum_i s_i.
\]

At \(\beta=1/(k_B T)\), the finite canonical ensemble has \(Z=\sum_{\mathbf{s}}e^{-\beta H(\mathbf{s})}\). The exact enumerator uses a numerically stable log-sum-exp for N between 3 and 12. The Metropolis proposal probability for a one-site flip is

\[
A(\Delta E)=\min\{1,e^{-\beta\Delta E}\}.
\]

For symmetric flip proposals it satisfies the **transition-probability detailed-balance ratio**, \(A(\Delta E)/A(-\Delta E)=e^{-\beta\Delta E}\). An observed Monte Carlo trace is not itself a proof of convergence to equilibrium.

## UAP4 — Jara's typed equivalent-exchange contract

The pop-cultural *equivalent exchange* motif is an artistic inspiration for a **typed resource ledger**, not a claim that fiction establishes physics. There is no quotation, character likeness, image, music or franchise license bundled.

1. **NUKLEA (physical carrier):** distinct named sites with \(s_i\in\{\pm1\}\), coupling \(J\), field \(h\); the energy function is pure and bounded.
2. **QORE (relational carrier):** a flip proposes a fresh occurrence on a specific site, preserving its parent, epoch and declared witness record.
3. **KOKOMPI (resource account):** the accepted state change records \(E_{after}=E_{before}+R_{in}\). Here \(R_{in}:=E_{after}-E_{before}\) is a **formal accounting entry**, not experimentally measured heat or work.
4. **KORE / UAP admission:** present JSON/CLI data but never infer actual authorization, scientific validation or CPython upstream acceptance from a balanced ledger.

Mathematical separation:

```text
ISING_ACCEPTANCE != PACAPDG_SOURCE_ADMISSION
ENERGY_BALANCE != CONSENT
RESOURCE_EQUIVALENCE != IDENTITY_COLLAPSE
ARTISTIC_TROPE != PHYSICAL_SPIN
RELEASE_CANDIDATE != RELEASE_CERTIFIED
```

The original **PACA GUAPA** teaching pattern uses art to explain the physics, without claiming that colors, embodied tropes or relational categories are themselves Ising observables.

## PACA GUAPA TDESIGN patterns

| Pattern | Classroom action | SIGIL proof obligation |
| --- | --- | --- |
| `TDesign.SiteFacet` | Give every spin its own name/color/voice | Same value does not identify sites |
| `TDesign.RelationalEdge` | Draw J-couplings on a ring | Neighborhood and J typed separately |
| `TDesign.ExchangeAccount` | Record before/after energy | Algebraic balance for every accepted move |
| `TDesign.KokompiChronicle` | Follow parent and epoch | Fresh IDs even for rejected proposals |
| `TDesign.PolycategoryPrompt` | Interpret spin/coupling → energy + trace as a multiport teaching analogy | No unproved polycategory/universal property asserted |
| `TDesign.GUAPAStyle` | Assign a fictional stained-glass color or musical timbre | Style cannot change the underlying measured physics silently |

**PACA.IO game artifact:** `Tools/sigil4cpython/teaching/paca_guapa_ising_v1.io` is a nonexecuting lesson specification with the syntax of a declared `.sym` source game. The source-only `.sym` parser lives in an independent proposed PR #17 and is **not** assumed to exist on public `main`. `.io` is not a CPython language extension.

## Hands-on exercises

**Exercise 1 — Ising energy.** For \(N=3,J=1,h=0\), show that \((+,+,+)\) has energy \(-3\), while \((-,+,+)\) has energy \(+1\). Determine the cost of flipping one spin. Explain why two equal spin values do not identify the sites.

**Exercise 2 — Exact Gibbs ensemble.** Count states by energy: 2 of energy \(-3\), 6 of energy \(+1\). Verify
\(Z(\beta)=2e^{3\beta}+6e^{-\beta}\)
and the value \(Z(0)=8\). Compare with the CLI enumerator.

**Exercise 3 — Detailed balance.** For \(\Delta E=4\), compute the Metropolis acceptance probability at beta 0.4. Explain the difference between a transition probability and actual energy exchange with a heat bath.

**Exercise 4 — Exchange ledger.** Generate 24 Monte Carlo proposals, record each event's parent, occurrence, acceptance flag, delta energy and the equality \(E_{before}+R_{in}=E_{after}\). The entries are educational accounting witnesses, not calibrated calorimetry.

**Exercise 5 — Symmetry/art.** Assign each site a distinct artistic trope (original descriptions or colors). Swap two colors without changing site identities and say which physical observables remain invariant. A value-equivalence class cannot erase an occurrence ID.

**Exercise 6 — Critical assessment.** Explain why finite \(N\) does not establish a thermodynamic-limit phase transition; why a reproducible seed does not prove Monte Carlo mixing; and why a Git commit or passing test does not grant release or CPython authority.

### Student evaluation

Assess the **correctness of computations and their interpretation**, not numerical output alone. Suggested rubric: Hamiltonian/counted states 30%; Gibbs vs Metropolis interpretation 30%; typed trace/identities 20%; limitations/reproducibility 20%.

## Commands (from repository root)

```bash
python Tools/sigil4cpython/teaching/paca_statphys_cli.py equilibrium --sites 3 --beta 0.7
python Tools/sigil4cpython/teaching/paca_statphys_cli.py play --sites 4 --beta 0.6 --steps 24 --seed 42
python Tools/sigil4cpython/teaching/test_paca_statphys_v1.py
cc -std=c99 -Wall -Wextra -Werror -pedantic \
  -o /tmp/paca_statphys_c_v1 Tools/sigil4cpython/teaching/paca_statphys_c_v1.c
/tmp/paca_statphys_c_v1 +++ 1 0
```

**Portability:** pure Python stdlib; standalone C99 only uses ISO C public interfaces and does not link against CPython. No `Include/internal/` edits, `_Py*` private APIs, interpreter semantics modifications, CGI, shell subprocess triggered by classroom input, package installation, network dispatch, OSC/MIDI or GitHub write are required for these lessons.

### Evidence and shipping policy

Author-run focused local checks for the *original authored source files* recorded:
- Python: **16 passed**, and `py_compile` passed.
- C99: compiler with strict warnings passed; \(+,+,+\) energy -3; \(-,+,+\) energy +1; invalid label rejected.
- Source files subsequently copied to public SIGIL4CPython branch: GitHub source readback and hash verification required before promoting evidence to exact published bytes.

Before assigning `SAFE_TO_SHIP`: run tests on the public branch, inspect diff against main, confirm licensing and human review, check AI disclosure/CPython contribution policy, archive the test transcript/commit SHA, and assess if any proposed actual CPython change belongs upstream. No release tag is created by this candidate, and no rights in unrelated fictional universes are granted.

**Artistic materials licensing:** code snippets newly authored for this kit carry MIT identifiers; educational prose and any eventual original visual assets remain **rights-review pending** before assigning an open content license. No franchise media are distributed.

**Source lineage:** SIGILBOOK `PACA_PDG_EDUCATION_PACK_V1`, relational-spin V1, PACA.IO GAME runtime, Jaranian resource-theory specifications, POLYARIA and Hyperjarra source notes. Their project-specific claims are not turned into verified physical theorems.

**PIORNALEGO ES CANON · PLURA MANENT · TRACE MANET.**
