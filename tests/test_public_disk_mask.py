import unittest

from eye_mystery.corpus import MESSAGES
from eye_mystery.public_disk_mask import decode


class PublicDiskMaskTests(unittest.TestCase):
    def test_literal_replay_vector(self) -> None:
        self.assertEqual(
            decode(MESSAGES["east1"]),
            "R0 7T- $$]\"4!^\".!( #\"=#8!%m/#&!3 /S/!.!4\"3#J$7#O$8\"? 8#K$1#8:*!!9% 4S+$&$8$5$S!2 h$-$q 0$? ,#'<-$2<",
        )

    def test_rejects_incomplete_stream(self) -> None:
        with self.assertRaises(ValueError):
            decode((0, 1))


if __name__ == "__main__":
    unittest.main()
