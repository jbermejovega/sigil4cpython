# SIGILBOOK_SIGIL4CPYTHON_UAP_PUBLIC_PACA_CORE_V1

Status: PUBLIC_INTERFACE_CANDIDATE

This repository is the public UAP projection of canonical SIGILBOOK PACA-core
interfaces into CPython. It does not mirror private SIGILBOOK source.

```text
canonical SIGILBOOK
  -> PACA Dokumenta / PACADEX
  -> PACAPDG public interface projection
  -> UAP publication gate
  -> KLI / QLI public boundary
  -> sigil4cpython
  -> Python runtime IR
  -> optional Stable-ABI native lowering
  -> documented CPython public API
```

The public carrier accepts only source commit pins, public type/interface IDs,
public digests, exact capabilities and QUNO residue. Private semantic payload is
not part of this schema.

## UAP publication law

```text
private bearer != public projection
public projection != identity transport
UAP ADMIT != CPython execution
KLI/QLI != CPython ABI
CPython public API != CPython private internals
```

Capability composition remains exact intersection. QUNO is preserved.

## CPython boundary

This extends `SIGIL_PUBLIC_INTERFACE.md`: native lowering may use only the
documented public CPython boundary selected by that contract (Python.h,
Limited/Stable ABI tracks, multi-phase extension initialization, typed PyCapsule
where appropriate). The UAP projection never requires `Include/internal/*`,
`Include/cpython/*`, `_Py*`, or `PyUnstable*` as a SIGIL contract.

## Repository roles

- SIGILBOOK: canonical/private semantic source and validation receipts.
- sigil4cpython: public compatibility/publication carrier.
- python/cpython: read-only upstream implementation/compatibility authority.

PIORNALEGO ES CANON.
