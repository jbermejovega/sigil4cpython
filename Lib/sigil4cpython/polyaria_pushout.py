"""Finite, inert public-interface pushout for POLYARIA and SIGIL4CPython.

This computes a pushout of *finite sets of public port names* under an
explicit witnessed span.  It is not a pushout in arbitrary categories and
neither transports identities nor executes CPython, OSC, or MIDI.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
from math import isfinite

SCHEMA_ID = "SIGIL4CPYTHON_POLYARIA_PUBLIC_PUSHOUT_V1"
SOURCE_REPOSITORY = "jbermejovega/sigilbook"
TARGET_REPOSITORY = "jbermejovega/sigil4cpython"


class Verdict(str, Enum):
    ADMIT = "ADMIT_SOURCE_PLAN"
    HOLD = "HOLD_QUNO"
    REJECT = "REJECT"


@dataclass(frozen=True, slots=True)
class PublicPort:
    port_id: str
    interface_id: str
    occurrence_id: str
    capabilities: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PublicSection:
    section_id: str
    context_id: str
    pi_ref: str
    ports: tuple[PublicPort, ...]


@dataclass(frozen=True, slots=True)
class BoundaryWitness:
    common_port_id: str
    left_port_id: str
    right_port_id: str
    witness_id: str
    trace_ref: str
    compatible: bool = True
    pi_fixed: bool = True
    no_identity_transport: bool = True


@dataclass(frozen=True, slots=True)
class PublicSpan:
    common: PublicSection
    left: PublicSection
    right: PublicSection
    witnesses: tuple[BoundaryWitness, ...]
    no_authority_transport: bool = True
    no_coercion: bool = True
    safe_replay: bool = True
    trace_preserved: bool = True
    private_source_payload_included: bool = False
    cpython_semantics_changed: bool = False
    runtime_executed: bool = False


@dataclass(frozen=True, slots=True)
class PushoutClass:
    class_id: str
    members: tuple[str, ...]
    occurrence_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PushoutPlan:
    schema_id: str
    verdict: Verdict
    classes: tuple[PushoutClass, ...]
    errors: tuple[str, ...]
    quno: tuple[str, ...]
    digest: str


@dataclass(frozen=True, slots=True)
class PolyariaEvent:
    source: str
    epoch: int
    occurrence: str
    operator: str
    ultraviolet: float
    witness_id: str
    trace_ref: str


@dataclass(frozen=True, slots=True)
class EventPlan:
    verdict: Verdict
    event_key: tuple[str, int, str]
    semantic_actions: tuple[str, ...]
    reasons: tuple[str, ...]


OPERATOR_ACTIONS = {
    "NAMO": ("descending_motif", "closure"),
    "TAE": ("melodic_incidence", "pitch_relation"),
    "REKOKO": ("epoch_transformation", "fresh_occurrence"),
    "SIGILA": ("plural_chord", "opening"),
}


def _digest(data: dict[str, object]) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return sha256(payload.encode("utf-8")).hexdigest()


def compile_public_pushout(span: PublicSpan) -> PushoutPlan:
    """Compute a finite Set pushout; retain both occurrence refs per class.

    An ADMIT verdict only admits an inert source plan.  External witness
    authenticity and universal properties in other categories remain unproved.
    """
    errors: list[str] = []
    quno: list[str] = []
    sections = (span.common, span.left, span.right)
    if len({section.section_id for section in sections}) != 3:
        errors.append("section_identity_collapse")
    if not span.common.pi_ref or any(s.pi_ref != span.common.pi_ref for s in sections):
        errors.append("protected_pi_mismatch")
    for section in sections:
        if not section.section_id or not section.context_id:
            errors.append("missing_section_identity_or_context")
        ids = [port.port_id for port in section.ports]
        if len(ids) != len(set(ids)) or not all(ids):
            errors.append(f"invalid_port_ids:{section.section_id}")
        for port in section.ports:
            if not port.interface_id or not port.occurrence_id:
                errors.append(f"missing_public_port_metadata:{section.section_id}:{port.port_id}")
            if not port.capabilities or len(set(port.capabilities)) != len(port.capabilities):
                errors.append(f"invalid_capabilities:{section.section_id}:{port.port_id}")
    if not all((span.no_authority_transport, span.no_coercion, span.safe_replay,
                span.trace_preserved)):
        errors.append("public_invariants_broken")
    if any((span.private_source_payload_included, span.cpython_semantics_changed,
            span.runtime_executed)):
        errors.append("forbidden_public_or_runtime_effect")

    common = {p.port_id: p for p in span.common.ports}
    left = {p.port_id: p for p in span.left.ports}
    right = {p.port_id: p for p in span.right.ports}
    referenced: set[str] = set()
    used_left: set[str] = set()
    used_right: set[str] = set()
    valid_edges: list[tuple[str, str]] = []
    for edge in span.witnesses:
        if edge.common_port_id in referenced:
            errors.append(f"duplicated_boundary:{edge.common_port_id}")
        referenced.add(edge.common_port_id)
        if edge.left_port_id in used_left or edge.right_port_id in used_right:
            errors.append(f"non_injective_leg:{edge.common_port_id}")
        used_left.add(edge.left_port_id)
        used_right.add(edge.right_port_id)
        if (edge.common_port_id not in common or edge.left_port_id not in left
                or edge.right_port_id not in right):
            errors.append(f"unknown_boundary_port:{edge.common_port_id}")
            continue
        c = common[edge.common_port_id]
        l = left[edge.left_port_id]
        r = right[edge.right_port_id]
        if c.interface_id != l.interface_id or c.interface_id != r.interface_id:
            errors.append(f"interface_type_mismatch:{edge.common_port_id}")
        if not set(c.capabilities).issubset(set(l.capabilities) & set(r.capabilities)):
            errors.append(f"capability_intersection_failure:{edge.common_port_id}")
        if l.occurrence_id == r.occurrence_id:
            errors.append(f"occurrence_identity_collapse:{edge.common_port_id}")
        if not edge.compatible or not edge.pi_fixed or not edge.no_identity_transport:
            errors.append(f"invalid_boundary_witness:{edge.common_port_id}")
        if not edge.witness_id or not edge.trace_ref:
            quno.append(f"missing_witness_or_trace:{edge.common_port_id}")
        if (c.interface_id == l.interface_id == r.interface_id
                and edge.compatible and edge.pi_fixed and edge.no_identity_transport
                and edge.witness_id and edge.trace_ref):
            valid_edges.append((f"L:{edge.left_port_id}", f"R:{edge.right_port_id}"))
    for missing in sorted(common.keys() - referenced):
        quno.append(f"missing_boundary:{missing}")

    # Complete, valid spans only: avoid presenting partial quotients as admitted.
    classes: tuple[PushoutClass, ...] = ()
    if not errors and not quno:
        parent = {f"{side}:{p.port_id}": f"{side}:{p.port_id}"
                  for side, ports in (("L", left.values()), ("R", right.values()))
                  for p in ports}

        def root(key: str) -> str:
            while parent[key] != key:
                key = parent[key]
            return key

        for a, b in valid_edges:
            ra, rb = root(a), root(b)
            if ra != rb:
                parent[max(ra, rb)] = min(ra, rb)
        groups: dict[str, list[str]] = {}
        for member in sorted(parent):
            groups.setdefault(root(member), []).append(member)
        all_ports = {**{f"L:{k}": v for k, v in left.items()},
                     **{f"R:{k}": v for k, v in right.items()}}
        classes = tuple(PushoutClass(
            class_id=f"PO:{index:04d}",
            members=tuple(members),
            occurrence_refs=tuple(all_ports[m].occurrence_id for m in members),
        ) for index, members in enumerate(sorted(groups.values()), 1))

    verdict = Verdict.REJECT if errors else Verdict.HOLD if quno else Verdict.ADMIT
    body = {
        "schema_id": SCHEMA_ID,
        "verdict": verdict.value,
        "classes": [asdict(c) for c in classes],
        "errors": sorted(set(errors)),
        "quno": sorted(set(quno)),
    }
    return PushoutPlan(SCHEMA_ID, verdict, classes, tuple(body["errors"]),
                       tuple(body["quno"]), _digest(body))


def plan_polyaria_event(
    event: PolyariaEvent,
    pushout: PushoutPlan,
    seen_occurrences: frozenset[tuple[str, int, str]] = frozenset(),
) -> EventPlan:
    """Admit a semantic event plan without output, IO, or ledger mutation."""
    key = (event.source, event.epoch, event.occurrence)
    errors = []
    quno = []
    if pushout.schema_id != SCHEMA_ID or pushout.verdict is not Verdict.ADMIT:
        quno.append("pushout_not_admitted")
    if not event.source or not event.occurrence or not event.trace_ref:
        quno.append("missing_event_provenance")
    if not event.witness_id:
        quno.append("missing_event_witness")
    if type(event.epoch) is not int or event.epoch < 0:
        errors.append("invalid_epoch")
    if event.operator not in OPERATOR_ACTIONS:
        errors.append("unknown_operator")
    if (type(event.ultraviolet) not in (int, float)
            or not isfinite(event.ultraviolet)
            or not 0 <= event.ultraviolet <= 1):
        errors.append("invalid_ultravioleta_modulation")
    if key in seen_occurrences:
        errors.append("duplicate_occurrence_replay")
    verdict = Verdict.REJECT if errors else Verdict.HOLD if quno else Verdict.ADMIT
    return EventPlan(verdict, key,
                     OPERATOR_ACTIONS[event.operator] if verdict is Verdict.ADMIT else (),
                     tuple(sorted(set(errors + quno))))
