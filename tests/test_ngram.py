import unittest

from eye_mystery.ngram import TetragramModel, ascii_letters


class NgramTests(unittest.TestCase):
    def test_model_prefers_seen_text(self) -> None:
        model = TetragramModel.train("THE QUICK BROWN FOX " * 10)
        seen = ascii_letters("THEQUICKBROWNFOX")
        unseen = ascii_letters("QZXJQZXJQZXJQZXJ")
        self.assertGreater(model.score(seen), model.score(unseen))


if __name__ == "__main__":
    unittest.main()
