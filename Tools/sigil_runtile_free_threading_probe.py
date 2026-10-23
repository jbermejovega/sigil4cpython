"""SIGIL RUNTILE free-threading compatibility probe (stdlib only).

This does not remove the GIL or prove parallel speedup. Run under both
ordinary and free-threaded CPython, compare receipts, and inspect results.
"""
from __future__ import annotations

import argparse
import json
import sys
import sysconfig
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256


def probe(workers: int = 4, occurrences: int = 128) -> dict[str, object]:
    if not (1 <= workers <= 64 and 1 <= occurrences <= 100000):
        raise ValueError("workers and occurrences outside bounded test range")

    def tile(index: int) -> tuple[int, str]:
        payload = f"SIGIL:RUNTILE:{index}".encode("ascii")
        return index, sha256(payload).hexdigest()

    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(tile, range(occurrences)))
    assert [index for index, _ in results] == list(range(occurrences))
    assert len({index for index, _ in results}) == occurrences
    serial = [tile(i) for i in range(occurrences)]
    assert results == serial, "parallel replay differs from serial reference"
    return {
        "schema": "SIGIL_RUNTILE_CPYTHON_FREETHREADING_PROBE_V1",
        "python": sys.version.split()[0],
        "free_threaded_build": bool(sysconfig.get_config_var("Py_GIL_DISABLED")),
        "gil_enabled": sys._is_gil_enabled() if hasattr(sys, "_is_gil_enabled") else None,
        "workers": workers,
        "occurrences": occurrences,
        "replay_equal": True,
        "digest": sha256("".join(x[1] for x in results).encode("ascii")).hexdigest(),
        "speedup_proved": False,
        "extension_thread_safety_proved": False,
        "external_effects": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--occurrences", type=int, default=128)
    args = parser.parse_args()
    print(json.dumps(probe(args.workers, args.occurrences), sort_keys=True))


if __name__ == "__main__":
    main()
