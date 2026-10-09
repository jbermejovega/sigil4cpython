# SPDX-License-Identifier: MIT
# Public, bounded projection of SIGILBOOK PACA .sym V1 (source-only).
"""SIGIL PACA .sym V1: pure symbolic game parser and source-only simulator.

This module never dispatches game, device, network, UAP or PACAPDG effects.
An input witness reference is descriptive, not authenticated authorization.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Literal

Verdict = Literal["ADMIT_SOURCE_PLAN", "HOLD_QUNO", "REJECT"]
_IDENT = r"[A-Za-z][A-Za-z0-9_]*"
_HEADER = re.compile(rf"GAME\s+({_IDENT})\s*\{{")
_ROOT = re.compile(rf"ROOT\s+({_IDENT});")
_TYPE = re.compile(r"TYPE\s+PACA_PDG<SymbolicGame,PLURAL,QUNO>;")
_STATE = re.compile(rf"STATE\s+({_IDENT});")
_INITIAL = re.compile(rf"INITIAL\s+({_IDENT});")
_TRANSITION = re.compile(
    rf"TRANSITION\s+({_IDENT})\s+FROM\s+({_IDENT})\s+TO\s+({_IDENT})\s+VIA\s+({_IDENT});"
)
ROOT = "SIGILBOOK_TOTAL_VOID_AST_OF_ALL_ASTS_V1"


@dataclass(frozen=True)
class Transition:
    name: str
    source_state: str
    destination: str
    witness_kind: str


@dataclass(frozen=True)
class SymGame:
    name: str
    root: str
    states: tuple[str, ...]
    initial: str
    transitions: tuple[Transition, ...]


@dataclass(frozen=True)
class Trace:
    source: str
    event_id: str
    transition: str
    witness_ref: str
    parent_occurrence: str
    occurrence: str
    epoch: int


@dataclass(frozen=True)
class SymState:
    game: str
    state: str
    epoch: int
    occurrence: str
    seen: frozenset[tuple[str, str]] = frozenset()
    trace: tuple[Trace, ...] = ()


@dataclass(frozen=True)
class SymMove:
    transition: str
    source: str
    event_id: str
    expected_epoch: int
    witness_ref: str = ""
    consent_declared: bool = False
    pacapdg_declared: bool = False


@dataclass(frozen=True)
class SymDecision:
    verdict: Verdict
    before: SymState
    after: SymState
    reason: str
    uap: Literal["UNJUDGED"] = "UNJUDGED"
    external_effect: bool = False


def parse_sym(source: str) -> SymGame:
    """Parse only the declared line-oriented V1 grammar; never eval expressions."""
    lines = [line.strip() for line in source.splitlines()
             if line.strip() and not line.lstrip().startswith("#")]
    if len(lines) < 5:
        raise ValueError("incomplete .sym game")
    head = _HEADER.fullmatch(lines[0])
    if not head or lines[-1] != "}":
        raise ValueError("expected GAME Name { ... }")
    game = head.group(1)
    roots: list[str] = []
    types = 0
    states: list[str] = []
    initials: list[str] = []
    transitions: list[Transition] = []
    for line in lines[1:-1]:
        if (m := _ROOT.fullmatch(line)):
            roots.append(m.group(1))
        elif _TYPE.fullmatch(line):
            types += 1
        elif (m := _STATE.fullmatch(line)):
            states.append(m.group(1))
        elif (m := _INITIAL.fullmatch(line)):
            initials.append(m.group(1))
        elif (m := _TRANSITION.fullmatch(line)):
            transitions.append(Transition(*m.groups()))
        else:
            raise ValueError(f"invalid .sym clause: {line!r}")
    if roots != [ROOT] or types != 1:
        raise ValueError("root and PACA_PDG type must be declared exactly once")
    if not states or len(states) != len(set(states)):
        raise ValueError("game must declare distinct states")
    if len(initials) != 1 or initials[0] not in states:
        raise ValueError("exactly one declared INITIAL state is required")
    if not transitions or len(transitions) != len({t.name for t in transitions}):
        raise ValueError("distinct named transitions are required")
    for t in transitions:
        if t.source_state not in states or t.destination not in states:
            raise ValueError(f"undefined state in transition {t.name}")
    return SymGame(game, roots[0], tuple(states), initials[0], tuple(transitions))


def load_sym(path: str | Path) -> SymGame:
    return parse_sym(Path(path).read_text(encoding="utf-8"))


def initial_state(game: SymGame) -> SymState:
    return SymState(game.name, game.initial, 0, f"{game.name}:GENESIS:0")


def step(game: SymGame, before: SymState, move: SymMove) -> SymDecision:
    """Pure, single-snapshot transition; not a durable dispatcher or policy oracle."""
    def out(verdict: Verdict, reason: str) -> SymDecision:
        return SymDecision(verdict, before, before, reason)

    if before.game != game.name or before.state not in game.states:
        return out("REJECT", "game/state mismatch")
    if move.expected_epoch != before.epoch:
        return out("HOLD_QUNO", "stale or future epoch")
    if not move.source.strip() or not move.event_id.strip():
        return out("HOLD_QUNO", "source and event_id required")
    key = (move.source, move.event_id)
    if key in before.seen:
        return out("HOLD_QUNO", "replayed occurrence: no new transition")
    matching = [t for t in game.transitions if t.name == move.transition]
    if not matching:
        return out("REJECT", "unknown transition")
    t = matching[0]
    if t.source_state != before.state:
        return out("REJECT", "transition incompatible with current state")
    if not move.witness_ref.strip() or not move.consent_declared or not move.pacapdg_declared:
        return out("HOLD_QUNO", "simulation witness/consent/PACAPDG declaration missing")

    # The fresh occurrence is only a symbolic source-plan ID, not an authority token.
    occurrence = f"{game.name}:{before.epoch + 1}:{move.source}:{move.event_id}"
    trace = Trace(move.source, move.event_id, t.name, move.witness_ref,
                  before.occurrence, occurrence, before.epoch + 1)
    after = SymState(game.name, t.destination, before.epoch + 1, occurrence,
                     before.seen | {key}, before.trace + (trace,))
    return SymDecision("ADMIT_SOURCE_PLAN", before, after,
                       "symbolic transition source plan only; UAP unjudged")
