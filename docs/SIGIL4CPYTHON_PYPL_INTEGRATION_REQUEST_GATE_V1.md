# SIGIL4CPython PYPL Integration Request Gate V1

**Contract:** `SIGIL4CPYTHON_PYPL_INTEGRATION_REQUEST_V1`  
**Implementation:** `Tools/sigil4cpython/pypl_integration_request_v1.py`  
**Public port:** `Tools/sigil4cpython/paca_sym_game_v1.py`  
**Origin:** `jbermejovega/sigilbook`, `feat/sym-typed-paca-game-v1-20261008`, commit `40b809720b797054864f6d2054fd8397fde3b2e6`.  
**Target base:** `jbermejovega/sigil4cpython` main at `974d7e06ea31d369c3e97defd8054588eccc3e88`.  
**Designation:** source-only public projection, not a CPython interpreter change.

## 1. PYPL is a SIGIL project profile, not PyPI or CPython approval

SIG4PYPL/PYPL denotes an internal compiled/parallel Python compatibility profile
as documented in `Tools/sigil/README.md`. The public SIGIL4CPython
repository is a reviewable carrier distinct from the private SIGILBOOK source
and from `python/cpython`, whose upstream maintainers own their admission
policy. Nothing in this pipeline writes to upstream or opens upstream PRs.

## 2. Stable request flow

```text
SOURCE_BIND (explicit SIGILBOOK source SHA)
  -> PUBLIC_PROJECTION (.sym AST + pure source-plan simulation)
  -> PIN TARGET BASE SHA (sigil4cpython)
  -> CHECK ALLOWLISTED FILES + SHA-256
  -> CHECK BOUNDARY FLAGS
  -> CHECK TEST / LICENSING / AUTHOR / MAINTAINER EVIDENCE REFS
  -> PACAPDG_SOURCE_VERDICT {REJECT | HOLD_QUNO | ADMIT_SOURCE_PLAN}
  -> HUMAN_REVIEW (external, never inferred from typed refs)
  -> DRAFT PR TO sigil4cpython
  -> OPTIONAL SEPARATE CPYTHON DESIGN/ISSUE/CLA/PR WORKFLOW
```

The independent public CPython workflow follows:
https://devguide.python.org/getting-started/pull-request-lifecycle/ and
https://devguide.python.org/contrib/project/generative-ai/ .
The contributor is responsible for understanding AI-assisted changes. CPython
contributions must respect its tests, policy, contribution agreement and
upstream maintainers' decisions. A public repo's approval is not upstream
acceptance.

## 3. Public artifacts

- `paca_sym_game_v1.py`: explicit grammar, immutable typed states, pure step
  transition, distinct event keys, provenance ledger, QUNO and REJECT.
- `fixtures/namotae.sym`: small user-authorized symbolic demonstration;
  no private backend, person-specific data, secret, or runtime authority.
- `fixtures/paca_sym_game_v1.ebnf`: grammar declaration.
- `test_paca_sym_game_v1.py`: source-only behavior and negative tests.
- `pypl_integration_request_v1.py`: guarded request evaluation.
- `test_pypl_integration_request_v1.py`: source digest, path,
  boundary, duplication, replay/external-effects and CLI checks.
- `fixtures/pypl_sym_request_v1.json`: digest-pinned **request candidate**
  with missing reviews explicitly left blank.

The source project branch may be private. Its source title, branch, and SHA
are provenance pointers; no other private files or private Git credentials
are projected into this public carrier.

## 4. Reproducible local commands

From the root of a local `sigil4cpython` checkout:

```bash
python Tools/sigil4cpython/test_paca_sym_game_v1.py
python Tools/sigil4cpython/test_pypl_integration_request_v1.py
python Tools/sigil4cpython/pypl_integration_request_v1.py \
  Tools/sigil4cpython/fixtures/pypl_sym_request_v1.json --root .
```

The included manifest intentionally has empty review/test evidence.
Therefore **the expected request verdict is `HOLD_QUNO`** until the
required evidence is actually generated and reviewed. Exit codes:
`0=ADMIT_SOURCE_PLAN` (only a reviewed *source proposal*),
`2=HOLD_QUNO`, `3=REJECT`. Only a human can decide whether the
request may be submitted or merged. The tool itself performs **no**
network, GitHub, CPython, gameplay, OSC, MIDI, or UAP effects.

When artifact bytes change, recalculate `sha256` fields before checking;
a mismatch is `REJECT`. Changing a file without updating the matching
review witness is not an admissible review shortcut. Verify the declared
source/target commits against GitHub separately: the local checker validates
their **shape**, not remote existence. Never present a hash as a proof of
copyright ownership or permission.

## 5. Admission and authority boundary

`ADMIT_SOURCE_PLAN` means that the *local structural request document*
is complete, with its source digest matching the local allowlisted files.
It **does not** mean the evidence references have been independently
authenticated. Result fields always report
`review_authenticity_verified=false`,
`source_pin_verified_remotely=false`,
`target_pin_verified_remotely=false`,
`cpython_upstream_requested=false`, `cpython_upstream_accepted=false`,
`uap=UNJUDGED` and `external_effect=false`.

A missing artifact, sha256 or review reference is `HOLD_QUNO`;
a dishonest/mismatching digest, forbidden path, duplicate artifact, wrong
repository or invalid declared boundary is `REJECT`. A pure source plan
does not establish a durable atomic replay guard or external action consent.

## 6. Licensing and compatibility

The new public-project-only helper files carry an MIT SPDX marker where
applicable, aligned with the origin project's stated root license. This is
**not** an assertion that all files in a CPython fork are MIT licensed or
that SIGIL code has been submitted under the Python Software Foundation
license. A human licensing review remains required before any upstream
proposal. No changes in `Python/`, `Objects/`, `Include/`,
`Modules/` or documented interpreter public interfaces are made here.

**Invariants:** `NO_COERCION`, `TRACE_PRESERVED`, `PI_FIXED`,
`SAFE_REPLAY` (source-only scope), `NO_IDENTITY_TRANSPORT`,
`NO_AUTHORITY_TRANSPORT`, `NO_PLURAL_COLLAPSE`,
`QUNO_VISIBLE`, `UPSTREAM_SEPARATE`.

**Evidence:** new source with authored focused tests; no hosted CI,
full CPython build, hardware test, mathematical certification,
human-reviewed licensing verdict, or upstream PR is claimed.

**PIORNALEGO ES CANON.**
