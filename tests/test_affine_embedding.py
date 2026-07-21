import unittest

from eye_mystery.affine_embedding import (
    context_from_sequences,
    find_affine_embedding,
    find_affine_embedding_graph,
    find_affine_mapping_unsat_core,
    verify_affine_embedding,
    z3_available,
)


@unittest.skipUnless(z3_available(), "optional z3-solver dependency is absent")
class AffineEmbeddingTests(unittest.TestCase):
    def test_context_rejects_non_function(self) -> None:
        with self.assertRaises(ValueError):
            context_from_sequences("bad", (1, 1), (2, 3))

    def test_finds_relabelled_affine_map(self) -> None:
        # The partial permutation 10->30, 20->50 is affine-compatible under
        # some relabeling regardless of the numeric glyph labels.
        context = context_from_sequences("sample", (10, 20), (30, 50))
        outcome, embedding, _ = find_affine_embedding(
            (context,), hidden_order=82, timeout_ms=5_000
        )
        self.assertEqual(outcome, "sat")
        self.assertIsNotNone(embedding)
        assert embedding is not None
        self.assertTrue(verify_affine_embedding((context,), embedding))

    def test_graph_solver_finds_relabelled_affine_map(self) -> None:
        context = context_from_sequences("sample", (10, 20), (30, 50))
        outcome, embedding, _ = find_affine_embedding_graph(
            (context,), hidden_order=82, timeout_ms=5_000
        )
        self.assertEqual(outcome, "sat")
        self.assertIsNotNone(embedding)
        assert embedding is not None
        self.assertTrue(verify_affine_embedding((context,), embedding))

    def test_two_fixed_points_force_identity(self) -> None:
        context = context_from_sequences("impossible", (1, 2, 3), (1, 2, 4))
        for solve in (find_affine_embedding, find_affine_embedding_graph):
            outcome, embedding, _ = solve(
                (context,), hidden_order=82, timeout_ms=5_000
            )
            self.assertEqual(outcome, "unsat")
            self.assertIsNone(embedding)

    def test_extracts_irreducible_mapping_core(self) -> None:
        context = context_from_sequences("impossible", (1, 2, 3), (1, 2, 4))
        outcome, core, _ = find_affine_mapping_unsat_core(
            (context,), hidden_order=82, timeout_ms=5_000
        )
        self.assertEqual(outcome, "unsat")
        self.assertEqual(len(core), 3)


if __name__ == "__main__":
    unittest.main()
