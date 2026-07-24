import unittest

from eye_mystery.lua_arithmetic_signatures import (
    scan_lua_arithmetic_signatures,
)


class LuaArithmeticSignatureTests(unittest.TestCase):
    def test_finds_domains_partitions_loops_moduli_and_lookup_flow(self) -> None:
        hits = scan_lua_arithmetic_signatures(
            (
                (
                    "fixture.lua",
                    "\n".join(
                        (
                            "local card = Random(0, 82)",
                            "return deck[card + 1]",
                            "if Random(0,100) < 83 then return 1 end",
                            "for i=1,42 do output[i] = i end",
                            "local position = value % 101",
                            "return ring[position]",
                        )
                    ),
                ),
            )
        )
        self.assertEqual(
            tuple((hit.cardinality, hit.kind) for hit in hits),
            (
                (83, "random_domain"),
                (101, "random_domain"),
                (83, "random_partition"),
                (42, "numeric_for"),
                (101, "modulo"),
            ),
        )
        self.assertEqual(
            tuple(hit.feeds_lookup for hit in hits),
            (True, False, False, True, True),
        )

    def test_ignores_comments_and_unrelated_literals(self) -> None:
        hits = scan_lua_arithmetic_signatures(
            (
                (
                    "fixture.lua",
                    "-- Random(0,82)\n"
                    "local width = 83\n"
                    "for i=9,1 do end\n",
                ),
            )
        )
        self.assertEqual(hits, ())


if __name__ == "__main__":
    unittest.main()
