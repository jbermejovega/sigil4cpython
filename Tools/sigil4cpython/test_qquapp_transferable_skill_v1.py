# SPDX-License-Identifier: MIT
"""Focused finite Set universal-property and optional sklearn tests."""
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


M = load("qquapp_transferable_skill_v1",
         "Tools/sigil4cpython/qquapp_transferable_skill_v1.py")
L = load("qquapp_incremental_skill_v1",
         "Tools/sigil4cpython/qquapp_incremental_skill_v1.py")


def p(name, occurrence=None, *, ctx="teacher", cap=("read", "learn"), features=("energy", "magnetization")):
    return M.SkillPort(name, "STATPHYS_ISING", features, ("ordered", "disordered"), ctx,
                       occurrence or ("occ:"+name+":"+ctx), "source:"+name, cap)


class TestQQUAPPFinite(unittest.TestCase):
    def setUp(self):
        self.l = (p("a"), p("b"))
        self.r = (p("x", ctx="student"), p("y", ctx="student"))
        self.pull = M.PullbackDiagram(("ising", "rest"), self.l, self.r,
            (M.Arrow("a", "ising"), M.Arrow("b", "rest")),
            (M.Arrow("x", "ising"), M.Arrow("y", "rest")),
            (M.Witness("a|x", "classroom:1"), M.Witness("b|y", "classroom:2")))
        self.push = M.PushoutDiagram(("shared",), self.l, self.r,
            (M.Arrow("shared", "a"),), (M.Arrow("shared", "x"),),
            (M.Witness("shared", "classroom:1"),))

    def test_pullback_pairs(self):
        result = M.pullback_set(self.pull)
        self.assertEqual(result.pairs_or_classes, (("a", "x"), ("b", "y")))
        self.assertEqual(result.verdict, "ADMIT_SOURCE_PLAN")
        self.assertFalse(result.external_effect)
        self.assertEqual(result.uap, "UNJUDGED")

    def test_pullback_is_fiber(self):
        result = M.pullback_set(self.pull)
        f = {x.source:x.target for x in self.pull.left_to_base}
        g = {x.source:x.target for x in self.pull.right_to_base}
        for a,b in result.pairs_or_classes:
            self.assertEqual(f[a],g[b])

    def test_missing_witness_holds(self):
        d = M.PullbackDiagram(self.pull.base,self.pull.left,self.pull.right,
            self.pull.left_to_base,self.pull.right_to_base,())
        self.assertEqual(M.pullback_set(d).verdict,"HOLD_QUNO")

    def test_bad_map_rejected(self):
        d = M.PullbackDiagram(self.pull.base,self.pull.left,self.pull.right,
            (M.Arrow("a","ising"),),self.pull.right_to_base,self.pull.pair_witnesses)
        with self.assertRaises(ValueError): M.pullback_set(d)

    def test_schema_mismatch_rejected(self):
        wrong = (p("x", ctx="student",features=("spin",)),self.r[1])
        d = M.PullbackDiagram(self.pull.base,self.pull.left,wrong,
            self.pull.left_to_base,self.pull.right_to_base,self.pull.pair_witnesses)
        with self.assertRaises(ValueError): M.pullback_set(d)

    def test_identity_collapse_rejected(self):
        bad=(p("x",self.l[0].occurrence,ctx="student"),self.r[1])
        d = M.PullbackDiagram(self.pull.base,self.pull.left,bad,
            self.pull.left_to_base,self.pull.right_to_base,self.pull.pair_witnesses)
        with self.assertRaises(ValueError): M.pullback_set(d)

    def test_pushout_classes_distinct_ports(self):
        result=M.pushout_set(self.push)
        self.assertEqual(result.verdict,"ADMIT_SOURCE_PLAN")
        self.assertEqual(len(result.pairs_or_classes),3)
        self.assertIn(("L:a","R:x"), result.pairs_or_classes)
        self.assertEqual(len(set(result.occurrence_refs)),4)

    def test_pushout_factorization(self):
        plan=M.pushout_set(self.push)
        f=M.factor_pushout(plan,self.push,{"a":"z","b":"left"},
                                            {"x":"z","y":"right"})
        self.assertEqual(len(f),3)
        self.assertEqual(f["L:a|R:x"],"z")

    def test_pushout_noncommuting_target_rejected(self):
        with self.assertRaises(ValueError):
            M.factor_pushout(M.pushout_set(self.push),self.push,
                             {"a":"z","b":"left"},{"x":"different","y":"right"})

    def test_pushout_missing_witness_holds(self):
        d=M.PushoutDiagram(self.push.base,self.push.left,self.push.right,
                           self.push.base_to_left,self.push.base_to_right,())
        self.assertEqual(M.pushout_set(d).verdict,"HOLD_QUNO")

    def test_transfer_source_only(self):
        plan=M.transferable_skill(self.l[0], self.r[0], "witness-1")
        self.assertEqual(plan.verdict,"ADMIT_SOURCE_PLAN")
        self.assertEqual(plan.capabilities,("learn","read"))
        self.assertFalse(plan.authority_transport)

    def test_transfer_missing_witness_holds(self):
        self.assertEqual(M.transferable_skill(self.l[0],self.r[0],"").verdict,"HOLD_QUNO")

    def test_transfer_capability_meet_empty_holds(self):
        other=p("z",ctx="student",cap=("write",))
        self.assertEqual(M.transferable_skill(self.l[0],other,"w").verdict,"HOLD_QUNO")

    def test_deterministic_hash(self):
        self.assertEqual(M.pushout_set(self.push).digest,M.pushout_set(self.push).digest)


