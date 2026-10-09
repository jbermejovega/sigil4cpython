# SPDX-License-Identifier: MIT
"""Strict typed source-plan interface for SIGIL4CPython PYPL request gate.

Typing and local validation do not authenticate human reviews, grant UAP
admission, modify CPython, or authorize any external execution.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol, TypedDict

from pypl_integration_request_v1 import SCHEMA_ID, evaluate_request

Verdict = Literal["ADMIT_SOURCE_PLAN", "HOLD_QUNO", "REJECT"]
Projection = Literal["PUBLIC_SOURCE_ONLY_PYPL"]
UAP = Literal["UNJUDGED"]


class ArtifactJSON(TypedDict):
    path: str
    sha256: str


class EvidenceJSON(TypedDict):
    local_tests_ref: str | None
    license_review_ref: str | None
    maintainer_review_ref: str | None
    author_review_ref: str | None


class BoundaryJSON(TypedDict):
    no_private_payload: bool
    no_cpython_internals: bool
    no_runtime_effect: bool
    no_authority_transport: bool
    no_identity_transport: bool
    ai_assisted_disclosed: bool


class RequestJSON(TypedDict):
    schema_id: str
    request_id: str
    source_repository: str
    source_commit: str
    target_repository: str
    target_base_commit: str
    projection: Projection
    artifacts: list[ArtifactJSON]
    evidence: EvidenceJSON
    boundaries: BoundaryJSON


class SourcePlanGate(Protocol):
    def __call__(self, manifest: object, repository_root: Path) -> dict[str, object]:
        """Calculate a local source-plan judgement, without external effects."""


@dataclass(frozen=True)
class Artifact:
    path: str
    sha256: str


@dataclass(frozen=True)
class Evidence:
    local_tests_ref: str | None
    license_review_ref: str | None
    maintainer_review_ref: str | None
    author_review_ref: str | None


@dataclass(frozen=True)
class Boundaries:
    no_private_payload: bool
    no_cpython_internals: bool
    no_runtime_effect: bool
    no_authority_transport: bool
    no_identity_transport: bool
    ai_assisted_disclosed: bool


@dataclass(frozen=True)
class IntegrationRequest:
    request_id: str
    source_repository: str
    source_commit: str
    target_repository: str
    target_base_commit: str
    artifacts: tuple[Artifact, ...]
    evidence: Evidence
    boundaries: Boundaries
    projection: Projection = "PUBLIC_SOURCE_ONLY_PYPL"
    schema_id: str = SCHEMA_ID

    def as_payload(self) -> RequestJSON:
        """Serialize without changing missing witnesses into positive evidence."""
        return {
            "schema_id": self.schema_id,
            "request_id": self.request_id,
            "source_repository": self.source_repository,
            "source_commit": self.source_commit,
            "target_repository": self.target_repository,
            "target_base_commit": self.target_base_commit,
            "projection": self.projection,
            "artifacts": [
                {"path": a.path, "sha256": a.sha256} for a in self.artifacts
            ],
            "evidence": {
                "local_tests_ref": self.evidence.local_tests_ref,
                "license_review_ref": self.evidence.license_review_ref,
                "maintainer_review_ref": self.evidence.maintainer_review_ref,
                "author_review_ref": self.evidence.author_review_ref,
            },
            "boundaries": {
                "no_private_payload": self.boundaries.no_private_payload,
                "no_cpython_internals": self.boundaries.no_cpython_internals,
                "no_runtime_effect": self.boundaries.no_runtime_effect,
                "no_authority_transport": self.boundaries.no_authority_transport,
                "no_identity_transport": self.boundaries.no_identity_transport,
                "ai_assisted_disclosed": self.boundaries.ai_assisted_disclosed,
            },
        }


@dataclass(frozen=True)
class IntegrationVerdict:
    verdict: Verdict
    request_id: str | None
    errors: tuple[str, ...]
    quno: tuple[str, ...]
    manifest_sha256: str
    source_plan_complete: bool
    uap: UAP = "UNJUDGED"
    external_effect: Literal[False] = False
    cpython_upstream_requested: Literal[False] = False
    cpython_upstream_accepted: Literal[False] = False
    review_authenticity_verified: Literal[False] = False

    def __post_init__(self) -> None:
        if self.verdict not in ("ADMIT_SOURCE_PLAN", "HOLD_QUNO", "REJECT"):
            raise ValueError("unknown_verdict")
        if self.uap != "UNJUDGED" or self.external_effect is not False:
            raise ValueError("authority_effect_not_allowed")
        if any(x is not False for x in (
            self.cpython_upstream_requested, self.cpython_upstream_accepted,
            self.review_authenticity_verified,
        )):
            raise ValueError("upstream_or_review_authority_not_allowed")
        if self.source_plan_complete != (self.verdict == "ADMIT_SOURCE_PLAN"):
            raise ValueError("verdict_plan_inconsistency")


class TypedShapeError(ValueError):
    """Structural type mismatch: it never promotes a QUNO field to authority."""


def _record(raw: object, required: set[str], name: str) -> dict[str, object]:
    if type(raw) is not dict or set(raw) != required:
        raise TypedShapeError(f"invalid_{name}_shape")
    return raw


def _str(raw: object, key: str) -> str:
    if type(raw) is not str:
        raise TypedShapeError(f"invalid_{key}_type")
    return raw


def _nullable_str(raw: object, key: str) -> str | None:
    if raw is None:
        return None
    return _str(raw, key)


def _bool(raw: object, key: str) -> bool:
    if type(raw) is not bool:
        raise TypedShapeError(f"invalid_{key}_type")
    return raw


def decode_request(raw: object) -> IntegrationRequest:
    """Check JSON shapes exactly; leave semantic checks to PACAPDG request gate."""
    request = _record(raw, set(RequestJSON.__annotations__), "request")
    if request["schema_id"] != SCHEMA_ID:
        raise TypedShapeError("invalid_schema")
    if request["projection"] != "PUBLIC_SOURCE_ONLY_PYPL":
        raise TypedShapeError("invalid_projection")
    fields = ("request_id", "source_repository", "source_commit",
              "target_repository", "target_base_commit")
    strs = {key: _str(request[key], key) for key in fields}
    raw_artifacts = request["artifacts"]
    if type(raw_artifacts) is not list:
        raise TypedShapeError("invalid_artifacts_type")
    artifacts = []
    for item in raw_artifacts:
        rec = _record(item, set(ArtifactJSON.__annotations__), "artifact")
        artifacts.append(Artifact(_str(rec["path"], "path"),
                                  _str(rec["sha256"], "sha256")))
    raw_evidence = _record(
        request["evidence"], set(EvidenceJSON.__annotations__), "evidence"
    )
    evidence = Evidence(**{
        key: _nullable_str(raw_evidence[key], key)
        for key in EvidenceJSON.__annotations__
    })
    raw_boundaries = _record(
        request["boundaries"], set(BoundaryJSON.__annotations__), "boundaries"
    )
    boundaries = Boundaries(**{
        key: _bool(raw_boundaries[key], key)
        for key in BoundaryJSON.__annotations__
    })
    return IntegrationRequest(
        **strs, artifacts=tuple(artifacts),
        evidence=evidence, boundaries=boundaries,
    )


def evaluate_typed_request(raw: object, repository_root: Path) -> IntegrationVerdict:
    """Strict interface adapter; never treats plan validation as UAP authority."""
    try:
        request = decode_request(raw)
    except TypedShapeError as exc:
        return IntegrationVerdict(
            verdict="REJECT", request_id=None,
            errors=(str(exc),), quno=(),
            manifest_sha256="", source_plan_complete=False,
        )
    decision = evaluate_request(request.as_payload(), repository_root)
    verdict = decision["verdict"]
    if verdict not in ("ADMIT_SOURCE_PLAN", "HOLD_QUNO", "REJECT"):
        raise ValueError("unexpected_gate_verdict")
    if any(decision.get(k) is not False for k in (
        "external_effect", "cpython_upstream_requested",
        "cpython_upstream_accepted", "review_authenticity_verified",
    )) or decision.get("uap") != "UNJUDGED":
        raise ValueError("gate_attempted_authority_transport")
    if type(decision.get("errors")) is not list or type(decision.get("quno")) is not list:
        raise ValueError("gate_result_shape_mismatch")
    return IntegrationVerdict(
        verdict=verdict,
        request_id=request.request_id,
        errors=tuple(decision["errors"]),
        quno=tuple(decision["quno"]),
        manifest_sha256=str(decision["manifest_sha256"]),
        source_plan_complete=decision["request_ready_for_review"],
    )
