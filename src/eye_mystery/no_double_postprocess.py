"""Exact signatures of sdlwdr's proposed no-double postprocessors."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import permutations


@dataclass(frozen=True)
class PostprocessWitness:
    message: str
    position: int
    model: str
    output: tuple[int, int, int]


def no_double_postprocess_witnesses(
    streams: Mapping[str, Sequence[int]],
    *,
    modulus: int = 83,
) -> tuple[PostprocessWitness, ...]:
    """Find exact three-output signatures from the public proposal.

    The broad function family allows every ordering of signed difference,
    sum, and product, both modulo ``modulus`` and without wrap.  The multiplier
    family includes the author's ``3,2,5`` examples and the chained powers of
    three that were discussed immediately beforehand.
    """

    if modulus < 2:
        raise ValueError("modulus must be at least two")
    output = []
    for name, stream_value in streams.items():
        stream = tuple(stream_value)
        if any(value not in range(modulus) for value in stream):
            raise ValueError("stream value lies outside the declared modulus")

        for position in range(len(stream) - 4):
            first, second = stream[position : position + 2]
            observed = stream[position + 2 : position + 5]
            modular = (
                (second - first) % modulus,
                (first + second) % modulus,
                (first * second) % modulus,
            )
            for order_index, candidate in enumerate(
                sorted(set(permutations(modular)))
            ):
                if observed == candidate:
                    output.append(
                        PostprocessWitness(
                            name,
                            position,
                            f"function-triple-mod-order{order_index}",
                            candidate,
                        )
                    )

            raw = (abs(second - first), first + second, first * second)
            if all(value < modulus for value in raw):
                for order_index, candidate in enumerate(
                    sorted(set(permutations(raw)))
                ):
                    if observed == candidate:
                        output.append(
                            PostprocessWitness(
                                name,
                                position,
                                f"function-triple-raw-order{order_index}",
                                candidate,
                            )
                        )

        for position in range(len(stream) - 3):
            value = stream[position]
            observed = stream[position + 1 : position + 4]
            models = (
                (
                    "multiples-original-3,2,5",
                    tuple(multiplier * value % modulus for multiplier in (3, 2, 5)),
                ),
                (
                    "multiples-chained-3,2,5",
                    tuple(multiplier * value % modulus for multiplier in (3, 6, 30)),
                ),
                (
                    "multiples-powers-of-3",
                    tuple(multiplier * value % modulus for multiplier in (3, 9, 27)),
                ),
            )
            output.extend(
                PostprocessWitness(name, position, model, candidate)
                for model, candidate in models
                if observed == candidate
            )
    return tuple(output)
