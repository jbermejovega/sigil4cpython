from __future__ import annotations

from dataclasses import replace
import unittest

from sigil4cpython.polyaria_pushout import (
    BoundaryWitness,
    PolyariaEvent,
    PublicPort,
    PublicSection,
    PublicSpan,
    Verdict,
    compile_public_pushout,
    plan_polyaria_event,
)


class PolyariaPushoutTests(unittest.TestCase):
    def setUp(self):
        common = PublicSection("C", "PACA_PDG", "PI:fixed", (
            PublicPort("music", "Music:Plural", "c:music", ("plan",)),
            PublicPort("quno", "QUNO:Relational", "c:quno", ("plan",)),
        ))
        left = PublicSection("A", "SonicPi:OSC", "PI:fixed", (
            PublicPort("music_a", "Music:Plural", "left:1", ("plan", "sonicpi")),
            PublicPort("quno_a", "QUNO:Relational", "left:2", ("plan",)),
            PublicPort("extra_a", "Ultravioleta:Modulation", "left:3", ("plan",)),
        ))
        right = PublicSection("B", "CPython:Public", "PI:fixed", (
            PublicPort("music_b", "Music:Plural", "right:1", ("plan", "cpython")),
            PublicPort("quno_b", "QUNO:Relational", "right:2", ("plan",)),
        ))
        self.span = PublicSpan(common, left, right, (
            BoundaryWitness("music", "music_a", "music_b", "w:music", "trace:music"),
            BoundaryWitness("quno", "quno_a", "quno_b", "w:quno", "trace:quno"),
        ))
        self.event = PolyariaEvent("sigilbook", 0, "occ:1", "SIGILA", 0.4,
                                   "w:event", "trace:event")

    def test_pushout_preserves_distinct_occurrences(self):
        plan = compile_public_pushout(self.span)
        self.assertEqual(plan.verdict, Verdict.ADMIT)
        self.assertEqual(len(plan.classes), 3)
        self.assertTrue(any(c.members == ("L:music_a", "R:music_b") for c in plan.classes))
        self.assertTrue(any(c.members == ("L:extra_a",) for c in plan.classes))
        self.assertTrue(all(len(c.occurrence_refs) == len(c.members) for c in plan.classes))
        self.assertEqual(plan.digest, compile_public_pushout(self.span).digest)

    def test_missing_boundary_is_quno(self):
        plan = compile_public_pushout(replace(self.span, witnesses=self.span.witnesses[:1]))
        self.assertEqual(plan.verdict, Verdict.HOLD)
        self.assertEqual(plan.classes, ())
        self.assertIn("missing_boundary:quno", plan.quno)

    def test_forged_type_and_capability_rejected(self):
        right = replace(self.span.right, ports=(
            replace(self.span.right.ports[0], interface_id="Wrong"),
            self.span.right.ports[1],
        ))
        self.assertEqual(compile_public_pushout(replace(self.span, right=right)).verdict,
                         Verdict.REJECT)
        common = replace(self.span.common, ports=(
            replace(self.span.common.ports[0], capabilities=("execute",)),
            self.span.common.ports[1],
        ))
        self.assertIn("capability_intersection_failure:music",
                      compile_public_pushout(replace(self.span, common=common)).errors)

    def test_protected_boundaries_fail_closed(self):
        self.assertEqual(compile_public_pushout(replace(self.span,
                         no_authority_transport=False)).verdict, Verdict.REJECT)
        self.assertEqual(compile_public_pushout(replace(self.span,
                         runtime_executed=True)).verdict, Verdict.REJECT)
        self.assertEqual(compile_public_pushout(replace(self.span,
                         private_source_payload_included=True)).verdict, Verdict.REJECT)
        edge = replace(self.span.witnesses[0], no_identity_transport=False)
        self.assertEqual(compile_public_pushout(replace(self.span,
                         witnesses=(edge, self.span.witnesses[1]))).verdict, Verdict.REJECT)

    def test_unknown_endpoint_and_noninjective_leg(self):
        bad = replace(self.span.witnesses[0], right_port_id="missing")
        self.assertIn("unknown_boundary_port:music", compile_public_pushout(
            replace(self.span, witnesses=(bad, self.span.witnesses[1]))).errors)
        bad = replace(self.span.witnesses[1], left_port_id="music_a")
        self.assertIn("non_injective_leg:quno", compile_public_pushout(
            replace(self.span, witnesses=(self.span.witnesses[0], bad))).errors)

    def test_missing_witness_holds(self):
        edge = replace(self.span.witnesses[0], witness_id="")
        result = compile_public_pushout(replace(self.span,
                         witnesses=(edge, self.span.witnesses[1])))
        self.assertEqual(result.verdict, Verdict.HOLD)
        self.assertEqual(result.classes, ())

    def test_four_distinct_operator_plans(self):
        plan = compile_public_pushout(self.span)
        for operator, action in (("NAMO", "descending_motif"),
                                  ("TAE", "melodic_incidence"),
                                  ("REKOKO", "fresh_occurrence"),
                                  ("SIGILA", "plural_chord")):
            with self.subTest(operator=operator):
                event = replace(self.event, operator=operator)
                result = plan_polyaria_event(event, plan)
                self.assertEqual(result.verdict, Verdict.ADMIT)
                self.assertIn(action, result.semantic_actions)

    def test_replay_is_rejected(self):
        plan = compile_public_pushout(self.span)
        result = plan_polyaria_event(self.event, plan,
                                    frozenset({("sigilbook", 0, "occ:1")}))
        self.assertEqual(result.verdict, Verdict.REJECT)
        self.assertIn("duplicate_occurrence_replay", result.reasons)
        fresh = replace(self.event, occurrence="occ:2", operator="REKOKO")
        self.assertEqual(plan_polyaria_event(fresh, plan,
                        frozenset({("sigilbook", 0, "occ:1")})).verdict, Verdict.ADMIT)

    def test_quno_and_rejection_event_edges(self):
        plan = compile_public_pushout(self.span)
        self.assertEqual(plan_polyaria_event(replace(self.event, witness_id=""),
                         plan).verdict, Verdict.HOLD)
        self.assertEqual(plan_polyaria_event(replace(self.event, ultraviolet=float("nan")),
                         plan).verdict, Verdict.REJECT)
        self.assertEqual(plan_polyaria_event(replace(self.event, epoch=True),
                         plan).verdict, Verdict.REJECT)
        self.assertEqual(plan_polyaria_event(replace(self.event, operator="XYZ"),
                         plan).verdict, Verdict.REJECT)


if __name__ == "__main__":
    unittest.main()
