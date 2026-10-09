# SIGIL4CPython — Plural-Typed PYPL Request Interface V1

**Primitive:** `SIGIL4CPYTHON_PYPL_TYPED_REQUEST_INTERFACE_V1`  
**Parent:** `SIGIL4CPYTHON_PYPL_INTEGRATION_REQUEST_V1`  
**Root:** `SIGILBOOK_TOTAL_VOID_AST_OF_ALL_ASTS_V1`  
**Host:** `jbermejovega/sigil4cpython` — public source-only compatibility carrier.

## Signature

\[
\mathsf{PYPLRequest}_\Gamma:
\mathsf{SourceBoundRequest}_\Gamma\times\mathsf{ReadOnlyLocalArtifacts}
\longrightarrow
\mathsf{SourcePlanVerdict}_\Gamma.
\]

The codomain is the tagged sum:
`ADMIT_SOURCE_PLAN | HOLD_QUNO | REJECT`.

A verdict of `ADMIT_SOURCE_PLAN` certifies *only structural local
completeness for proposed review*, never real consent, UAP authority,
CPython upstream acceptance, or hardware/software execution.

## Typed carriers

| Sort | Python type | Meaning |
| --- | --- | --- |
| SOURCE_PIN/TARGET_PIN | repository and commit strings | provenance coordinates |
| ARTIFACT | `Artifact` | allowlisted path and SHA-256 |
| EVIDENCE | `Evidence` | missing/present references; no authentication |
| BOUNDARY | `Boundaries` | no coercion and no external effects |
| REQUEST | `IntegrationRequest` | frozen structured source-plan envelope |
| VERDICT | `IntegrationVerdict` | exclusive three-way disposition |

`RequestJSON`, `ArtifactJSON`, `EvidenceJSON`, and `BoundaryJSON` describe
the JSON interchange. Python `TypedDict` does not enforce runtime types:
`decode_request()` validates exact keys and primitive types, rejecting
implicit coercion (for example, the integer `1` as a boolean).

`evaluate_typed_request(raw, root)` delegates to the existing
`evaluate_request()` gate and checks that the resulting decision
cannot claim external effects, verified reviews, UAP admission or
upstream CPython acceptance.

## Boundary

```text
SOURCE_PIN → TYPED_DECODE → PACAPDG_SOURCE_GATE
                         → ADMIT_SOURCE_PLAN / HOLD_QUNO / REJECT
                         → HUMAN_REVIEW_REQUIRED
```

Every result has `uap=UNJUDGED`, `external_effect=False`,
`cpython_upstream_requested=False`,
`cpython_upstream_accepted=False`, and
`review_authenticity_verified=False`.

The checked `SourcePlanGate` Protocol is an interface contract,
**not** an external connector or authority capability.

## Reproduction

```bash
python Tools/sigil4cpython/test_pypl_typed_interface_v1.py
python Tools/sigil4cpython/test_pypl_integration_request_v1.py
python Tools/sigil4cpython/pypl_integration_request_v1.py \
  Tools/sigil4cpython/fixtures/pypl_sym_request_v1.json --root .
```

The request fixture deliberately leaves four review/test references
unresolved. Expected verdict: `HOLD_QUNO`.

Invariants: `PI_FIXED`, `SAFE_REPLAY_SOURCE_ONLY`,
`NO_COERCION`, `NO_IDENTITY_TRANSPORT`, `NO_AUTHORITY_TRANSPORT`,
`TRACE_PRESERVED`, `QUNO_VISIBLE`.

No CPython internals, interpreter modifications, actual UAP admission,
device execution, proof certification or upstream submission.

**PIORNALEGO ES CANON.**
