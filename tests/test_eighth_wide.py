from __future__ import annotations

import unittest

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.eighth_wide import (
    codebook_score,
    cocycle_score,
    nonoverlapping_pair_count,
    nonoverlapping_pair_counts,
    packet_score,
    repair_score,
    replace_pair,
)


class EighthWideUnitTests(unittest.TestCase):
    def test_repair_replacement_is_nonoverlapping(self) -> None:
        self.assertEqual(
            replace_pair(((1, 1, 1, 1, 2),), (1, 1), 9),
            ((9, 9, 2),),
        )

    def test_simultaneous_pair_counts_match_direct_scans(self) -> None:
        sequences = ((1, 1, 1, 1, 2, 1, 2), (2, 1, 2, 2, 2))
        counts = nonoverlapping_pair_counts(sequences)

        for pair in {(1, 1), (1, 2), (2, 1), (2, 2)}:
            self.assertEqual(
                counts[pair],
                nonoverlapping_pair_count(sequences, pair),
            )


class EighthWideCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.streams = {
            name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
        }

    def test_observed_structural_scores_are_stable(self) -> None:
        codebook = codebook_score()
        packets = packet_score(self.streams)
        cocycle = cocycle_score(self.streams)
        grammar = repair_score(self.streams)

        self.assertEqual(
            (
                codebook.minimum_distance,
                codebook.distance_one_pairs,
                codebook.valid_splices,
                codebook.splices,
                codebook.distinct_splice_words,
            ),
            (1, 415, 9746, 2 * 83 * 83, 115),
        )
        self.assertEqual(
            (
                packets.records_26,
                packets.unique_26,
                packets.blocks_83,
                packets.unique_83,
            ),
            (34, 750, 9, 474),
        )
        self.assertEqual(
            (
                cocycle.repeated_bigram_types,
                cocycle.repeated_bigram_occurrences,
                cocycle.quotient_nodes,
                cocycle.constraints,
                cocycle.components,
                cocycle.contradictions,
            ),
            (104, 279, 729, 786, 1, 57),
        )
        self.assertEqual(
            (
                grammar.original_symbols,
                grammar.final_stream_symbols,
                grammar.rules,
                grammar.encoded_symbols,
                grammar.savings,
            ),
            (1027, 867, 46, 959, 68),
        )


if __name__ == "__main__":
    unittest.main()
