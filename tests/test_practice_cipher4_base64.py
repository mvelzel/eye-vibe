import base64
import random
import unittest

from eye_mystery.practice_cipher4_base64 import (
    BASE64_ALPHABET,
    Base64SubstitutionAnnealer,
    ByteNgrams,
    decode_base64_values,
    encode_base64_substitution,
)


class PracticeCipher4Base64Tests(unittest.TestCase):
    def test_value_decoder_handles_every_unpadded_tail(self) -> None:
        for plaintext in (b"a", b"ab", b"abc", b"abcd", b"abcde"):
            encoded = base64.b64encode(plaintext).decode("ascii").rstrip("=")
            values = tuple(BASE64_ALPHABET.index(character) for character in encoded)
            self.assertEqual(decode_base64_values(values), plaintext)

    def test_substitution_encoder_and_fixed_key_decode(self) -> None:
        plaintext = b"a small planted base64 control"
        shuffled = list(BASE64_ALPHABET)
        random.Random(4).shuffle(shuffled)
        inverse = {character: index for index, character in enumerate(shuffled)}
        stream = encode_base64_substitution(plaintext, inverse)
        model = ByteNgrams.train(plaintext * 20, order=3)
        annealer = Base64SubstitutionAnnealer((stream,), model, random.Random(5))
        key = [0] * 64
        used_values = set()
        for token in annealer.observed:
            value = BASE64_ALPHABET.index(shuffled[token])
            key[annealer.slot_by_token[token]] = value
            used_values.add(value)
        for slot, value in zip(
            range(len(annealer.observed), 64),
            sorted(set(range(64)) - used_values),
            strict=True,
        ):
            key[slot] = value
        self.assertEqual(bytes(annealer.decode(key)[0]), plaintext)


if __name__ == "__main__":
    unittest.main()
