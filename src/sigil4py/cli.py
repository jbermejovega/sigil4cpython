from __future__ import annotations

import argparse
import json
from pathlib import Path

from .codebook import CODEBOOK_SCHEMA, new_manifest, validate_codebook


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sigil4py",
        description="Public SIGIL4PY typed codebook tools",
    )
    sub = parser.add_subparsers(dest="command")

    check = sub.add_parser("check", help="validate a SIGIL public codebook manifest")
    check.add_argument("manifest", nargs="?", default="codebook.sigil.json")
    check.add_argument("--root", default=None)

    init = sub.add_parser("init-codebook", help="write a minimal typed codebook manifest")
    init.add_argument("--book-id", required=True)
    init.add_argument("--title", required=True)
    init.add_argument("--notebook", required=True)
    init.add_argument("--repository", required=True)
    init.add_argument("--ref", default="main")
    init.add_argument("--output", default="codebook.sigil.json")

    sub.add_parser("version", help="show the public codebook schema")
    return parser


def main() -> int:
    parser = _parser()
    args = parser.parse_args()

    # Compatibility: sigil4py-check with no subcommand validates the default manifest.
    if args.command is None:
        candidate = Path("codebook.sigil.json")
        if not candidate.exists():
            parser.print_help()
            return 0
        manifest = validate_codebook(candidate)
        print(f"PASS {manifest.book_id}: {manifest.title}")
        return 0

    if args.command == "check":
        manifest = validate_codebook(args.manifest, root=args.root)
        print(f"PASS {manifest.book_id}: {manifest.title}")
        print("types:", ", ".join(manifest.types))
        print("entry:", manifest.entry_notebook)
        return 0

    if args.command == "init-codebook":
        manifest = new_manifest(
            book_id=args.book_id,
            title=args.title,
            entry_notebook=args.notebook,
            repository=args.repository,
            ref=args.ref,
        )
        Path(args.output).write_text(
            json.dumps(manifest.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(args.output)
        return 0

    if args.command == "version":
        print(CODEBOOK_SCHEMA)
        return 0

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
