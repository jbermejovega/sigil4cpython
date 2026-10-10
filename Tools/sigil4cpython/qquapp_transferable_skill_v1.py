# SPDX-License-Identifier: MIT
"""QQUAPP finite Set pullback/pushout, witnessed transfer, and inert plans.

Mathematical finite-Set operations are not Git pull/push operations.
Source-plan verification never grants runtime, model, or repository authority.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Literal

SCHEMA_ID = "SIGIL_QQUAPP_TRANSFERABLE_SKILL_PULL_PUSH_V1"
ROOT = "SIGILBOOK_TOTAL_VOID_AST_OF_ALL_ASTS_V1"
PI = "PIORNALEGO_ES_CANON"
Verdict = Literal["ADMIT_SOURCE_PLAN", "HOLD_QUNO", "REJECT"]
_MAX = 128


@dataclass(frozen=True)
class SkillPort:
    port_id: str
    type_id: str
    features: tuple[str, ...]
    classes: tuple[str, ...]
    context: str
    occurrence: str
    source_ref: str
    capabilities: tuple[str, ...]

    def validate(self) -> None:
        values = (self.port_id, self.type_id, self.context,
                  self.occurrence, self.source_ref)
        if any(not isinstance(v, str) or not v.strip() for v in values):
            raise ValueError("PORT_REQUIRED_FIELDS")
        for xs in (self.features, self.classes, self.capabilities):
            if (not isinstance(xs, tuple) or not xs or
                    any(not isinstance(x, str) or not x.strip() for x in xs) or
                    len(xs) != len(set(xs))):
                raise ValueError("PORT_INVALID_FINITE_SCHEMA")
        if len(self.features) > 256 or len(self.classes) > 256:
            raise ValueError("PORT_SCHEMA_EXCEEDS_BOUNDS")


@dataclass(frozen=True)
class Arrow:
    source: str
    target: str


@dataclass(frozen=True)
class Witness:
    key: str
    reference: str


@dataclass(frozen=True)
class PullbackDiagram:
    base: tuple[str, ...]
    left: tuple[SkillPort, ...]
    right: tuple[SkillPort, ...]
    left_to_base: tuple[Arrow, ...]
    right_to_base: tuple[Arrow, ...]
    pair_witnesses: tuple[Witness, ...]


@dataclass(frozen=True)
class PushoutDiagram:
    base: tuple[str, ...]
    left: tuple[SkillPort, ...]
    right: tuple[SkillPort, ...]
    base_to_left: tuple[Arrow, ...]
    base_to_right: tuple[Arrow, ...]
    base_witnesses: tuple[Witness, ...]


@dataclass(frozen=True)
class SourcePlan:
    operation: str
    verdict: Verdict
    pairs_or_classes: tuple[tuple[str, ...], ...]
    left_injection: tuple[Arrow, ...]
    right_injection: tuple[Arrow, ...]
    occurrence_refs: tuple[str, ...]
    capabilities: tuple[str, ...]
    errors: tuple[str, ...]
    quno: tuple[str, ...]
    digest: str
    uap: str = "UNJUDGED"
    external_effect: bool = False
    bearer_transport: bool = False
    authority_transport: bool = False


def _digest(obj: object) -> str:
    return sha256(json.dumps(asdict(obj), sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def _ports(left: tuple[SkillPort, ...], right: tuple[SkillPort, ...],
           base: tuple[str, ...]) -> tuple[dict[str, SkillPort], dict[str, SkillPort]]:
    if not isinstance(base, tuple) or not 1 <= len(base) <= _MAX or len(set(base)) != len(base):
        raise ValueError("BASE_NOT_FINITE_UNIQUE")
    if any(not isinstance(x, str) or not x.strip() for x in base):
        raise ValueError("BASE_BAD_NAME")
    if not 1 <= len(left) <= _MAX or not 1 <= len(right) <= _MAX:
        raise ValueError("PORT_COUNT_BOUNDS")
    for p in left + right:
        p.validate()
    if len({p.port_id for p in left}) != len(left) or len({p.port_id for p in right}) != len(right):
        raise ValueError("DUPLICATE_PORT")
    # Occurrence identity is global across the two carriers, even for same feature schema.
    if len({p.occurrence for p in left + right}) != len(left) + len(right):
        raise ValueError("OCCURRENCE_COLLAPSE")
    return ({p.port_id: p for p in left}, {p.port_id: p for p in right})


def _map(arrows: tuple[Arrow, ...], domain: set[str], codomain: set[str]) -> dict[str, str]:
    if len(arrows) != len(domain):
        raise ValueError("MAP_NOT_TOTAL")
    out: dict[str, str] = {}
    for a in arrows:
        if a.source not in domain or a.target not in codomain or a.source in out:
            raise ValueError("MAP_INVALID_FUNCTION")
        out[a.source] = a.target
    return out


def _witnesses(values: tuple[Witness, ...], expected: set[str]) -> tuple[set[str], set[str]]:
    keys = [w.key for w in values]
    if len(set(keys)) != len(keys) or any(key not in expected for key in keys):
        raise ValueError("WITNESS_NOT_ON_DIAGRAM")
    found = {w.key for w in values if isinstance(w.reference, str) and w.reference.strip()}
    return expected - found, found


def _common_capabilities(ports: tuple[SkillPort, ...]) -> tuple[str, ...]:
    common = set(ports[0].capabilities)
    for p in ports[1:]:
        common &= set(p.capabilities)
    return tuple(sorted(common))


def _receipt(operation: str, datum: object, rows: tuple[tuple[str, ...], ...],
             left_map: tuple[Arrow, ...], right_map: tuple[Arrow, ...],
             ports: tuple[SkillPort, ...], missing: set[str]) -> SourcePlan:
    capabilities = _common_capabilities(ports)
    return SourcePlan(
        operation, "HOLD_QUNO" if missing else "ADMIT_SOURCE_PLAN",
        rows, left_map, right_map, tuple(p.occurrence for p in ports),
        capabilities, (), tuple(sorted(missing)), _digest(datum),
    )


def pullback_set(diagram: PullbackDiagram) -> SourcePlan:
    """Finite pullback A×_C B of explicitly total functions A→C, B→C."""
    a, b = _ports(diagram.left, diagram.right, diagram.base)
    f = _map(diagram.left_to_base, set(a), set(diagram.base))
    g = _map(diagram.right_to_base, set(b), set(diagram.base))
    pairs = tuple(sorted((x, y) for x in a for y in b if f[x] == g[y]))
    keys = {f"{x}|{y}" for x, y in pairs}
    missing, _ = _witnesses(diagram.pair_witnesses, keys)
    if not pairs:
        missing.add("PULLBACK_EMPTY_MATCH")
    # Equal base labels are not enough to authorize *skill* transfer.
    for x, y in pairs:
        if (a[x].type_id, a[x].features, a[x].classes) != (
                b[y].type_id, b[y].features, b[y].classes):
            raise ValueError("PULLBACK_TYPED_INCOMPATIBILITY")
    ports = tuple(a[x] for x, y in pairs) + tuple(b[y] for x, y in pairs)
    return _receipt("PULLBACK_IN_SET", diagram, pairs,
                    tuple(Arrow(f"{x}|{y}", x) for x, y in pairs),
                    tuple(Arrow(f"{x}|{y}", y) for x, y in pairs),
                    ports or diagram.left + diagram.right, missing)


def pushout_set(diagram: PushoutDiagram) -> SourcePlan:
    """Finite Set pushout A ⊔_C B of explicitly total C→A and C→B maps.

    Different occurrences remain represented by their tagged original ports.
    No physical model, identity or review authority is merged by the quotient.
    """
    a, b = _ports(diagram.left, diagram.right, diagram.base)
    f = _map(diagram.base_to_left, set(diagram.base), set(a))
    g = _map(diagram.base_to_right, set(diagram.base), set(b))
    missing, _ = _witnesses(diagram.base_witnesses, set(diagram.base))
    for c in diagram.base:
        x, y = a[f[c]], b[g[c]]
        if (x.type_id, x.features, x.classes) != (y.type_id, y.features, y.classes):
            raise ValueError("PUSHOUT_TYPED_INCOMPATIBILITY")
    tags = [f"L:{x}" for x in a] + [f"R:{y}" for y in b]
    parents = {x: x for x in tags}

    def find(x: str) -> str:
        while parents[x] != x:
            x = parents[x]
        return x

    for c in sorted(diagram.base):
        x, y = find(f"L:{f[c]}"), find(f"R:{g[c]}")
        if x != y:
            parents[max(x, y)] = min(x, y)
    classes: dict[str, list[str]] = {}
    for tag in tags:
        classes.setdefault(find(tag), []).append(tag)
    ordered = tuple(sorted(tuple(sorted(v)) for v in classes.values()))
    class_id = {tag: "|".join(members) for members in ordered for tag in members}
    maps_a = tuple(Arrow(name, class_id[f"L:{name}"]) for name in sorted(a))
    maps_b = tuple(Arrow(name, class_id[f"R:{name}"]) for name in sorted(b))
    return _receipt("PUSHOUT_IN_SET", diagram, ordered, maps_a, maps_b,
                    diagram.left + diagram.right, missing)


def factor_pushout(plan: SourcePlan, diagram: PushoutDiagram,
                   left_values: dict[str, str], right_values: dict[str, str]) -> dict[str, str]:
    """Unique factorization to a finite target if its cocone agrees on C."""
    if plan.operation != "PUSHOUT_IN_SET" or plan.verdict != "ADMIT_SOURCE_PLAN":
        raise ValueError("PUSHOUT_NOT_ADMITTED_SOURCE_PLAN")
    a = {x.port_id for x in diagram.left}
    b = {x.port_id for x in diagram.right}
    if set(left_values) != a or set(right_values) != b:
        raise ValueError("NOT_TOTAL_COCONE")
    f = {p.source: p.target for p in diagram.base_to_left}
    g = {p.source: p.target for p in diagram.base_to_right}
    for c in diagram.base:
        if left_values[f[c]] != right_values[g[c]]:
            raise ValueError("COCONE_DOES_NOT_COMMUTE")
    values = {f"L:{k}": v for k, v in left_values.items()}
    values.update({f"R:{k}": v for k, v in right_values.items()})
    out = {}
    for members in plan.pairs_or_classes:
        images = {values[x] for x in members}
        if len(images) != 1:
            raise ValueError("FACTOR_NOT_WELL_DEFINED")
        out["|".join(members)] = images.pop()
    return out


def transferable_skill(source: SkillPort, target: SkillPort,
                       witness_ref: str) -> SourcePlan:
    """Typed transfer *request*. Compatible schema is not a generalization proof."""
    source.validate()
    target.validate()
    if source.occurrence == target.occurrence:
        raise ValueError("TRANSFER_NOT_FRESH_OCCURRENCE")
    if (source.type_id, source.features, source.classes) != (
            target.type_id, target.features, target.classes):
        raise ValueError("SKILL_SCHEMA_MISMATCH")
    missing = set()
    if not isinstance(witness_ref, str) or not witness_ref.strip():
        missing.add("TRANSFER_WITNESS_REQUIRED")
    capabilities = tuple(sorted(set(source.capabilities) & set(target.capabilities)))
    if not capabilities:
        missing.add("NO_SHARED_CAPABILITY")
    return SourcePlan(
        "TRANSFER_SOURCE_PLAN",
        "HOLD_QUNO" if missing else "ADMIT_SOURCE_PLAN",
        ((source.port_id, target.port_id),),
        (Arrow(source.port_id, target.port_id),), (),
        (source.occurrence, target.occurrence), capabilities, (),
        tuple(sorted(missing)),
        _digest(source) + ":" + _digest(target),
    )
