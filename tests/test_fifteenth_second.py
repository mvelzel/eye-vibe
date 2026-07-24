from __future__ import annotations

import unittest

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.fifteenth_second import (
    ChecksumRule,
    ReductionSpec,
    audit_checksum_dispatch,
    audit_reduction_events,
    audit_uniform_morphisms,
    checksum_value,
    deduplicated_reduction_specs,
    factor_complexity,
    fit_uniform_morphism,
    reduction_event,
    trimmed_eye_words,
)


def fixed_point(seed: int, length: int) -> tuple[int, ...]:
    productions = {0: (0, 1), 1: (1, 0)}
    word = (seed,)
    while len(word) < length:
        word = tuple(value for symbol in word for value in productions[symbol])
    return word[:length]


class FifteenthSecondTests(unittest.TestCase):
    def test_uniform_morphism_recovers_shared_plant(self) -> None:
        words = {
            name: fixed_point(index % 2, 160 - 3 * index)
            for index, name in enumerate(MESSAGE_ORDER)
        }
        audits = audit_uniform_morphisms(words)
        length_two = next(audit for audit in audits if audit.length == 2)
        self.assertTrue(length_two.exact)
        self.assertEqual(
            {0: (0, 1), 1: (1, 0)},
            length_two.training.production_map(),
        )
        self.assertIsNotNone(length_two.heldout)
        assert length_two.heldout is not None
        self.assertGreater(length_two.heldout.predicted_observations, 0)

    def test_uniform_morphism_reports_first_literal_contradiction(self) -> None:
        fit = fit_uniform_morphism({"x": (0, 1, 0, 0, 1, 1)}, 2)
        self.assertFalse(fit.exact)
        self.assertIsNotNone(fit.contradiction)

    def test_factor_complexity_does_not_cross_panel_boundaries(self) -> None:
        profile = factor_complexity({"a": (0, 1), "b": (2, 3)}, maximum_length=2)
        self.assertEqual((4, 2), tuple(item.factors for item in profile))
        self.assertNotIn(
            (1, 2),
            {
                tuple(word[start : start + 2])
                for word in ((0, 1), (2, 3))
                for start in range(len(word) - 1)
            },
        )

    def test_checksum_rule_definitions(self) -> None:
        body = (1, 2, 3)
        self.assertEqual(6, checksum_value(body, ChecksumRule("sum", 83, 1)))
        self.assertEqual(2, checksum_value(body, ChecksumRule("alternating", 83, 1)))
        self.assertEqual(10, checksum_value(body, ChecksumRule("fletcher2", 83, 1)))
        self.assertEqual(14, checksum_value(body, ChecksumRule("moment", 83, 1, False, 1)))

    def test_reduction_catalog_has_eighteen_distinct_tables(self) -> None:
        self.assertEqual(18, len(deduplicated_reduction_specs()))

    def test_reduction_event_enters_and_leaves_missing_range(self) -> None:
        spec = ReductionSpec("sum", (0, 1, 2))
        self.assertEqual(0, reduction_event(0, 0, spec))
        self.assertEqual(1, reduction_event(1, 82, spec))

    def test_reduction_audit_selects_exact_planted_relation(self) -> None:
        target = ReductionSpec("sum", (0, 1, 2))
        contexts = (
            ("train", (0, 1, 2, 3), (0, 1, 2, 3)),
            ("heldout", (40, 41, 42), (40, 41, 42)),
        )
        audit = audit_reduction_events(
            contexts=contexts,
            train_names=frozenset(("train",)),
            heldout_names=frozenset(("heldout",)),
        )
        self.assertTrue(audit.exact)
        self.assertIn(target.name, audit.exact_training_specs)

    def test_eye_uniform_morphisms_have_training_contradictions(self) -> None:
        audits = audit_uniform_morphisms(trimmed_eye_words())
        self.assertEqual((2, 3, 4, 5), tuple(audit.length for audit in audits))
        self.assertTrue(
            all(
                not audit.training.exact and audit.heldout is None
                for audit in audits
            )
        )
        self.assertEqual(
            (8, 8, 8, 8),
            tuple(
                audit.training.contradiction.source_index
                for audit in audits
                if audit.training.contradiction is not None
            ),
        )

    def test_eye_checksum_dispatch_result_is_frozen(self) -> None:
        streams = {
            name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        }
        audit = audit_checksum_dispatch(streams)
        self.assertEqual(32, audit.rules)
        self.assertEqual(0, audit.correct_folds)
        self.assertFalse(audit.passed)
        self.assertEqual(
            (
                ("no-prediction", "no-prediction", "no-prediction"),
                ("no-prediction", "no-prediction", "no-prediction"),
                ("no-prediction", "incorrect", "no-prediction"),
            ),
            tuple(
                tuple(fold.status for fold in group.folds)
                for group in audit.classes
            ),
        )

    def test_eye_reduction_result_is_frozen(self) -> None:
        audit = audit_reduction_events()
        self.assertEqual(18, audit.catalog_size)
        self.assertEqual("sum-order012", audit.selected.name)
        self.assertEqual(
            (45, 59),
            (audit.training.agreements, audit.training.comparisons),
        )
        self.assertEqual(
            (41, 82),
            (audit.heldout.agreements, audit.heldout.comparisons),
        )
        self.assertEqual((), audit.exact_training_specs)
        self.assertFalse(audit.exact)


if __name__ == "__main__":
    unittest.main()
