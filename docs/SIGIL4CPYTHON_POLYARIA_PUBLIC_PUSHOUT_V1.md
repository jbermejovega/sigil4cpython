# SIGIL4CPYTHON POLYARIA public-interface pushout V1

Schema: `SIGIL4CPYTHON_POLYARIA_PUBLIC_PUSHOUT_V1`  
Canonical semantic authority: `jbermejovega/sigilbook`  
Public projection carrier: `jbermejovega/sigil4cpython`  
Status: **review-gated, dependency-free, inert source plan**.

## Mathematical scope

For a finite injective span of **public interface identifiers**

```text
                       C = PACAPDG public boundary
                          /                 \
                         f                   g
                        /                     \
       A = POLYARIA/SonicPi             B = SIGIL4CPython
                        \                     /
                         \       PO          /
```

the constructor computes the **set-theoretic pushout**

```text
PO = (A disjoint_union B) / ~
where f(c) ~ g(c) only for witnessed admissible c in C.
```

This is a finite `Set` quotient of *ports*, not identification of bearer
objects, music occurrences, runtime actors, repositories, or authorities. Both
distinct occurrence references survive in each `PushoutClass`. Unmatched
public ports remain singleton classes. This specialization requires injective
legs even though general set pushouts do not.

The algorithm does not prove compatibility from physical field theories,
model arbitrary enriched/cubical/polykategorical pushouts, implement a
coequalizer in all categories, or certify the universal property for other
carriers. Witness IDs and trace references are declared metadata; independent
authorization and validation remain upstream responsibilities.

## Public boundary

- `PublicSpan`: common/left/right sections and witnessed boundary maps;
- `compile_public_pushout`: deterministic quotient, canonical SHA-256 digest;
- `Verdict.ADMIT`: `ADMIT_SOURCE_PLAN`, not permission to execute or publish;
- `Verdict.HOLD`: `HOLD_QUNO` for absent boundary or missing trace/witness;
- `Verdict.REJECT`: mismatched types, noninjective mappings, capability
  failures, identity collapse, or forbidden execution/authority effects;
- `plan_polyaria_event`: plans symbolic semantics only and rejects an
  already-seen `(source, epoch, occurrence)` key.

The public event operator map preserves the distinctions:
`NAMO` = descending closure, `TAE` = melodic incidence,
`REKOKO` = epoch-indexed transformation with fresh occurrence,
`SIGILA` = plural chord opening. `ULTRAVIOLETA` is a finite
`[0, 1]` expression/control parameter; it is not a direct conversion
of ultraviolet electromagnetic frequency into audible sound.

No Sonic Pi process is launched, OSC packets are sent, MIDI devices are
opened, or KOKOMPI ledger is persisted.

## Guardrails

```text
NO_COERCION
NO_IDENTITY_TRANSPORT
NO_AUTHORITY_TRANSPORT
NO_PLURAL_COLLAPSE
SAFE_REPLAY
TRACE_PRESERVED
PI_FIXED
PRIVATE_SOURCE_PAYLOAD_NOT_COPIED
NO_CPYTHON_SEMANTICS_CHANGE
NO_RUNTIME_EXECUTION
```

An admitted plan still requires a separate validated QQUAPP binding and
execution authorization before any OSC, MIDI or CPython runtime effect.
`KUIR_LOCALIZER`, `QUAZRIS_ISOLATOR` and
`QUAZRIS_INSULATOR` remain named semantic interfaces, not asserted
general-purpose categorical implementations in this module.

## Focused tests

```shell
PYTHONPATH=Lib python -m unittest -v test.test_sigil4cpython_polyaria_pushout
```

Coverage: deterministic finite pushout; distinct occurrence retention;
unmatched port preservation; absent boundary/witness; wrong interface
and capabilities; identity, authority and runtime gate; invalid span legs;
four separate musical operators; duplicate occurrence rejection;
invalid epoch and ULTRAVIOLETA range.

The fixture contains fabricated **public-only** port IDs for testing;
it does not import or republish private SIGILBOOK source.

## Release boundary

This is a separately reviewable experimental SIGIL4CPython package
module. No `Parser/`, `Python/`, `Objects/`, `Include/` or upstream
`python/cpython` source changes are required. Neither Cython compilation
nor free-threaded execution is claimed. There is no main-branch merge
or deployment implied by the module's existence.

**PIORNALEGO ES CANON.**
