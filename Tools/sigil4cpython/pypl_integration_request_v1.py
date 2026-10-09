# SPDX-License-Identifier: MIT
"""Source-only request gate for SIGIL4CPython PYPL public projections.

Does not import CPython internals, execute a projected program, submit PRs,
or attest human approval. An ADMIT_SOURCE_PLAN verdict is NOT integration.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any

SCHEMA_ID = "SIGIL4CPYTHON_PYPL_INTEGRATION_REQUEST_V1"
SOURCE_REPO = "jbermejovega/sigilbook"
TARGET_REPO = "jbermejovega/sigil4cpython"
_SHA40 = re.compile(r"[0-9a-f]{40}\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9_.:-]{1,127}\Z")
_ALLOWED_EXTENSIONS = frozenset({".py", ".sym", ".ebnf", ".md", ".json"})
_KEYS = frozenset({
    "schema_id", "request_id", "source_repository", "source_commit",
    "target_repository", "target_base_commit", "projection",
    "artifacts", "evidence", "boundaries",
})
_ARTIFACT_KEYS = frozenset({"path", "sha256"})
_EVIDENCE_KEYS = frozenset({
    "local_tests_ref", "license_review_ref", "maintainer_review_ref",
    "author_review_ref",
})
_BOUNDARY_KEYS = frozenset({
    "no_private_payload", "no_cpython_internals",
    "no_runtime_effect", "no_authority_transport",
    "no_identity_transport", "ai_assisted_disclosed",
})


def _safe_path(path: object) -> bool:
    if not isinstance(path, str) or "\\" in path or path.startswith("/"):
        return False
    posix = PurePosixPath(path)
    if not path or any(x in {"", ".", ".."} for x in path.split("/")):
        return False
    if posix.suffix not in _ALLOWED_EXTENSIONS:
        return False
    return path.startswith("Tools/sigil4cpython/") or path.startswith(
        "docs/SIGIL4CPYTHON_"
    )


def _canonical_digest(payload: dict[str, Any]) -> str:
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True).encode("utf-8")).hexdigest()


def evaluate_request(manifest: object, repository_root: Path) -> dict[str, Any]:
    """Validate finite public source artifacts; require independent review later.

    Returns REJECT for contradictions, HOLD_QUNO for missing evidence and
    ADMIT_SOURCE_PLAN for a complete local *proposal*, never an actual merge.
    """
    errors: list[str] = []
    missing: list[str] = []
    digest = ""
    if not isinstance(manifest, dict):
        errors.append("manifest_must_be_object")
        manifest = {}
    else:
        try:
            digest = _canonical_digest(manifest)
        except (TypeError, ValueError):
            errors.append("manifest_not_canonical_json")
    if set(manifest) != _KEYS:
        errors.append("manifest_schema_keys_mismatch")
    if manifest.get("schema_id") != SCHEMA_ID:
        errors.append("invalid_schema_id")
    if not isinstance(manifest.get("request_id"), str) or not _TOKEN.fullmatch(
        manifest["request_id"]
    ):
        errors.append("invalid_request_id")
    if manifest.get("source_repository") != SOURCE_REPO:
        errors.append("source_not_allowlisted")
    if manifest.get("target_repository") != TARGET_REPO:
        errors.append("target_not_public_interface_carrier")
    for key in ("source_commit", "target_base_commit"):
        value = manifest.get(key)
        if not isinstance(value, str) or not _SHA40.fullmatch(value):
            errors.append(f"invalid_{key}")
    if manifest.get("projection") != "PUBLIC_SOURCE_ONLY_PYPL":
        errors.append("unsupported_projection")
    boundaries = manifest.get("boundaries")
    if not isinstance(boundaries, dict) or set(boundaries) != _BOUNDARY_KEYS:
        errors.append("boundary_schema_mismatch")
    elif any(type(v) is not bool or not v for v in boundaries.values()):
        errors.append("public_boundary_violation")
    # A declaration is only a statement of intent; the reviewer checks it.
    evidence = manifest.get("evidence")
    if not isinstance(evidence, dict) or set(evidence) != _EVIDENCE_KEYS:
        errors.append("evidence_schema_mismatch")
    else:
        for key in sorted(_EVIDENCE_KEYS):
            value = evidence[key]
            if value is None or value == "":
                missing.append(f"missing_{key}")
            elif not isinstance(value, str) or len(value) > 1024:
                errors.append(f"invalid_{key}")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("no_artifacts")
        artifacts = []
    seen: set[str] = set()
    root = Path(repository_root).resolve()
    for i, item in enumerate(artifacts):
        if not isinstance(item, dict) or set(item) != _ARTIFACT_KEYS:
            errors.append(f"bad_artifact_schema:{i}")
            continue
        path = item["path"]
        recorded_hash = item["sha256"]
        if not _safe_path(path):
            errors.append(f"forbidden_artifact_path:{i}")
            continue
        if path in seen:
            errors.append(f"duplicate_artifact:{path}")
            continue
        seen.add(path)
        if not isinstance(recorded_hash, str) or not _SHA256.fullmatch(
            recorded_hash
        ):
            missing.append(f"unresolved_digest:{path}")
            continue
        artifact = (root / path).resolve()
        if not artifact.is_relative_to(root):
            errors.append(f"artifact_escapes_root:{path}")
            continue
        if not artifact.is_file():
            missing.append(f"artifact_missing:{path}")
            continue
        if sha256(artifact.read_bytes()).hexdigest() != recorded_hash:
            errors.append(f"digest_mismatch:{path}")
    verdict = "REJECT" if errors else ("HOLD_QUNO" if missing else "ADMIT_SOURCE_PLAN")
    return {
        "schema_id": SCHEMA_ID,
        "request_id": manifest.get("request_id"),
        "verdict": verdict,
        "request_ready_for_review": verdict == "ADMIT_SOURCE_PLAN",
        "errors": sorted(errors),
        "quno": sorted(missing),
        "manifest_sha256": digest,
        "source_pin_verified_remotely": False,
        "target_pin_verified_remotely": False,
        "review_authenticity_verified": False,
        "cpython_upstream_requested": False,
        "cpython_upstream_accepted": False,
        "uap": "UNJUDGED",
        "external_effect": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="integration request JSON")
    parser.add_argument("--root", type=Path, default=Path.cwd(),
                        help="repository checkout root")
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
        result = evaluate_request(data, args.root)
    except (OSError, json.JSONDecodeError) as exc:
        result = {
            "schema_id": SCHEMA_ID,
            "verdict": "HOLD_QUNO",
            "quno": [f"manifest_unavailable_or_invalid:{type(exc).__name__}"],
            "cpython_upstream_requested": False,
            "external_effect": False,
        }
    print(json.dumps(result, sort_keys=True, indent=2))
    return {"ADMIT_SOURCE_PLAN": 0, "HOLD_QUNO": 2, "REJECT": 3}[result["verdict"]]


if __name__ == "__main__":
    raise SystemExit(main())
