# SPDX-License-Identifier: MIT
"""Unit tests for the inert PYPL integration-request gate."""
from __future__ import annotations

import copy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pypl_integration_request_v1 import (  # noqa: E402
    SCHEMA_ID, evaluate_request,
)


class PYPLRequestGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.path = "Tools/sigil4cpython/demo.sym"
        file = self.root / self.path
        file.parent.mkdir(parents=True)
        file.write_text("GAME SAFE {}\n", encoding="utf-8")
        self.data = {
            "schema_id": SCHEMA_ID,
            "request_id": "SYM_GAME_DEMO_V1",
            "source_repository": "jbermejovega/sigilbook",
            "source_commit": "a" * 40,
            "target_repository": "jbermejovega/sigil4cpython",
            "target_base_commit": "b" * 40,
            "projection": "PUBLIC_SOURCE_ONLY_PYPL",
            "artifacts": [
                {"path": self.path, "sha256": sha256(file.read_bytes()).hexdigest()}
            ],
            "evidence": {
                "local_tests_ref": "local:test-pass:example",
                "license_review_ref": "human-pending-verification:license",
                "maintainer_review_ref": "human-pending-verification:maintainer",
                "author_review_ref": "human-pending-verification:author",
            },
            "boundaries": {
                "no_private_payload": True,
                "no_cpython_internals": True,
                "no_runtime_effect": True,
                "no_authority_transport": True,
                "no_identity_transport": True,
                "ai_assisted_disclosed": True,
            },
        }

    def assess(self, data=None):
        return evaluate_request(self.data if data is None else data, self.root)

    def test_valid_is_only_source_plan(self):
        result = self.assess()
        self.assertEqual(result["verdict"], "ADMIT_SOURCE_PLAN")
        self.assertTrue(result["request_ready_for_review"])
        self.assertFalse(result["cpython_upstream_requested"])
        self.assertFalse(result["review_authenticity_verified"])
        self.assertFalse(result["external_effect"])
        self.assertEqual(result["uap"], "UNJUDGED")

    def test_empty_review_reference_holds(self):
        data = copy.deepcopy(self.data)
        data["evidence"]["maintainer_review_ref"] = ""
        self.assertEqual(self.assess(data)["verdict"], "HOLD_QUNO")

    def test_missing_file_holds(self):
        data = copy.deepcopy(self.data)
        data["artifacts"][0]["path"] = "Tools/sigil4cpython/absent.sym"
        result = self.assess(data)
        self.assertEqual(result["verdict"], "HOLD_QUNO")
        self.assertTrue(any("artifact_missing:" in q for q in result["quno"]))

    def test_unresolved_sha256_holds(self):
        data = copy.deepcopy(self.data)
        data["artifacts"][0]["sha256"] = ""
        self.assertEqual(self.assess(data)["verdict"], "HOLD_QUNO")

    def test_changed_bytes_rejected(self):
        (self.root / self.path).write_text("GAME TAMPERED {}\n", encoding="utf-8")
        result = self.assess()
        self.assertEqual(result["verdict"], "REJECT")
        self.assertTrue(any("digest_mismatch:" in e for e in result["errors"]))

    def test_parent_traversal_rejected(self):
        data = copy.deepcopy(self.data)
        data["artifacts"][0]["path"] = "Tools/sigil4cpython/../../secret.sym"
        self.assertEqual(self.assess(data)["verdict"], "REJECT")

    def test_escape_by_symlink_rejected(self):
        # With a symlink to outside root, normalization cannot stay in root.
        outside = self.root.parent / (self.root.name + "-external.sym")
        outside.write_text("EXTERNAL", encoding="utf-8")
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        link = self.root / "Tools/sigil4cpython/outside.sym"
        try:
            link.symlink_to(outside)
        except (NotImplementedError, OSError):
            self.skipTest("symlinks unavailable")
        data = copy.deepcopy(self.data)
        data["artifacts"][0]["path"] = "Tools/sigil4cpython/outside.sym"
        self.assertEqual(self.assess(data)["verdict"], "REJECT")

    def test_cpython_internal_path_rejected(self):
        data = copy.deepcopy(self.data)
        data["artifacts"][0]["path"] = "Include/internal/pycore_interp.h"
        self.assertEqual(self.assess(data)["verdict"], "REJECT")

    def test_wrong_target_rejected(self):
        data = copy.deepcopy(self.data)
        data["target_repository"] = "python/cpython"
        self.assertEqual(self.assess(data)["verdict"], "REJECT")

    def test_forbidden_effect_rejected(self):
        data = copy.deepcopy(self.data)
        data["boundaries"]["no_runtime_effect"] = False
        self.assertEqual(self.assess(data)["verdict"], "REJECT")

    def test_duplicate_artifacts_rejected(self):
        data = copy.deepcopy(self.data)
        data["artifacts"].append(dict(data["artifacts"][0]))
        self.assertEqual(self.assess(data)["verdict"], "REJECT")

    def test_invalid_sha_ref_rejected(self):
        data = copy.deepcopy(self.data)
        data["source_commit"] = "branch-name"
        self.assertEqual(self.assess(data)["verdict"], "REJECT")

    def test_unexpected_keys_rejected(self):
        data = copy.deepcopy(self.data)
        data["submit_upstream"] = True
        self.assertEqual(self.assess(data)["verdict"], "REJECT")

    def test_cli_is_observational(self):
        path = self.root / "request.json"
        path.write_text(json.dumps(self.data), encoding="utf-8")
        tool = Path(__file__).with_name("pypl_integration_request_v1.py")
        run = subprocess.run(
            [sys.executable, str(tool), str(path), "--root", str(self.root)],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        self.assertFalse(result["cpython_upstream_requested"])
        self.assertEqual(result["verdict"], "ADMIT_SOURCE_PLAN")


if __name__ == "__main__":
    unittest.main()
