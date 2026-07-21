import unittest

from eye_mystery.corpus import MESSAGE_ORDER
from eye_mystery.storage_serialization import (
    MAX_U64,
    corpus_packed_words,
    decode_storage_chunk,
    greedy_pack_storage,
    nonfinal_capacity_bits,
    packed_words_sha256,
    storage_stream,
)


class StorageSerializationTests(unittest.TestCase):
    def test_greedy_pack_round_trips_every_message(self) -> None:
        for name in MESSAGE_ORDER:
            stream = storage_stream(name)
            words, _ = greedy_pack_storage(stream)
            decoded = tuple(
                symbol for word in words for symbol in decode_storage_chunk(word)
            )
            self.assertEqual(decoded, stream)

    def test_every_nonfinal_chunk_is_maximal(self) -> None:
        for name in MESSAGE_ORDER:
            stream = storage_stream(name)
            words, lengths = greedy_pack_storage(stream)
            cursor = 0
            for word, length in zip(words[:-1], lengths[:-1], strict=True):
                self.assertLessEqual(word, MAX_U64)
                extended = stream[cursor : cursor + length + 1]
                value = 0
                for symbol in extended:
                    value = 7 * value + symbol + 1
                self.assertGreater(value * 7, MAX_U64)
                cursor += length

    def test_derived_words_match_verified_engine_fixture_digest(self) -> None:
        words = corpus_packed_words()
        self.assertEqual(len(words), 150)
        self.assertEqual(words[0], 0xACF686745634505C)
        self.assertEqual(words[-1], 0x8C)
        self.assertEqual(
            packed_words_sha256(words),
            "5de6ccb3a045218827b7ddaad0f1493254f501b08addd1929495ce060242de94",
        )

    def test_capacity_bit_inventory(self) -> None:
        bits = nonfinal_capacity_bits()
        self.assertEqual(len(bits), 141)
        self.assertEqual(sum(bits), 29)


if __name__ == "__main__":
    unittest.main()
