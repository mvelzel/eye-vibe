import unittest

from eye_mystery.source_fingerprints import (
    extract_card_body,
    first_family_source_matches,
    gap_repeats,
    normalize_source,
)


class SourceFingerprintTests(unittest.TestCase):
    def test_extract_card_body_omits_page_chrome_and_scripts(self) -> None:
        source = """
        <nav>menu</nav><div class="card-body"><p>Alpha <b>Beta</b></p>
        <script>ignored()</script><div>Gamma</div></div><footer>footer</footer>
        """
        self.assertEqual("Alpha Beta Gamma", " ".join(extract_card_body(source).split()))

    def test_normalization(self) -> None:
        self.assertEqual(normalize_source("As above, SO below!"), "asabovesobelow")
        self.assertEqual(
            normalize_source("As above, SO below!", "spaces"),
            "as above so below",
        )

    def test_finnish_transliteration(self) -> None:
        self.assertEqual(
            normalize_source(
                "Hyvää yötä, Åbo!", transliterate_finnish=True
            ),
            "hyvaayotaabo",
        )

    def test_gap_repeat(self) -> None:
        self.assertEqual(
            gap_repeats("abcdef___abcdef", length=6, gap=9),
            {"abcdef": (0,)},
        )

    def test_joint_first_family_fingerprint(self) -> None:
        block = "abcdefghijklmnopqr"
        inner = block[6:15]
        texts = {
            "west1": "x" * 34 + block + "y" * 12 + block + "z" * 21,
            "east2": "x" * 39 + block + "y" * 17 + block + "z" * 26,
            "east1": "x" * 40 + inner + "y" * 19 + inner + "z" * 22,
        }
        matches = first_family_source_matches(texts)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].block, block)


if __name__ == "__main__":
    unittest.main()
