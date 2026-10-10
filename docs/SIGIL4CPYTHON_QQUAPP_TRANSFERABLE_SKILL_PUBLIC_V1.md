# SIGIL4CPython QQUAPP Transferable Skill — Public Projection V1

**Public schema:** `SIGIL_QQUAPP_TRANSFERABLE_SKILL_PULL_PUSH_V1`
**Root reference:** `SIGILBOOK_TOTAL_VOID_AST_OF_ALL_ASTS_V1`
**Source:** `jbermejovega/sigilbook` branch `feat/qquapp-transferable-skill-pull-push-v1-20261010`, source PR #3745.
**Authorial concept:** Jara Juana Bermejo Vega; AI-assisted public source projection.
**Authority:** public SIGIL4CPython tools, NOT CPython upstream and NOT a change to interpreter semantics.

## Minimal portable interface

The public copy lives exclusively in `Tools/sigil4cpython/` and uses ordinary Python, not private CPython internals. The finite **Set** operations are pure; `scikit-learn` is imported only when an explicit in-memory learning session is created.

```sh
python Tools/sigil4cpython/qquapp_skill_cli_v1.py demo
python Tools/sigil4cpython/qquapp_skill_cli_v1.py demo --learn
python Tools/sigil4cpython/test_qquapp_transferable_skill_v1.py
```

Optional `--learn` requires installation of `scikit-learn` and `numpy` into the caller's permitted environment. The default demo uses no ML and no external I/O beyond printed JSON. No serialized model files, networking, Git commands, subprocess-mediated action or device output.

## Pull and push

For typed finite sets with total functions `f:A→C` and `g:B→C`, `pullback_set` computes `A×_C B`. With `i:C→A` and `j:C→B`, `pushout_set` computes the quotient of disjoint tagged union `A+B` by the identifications induced by `C`. `factor_pushout` tests the unique induced factor for a supplied commuting Set-cocone. These definitions follow [nLab pullback](https://ncatlab.org/nlab/show/pullback) and [nLab pushout](https://ncatlab.org/nlab/show/pushout).

### QQUAPP guards

- Each port has a distinct occurrence ID; a quotient class retains the original tagged source carriers.
- Exact ordered feature names, class vocabulary and semantic type must match; no implicit retyping.
- Explicit witness references gate source-plan admission. A reference alone is not independently verified permission.
- Capabilities compose by intersection. Unsupported learning context returns `HOLD_QUNO`.
- `transferable_skill` does not copy weights. Learning transfer outside matched schema is NOT automatically valid.
- `StandardScaler` preparation is frozen before `SGDClassifier.partial_fit`, avoiding a silent feature-coordinate change; predictions remain advisory.
- `UAP=UNJUDGED`, `external_effect=false`, `cpython_upstream_requested=false`.

### Operational note

`PULL`/`PUSH` are categorical operations, not Git or QQUAPP cloud sync commands. This project does not submit code to `python/cpython`. A separate GitHub PR and author/reviewer consent are required for repo integration; a model decision must be independently admitted by the application.

## Testing and release boundary

23 focused tests passed on the standalone local source/projection in the drafting environment; Git SHA readback confirms published executable files match those tested. These tests do not cover the full CPython build matrix, long-running incremental learning, cross-domain generalization, human-review authenticity, or upstream compatibility certification. No release tag or package index upload.

**PIORNALEGO ES CANON** · `NO_COERCION` · `PI_FIXED` · `SAFE_REPLAY` · `TRACE_PRESERVED` · `NO_IDENTITY_TRANSPORT` · `NO_AUTHORITY_TRANSPORT`.
