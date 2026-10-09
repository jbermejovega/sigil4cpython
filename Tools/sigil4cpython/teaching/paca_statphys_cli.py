#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""PACA KORE CLI: finite, offline statistical-physics lesson, JSON output only."""
import argparse
import json

from paca_statphys_v1 import Ring, exact_equilibrium, source_receipt, trajectory


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("equilibrium", "play"):
        p = commands.add_parser(command)
        p.add_argument("--sites", type=int, default=4)
        p.add_argument("--coupling", type=int, default=1)
        p.add_argument("--field", type=int, default=0)
        p.add_argument("--beta", type=float, default=0.5)
        if command == "play":
            p.add_argument("--steps", type=int, default=12)
            p.add_argument("--seed", type=int, default=42)
    args = parser.parse_args(argv)
    ring = Ring(tuple(f"site_{i}" for i in range(args.sites)),
                coupling=args.coupling, field=args.field)
    if args.command == "equilibrium":
        out = exact_equilibrium(ring, args.beta)
    else:
        spins, trace = trajectory(ring, beta=args.beta,
                                  steps=args.steps, seed=args.seed)
        out = source_receipt(ring, spins, trace)
    print(json.dumps(out, sort_keys=True, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
