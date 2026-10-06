from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Iterable

CODEBOOK_SCHEMA = "SIGIL_PUBLIC_CODEBOOK_V1"
REQUIRED_TYPES = ("SIGILBookTyped", "PluralTyped", "QUNOTyped")


@dataclass(frozen=True)
class CodebookManifest:
    schema: str
    book_id: str
    title: str
    entry_notebook: str
    types: tuple[str, ...]
    repository: str
    ref: str
    audiences: tuple[str, ...] = ()
    requirements: tuple[str, ...] = ()
    source_lineage: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "CodebookManifest":
        source = payload.get("source", {})
        runtime = payload.get("runtime", {})
        return cls(
            schema=str(payload.get("schema", "")),
            book_id=str(payload.get("book_id", "")),
            title=str(payload.get("title", "")),
            entry_notebook=str(payload.get("entry_notebook", "")),
            types=tuple(str(x) for x in payload.get("types", ())),
            repository=str(source.get("repository", "")),
            ref=str(source.get("ref", "")),
            audiences=tuple(str(x) for x in payload.get("audiences", ())),
            requirements=tuple(str(x) for x in runtime.get("requirements", ())),
            source_lineage=tuple(str(x) for x in payload.get("source_lineage", ())),
        )

    def validate(self, root: Path | None = None) -> "CodebookManifest":
        errors: list[str] = []
        if self.schema != CODEBOOK_SCHEMA:
            errors.append(f"schema must be {CODEBOOK_SCHEMA}")
        for field_name in ("book_id", "title", "entry_notebook", "repository", "ref"):
            if not getattr(self, field_name):
                errors.append(f"{field_name} must be non-empty")

        missing_types = [t for t in REQUIRED_TYPES if t not in self.types]
        if missing_types:
            errors.append(f"missing required types: {', '.join(missing_types)}")
        if len(self.types) != len(set(self.types)):
            errors.append("types must not contain duplicates")

        if root is not None:
            notebook = root / self.entry_notebook
            if not notebook.is_file():
                errors.append(f"entry notebook not found: {self.entry_notebook}")

        if errors:
            raise ValueError("; ".join(errors))
        return self

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "book_id": self.book_id,
            "title": self.title,
            "types": list(self.types),
            "audiences": list(self.audiences),
            "entry_notebook": self.entry_notebook,
            "runtime": {
                "python": ">=3.9",
                "requirements": list(self.requirements),
            },
            "source": {
                "repository": self.repository,
                "ref": self.ref,
            },
            "source_lineage": list(self.source_lineage),
            "invariants": {
                "presentation_is_not_certification": True,
                "same_projection_is_not_same_bearer": True,
                "no_identity_transport": True,
                "no_authority_transport": True,
            },
        }


def load_codebook(path: str | Path) -> CodebookManifest:
    p = Path(path)
    payload = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("codebook manifest must be a JSON object")
    return CodebookManifest.from_dict(payload)


def validate_codebook(path: str | Path, *, root: str | Path | None = None) -> CodebookManifest:
    p = Path(path)
    manifest = load_codebook(p)
    base = Path(root) if root is not None else p.parent
    return manifest.validate(base)


def new_manifest(
    *,
    book_id: str,
    title: str,
    entry_notebook: str,
    repository: str,
    ref: str,
    audiences: Iterable[str] = (),
    requirements: Iterable[str] = (),
    source_lineage: Iterable[str] = (),
) -> CodebookManifest:
    return CodebookManifest(
        schema=CODEBOOK_SCHEMA,
        book_id=book_id,
        title=title,
        entry_notebook=entry_notebook,
        types=REQUIRED_TYPES,
        repository=repository,
        ref=ref,
        audiences=tuple(audiences),
        requirements=tuple(requirements),
        source_lineage=tuple(source_lineage),
    ).validate()
