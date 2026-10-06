"""Dependency-free projection of the PACACORE Standard-Model source plan.

This module mirrors a finite sigilbook receipt. It does not import Pydantic,
change CPython semantics, execute a backend, or claim physical correctness.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Final

SCHEMA_ID: Final = "SIGIL4CPYTHON_PACACORE_STANDARD_MODEL_PROJECTION_V1"
SOURCE_REPOSITORY: Final = "jbermejovega/sigilbook"
SOURCE_PULL_REQUEST: Final = 750
SOURCE_SHA: Final = "4c94b3f847cc26b17d3e54cc253c1f99655ea6fb"
SOURCE_SCHEMA: Final = "PACACORE_STANDARD_MODEL_AST_V1"
SOURCE_BUNDLE_SHA256: Final = "5b343a2fffb3f25e81567e42072b9f5cdbf38bd049f0496b4dea980b22e0aa05"
SOURCE_REPLAY_TIP: Final = "b73c37879d7b7f9c3fea2b4b89d53848333c204adfeda6169dd595444c524261"
FACETS: Final = (
    "PACA_TYPED", "KOKOMPY_TYPED", "ALGEBRAIC_TYPED", "SYNTACTICAL_TYPED",
    "SEMANTICAL_TYPED", "SEMIOTIC_TYPED", "JARANIAN_TYPED", "CONTENT_TYPED",
    "TROPE_TYPED", "MANTRA_TYPED",
)
BACKENDS: Final = (
    "MACAULAY2", "MLIR", "SIGIL4PY", "SIGIL4GODOT", "SIGIL4CPYTHON",
    "MPI4PY", "CYTHON", "NUMBA", "PYOMP",
)


@dataclass(frozen=True, slots=True)
class PACACoreStandardModelProjection:
    schema_id: str
    source_repository: str
    source_pull_request: int
    source_sha: str
    source_schema: str
    source_bundle_sha256: str
    source_replay_tip: str
    facets: tuple[str, ...]
    backends: tuple[str, ...]
    field_count: int
    fusion_count: int
    transport_deprecated: bool
    safe_replay: bool
    pi_fixed: bool
    dependency_free: bool
    pydantic_imported: bool
    interpreter_semantics_changed: bool
    abi_changed: bool
    runtime_executed: bool
    identity_transport: bool
    final_kapsyla: bool
    projection_sha256: str


def _payload_without_digest(projection: PACACoreStandardModelProjection) -> dict[str, object]:
    data = {name: getattr(projection, name) for name in projection.__dataclass_fields__}
    data.pop("projection_sha256")
    return data


def _digest(payload: dict[str, object]) -> str:
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def build_pacacore_standard_model_projection() -> PACACoreStandardModelProjection:
    provisional = PACACoreStandardModelProjection(
        schema_id=SCHEMA_ID,
        source_repository=SOURCE_REPOSITORY,
        source_pull_request=SOURCE_PULL_REQUEST,
        source_sha=SOURCE_SHA,
        source_schema=SOURCE_SCHEMA,
        source_bundle_sha256=SOURCE_BUNDLE_SHA256,
        source_replay_tip=SOURCE_REPLAY_TIP,
        facets=FACETS,
        backends=BACKENDS,
        field_count=7,
        fusion_count=3,
        transport_deprecated=True,
        safe_replay=True,
        pi_fixed=True,
        dependency_free=True,
        pydantic_imported=False,
        interpreter_semantics_changed=False,
        abi_changed=False,
        runtime_executed=False,
        identity_transport=False,
        final_kapsyla=False,
        projection_sha256="0" * 64,
    )
    return PACACoreStandardModelProjection(
        **{**_payload_without_digest(provisional), "projection_sha256": _digest(_payload_without_digest(provisional))}
    )


def validate_pacacore_standard_model_projection(projection: PACACoreStandardModelProjection) -> bool:
    return (
        projection == build_pacacore_standard_model_projection()
        and projection.projection_sha256 == _digest(_payload_without_digest(projection))
        and projection.facets == FACETS
        and projection.backends == BACKENDS
        and projection.transport_deprecated
        and projection.safe_replay
        and projection.pi_fixed
        and projection.dependency_free
        and not any((projection.pydantic_imported, projection.interpreter_semantics_changed, projection.abi_changed, projection.runtime_executed, projection.identity_transport, projection.final_kapsyla))
    )
