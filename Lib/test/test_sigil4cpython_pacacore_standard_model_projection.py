from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

MODULE = Path(__file__).parents[1] / "sigil4cpython" / "pacacore_standard_model_projection.py"
spec = importlib.util.spec_from_file_location("pacacore_projection", MODULE)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def test_projection_is_deterministic_and_valid():
    first = module.build_pacacore_standard_model_projection()
    second = module.build_pacacore_standard_model_projection()
    assert first == second
    assert module.validate_pacacore_standard_model_projection(first)


def test_projection_is_dependency_free_and_inert():
    value = module.build_pacacore_standard_model_projection()
    assert value.dependency_free and not value.pydantic_imported
    assert not value.interpreter_semantics_changed
    assert not value.abi_changed
    assert not value.runtime_executed
    assert not value.final_kapsyla


def test_transport_is_deprecated_and_replay_is_canonical():
    value = module.build_pacacore_standard_model_projection()
    assert value.transport_deprecated
    assert value.safe_replay
    assert value.pi_fixed
    assert value.identity_transport is False


def test_source_epoch_is_exact():
    value = module.build_pacacore_standard_model_projection()
    assert value.source_pull_request == 750
    assert value.source_sha == "4c94b3f847cc26b17d3e54cc253c1f99655ea6fb"
    assert value.source_bundle_sha256 == "5b343a2fffb3f25e81567e42072b9f5cdbf38bd049f0496b4dea980b22e0aa05"
    assert value.source_replay_tip == "b73c37879d7b7f9c3fea2b4b89d53848333c204adfeda6169dd595444c524261"
