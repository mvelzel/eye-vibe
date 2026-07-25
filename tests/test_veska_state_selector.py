from __future__ import annotations

import unittest

from eye_mystery.veska_state_selector import (
    SelectorParse,
    VESKA_COMPONENTS,
    all_class_cross_hits,
    audit_veska_selector,
    distinct_suffix_widths,
    permuted_valid_splits,
    repeated_classes,
    repeated_cross_hits,
    valid_splits,
)


class VeskaStateSelectorTests(unittest.TestCase):
    def test_fixed_selector_parse(self) -> None:
        expected = (SelectorParse((1, 5, 3), 2, 15, 3),)
        self.assertEqual(
            valid_splits(
                VESKA_COMPONENTS,
                repeated_classes(),
                distinct_suffix_widths(),
            ),
            expected,
        )
        self.assertEqual(
            valid_splits(
                VESKA_COMPONENTS,
                tuple(range(25)),
                distinct_suffix_widths(),
            ),
            expected,
        )

    def test_broad_cross_and_permutation_inventories(self) -> None:
        self.assertEqual(repeated_cross_hits(), ((15, 3),))
        self.assertEqual(all_class_cross_hits(), ((15, 3),))
        self.assertEqual(
            permuted_valid_splits(),
            (SelectorParse((1, 5, 3), 2, 15, 3),),
        )

    def test_selector_executes_restart_and_locale(self) -> None:
        audit = audit_veska_selector()
        self.assertEqual(audit.components, (1, 5, 3))
        self.assertEqual((audit.number, audit.increment), (153, 3))
        self.assertEqual((audit.terminal_class, audit.loop_suffix), (15, 3))
        self.assertEqual(audit.panel_suffix_matches, ("east4", "east5"))
        self.assertEqual(
            (audit.returned_header, audit.restarted_phase, audit.late_phase_length),
            (27, 30, 30),
        )
        self.assertEqual(audit.locale_text, "fi")
        self.assertEqual(
            (
                audit.repeated_cross_probability.numerator,
                audit.repeated_cross_probability.denominator,
            ),
            (1, 10),
        )
        self.assertTrue(audit.selector_executes)

    def test_changed_class_or_suffix_is_not_primary(self) -> None:
        self.assertEqual(
            valid_splits(
                (1, 4, 3),
                repeated_classes(),
                distinct_suffix_widths(),
            ),
            (),
        )
        changed_suffix = valid_splits(
            (1, 5, 4),
            repeated_classes(),
            distinct_suffix_widths(),
        )
        self.assertEqual(
            changed_suffix,
            (SelectorParse((1, 5, 4), 2, 15, 4),),
        )
        self.assertNotEqual(changed_suffix[0].suffix_width, 3)


if __name__ == "__main__":
    unittest.main()
