import unittest

from eye_mystery.fourteenth_automata import (
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


if __name__ == "__main__":
    unittest.main()
