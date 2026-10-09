# SPDX-License-Identifier: MIT
"""Tests for the strict typed PACAPDG/PYPL interface: no authority effect."""
from __future__ import annotations

import copy
from hashlib import sha256
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pypl_typed_interface_v1 import (  # noqa: E402
    IntegrationVerdict, TypedShapeError, decode_request, evaluate_typed_request,
)

FIXTURE = Path(__file__).resolve().parent / "fixtures/pypl_sym_request_v1.json"


class TypedPYPLTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.name = "Tools/sigil4cpython/demo.sym"
        dest = self.root / self.name
        dest.parent.mkdir(parents=True)
        dest.write_text("GAME SAFE {}\n", encoding="utf-8")
        self.data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.data["artifacts"] = [
            {"path": self.name, "sha256": sha256(dest.read_bytes()).hexdigest()}
        ]

    def test_public_manifest_decodes_losslessly(self) -> None:
        raw = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(decode_request(raw).as_payload(), raw)

    def test_candidate_stays_hold(self) -> None:
        decision = evaluate_typed_request(self.data, self.root)
        self.assertEqual(decision.verdict, "HOLD_QUNO")
        self.assertEqual(len(decision.quno), 4)
        self.assertFalse(decision.source_plan_complete)
        self.assertEqual(decision.uap, "UNJUDGED")
        self.assertFalse(decision.cpython_upstream_requested)

    def test_valid_shape_with_dummy_refs_is_only_source_plan(self) -> None:
        for key in self.data["evidence"]:
            self.data["evidence"][key] = "fixture:not-verified"
        decision = evaluate_typed_request(self.data, self.root)
        self.assertEqual(decision.verdict, "ADMIT_SOURCE_PLAN")
        self.assertTrue(decision.source_plan_complete)
        self.assertFalse(decision.review_authenticity_verified)
        self.assertFalse(decision.external_effect)
        self.assertFalse(decision.cpython_upstream_accepted)

    def test_wrong_bool_type_rejected(self) -> None:
        self.data["boundaries"]["no_runtime_effect"] = 1
        self.assertEqual(evaluate_typed_request(self.data, self.root).verdict, "REJECT")

    def test_bad_artifact_shape_rejected(self) -> None:
        self.data["artifacts"][0]["execute"] = True
        result = evaluate_typed_request(self.data, self.root)
        self.assertIn("invalid_artifact_shape", result.errors)

    def test_invalid_request_string_types_rejected(self) -> None:
        self.data["request_id"] = ["not", "a", "string"]
        self.assertEqual(evaluate_typed_request(self.data, self.root).verdict, "REJECT")

    def test_unknown_request_key_rejected(self) -> None:
        self.data["submit_to_cpython"] = True
        self.assertEqual(evaluate_typed_request(self.data, self.root).verdict, "REJECT")

    def test_invalid_projection_rejected(self) -> None:
        self.data["projection"] = "EXECUTE"
        self.assertEqual(evaluate_typed_request(self.data, self.root).verdict, "REJECT")

    def test_missing_artifact_holds(self) -> None:
        self.data["artifacts"][0]["path"] = "Tools/sigil4cpython/missing.sym"
        self.assertEqual(evaluate_typed_request(self.data, self.root).verdict, "HOLD_QUNO")

    def test_tampered_artifact_rejected(self) -> None:
        (self.root / self.name).write_text("GAME BAD {}\n", encoding="utf-8")
        self.assertEqual(evaluate_typed_request(self.data, self.root).verdict, "REJECT")

    def test_new_evidence_not_coerced_from_null(self) -> None:
        self.data["evidence"]["author_review_ref"] = None
        self.assertIsNone(decode_request(self.data).evidence.author_review_ref)
        self.assertEqual(evaluate_typed_request(self.data, self.root).verdict, "HOLD_QUNO")

    def test_bool_evidence_rejected(self) -> None:
        self.data["evidence"]["local_tests_ref"] = True
        self.assertEqual(evaluate_typed_request(self.data, self.root).verdict, "REJECT")

    def test_result_cannot_claim_external_effect(self) -> None:
        with self.assertRaises(ValueError):
            IntegrationVerdict("ADMIT_SOURCE_PLAN", "r", (), (), "", True,
                               external_effect=True)

    def test_result_cannot_claim_upstream_submission(self) -> None:
        with self.assertRaises(ValueError):
            IntegrationVerdict("HOLD_QUNO", "r", (), ("w",), "", False,
                               cpython_upstream_requested=True)

    def test_result_must_match_status(self) -> None:
        with self.assertRaises(ValueError):
            IntegrationVerdict("REJECT", None, ("error",), (), "", True)

    def test_input_is_not_mutated(self) -> None:
        snapshot = copy.deepcopy(self.data)
        evaluate_typed_request(self.data, self.root)
        self.assertEqual(self.data, snapshot)


if __name__ == "__main__":
    unittest.main()
