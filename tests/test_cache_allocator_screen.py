import unittest

from eye_mystery.cache_allocator_screen import (
    TRAINING_LENGTH,
    identifiability_certificate,
    initial_order,
    target_card_trace,
    update_deck,
)


class CacheAllocatorScreenTests(unittest.TestCase):
    def test_initial_orders_are_permutations(self) -> None:
        for sign in (-1, 1):
            for offset in (0, 17, 82):
                self.assertEqual(
                    set(initial_order(sign, offset)),
                    set(range(83)),
                )

    def test_updates_preserve_cards(self) -> None:
        for policy in (
            "none",
            "front",
            "back",
            "left",
            "right",
            "reverse_prefix",
            "reverse_suffix",
        ):
            deck = list(range(9))
            update_deck(deck, 4, policy)
            self.assertEqual(set(deck), set(range(9)))

    def test_identical_updates_preserve_identity_mapping(self) -> None:
        signature = (0, 1, 2, 1, 3, 0)
        for policy in ("none", "front", "back", "left", "right"):
            self.assertEqual(
                target_card_trace(
                    signature,
                    source_sign=1,
                    source_offset=0,
                    source_policy=policy,
                    target_policy=policy,
                ),
                signature,
            )

    def test_identifiability_count(self) -> None:
        certificate = identifiability_certificate()
        self.assertEqual(certificate.classes, 25)
        self.assertEqual(certificate.available_labels, 83)
        self.assertGreater(certificate.information_bits, 150)
        self.assertEqual(TRAINING_LENGTH, 30)


if __name__ == "__main__":
    unittest.main()

