import unittest

from eye_mystery.fourteenth_automata import (
    failure_link_sieve,
    minimal_dictionary_automaton,
)


class FourteenthAutomataTests(unittest.TestCase):
    def test_common_suffix_merges_internal_right_languages(self) -> None:
        result = minimal_dictionary_automaton(
            {"a": (1, 2), "b": (3, 2)},
            alphabet_size=4,
        )
        self.assertEqual(result.trie_nodes, 5)
        self.assertEqual(result.trie_transitions, 4)
        self.assertEqual(result.minimal_nodes, 3)
        self.assertEqual(result.minimal_transitions, 3)
        self.assertEqual(result.accepting_classes, 1)
        self.assertEqual(result.internal_merged_nodes, 1)
        self.assertEqual(result.class_sizes, (2, 2, 1))
        self.assertEqual(result.label_multiplicities, (0, 1, 1, 1))

    def test_terminal_merge_alone_does_not_remove_transitions(self) -> None:
        result = minimal_dictionary_automaton(
            {"a": (1, 2), "b": (3, 0)},
            alphabet_size=4,
        )
        self.assertEqual(result.trie_transitions, 4)
        self.assertEqual(result.minimal_transitions, 4)
        self.assertEqual(result.internal_merged_nodes, 0)
        self.assertEqual(result.class_sizes, (2, 1, 1, 1))

    def test_duplicate_word_does_not_duplicate_trie_path(self) -> None:
        result = minimal_dictionary_automaton(
            {"a": (1, 2), "b": (1, 2)},
            alphabet_size=3,
        )
        self.assertEqual(result.trie_nodes, 3)
        self.assertEqual(result.minimal_nodes, 3)
        self.assertEqual(result.minimal_transitions, 2)

    def test_rejects_labels_outside_declared_alphabet(self) -> None:
        with self.assertRaises(ValueError):
            minimal_dictionary_automaton(
                {"a": (0, 3)}, alphabet_size=3
            )

    def test_failure_links_find_internal_suffix_prefixes(self) -> None:
        result = failure_link_sieve(
            {"a": (1, 2), "b": (3, 1, 2)},
            alphabet_size=4,
            target_word=(1, 1),
        )
        self.assertEqual(result.trie_nodes, 6)
        self.assertEqual(result.selected_nodes, 2)
        self.assertEqual(result.incoming_total, 3)
        self.assertEqual(result.label_multiplicities, (0, 1, 1, 0))
        self.assertEqual(result.failure_depth_histogram, (0, 1, 1))
        self.assertEqual(result.depth_drop_word, (1, 1))
        self.assertEqual(result.bexit_positions, (0,))

    def test_failure_tape_uses_numeric_label_bfs(self) -> None:
        first = failure_link_sieve(
            {"a": (1, 2), "b": (3, 1, 2)},
            alphabet_size=4,
        )
        second = failure_link_sieve(
            {"b": (3, 1, 2), "a": (1, 2)},
            alphabet_size=4,
        )
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
