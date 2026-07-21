import hashlib
import unittest

from eye_mystery.practice_cipher5 import (
    REVISED_SECTIONS,
    common_prefix_length,
    decode_dynamic_substitution,
    decode_revised_sections,
    encode_dynamic_substitution,
    recursive_increasing_chunk_reversal,
    recursive_fixed_interleave,
    recursive_increasing_interleaves,
    render_plaintext,
)


class PracticeCipher5Tests(unittest.TestCase):
    def test_revised_section_lengths_and_alphabet(self) -> None:
        self.assertEqual(
            tuple(map(len, REVISED_SECTIONS)),
            (98, 170, 259, 259, 228, 73, 451, 152, 522),
        )
        alphabet = set().union(*map(set, REVISED_SECTIONS))
        self.assertEqual(len(alphabet), 83)

    def test_common_prefix(self) -> None:
        self.assertEqual(common_prefix_length("abc", "abd"), 2)
        self.assertEqual(common_prefix_length("abc", "abcde"), 3)

    def test_recursive_families_are_permutations(self) -> None:
        for factory in (recursive_fixed_interleave, recursive_increasing_interleaves):
            operations = tuple(factory(11, index, one_based=True) for index in range(11))
            self.assertTrue(all(sorted(operation) == list(range(11)) for operation in operations))

    def test_dynamic_substitution_round_trip_shape(self) -> None:
        operations = tuple(
            recursive_increasing_interleaves(11, index, one_based=True)
            for index in range(11)
        )
        plaintext = (1, 4, 1, 5, 9, 2, 6)
        deck = tuple(range(11))
        ciphertext = []
        for index in plaintext:
            ciphertext.append(deck[index])
            deck = tuple(deck[position] for position in operations[index])
        self.assertEqual(
            decode_dynamic_substitution(ciphertext, operations),
            plaintext,
        )

    def test_intended_operations_are_distinct_permutations(self) -> None:
        operations = tuple(
            recursive_increasing_chunk_reversal(83, index)
            for index in range(83)
        )
        self.assertEqual(len(set(operations)), 83)
        self.assertTrue(
            all(sorted(operation) == list(range(83)) for operation in operations)
        )

    def test_revised_ciphertext_replays_exactly(self) -> None:
        operations = tuple(
            recursive_increasing_chunk_reversal(83, index)
            for index in range(83)
        )
        plaintexts = decode_revised_sections()
        replayed = tuple(
            "".join(chr(card + 33) for card in encode_dynamic_substitution(text, operations))
            for text in plaintexts
        )
        self.assertEqual(replayed, REVISED_SECTIONS)

    def test_recovered_plaintext_fingerprints(self) -> None:
        expected = (
            "c58e1976a553e32677e0cc62ecea0804893463f501bb0c49f018d350baa7ce0d",
            "c64ee65ca2920e19ab6f639568897314c8b0ae59c007d4aaf7de18dd7a6e9892",
            "36a2bb24ff52afc495dd1f054e622c6e7d32b370dea97dd84b3d931690e594a8",
            "66c7be50362f695c7ab68524de27444cc8f0671af954a6c40bd9318a974bf023",
            "57291e34bb8fe80922c06ce53b3efc851fbf3ffb633234bd24884a046ea89cdf",
            "de8e6fd73ee59a5eb39d1523a27a335c85e43f6981bf4b6eb6dd72ecb53a9543",
            "e25b7e3f04cfa1507f04afeda023f137d5b7297a1d613d559f06a7f1c192bb62",
            "0614493184b9cc4bd7338a3113e38176371a04af6fa33780fe79ade843bd32ca",
            "929a8d03e6fd435580e91c4ae213978c1fe78a3ab4610c7bb616837d81aa2217",
        )
        rendered = tuple(map(render_plaintext, decode_revised_sections()))
        observed = tuple(
            hashlib.sha256(section.encode()).hexdigest() for section in rendered
        )
        self.assertEqual(observed, expected)
        self.assertTrue(
            rendered[0].startswith("1\n DO YOU LIKE GREEN EGGS AND HAM?")
        )


if __name__ == "__main__":
    unittest.main()
