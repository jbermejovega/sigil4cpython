"""Primitive-typed QQUAPP ruleset/codebook projection for SIGIL4CPython.

This module is a dependency-free public governance and configuration carrier.
It does not mirror private SIGILBOOK payloads, mutate GitHub rulesets, patch the
CPython interpreter, or grant semantic authority to repository policy.

PYKARA carves a public typed factor.
KIRBY performs a witnessed presentation rewrite.
SWALLO/SWALLOW absorbs a compatible factor into a fresh public occurrence.
QQUAPP supplies the typed pull/tensor/push resource boundary.

KOKOMPI is a typed design pattern, not a person/agent identity. Every public
type carrier is PluralTyped, ResourceTyped, RelationTyped and QUNOTyped.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Iterable, Mapping

SCHEMA_ID = "SIGIL4CPYTHON_PRIMITIVE_TYPED_QQUAPP_RULESET_CODEBOOK_V1"
SOURCE_ROOT = "SIGILBOOK_TOTAL_VOID_AST_OF_ALL_ASTS_V1"
SOURCE_REPOSITORY = "jbermejovega/sigilbook"
PUBLIC_REPOSITORY = "jbermejovega/sigil4cpython"
UPSTREAM_REPOSITORY = "python/cpython"
PROTECTED_PI = "PIORNALEGO_ES_CANON"
PUBLICATION_CHECK = "Validate primitive typed publication codebook"


class EnforcementStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"


class RuleKind(str, Enum):
    RESTRICT_DELETIONS = "RESTRICT_DELETIONS"
    REQUIRE_LINEAR_HISTORY = "REQUIRE_LINEAR_HISTORY"
    REQUIRE_PULL_REQUEST = "REQUIRE_PULL_REQUEST"
    REQUIRE_STATUS_CHECKS = "REQUIRE_STATUS_CHECKS"
    BLOCK_FORCE_PUSHES = "BLOCK_FORCE_PUSHES"
    REQUIRE_SIGNED_COMMITS = "REQUIRE_SIGNED_COMMITS"
    REQUIRE_CODE_SCANNING = "REQUIRE_CODE_SCANNING"
    REQUIRE_CODE_QUALITY = "REQUIRE_CODE_QUALITY"
    RESTRICT_CODE_COVERAGE = "RESTRICT_CODE_COVERAGE"


class PatternStage(str, Enum):
    PYKARA_CARVE = "PYKARA_CARVE"
    KIRBY_REWRITE = "KIRBY_REWRITE"
    SWALLO_SWALLOW = "SWALLO_SWALLOW"
    QQUAPP_PULL_TENSOR_PUSH = "QQUAPP_PULL_TENSOR_PUSH"


@dataclass(frozen=True)
class PrimitiveTypedFacet:
    type_id: str
    quno: str
    replay_witness: str
    plural_typed: bool = True
    resource_typed: bool = True
    relation_typed: bool = True
    quno_typed: bool = True
    identity_transport: bool = False
    authority_transport: bool = False

    def validate(self) -> None:
        if not all((self.type_id, self.quno, self.replay_witness)):
            raise ValueError("INCOMPLETE_PRIMITIVE_TYPED_FACET")
        if not (
            self.plural_typed
            and self.resource_typed
            and self.relation_typed
            and self.quno_typed
        ):
            raise ValueError("ALL_PUBLIC_TYPES_MUST_BE_PLURAL_RESOURCE_RELATION_QUNO_TYPED")
        if self.identity_transport:
            raise ValueError("IDENTITY_TRANSPORT_FORBIDDEN")
        if self.authority_transport:
            raise ValueError("AUTHORITY_TRANSPORT_FORBIDDEN")


@dataclass(frozen=True)
class QQUAPPResource:
    resource_id: str
    facet: PrimitiveTypedFacet
    pull_witness: str
    tensor_witness: str
    push_witness: str
    krone_gate_witness: str
    capacity: int
    consumed: int = 0
    physical_execution: bool = False

    def validate(self) -> None:
        self.facet.validate()
        if not all(
            (
                self.resource_id,
                self.pull_witness,
                self.tensor_witness,
                self.push_witness,
                self.krone_gate_witness,
            )
        ):
            raise ValueError("INCOMPLETE_QQUAPP_RESOURCE")
        if self.capacity < 0 or self.consumed < 0 or self.consumed > self.capacity:
            raise ValueError("INVALID_QQUAPP_RESOURCE_BUDGET")
        if self.physical_execution:
            raise ValueError("RESOURCE_TYPE_IS_NOT_PHYSICAL_EXECUTION")


@dataclass(frozen=True)
class TypedRelation:
    relation_id: str
    facet: PrimitiveTypedFacet
    source_type_ids: tuple[str, ...]
    target_type_ids: tuple[str, ...]
    witness_id: str

    def validate(self) -> None:
        self.facet.validate()
        if not self.relation_id or not self.source_type_ids or not self.target_type_ids:
            raise ValueError("INCOMPLETE_TYPED_RELATION")
        if not self.witness_id:
            raise ValueError("RELATION_WITNESS_REQUIRED")


@dataclass(frozen=True)
class PublicCodebookEntry:
    facet: PrimitiveTypedFacet
    public_interface_id: str
    public_digest: str
    capabilities: tuple[str, ...]
    resource_ids: tuple[str, ...]
    relation_ids: tuple[str, ...]
    source_commit: str
    source_schema_id: str
    private_payload_embedded: bool = False
    cpython_private_api_required: bool = False

    def validate(self) -> None:
        self.facet.validate()
        if not all(
            (
                self.public_interface_id,
                self.public_digest,
                self.source_commit,
                self.source_schema_id,
            )
        ):
            raise ValueError("INCOMPLETE_PUBLIC_CODEBOOK_ENTRY")
        if len(self.capabilities) != len(set(self.capabilities)):
            raise ValueError("DUPLICATE_PUBLIC_CAPABILITY")
        if len(self.resource_ids) != len(set(self.resource_ids)):
            raise ValueError("DUPLICATE_PUBLIC_RESOURCE_REFERENCE")
        if len(self.relation_ids) != len(set(self.relation_ids)):
            raise ValueError("DUPLICATE_PUBLIC_RELATION_REFERENCE")
        if self.private_payload_embedded:
            raise ValueError("PRIVATE_SIGILBOOK_PAYLOAD_FORBIDDEN")
        if self.cpython_private_api_required:
            raise ValueError("CPYTHON_PRIVATE_API_FORBIDDEN")


@dataclass(frozen=True)
class KroneTypedGate:
    gate_id: str
    facet: PrimitiveTypedFacet
    input_type_ids: tuple[str, ...]
    resource_ids: tuple[str, ...]
    relation_ids: tuple[str, ...]
    required_capabilities: tuple[str, ...]
    witness_id: str

    def validate(self) -> None:
        self.facet.validate()
        if not all(
            (
                self.gate_id,
                self.input_type_ids,
                self.resource_ids,
                self.relation_ids,
                self.required_capabilities,
                self.witness_id,
            )
        ):
            raise ValueError("INCOMPLETE_KRONE_TYPED_GATE")


@dataclass(frozen=True)
class RulesetRule:
    kind: RuleKind
    parameters: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class GitHubRulesetProjection:
    ruleset_id: str
    facet: PrimitiveTypedFacet
    name: str
    desired_enforcement: EnforcementStatus
    target_branches: tuple[str, ...]
    rules: tuple[RulesetRule, ...]
    required_status_checks: tuple[str, ...]
    bypass_actors: tuple[str, ...] = ()
    observed_github_ruleset_id: int | None = None
    observed_active: bool = False
    repository_policy_is_semantic_authority: bool = False
    github_mutation_executed: bool = False

    def validate(self) -> None:
        self.facet.validate()
        if not self.ruleset_id or not self.name or not self.target_branches:
            raise ValueError("INCOMPLETE_RULESET_PROJECTION")
        kinds = tuple(rule.kind for rule in self.rules)
        if len(kinds) != len(set(kinds)):
            raise ValueError("DUPLICATE_RULESET_RULE_KIND")
        if RuleKind.REQUIRE_STATUS_CHECKS in kinds and not self.required_status_checks:
            raise ValueError("STATUS_CHECK_RULE_REQUIRES_CHECK_NAMES")
        if self.repository_policy_is_semantic_authority:
            raise ValueError("GITHUB_RULESET_CANNOT_BE_SEMANTIC_AUTHORITY")
        if self.github_mutation_executed:
            raise ValueError("SOURCE_PRIMITIVE_MUST_NOT_CLAIM_GITHUB_MUTATION")


@dataclass(frozen=True)
class KokompiDesignPattern:
    pattern_id: str
    facet: PrimitiveTypedFacet
    stages: tuple[PatternStage, ...]
    source_type_ids: tuple[str, ...]
    target_ruleset_id: str
    witness_ids: tuple[str, ...]
    kokompi_is_design_pattern: bool = True
    kokompi_is_person_identity: bool = False

    def validate(self) -> None:
        self.facet.validate()
        expected = (
            PatternStage.PYKARA_CARVE,
            PatternStage.KIRBY_REWRITE,
            PatternStage.SWALLO_SWALLOW,
            PatternStage.QQUAPP_PULL_TENSOR_PUSH,
        )
        if self.stages != expected:
            raise ValueError("KOKOMPI_PATTERN_STAGE_ORDER_DRIFT")
        if not self.source_type_ids or not self.target_ruleset_id or not self.witness_ids:
            raise ValueError("INCOMPLETE_KOKOMPI_DESIGN_PATTERN")
        if not self.kokompi_is_design_pattern or self.kokompi_is_person_identity:
            raise ValueError("KOKOMPI_MUST_REMAIN_DESIGN_PATTERN")


@dataclass(frozen=True)
class ConfigurationAxis:
    axis_id: str
    allowed_values: tuple[str, ...]
    default_value: str
    facet: PrimitiveTypedFacet

    def validate(self) -> None:
        self.facet.validate()
        if not self.axis_id or not self.allowed_values:
            raise ValueError("INCOMPLETE_CONFIGURATION_AXIS")
        if len(self.allowed_values) != len(set(self.allowed_values)):
            raise ValueError("DUPLICATE_CONFIGURATION_VALUE")
        if self.default_value not in self.allowed_values:
            raise ValueError("CONFIGURATION_DEFAULT_OUTSIDE_AXIS")


@dataclass(frozen=True)
class GuidedConfigurationSpace:
    config_space_id: str
    facet: PrimitiveTypedFacet
    axes: tuple[ConfigurationAxis, ...]
    krone_gate_id: str
    output_type_id: str
    source_only: bool = True
    runtime_executed: bool = False

    def validate(self) -> None:
        self.facet.validate()
        if not self.config_space_id or not self.axes or not self.krone_gate_id:
            raise ValueError("INCOMPLETE_GUIDED_CONFIGURATION_SPACE")
        ids = [axis.axis_id for axis in self.axes]
        if len(ids) != len(set(ids)):
            raise ValueError("DUPLICATE_CONFIGURATION_AXIS")
        for axis in self.axes:
            axis.validate()
        if not self.source_only or self.runtime_executed:
            raise ValueError("CONFIGURATION_SPACE_IS_SOURCE_ONLY")


@dataclass(frozen=True)
class ConfigurationOccurrence:
    config_space_id: str
    occurrence_id: str
    epoch: int
    selection: tuple[tuple[str, str], ...]
    digest: str
    native_lowering_requested: bool
    cpython_minimum: str


@dataclass(frozen=True)
class PublicationPrimitive:
    schema_id: str
    source_root: str
    source_repository: str
    public_repository: str
    upstream_repository: str
    protected_pi: str
    codebook: tuple[PublicCodebookEntry, ...]
    resources: tuple[QQUAPPResource, ...]
    relations: tuple[TypedRelation, ...]
    krone_gate: KroneTypedGate
    kokompi_pattern: KokompiDesignPattern
    configuration_space: GuidedConfigurationSpace
    ruleset: GitHubRulesetProjection
    admission_spine: tuple[str, ...] = ("PACAPDG", "UAP", "SAFE_REPLAY")
    cpython_public_boundary: tuple[str, ...] = (
        "Python.h",
        "Limited API",
        "Stable ABI",
        "multi-phase extension initialization",
        "typed PyCapsule",
    )
    cpython_forbidden_contracts: tuple[str, ...] = (
        "Include/internal/*",
        "Include/cpython/*",
        "_Py*",
        "PyUnstable*",
        "CPython object layout",
    )
    private_source_mirrored: bool = False
    interpreter_semantics_changed: bool = False
    repository_mutation_authority: bool = False
    identity_transport: bool = False
    authority_transport: bool = False


@dataclass(frozen=True)
class PublicationReceipt:
    schema_id: str
    verdict: str
    primitive_digest: str
    effective_capabilities: tuple[str, ...]
    obligations: tuple[str, ...]
    ruleset_mutation_executed: bool = False
    runtime_executed: bool = False
    identity_transport: bool = False
    authority_transport: bool = False


@dataclass(frozen=True)
class KokompiPatternReceipt:
    pattern_id: str
    source_occurrences: tuple[str, ...]
    target_occurrence: str
    fresh_occurrence: bool
    provenance_preserved: bool
    admitted_symbolically: bool
    ruleset_mutation_executed: bool = False
    git_merge_executed: bool = False
    identity_transport: bool = False
    authority_transport: bool = False


def _stable_digest(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        default=str,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _facet(type_id: str) -> PrimitiveTypedFacet:
    return PrimitiveTypedFacet(
        type_id=type_id,
        quno="QUNO:SIGIL4CPYTHON:PUBLICATION",
        replay_witness=f"REPLAY:{type_id}",
    )


def effective_capability_meet(entries: Iterable[PublicCodebookEntry]) -> tuple[str, ...]:
    materialized = tuple(entries)
    if not materialized:
        return ()
    meet = set(materialized[0].capabilities)
    for entry in materialized[1:]:
        meet.intersection_update(entry.capabilities)
    return tuple(sorted(meet))


def validate_publication_primitive(primitive: PublicationPrimitive) -> PublicationReceipt:
    obligations: list[str] = []
    if primitive.schema_id != SCHEMA_ID:
        obligations.append("SCHEMA_ID_DRIFT")
    if primitive.source_root != SOURCE_ROOT:
        obligations.append("SOURCE_ROOT_DRIFT")
    if primitive.admission_spine != ("PACAPDG", "UAP", "SAFE_REPLAY"):
        obligations.append("ADMISSION_SPINE_DRIFT")
    if primitive.private_source_mirrored:
        obligations.append("PRIVATE_SOURCE_MIRROR_FORBIDDEN")
    if primitive.interpreter_semantics_changed:
        obligations.append("CPYTHON_INTERPRETER_SEMANTICS_CHANGE_FORBIDDEN")
    if primitive.repository_mutation_authority:
        obligations.append("REPOSITORY_MUTATION_AUTHORITY_FORBIDDEN")
    if primitive.identity_transport:
        obligations.append("IDENTITY_TRANSPORT_FORBIDDEN")
    if primitive.authority_transport:
        obligations.append("AUTHORITY_TRANSPORT_FORBIDDEN")

    try:
        primitive.ruleset.validate()
        primitive.krone_gate.validate()
        primitive.kokompi_pattern.validate()
        primitive.configuration_space.validate()
        for resource in primitive.resources:
            resource.validate()
        for relation in primitive.relations:
            relation.validate()
        for entry in primitive.codebook:
            entry.validate()
    except ValueError as exc:
        obligations.append(str(exc))

    type_ids = {entry.facet.type_id for entry in primitive.codebook}
    resource_ids = {resource.resource_id for resource in primitive.resources}
    relation_ids = {relation.relation_id for relation in primitive.relations}
    if len(type_ids) != len(primitive.codebook):
        obligations.append("PUBLIC_CODEBOOK_TYPE_ID_COLLAPSE")
    if len(resource_ids) != len(primitive.resources):
        obligations.append("PUBLIC_RESOURCE_ID_COLLAPSE")
    if len(relation_ids) != len(primitive.relations):
        obligations.append("PUBLIC_RELATION_ID_COLLAPSE")

    for entry in primitive.codebook:
        if not set(entry.resource_ids) <= resource_ids:
            obligations.append(f"UNKNOWN_RESOURCE_REF:{entry.public_interface_id}")
        if not set(entry.relation_ids) <= relation_ids:
            obligations.append(f"UNKNOWN_RELATION_REF:{entry.public_interface_id}")
    for relation in primitive.relations:
        if not set(relation.source_type_ids + relation.target_type_ids) <= type_ids:
            obligations.append(f"UNKNOWN_RELATION_ENDPOINT:{relation.relation_id}")

    if not set(primitive.krone_gate.input_type_ids) <= type_ids:
        obligations.append("KRONE_GATE_UNKNOWN_INPUT_TYPE")
    if not set(primitive.krone_gate.resource_ids) <= resource_ids:
        obligations.append("KRONE_GATE_UNKNOWN_RESOURCE")
    if not set(primitive.krone_gate.relation_ids) <= relation_ids:
        obligations.append("KRONE_GATE_UNKNOWN_RELATION")
    if not set(primitive.kokompi_pattern.source_type_ids) <= type_ids:
        obligations.append("KOKOMPI_PATTERN_UNKNOWN_SOURCE_TYPE")
    if primitive.kokompi_pattern.target_ruleset_id != primitive.ruleset.ruleset_id:
        obligations.append("KOKOMPI_RULESET_TARGET_DRIFT")

    capabilities = effective_capability_meet(primitive.codebook)
    if not set(primitive.krone_gate.required_capabilities) <= set(capabilities):
        obligations.append("KRONE_CAPABILITY_MEET_TOO_WEAK")

    digest_payload = {
        "schema_id": primitive.schema_id,
        "codebook": [
            {
                "type_id": entry.facet.type_id,
                "interface": entry.public_interface_id,
                "digest": entry.public_digest,
                "capabilities": list(entry.capabilities),
                "resources": list(entry.resource_ids),
                "relations": list(entry.relation_ids),
                "source_commit": entry.source_commit,
                "source_schema_id": entry.source_schema_id,
            }
            for entry in primitive.codebook
        ],
        "ruleset": {
            "name": primitive.ruleset.name,
            "targets": list(primitive.ruleset.target_branches),
            "rules": [rule.kind.value for rule in primitive.ruleset.rules],
            "checks": list(primitive.ruleset.required_status_checks),
            "bypass": list(primitive.ruleset.bypass_actors),
        },
        "pattern": [stage.value for stage in primitive.kokompi_pattern.stages],
    }
    return PublicationReceipt(
        schema_id=SCHEMA_ID,
        verdict="ADMIT_SOURCE_PLAN" if not obligations else "HOLD_WITH_OBSTRUCTION",
        primitive_digest=_stable_digest(digest_payload),
        effective_capabilities=capabilities,
        obligations=tuple(sorted(set(obligations))),
    )


def compile_kokompi_pattern(
    pattern: KokompiDesignPattern,
    *,
    source_occurrences: tuple[str, ...],
    target_occurrence: str,
) -> KokompiPatternReceipt:
    pattern.validate()
    if not source_occurrences or len(source_occurrences) != len(set(source_occurrences)):
        raise ValueError("PYKARA_REQUIRES_DISTINCT_SOURCE_OCCURRENCES")
    fresh = bool(target_occurrence) and target_occurrence not in source_occurrences
    return KokompiPatternReceipt(
        pattern_id=pattern.pattern_id,
        source_occurrences=source_occurrences,
        target_occurrence=target_occurrence,
        fresh_occurrence=fresh,
        provenance_preserved=True,
        admitted_symbolically=fresh,
    )


def materialize_configuration(
    space: GuidedConfigurationSpace,
    selection: Mapping[str, str],
    *,
    epoch: int,
) -> ConfigurationOccurrence:
    space.validate()
    if epoch < 0:
        raise ValueError("NEGATIVE_CONFIGURATION_EPOCH")
    axes = {axis.axis_id: axis for axis in space.axes}
    unknown = set(selection) - set(axes)
    if unknown:
        raise ValueError("UNKNOWN_CONFIGURATION_AXIS:" + ",".join(sorted(unknown)))

    resolved: dict[str, str] = {}
    for axis_id, axis in axes.items():
        value = selection.get(axis_id, axis.default_value)
        if value not in axis.allowed_values:
            raise ValueError(f"CONFIGURATION_VALUE_OUTSIDE_AXIS:{axis_id}:{value}")
        resolved[axis_id] = value

    abi = resolved["ABI_TRACK"]
    version = resolved["CPYTHON_MINIMUM"]
    version_tuple = tuple(map(int, version.split(".")))
    if abi == "ABI3T" and version_tuple < (3, 15):
        raise ValueError("ABI3T_REQUIRES_CPYTHON_3_15_OR_NEWER")
    if abi == "ABI3" and version_tuple < (3, 10):
        raise ValueError("ABI3_REQUIRES_CPYTHON_3_10_OR_NEWER")

    native = abi in {"ABI3", "ABI3T"}
    payload = {
        "config_space_id": space.config_space_id,
        "epoch": epoch,
        "selection": sorted(resolved.items()),
        "native_lowering_requested": native,
    }
    checksum = _stable_digest(payload)
    return ConfigurationOccurrence(
        config_space_id=space.config_space_id,
        occurrence_id=f"SIGIL4CPYTHON:CONFIG:{epoch}:{checksum[:16]}",
        epoch=epoch,
        selection=tuple(sorted(resolved.items())),
        digest=checksum,
        native_lowering_requested=native,
        cpython_minimum=version,
    )


def build_reference_publication_primitive(
    *,
    source_commit: str = "SOURCE_COMMIT_REQUIRED",
) -> PublicationPrimitive:
    resource = QQUAPPResource(
        resource_id="RESOURCE:PUBLICATION_METADATA",
        facet=_facet("TYPE:RESOURCE:PUBLICATION_METADATA"),
        pull_witness="W:QQUAPP:PULL:PUBLICATION",
        tensor_witness="W:QQUAPP:TENSOR:PUBLICATION",
        push_witness="W:QQUAPP:PUSH:PUBLICATION",
        krone_gate_witness="W:KRONE:PUBLICATION",
        capacity=8,
    )
    ci_resource = QQUAPPResource(
        resource_id="RESOURCE:CI_GATE",
        facet=_facet("TYPE:RESOURCE:CI_GATE"),
        pull_witness="W:QQUAPP:PULL:CI",
        tensor_witness="W:QQUAPP:TENSOR:CI",
        push_witness="W:QQUAPP:PUSH:CI",
        krone_gate_witness="W:KRONE:CI",
        capacity=4,
    )
    type_names = (
        "TYPE:PUBLIC_CODEBOOK",
        "TYPE:QQUAPP_PUBLICATION",
        "TYPE:KOKOMPI_DESIGN_PATTERN",
        "TYPE:KRONE_TYPED_GATE",
        "TYPE:CPYTHON_PUBLIC_PROJECTION",
        "TYPE:GITHUB_RULESET_GOVERNANCE",
    )
    relations = (
        TypedRelation(
            "REL:SOURCE_TO_CODEBOOK",
            _facet("TYPE:RELATION:SOURCE_TO_CODEBOOK"),
            ("TYPE:PUBLIC_CODEBOOK",),
            ("TYPE:CPYTHON_PUBLIC_PROJECTION",),
            "W:REL:SOURCE_TO_CODEBOOK",
        ),
        TypedRelation(
            "REL:QQUAPP_GATES_PROJECTION",
            _facet("TYPE:RELATION:QQUAPP_GATES_PROJECTION"),
            ("TYPE:QQUAPP_PUBLICATION", "TYPE:KRONE_TYPED_GATE"),
            ("TYPE:CPYTHON_PUBLIC_PROJECTION",),
            "W:REL:QQUAPP_GATES_PROJECTION",
        ),
        TypedRelation(
            "REL:KOKOMPI_DESIGNS_PUBLICATION",
            _facet("TYPE:RELATION:KOKOMPI_DESIGNS_PUBLICATION"),
            ("TYPE:KOKOMPI_DESIGN_PATTERN",),
            ("TYPE:PUBLIC_CODEBOOK",),
            "W:REL:KOKOMPI_DESIGNS_PUBLICATION",
        ),
        TypedRelation(
            "REL:RULESET_PROTECTS_PUBLICATION",
            _facet("TYPE:RELATION:RULESET_PROTECTS_PUBLICATION"),
            ("TYPE:GITHUB_RULESET_GOVERNANCE",),
            ("TYPE:PUBLIC_CODEBOOK",),
            "W:REL:RULESET_PROTECTS_PUBLICATION",
        ),
    )
    all_relation_ids = tuple(relation.relation_id for relation in relations)
    codebook = tuple(
        PublicCodebookEntry(
            facet=_facet(type_id),
            public_interface_id="KLI:" + type_id.removeprefix("TYPE:"),
            public_digest="sha256:" + sha256(type_id.encode()).hexdigest(),
            capabilities=("READ", "TYPECHECK", "PLAN"),
            resource_ids=(resource.resource_id, ci_resource.resource_id),
            relation_ids=all_relation_ids,
            source_commit=source_commit,
            source_schema_id=type_id.replace("TYPE:", "SIGILBOOK_PUBLIC_") + "_V1",
        )
        for type_id in type_names
    )
    gate = KroneTypedGate(
        gate_id="KRONE:GATE:PUBLICATION",
        facet=_facet("TYPE:KRONE:GATE:PUBLICATION"),
        input_type_ids=type_names,
        resource_ids=(resource.resource_id, ci_resource.resource_id),
        relation_ids=all_relation_ids,
        required_capabilities=("READ", "TYPECHECK", "PLAN"),
        witness_id="W:KRONE:GATE:PUBLICATION",
    )
    ruleset = GitHubRulesetProjection(
        ruleset_id="GITHUB:RULESET:MAIN:PUBLICATION_V1",
        facet=_facet("TYPE:GITHUB:RULESET:MAIN:PUBLICATION_V1"),
        name="SIGIL4CPython public main publication gate",
        desired_enforcement=EnforcementStatus.ACTIVE,
        target_branches=("main",),
        rules=(
            RulesetRule(RuleKind.RESTRICT_DELETIONS),
            RulesetRule(RuleKind.REQUIRE_LINEAR_HISTORY),
            RulesetRule(
                RuleKind.REQUIRE_PULL_REQUEST,
                (("required_approvals", "1"), ("dismiss_stale_reviews", "true")),
            ),
            RulesetRule(RuleKind.REQUIRE_STATUS_CHECKS),
            RulesetRule(RuleKind.BLOCK_FORCE_PUSHES),
        ),
        required_status_checks=(PUBLICATION_CHECK,),
    )
    pattern = KokompiDesignPattern(
        pattern_id="KOKOMPI:PUBLICATION:PYKARA_KIRBY_SWALLO",
        facet=_facet("TYPE:KOKOMPI:PUBLICATION:PATTERN"),
        stages=(
            PatternStage.PYKARA_CARVE,
            PatternStage.KIRBY_REWRITE,
            PatternStage.SWALLO_SWALLOW,
            PatternStage.QQUAPP_PULL_TENSOR_PUSH,
        ),
        source_type_ids=type_names,
        target_ruleset_id=ruleset.ruleset_id,
        witness_ids=(
            "W:PYKARA:PUBLIC:CARVE",
            "W:KIRBY:PUBLIC:REWRITE",
            "W:SWALLO:PUBLIC:ABSORB",
            "W:QQUAPP:PUBLIC:PULL_TENSOR_PUSH",
        ),
    )
    axis_facet = _facet("TYPE:CONFIGURATION:AXIS")
    config = GuidedConfigurationSpace(
        config_space_id="CONFIG:SIGIL4CPYTHON:DIY:V1",
        facet=_facet("TYPE:CONFIGURATION:SPACE"),
        axes=(
            ConfigurationAxis(
                "ABI_TRACK",
                ("PURE_PYTHON", "ABI3", "ABI3T"),
                "PURE_PYTHON",
                axis_facet,
            ),
            ConfigurationAxis(
                "CPYTHON_MINIMUM",
                ("3.10", "3.11", "3.12", "3.13", "3.14", "3.15"),
                "3.11",
                axis_facet,
            ),
            ConfigurationAxis(
                "PUBLICATION_PROFILE",
                ("LIBRARY", "RESEARCH", "DEMO"),
                "LIBRARY",
                axis_facet,
            ),
            ConfigurationAxis(
                "EXECUTION_BOUNDARY",
                ("METADATA_ONLY", "NATIVE_EXTENSION_PLAN"),
                "METADATA_ONLY",
                axis_facet,
            ),
        ),
        krone_gate_id=gate.gate_id,
        output_type_id="TYPE:CPYTHON_PUBLIC_PROJECTION",
    )
    return PublicationPrimitive(
        schema_id=SCHEMA_ID,
        source_root=SOURCE_ROOT,
        source_repository=SOURCE_REPOSITORY,
        public_repository=PUBLIC_REPOSITORY,
        upstream_repository=UPSTREAM_REPOSITORY,
        protected_pi=PROTECTED_PI,
        codebook=codebook,
        resources=(resource, ci_resource),
        relations=relations,
        krone_gate=gate,
        kokompi_pattern=pattern,
        configuration_space=config,
        ruleset=ruleset,
    )


__all__ = [
    "SCHEMA_ID",
    "SOURCE_ROOT",
    "SOURCE_REPOSITORY",
    "PUBLIC_REPOSITORY",
    "UPSTREAM_REPOSITORY",
    "PROTECTED_PI",
    "PUBLICATION_CHECK",
    "EnforcementStatus",
    "RuleKind",
    "PatternStage",
    "PrimitiveTypedFacet",
    "QQUAPPResource",
    "TypedRelation",
    "PublicCodebookEntry",
    "KroneTypedGate",
    "RulesetRule",
    "GitHubRulesetProjection",
    "KokompiDesignPattern",
    "ConfigurationAxis",
    "GuidedConfigurationSpace",
    "ConfigurationOccurrence",
    "PublicationPrimitive",
    "PublicationReceipt",
    "KokompiPatternReceipt",
    "effective_capability_meet",
    "validate_publication_primitive",
    "compile_kokompi_pattern",
    "materialize_configuration",
    "build_reference_publication_primitive",
]
