"""Focused source-only PACA .sym grammar and transition tests."""
import unittest
from pathlib import Path

from paca_sym_game_v1 import (
    SymMove, initial_state, load_sym, parse_sym, step,
)

FIXTURE = Path(__file__).resolve().parent / "fixtures/namotae.sym"


def move(name, epoch, event_id, **kwargs):
    return SymMove(name, "test", event_id, epoch, witness_ref="w:local:fixture",
                   consent_declared=True, pacapdg_declared=True, **kwargs)


class TestSymGame(unittest.TestCase):
    def setUp(self):
        self.game = load_sym(FIXTURE)
        self.start = initial_state(self.game)

    def test_source_is_accepted(self):
        self.assertEqual(self.game.initial, "MOONLIGHT")
        self.assertEqual([t.name for t in self.game.transitions],
                         ["NAMO", "TAE", "REKOKO", "SIGILA"])

    def test_namo_tae_sigila(self):
        a = step(self.game, self.start, move("NAMO", 0, "a"))
        b = step(self.game, a.after, move("TAE", 1, "b"))
        c = step(self.game, b.after, move("SIGILA", 2, "c"))
        self.assertEqual((a.verdict, b.verdict, c.verdict),
                         ("ADMIT_SOURCE_PLAN",) * 3)
        self.assertEqual(c.after.state, "HARMONY")
        self.assertEqual(c.after.epoch, 3)
        self.assertEqual(len(c.after.trace), 3)
        self.assertNotEqual(a.after.occurrence, b.after.occurrence)
        self.assertTrue(all(not x.external_effect and x.uap == "UNJUDGED"
                            for x in (a, b, c)))

    def test_rekoko_fresh(self):
        a = step(self.game, self.start, move("NAMO", 0, "a")).after
        b = step(self.game, a, move("TAE", 1, "b")).after
        c = step(self.game, b, move("REKOKO", 2, "c")).after
        self.assertEqual(c.state, "RELATION")
        self.assertEqual(c.trace[-1].parent_occurrence, b.occurrence)
        self.assertNotEqual(c.occurrence, b.occurrence)

    def test_replayed_key_holds(self):
        a = step(self.game, self.start, move("NAMO", 0, "a")).after
        dup = step(self.game, a, move("TAE", 1, "a"))
        self.assertEqual(dup.verdict, "HOLD_QUNO")
        self.assertEqual(dup.after, a)

    def test_stale_epoch_holds(self):
        self.assertEqual(step(self.game, self.start, move("NAMO", 1, "a")).verdict,
                         "HOLD_QUNO")

    def test_missing_witness_holds(self):
        m = SymMove("NAMO", "test", "a", 0, consent_declared=True,
                    pacapdg_declared=True)
        self.assertEqual(step(self.game, self.start, m).verdict, "HOLD_QUNO")

    def test_missing_consent_holds(self):
        m = SymMove("NAMO", "test", "a", 0, witness_ref="w", pacapdg_declared=True)
        self.assertEqual(step(self.game, self.start, m).verdict, "HOLD_QUNO")

    def test_invalid_transition_rejected(self):
        self.assertEqual(step(self.game, self.start, move("TAE", 0, "a")).verdict,
                         "REJECT")
        self.assertEqual(step(self.game, self.start, move("UNKNOWN", 0, "a")).verdict,
                         "REJECT")

    def test_undeclared_state_rejected(self):
        content = FIXTURE.read_text(encoding="utf-8").replace(
            "TO HARMONY", "TO NONEXISTENT")
        with self.assertRaises(ValueError):
            parse_sym(content)

    def test_duplicate_transition_rejected(self):
        content = FIXTURE.read_text(encoding="utf-8").replace(
            "  TRANSITION SIGILA", "  TRANSITION NAMO")
        with self.assertRaises(ValueError):
            parse_sym(content)

    def test_grammar_refuses_code_execution(self):
        with self.assertRaises(ValueError):
            parse_sym(FIXTURE.read_text(encoding="utf-8").replace(
                "  STATE WEAVE;", "  import os;"))


if __name__ == "__main__":
    unittest.main()
