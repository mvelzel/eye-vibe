import unittest

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.fourteenth_recursive import (
    RecursiveRule,
    audit_recursive_checks,
    planted_branch_dictionary,
    recursive_rules,
    recursive_values,
)


class FourteenthRecursiveTests(unittest.TestCase):
    def test_rule_catalog_has_exactly_54_label_consuming_rules(self) -> None:
        rules = recursive_rules()
        self.assertEqual(54, len(rules))
        self.assertEqual(len(rules), len(set(rules)))
        self.assertTrue(all(rule.incoming in (-1, 1) for rule in rules))

    def test_planted_nested_tree_predicts_all_branches_and_root(self) -> None:
        audit = audit_recursive_checks(planted_branch_dictionary())
        self.assertEqual(5, len(audit.branch_paths))
        self.assertEqual(5, audit.leave_one_out_correct)
        self.assertTrue(audit.root_zero)
        self.assertEqual(5, audit.selected_branch_zeros)

    def test_ordinary_rule_root_is_transition_sum(self) -> None:
        streams = {"a": (1, 2), "b": (1, 3)}
        values, branches, paths = recursive_values(
            streams,
            RecursiveRule(1, 1, 0, 0),
        )
        self.assertEqual(6, values[0])
        self.assertEqual(1, len(branches))
        self.assertEqual(((1,),), paths)

    def test_branch_order_is_dictionary_insertion_invariant(self) -> None:
        streams = planted_branch_dictionary()
        reversed_streams = dict(reversed(tuple(streams.items())))
        self.assertEqual(
            audit_recursive_checks(streams).branch_paths,
            audit_recursive_checks(reversed_streams).branch_paths,
        )

    def test_eye_branch_result_is_frozen(self) -> None:
        bodies = {
            name: trigram_values(MESSAGES[name])[1:]
            for name in MESSAGE_ORDER
        }
        audit = audit_recursive_checks(bodies)
        self.assertEqual(
            (2, 24, 5, 9, 20),
            tuple(map(len, audit.branch_paths)),
        )
        self.assertEqual(0, audit.leave_one_out_correct)
        self.assertEqual((96, 32, 64, 73, 5), audit.selected_branch_values)
        self.assertEqual(0, audit.selected_branch_zeros)
        self.assertEqual(62, audit.root_value)


if __name__ == "__main__":
    unittest.main()
