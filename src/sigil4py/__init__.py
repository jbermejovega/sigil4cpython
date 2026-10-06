"""Public SIGIL4PY compatibility layer.

This package is a public projection. It does not expose or imply access to the
private SIGILBOOK canonical source.
"""

from .codebook import (
    CODEBOOK_SCHEMA,
    REQUIRED_TYPES,
    CodebookManifest,
    load_codebook,
    validate_codebook,
)

__all__ = [
    "CODEBOOK_SCHEMA",
    "REQUIRED_TYPES",
    "CodebookManifest",
    "load_codebook",
    "validate_codebook",
]

__version__ = "0.1.1"
