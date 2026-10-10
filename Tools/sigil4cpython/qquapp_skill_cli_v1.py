# SPDX-License-Identifier: MIT
"""QQUAPP Universal APP: offline, inert CLI for typed skill interfaces.

Examples are synthetic and source-only. Optional --learn updates an in-memory
scikit-learn model; no model is persisted and no action is authorized.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json

from qquapp_transferable_skill_v1 import (
    Arrow, PullbackDiagram, PushoutDiagram, SkillPort, Witness,
    pullback_set, pushout_set, transferable_skill,
)


def example(*, learn: bool = False) -> dict[str, object]:
    teacher = SkillPort("teacher", "ISING_BINARY", ("energy", "magnetization"),
                        ("ordered", "disordered"), "classroom", "teacher:1",
                        "sigilbook:public-teaching", ("read", "learn", "present"))
    student = SkillPort("student", "ISING_BINARY", ("energy", "magnetization"),
                        ("ordered", "disordered"), "workshop", "student:1",
                        "qquapp:offline-demo", ("read", "learn"))
    pull = pullback_set(PullbackDiagram(
        ("ising",), (teacher,), (student,),
        (Arrow("teacher", "ising"),), (Arrow("student", "ising"),),
        (Witness("teacher|student", "public-demo:teacher-student"),),
    ))
    push = pushout_set(PushoutDiagram(
        ("shared-ising",), (teacher,), (student,),
        (Arrow("shared-ising", "teacher"),),
        (Arrow("shared-ising", "student"),),
        (Witness("shared-ising", "public-demo:shared-contract"),),
    ))
    transfer = transferable_skill(teacher, student, "public-demo:consented-learning")
    ml: dict[str, object] = {
        "status": "HOLD_QUNO:OPT_IN_REQUIRED", "decision_authority": False,
        "uap": "UNJUDGED", "external_effect": False,
    }
    if learn:
        try:
            from qquapp_incremental_skill_v1 import IncrementalSkill
            learner = IncrementalSkill(features=teacher.features,
                                       classes=teacher.classes, occurrence="student:epoch:2")
            # Synthetic demonstration data: never attributed to students.
            learner.calibrate([[-2, -1], [-1, -1], [1, 1], [2, 1]])
            learner.learn([[-2, -1], [2, 1]], ["ordered", "disordered"], epoch=1)
            learner.learn([[-1, -1], [1, 1]], ["ordered", "disordered"], epoch=2)
            prediction = learner.advise([[1, 1]])
            ml = {**asdict(prediction), "training_batched": learner.batches,
                  "synthetic_data": True}
        except ImportError:
            ml = {"status": "HOLD_QUNO:SCIKIT_LEARN_UNAVAILABLE",
                  "uap": "UNJUDGED", "external_effect": False,
                  "decision_authority": False}
    return {
        "app": "QQUAPP_UNIVERSAL_TRANSFERABLE_SKILL_V1",
        "root": "SIGILBOOK_TOTAL_VOID_AST_OF_ALL_ASTS_V1",
        "pullback": asdict(pull),
        "pushout": asdict(push),
        "transfer": asdict(transfer),
        "learning": ml,
        "live_repository_push": False,
        "cpython_upstream_requested": False,
        "uap": "UNJUDGED",
        "release_certified": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("demo",))
    parser.add_argument("--learn", action="store_true",
                        help="opt into bounded synthetic-data in-memory sklearn training")
    args = parser.parse_args(argv)
    print(json.dumps(example(learn=args.learn), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