class TestIncrementalLearner(unittest.TestCase):
    def setUp(self):
        try:
            self.a=L.IncrementalSkill(features=("E","M"),classes=("low","high"),occurrence="teacher:1")
        except ImportError:
            self.skipTest("optional sklearn is unavailable")

    def test_untrained_advice_rejected(self):
        with self.assertRaises(ValueError):self.a.advise([[0.,1.]])

    def test_hold_until_calibration(self):
        self.assertIn("HOLD_QUNO",self.a.learn([[0.,1.]], ["low"],epoch=1))

    def test_partial_fit_two_batches(self):
        self.a.calibrate([[0.,0.],[1.,1.],[2.,2.],[3.,3.]])
        self.assertTrue(self.a.learn([[0.,0.],[3.,3.]],["low","high"],epoch=1).startswith("ADMIT"))
        self.assertTrue(self.a.learn([[1.,1.],[2.,2.]],["low","high"],epoch=2).startswith("ADMIT"))
        result=self.a.advise([[0.,0.],[2.,2.]])
        self.assertEqual(len(result.labels),2)
        self.assertFalse(result.decision_authority)
        self.assertEqual(result.uap,"UNJUDGED")
        self.assertEqual(self.a.batches,2)

    def test_scaler_cannot_drift(self):
        self.a.calibrate([[0.,0.],[1.,1.]])
        with self.assertRaises(ValueError):self.a.calibrate([[2.,2.]])

    def test_epoch_replay_holds(self):
        self.a.calibrate([[0.,0.],[1.,1.]])
        self.a.learn([[0.,0.],[1.,1.]],["low","high"],epoch=1)
        self.assertEqual(self.a.learn([[0.,0.]], ["low"],epoch=1),"HOLD_QUNO:NONFRESH_EPOCH")

    def test_bad_feature_schema_rejected(self):
        with self.assertRaises(ValueError):self.a.calibrate([[1.,2.,3.]])

    def test_bad_label_rejected(self):
        self.a.calibrate([[0.,0.],[1.,1.]])
        with self.assertRaises(ValueError):self.a.learn([[0.,0.]],["unknown"],epoch=1)


if __name__ == "__main__": unittest.main()

class TestUniversalApp(unittest.TestCase):
    def test_demo_is_source_only(self):
        import subprocess, json
        p = __import__('subprocess').run(
            [sys.executable, str(ROOT / 'Tools/sigil4cpython/qquapp_skill_cli_v1.py'), 'demo'],
            env={**__import__('os').environ, 'PYTHONPATH': str(ROOT)},
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(p.returncode, 0, p.stderr)
        payload = json.loads(p.stdout)
        self.assertEqual(payload['pullback']['verdict'], 'ADMIT_SOURCE_PLAN')
        self.assertEqual(payload['pushout']['verdict'], 'ADMIT_SOURCE_PLAN')
        self.assertEqual(payload['transfer']['verdict'], 'ADMIT_SOURCE_PLAN')
        self.assertEqual(payload['learning']['status'], 'HOLD_QUNO:OPT_IN_REQUIRED')
        self.assertFalse(payload['live_repository_push'])
        self.assertFalse(payload['release_certified'])

    def test_explicit_synthetic_training_only_advises(self):
        try:
            import sklearn  # noqa: F401
        except ImportError:
            self.skipTest('optional scikit-learn missing')
        import subprocess, json
        p = subprocess.run([sys.executable, str(ROOT / 'Tools/sigil4cpython/qquapp_skill_cli_v1.py'),
                            'demo', '--learn'],
                           env={**__import__('os').environ, 'PYTHONPATH': str(ROOT)},
                           capture_output=True, text=True, check=False)
        self.assertEqual(p.returncode, 0, p.stderr)
        payload = json.loads(p.stdout)
        self.assertEqual(payload['learning']['training_batched'], 2)
        self.assertFalse(payload['learning']['decision_authority'])
        self.assertEqual(payload['learning']['verdict'], 'PREDICTION_ONLY')
