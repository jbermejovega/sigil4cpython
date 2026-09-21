# SIGILITAS_SYNKK_UPSTREAM_INTERFACE_V1

Status: PUBLIC_INTERFACE_CANDIDATE

SYNKK is the SIGILITAS typed synchronization interface between canonical
SIGILBOOK and its public sigil4cpython projection.

Current observed pins at design time:

- SIGILBOOK main: `b170dc624aa14b91581267a9b9378cf5b38cfc5c`
- sigil4cpython main: `64f87ac0f642250219e4b7053f05ad570675dd49`
- public UAP candidate: PR #13, head `a95ef4af701e524b80c84822142d1b0cba9174ce`

## Typed OS interface

```text
SynkkSourcePin
  repository
  commit
  PACADEX/public-interface schema
       |
       v
SYNKK_COMPARE
       |
       +-- ALIGNED
       +-- SOURCE_AHEAD
       +-- HOLD[QUNO]
       +-- REJECT
       |
       v
UAP_PUBLICATION_PLAN
       |
       v
KLI/QLI public boundary
       |
       v
sigil4cpython
```

SYNKK is comparison/planning, not Git mutation.

```text
SYNKK != git pull
SYNKK != git merge
SYNKK != git push
SYNKK != workflow dispatch
SYNKK != private-source publication
```

## SIGILITAS service shape

```text
SYNKKD[
  SourcePin,
  PublicPin,
  PACADEXDiff,
  QUNO,
  PublicationWitness
]
```

The daemon may observe pins and compute a publication plan. A repository effect
requires a separate capability/effect gate.

## Walkthrough

1. Observe the exact SIGILBOOK `main` commit.
2. Observe the exact sigil4cpython `main` commit.
3. Export only the public PACADEX/UAP interface manifest from SIGILBOOK.
4. Run SYNKK compare. Never compare private bearers by identity.
5. If `ALIGNED`, emit a no-op receipt.
6. If `SOURCE_AHEAD`, produce a public projection delta.
7. If required public digest/witness data is absent, emit `HOLD[QUNO]`.
8. Validate the delta through UAP publication.
9. Materialize it on a non-`main` branch in sigil4cpython.
10. Run the public repository tests/status checks.
11. Submit a PR. With main protection enabled, only the protected PR/status-check
    path updates the public stabilization lineage.
12. SafeReplay records source pin, public parent pin, projection digest and final
    public commit.

No step is allowed to infer authority from matching names or matching ASTs.

## Branch protection interaction

The intended repository policy is:

```text
feature/publication branch
       -> tests/status checks
       -> PR
       -> protected main
```

SYNKK emits the candidate and evidence. GitHub rulesets enforce repository
mutation policy. They are identity-distinct layers.

PIORNALEGO ES CANON.
