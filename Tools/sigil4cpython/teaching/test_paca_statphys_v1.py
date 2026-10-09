# SPDX-License-Identifier: MIT
"""Finite numerical and provenance tests for PACA GUAPA / UAP4 statphys."""
import json
import math
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paca_statphys_v1 import (
    Ring, energy, exact_equilibrium, metropolis_probability, source_receipt, trajectory
)


class TestPacaStatphys(unittest.TestCase):
    def setUp(self):
        self.ring = Ring(("jara", "sigila", "lilith"), coupling=1)

    def test_edges_unique_sites(self):
        self.assertEqual(self.ring.edges, (("jara", "sigila"),
                                            ("sigila", "lilith"),
                                            ("lilith", "jara")))

    def test_identical_values_not_identical_sites(self):
        self.assertEqual(energy(self.ring, (1, 1, 1)), -3)
        self.assertNotEqual(self.ring.sites[0], self.ring.sites[1])

    def test_single_flip_cost(self):
        self.assertEqual(energy(self.ring, (-1, 1, 1)), 1)

    def test_field_term(self):
        model = Ring(self.ring.sites, field=2)
        self.assertEqual(energy(model, (1, 1, 1)), -9)

    def test_invalid_assignments_rejected(self):
        for state in ((1, 1), (1, 1, 0), (1, True, 1)):
            with self.assertRaises(ValueError):
                energy(self.ring, state)

    def test_sites_must_be_immutable_tuple(self):
        with self.assertRaises(ValueError):
            Ring(["a", "b", "c"])

    def test_beta_boolean_and_excess_rejected(self):
        for value in (True, float("inf"), 10001.0):
            with self.assertRaises(ValueError):
                metropolis_probability(4, value)

    def test_initial_mutable_list_rejected(self):
        with self.assertRaises(ValueError):
            trajectory(self.ring, beta=0.2, steps=1, seed=1, initial=[1,1,1])

    def test_bad_site_identity_rejected(self):
        with self.assertRaises(ValueError):
            Ring(("same", "same", "other"))

    def test_negative_temperature_parameter_rejected(self):
        with self.assertRaises(ValueError):
            exact_equilibrium(self.ring, -0.2)

    def test_detailed_balance_ratio(self):
        beta = 0.4
        self.assertAlmostEqual(
            metropolis_probability(4, beta) / metropolis_probability(-4, beta),
            math.exp(-4 * beta)
        )

    def test_zero_beta_partition(self):
        e = exact_equilibrium(self.ring, 0)
        self.assertAlmostEqual(e["log_partition"], math.log(8))
        self.assertAlmostEqual(e["mean_energy"], 0)
        self.assertAlmostEqual(e["heat_capacity_kB1"], 0)

    def test_ising_three_partition(self):
        b = 0.7
        result = exact_equilibrium(self.ring, b)
        self.assertAlmostEqual(result["log_partition"],
                               math.log(2 * math.exp(3*b)+6*math.exp(-b)))

    def test_trace_balanced_unique(self):
        final, trace = trajectory(self.ring, beta=0.3, steps=48, seed=42)
        self.assertEqual(len(trace), 48)
        self.assertEqual(len(set(x.occurrence for x in trace)), 48)
        self.assertTrue(all(x.balanced and x.uap == "UNJUDGED" for x in trace))
        self.assertEqual(energy(self.ring, final), trace[-1].after_energy)
        self.assertEqual(trace[1].parent, trace[0].occurrence)

    def test_deterministic_seed(self):
        a = trajectory(self.ring, beta=0.9, steps=50, seed=11)
        b = trajectory(self.ring, beta=0.9, steps=50, seed=11)
        self.assertEqual(a, b)

    def test_bounded_steps(self):
        with self.assertRaises(ValueError):
            trajectory(self.ring, beta=1, steps=10001, seed=1)

    def test_receipt_is_not_authority(self):
        final, trace = trajectory(self.ring, beta=0, steps=1, seed=0)
        d = source_receipt(self.ring, final, trace)
        self.assertFalse(d["external_effect"])
        self.assertFalse(d["safe_to_ship"])
        self.assertEqual(d["uap"], "UNJUDGED")
        self.assertEqual(d["trace"][0]["pacapdg"], "ADMIT_SOURCE_PLAN")

    def test_cli_equilibrium_json(self):
        cli = Path(__file__).with_name("paca_statphys_cli.py")
        p = subprocess.run([sys.executable, str(cli), "equilibrium",
                            "--sites", "3", "--beta", "0"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertAlmostEqual(json.loads(p.stdout)["log_partition"], math.log(8))

    def test_cli_oversized_sites_rejected(self):
        cli = Path(__file__).with_name("paca_statphys_cli.py")
        p = subprocess.run([sys.executable, str(cli), "equilibrium",
                            "--sites", "100000000"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertIn("--sites must be between 3 and 12", p.stderr)

    def test_cli_simulate_json(self):
        cli = Path(__file__).with_name("paca_statphys_cli.py")
        p = subprocess.run([sys.executable, str(cli), "play",
                            "--sites", "3", "--beta", "0",
                            "--steps", "4", "--seed", "42"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(len(json.loads(p.stdout)["trace"]), 4)


if __name__ == "__main__":
    unittest.main()
