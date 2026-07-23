import unittest

from eye_mystery.practice_cipher4_routes import (
    PatternModel,
    RouteSpec,
    apply_route,
    route_order,
    route_specs,
)


class PracticeCipher4RouteTests(unittest.TestCase):
    def test_every_declared_route_is_a_permutation(self) -> None:
        for length in (17, 28, 31):
            for spec in route_specs():
                self.assertEqual(
                    sorted(route_order(length, spec)),
                    list(range(length)),
                    spec.name,
                )

    def test_route_can_be_inverted_for_a_planted_stream(self) -> None:
        values = tuple(range(31))
        spec = RouteSpec("rect", 7, "inverse-columns")
        order = route_order(len(values), spec)
        encrypted = [0] * len(values)
        for output, source in enumerate(order):
            encrypted[source] = values[output]
        self.assertEqual(apply_route(encrypted, spec), values)

    def test_pattern_model_ignores_symbol_labels(self) -> None:
        source = (0, 1, 0, 2, 3, 2, 0) * 20
        relabeled = tuple({0: 7, 1: 2, 2: 9, 3: 4}[value] for value in source)
        model = PatternModel.train(source, order=5)
        self.assertEqual(
            model.score((source,)),
            model.score((relabeled,)),
        )


if __name__ == "__main__":
    unittest.main()
