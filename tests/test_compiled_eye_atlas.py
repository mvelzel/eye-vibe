import unittest

from eye_mystery.compiled_eye_atlas import (
    ADD_MASK,
    OBFUSCATED_WORDS,
    XOR_MASK,
    atlas_frames,
    decode_words,
)


class CompiledEyeAtlasTests(unittest.TestCase):
    def test_compiled_words_decode_to_five_distinct_frames(self) -> None:
        self.assertEqual(len(OBFUSCATED_WORDS), 5)
        self.assertEqual(
            decode_words(),
            (
                0x0031888A38A22318,
                0x0031880A10A72358,
                0x0031890A70A42318,
                0x003589CA10A02318,
                0x0031884A1CA12318,
            ),
        )
        frames = atlas_frames()
        self.assertEqual(len(frames), 5)
        self.assertEqual({frame for frame in frames}.__len__(), 5)
        self.assertTrue(all(len(frame) == 77 for frame in frames))

    def test_top_and_bottom_rows_are_compiled_buffer_shape(self) -> None:
        for frame in atlas_frames():
            self.assertEqual(frame[:11], (0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0))
            self.assertEqual(frame[-11:], (0,) * 11)

    def test_masks_are_independent_of_plaintext_decoder(self) -> None:
        self.assertNotEqual(XOR_MASK, 0)
        self.assertNotEqual(ADD_MASK, 0)


if __name__ == "__main__":
    unittest.main()
