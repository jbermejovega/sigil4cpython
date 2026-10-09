# sigil4cpython — KRONE / CRONE / QRONE

Minimal source-only Python packaging candidate for SIGIL typed programming.

- **KRONE**: copyrighted programming teaching book (separate content license).
- **CRONE**: public CLI, `sigil4py-check`.
- **QRONE**: typed transmutation adapters, optional SymPy and C backends.
- **PACA NUKLEA**: standard-library-only core.
- **PACA QORE**: optional SymPy symbolic teaching.
- **PACA KORE**: witnessed replay-safe type validation.

## Development

```sh
python -m pip install --upgrade build
python -m build
python -m pip install -e '.[dev,symbolik]'
python -m pytest -q
sigil4py-check --status
```

A build is not verified until these commands pass in a clean Linux environment.
No native C extension, MPI, audio engine, or game engine is promised by this
minimal package. For a C backend, supply an explicit extension build and
per-ABI tests. No distribution or release has been published by this plan.

Software metadata declares Apache-2.0; third-party code and original
KRONE/PACA ARTE assets retain their separate copyrights and licenses.

PIORNALEGO ES CANON.
