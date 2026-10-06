import unittest

from sigil4cpython.primitive_typed_qquapp_ruleset_codebook import (
    PUBLICATION_CHECK,
    RuleKind,
    build_reference_publication_primitive,
    compile_kokompi_pattern,
    materialize_configuration,
    validate_publication_primitive,
)


class PrimitiveTypedRulesetCodebookTests(unittest.TestCase):
    def test_reference_publication_primitive_admits_source_plan(self):
        primitive = build_reference_publication_primitive(
            source_commit="67482d4f2f0ce4b803a8fb1d4d9c8fc8cf34ac21"
        )
        receipt = validate_publication_primitive(primitive)
        self.assertEqual(receipt.verdict, "ADMIT_SOURCE_PLAN")
        self.assertEqual(receipt.obligations, ())
        self.assertEqual(
            receipt.effective_capabilities,
            ("PLAN", "READ", "TYPECHECK"),
        )
        self.assertFalse(receipt.ruleset_mutation_executed)

    def test_every_public_type_is_plural_resource_relation_and_quno_typed(self):
        primitive = build_reference_publication_primitive()
        facets = [entry.facet for entry in primitive.codebook]
        facets += [resource.facet for resource in primitive.resources]
        facets += [relation.facet for relation in primitive.relations]
        facets += [
            primitive.krone_gate.facet,
            primitive.kokompi_pattern.facet,
            primitive.configuration_space.facet,
            primitive.ruleset.facet,
        ]
        for facet in facets:
            self.assertTrue(facet.plural_typed)
            self.assertTrue(facet.resource_typed)
            self.assertTrue(facet.relation_typed)
            self.assertTrue(facet.quno_typed)
            self.assertFalse(facet.identity_transport)
            self.assertFalse(facet.authority_transport)

    def test_ruleset_is_governance_projection_not_semantic_authority(self):
        primitive = build_reference_publication_primitive()
        ruleset = primitive.ruleset
        kinds = {rule.kind for rule in ruleset.rules}
        self.assertEqual(ruleset.target_branches, ("main",))
        self.assertEqual(ruleset.bypass_actors, ())
        self.assertIn(RuleKind.REQUIRE_PULL_REQUEST, kinds)
        self.assertIn(RuleKind.REQUIRE_STATUS_CHECKS, kinds)
        self.assertIn(RuleKind.BLOCK_FORCE_PUSHES, kinds)
        self.assertIn(RuleKind.RESTRICT_DELETIONS, kinds)
        self.assertEqual(ruleset.required_status_checks, (PUBLICATION_CHECK,))
        self.assertFalse(ruleset.repository_policy_is_semantic_authority)
        self.assertFalse(ruleset.github_mutation_executed)
        self.assertFalse(ruleset.observed_active)

    def test_kokompi_pattern_is_fresh_symbolic_swallow_not_git_merge(self):
        primitive = build_reference_publication_primitive()
        receipt = compile_kokompi_pattern(
            primitive.kokompi_pattern,
            source_occurrences=("public:type:0", "public:rule:0"),
            target_occurrence="public:codebook:1",
        )
        self.assertTrue(receipt.admitted_symbolically)
        self.assertTrue(receipt.fresh_occurrence)
        self.assertTrue(receipt.provenance_preserved)
        self.assertFalse(receipt.git_merge_executed)
        self.assertFalse(receipt.ruleset_mutation_executed)

    def test_guided_diy_configuration_defaults_to_pure_python(self):
        primitive = build_reference_publication_primitive()
        config = materialize_configuration(
            primitive.configuration_space,
            {},
            epoch=1,
        )
        self.assertFalse(config.native_lowering_requested)
        self.assertEqual(config.cpython_minimum, "3.11")
        self.assertIn(("ABI_TRACK", "PURE_PYTHON"), config.selection)

    def test_abi3t_requires_cpython_315(self):
        primitive = build_reference_publication_primitive()
        with self.assertRaisesRegex(
            ValueError,
            "ABI3T_REQUIRES_CPYTHON_3_15_OR_NEWER",
        ):
            materialize_configuration(
                primitive.configuration_space,
                {"ABI_TRACK": "ABI3T", "CPYTHON_MINIMUM": "3.14"},
                epoch=2,
            )

    def test_abi3t_315_is_admitted_as_native_plan(self):
        primitive = build_reference_publication_primitive()
        config = materialize_configuration(
            primitive.configuration_space,
            {
                "ABI_TRACK": "ABI3T",
                "CPYTHON_MINIMUM": "3.15",
                "EXECUTION_BOUNDARY": "NATIVE_EXTENSION_PLAN",
            },
            epoch=3,
        )
        self.assertTrue(config.native_lowering_requested)
        self.assertEqual(config.cpython_minimum, "3.15")


if __name__ == "__main__":
    unittest.main()
