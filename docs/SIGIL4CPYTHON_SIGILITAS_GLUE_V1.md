# SIGIL4CPYTHON SIGILITAS Virtual RPM Glue V1

Status: FINAL_VERSIONED_GLUE_CONTRACT  
Version: 1.0.0  
Repository: jbermejovega/sigil4cpython

This document defines the CPython-facing glue contract for SIGIL plural-typed and
QUNO-typed matrix protocol projections into the SIGILITAS virtual package/runtime
surfaces:

SIGIL → Plural → QUNO → MatrixProtocol → SynthGitHub/Fediverse

The final boundary is:

SIGILITAS.VirtualRPM → Virtual.PACADEX → PACA.Terminal

## Meaning of “final”

“Final” applies to this versioned glue contract and its manifest. It does not
claim that a wheel, CPython build, free-threaded audit, or external publication
has passed. Those are independent evidence gates. A release claim is withheld
until the gates in the manifest have matching artifacts and deterministic receipts.

## Type and identity law

- SIGIL is the native CPython-facing carrier.
- Plural and QUNO are relational type carriers; their facets remain explicit in serialized envelopes.
- MatrixProtocol is a versioned boundary envelope, not a type erasure layer.
- SynthGitHub and Fediverse are external projections with provenance edges. They must never be treated as the same identity as a native SIGIL object.
- Virtual RPM resolves package/runtime plans. It does not grant execution or publication authority.
- PACADEX and PACA Terminal may inspect, validate, encode, decode, and prepare a plan; transport requires a separate consent gate.

## Minimum envelope

~~~
{
  "schema": "SIGIL_MATRIX_PROTOCOL_V1",
  "trace_id": "trace:<stable-id>",
  "native_type": "SIGIL",
  "relational_facets": ["Plural", "QUNO"],
  "projection": "SynthGitHub",
  "target_surface": "SIGILITAS.VirtualRPM",
  "provenance": {"source_commit": "<immutable-sha>"},
  "authority": "plan_only",
  "safe_replay": true
}
~~~

A Fediverse projection uses the same envelope with projection set to Fediverse;
it is a distinct typed projection, not a transport instruction.

## Gates

1. Validate the manifest and envelope schema.
2. Run ordinary CPython tests.
3. Run the free-threaded/interpreter-isolation audit separately.
4. Verify stable PDG/SIGIL serialization round trips.
5. Recompute the receipt from normalized inputs.
6. Only then consider a wheel/sdist or external publication.

Corrections require a successor version; immutable artifacts are never rewritten.
