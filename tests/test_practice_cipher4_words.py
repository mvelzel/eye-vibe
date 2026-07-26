from __future__ import annotations

import unittest

from eye_mystery.practice_cipher4_gak import (
    encode_nonlinear_gak,
    normalize_language,
    render_plaintext,
)
from eye_mystery.practice_cipher4_words import (
    SymbolModel,
    WordTrie,
    encode_word_gak,
    render_symbols,
    word_constrained_gak_beam,
)


class PracticeCipher4WordTests(unittest.TestCase):
    def test_word_trie_rejects_nonwords_and_accepts_space(self) -> None:
        trie = WordTrie.train("ALPHA BETA BETA")
        node = trie.starts()[0][1]
        for code in (11, 15, 7, 0):
            advanced = trie.advance(node, code)
            self.assertIsNotNone(advanced)
            assert advanced is not None
            node, _ = advanced
        self.assertIsNotNone(trie.advance(node, 26))
        self.assertIsNone(trie.advance(node, 25))

    def test_word_beam_recovers_a_matched_sentence(self) -> None:
        sentence = (
            "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG "
            "AND THEN THE QUICK FOX RESTS"
        )
        corpus = (sentence + " ") * 100
        plaintext = normalize_language(sentence)
        key = tuple((17 * index + 9) % 83 for index in range(27))
        differences = encode_nonlinear_gak(
            plaintext, key, space_position=36
        )
        result = word_constrained_gak_beam(
            differences,
            WordTrie.train(corpus),
            SymbolModel.train(
                corpus, "ABCDEFGHIJKLMNOPQRSTUVWXYZ ", order=5
            ),
            space_position=36,
            beam_width=50_000,
        )
        self.assertEqual(result.completed, len(differences))
        recovered = {
            render_plaintext(candidate.plaintext)
            for candidate in result.candidates
        }
        self.assertIn(sentence, recovered)

    def test_word_beam_recovers_natural_position_punctuation(self) -> None:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ .-'?!"
        positions = tuple(range(26)) + tuple(range(36, 42))
        sentence = "THE QUICK-FOX'S PUZZLE? YES!"
        corpus = (sentence + " ") * 100
        plaintext = bytes(alphabet.index(character) for character in sentence)
        key = tuple((17 * index + 9) % 83 for index in range(len(positions)))
        differences = encode_word_gak(plaintext, key, positions)
        result = word_constrained_gak_beam(
            differences,
            WordTrie.train(corpus),
            SymbolModel.train(corpus, alphabet, order=5),
            space_position=36,
            beam_width=20_000,
            plaintext_positions=positions,
            space_code=26,
            punctuation_codes=tuple(range(27, 32)),
        )
        self.assertEqual(result.completed, len(differences))
        recovered = {
            render_symbols(candidate.plaintext, alphabet)
            for candidate in result.candidates
        }
        self.assertIn(sentence, recovered)


if __name__ == "__main__":
    unittest.main()
