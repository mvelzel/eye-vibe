"""Small exact certificate against a position-progressive permutation.

For ``cipher_i = P**i(S[plain_i])``, two copies of the same plaintext at
positions separated by ``d`` must be related by ``P**d``.  The strong
last-family contexts provide both one-step and three-step mappings and directly
contradict that requirement.
"""

from __future__ import annotations

from dataclasses import dataclass

from eye_mystery.corpus import MESSAGES, trigram_values


LAST_REFERENCE = ("east4", 68)
LAST_ONE_STEP = ("east5", 69)
LAST_THREE_STEP = ("west4", 71)
LAST_CONTEXT_LENGTH = 30


@dataclass(frozen=True)
class ProgressionContradiction:
    start: int
    forced_chain: tuple[int, ...]
    required_target: int


@dataclass(frozen=True)
class CommutationContradiction:
    start: int
    first_then_second: tuple[int, int, int]
    second_then_first: tuple[int, int, int]
    colliding_source: int


def context_mapping(
    left_name: str,
    left_start: int,
    right_name: str,
    right_start: int,
    length: int,
) -> dict[int, int]:
    left = trigram_values(MESSAGES[left_name])[left_start : left_start + length]
    right = trigram_values(MESSAGES[right_name])[
        right_start : right_start + length
    ]
    mapping: dict[int, int] = {}
    reverse: dict[int, int] = {}
    for source, target in zip(left, right, strict=True):
        if source in mapping and mapping[source] != target:
            raise ValueError("context does not define a function")
        if target in reverse and reverse[target] != source:
            raise ValueError("context does not define an injective mapping")
        mapping[source] = target
        reverse[target] = source
    return mapping


def last_family_progression_contradictions(
) -> tuple[ProgressionContradiction, ...]:
    reference_name, reference_start = LAST_REFERENCE
    one_name, one_start = LAST_ONE_STEP
    three_name, three_start = LAST_THREE_STEP
    one_step = context_mapping(
        reference_name,
        reference_start,
        one_name,
        one_start,
        LAST_CONTEXT_LENGTH,
    )
    three_step = context_mapping(
        reference_name,
        reference_start,
        three_name,
        three_start,
        LAST_CONTEXT_LENGTH,
    )

    contradictions = []
    for start, required_target in three_step.items():
        chain = [start]
        value = start
        for _ in range(3):
            if value not in one_step:
                break
            value = one_step[value]
            chain.append(value)
        if len(chain) == 4 and value != required_target:
            contradictions.append(
                ProgressionContradiction(
                    start=start,
                    forced_chain=tuple(chain),
                    required_target=required_target,
                )
            )
    return tuple(contradictions)


def last_family_commutation_contradiction() -> CommutationContradiction:
    """Return a four-edge proof that the two context maps cannot commute.

    Call the East 4→East 5 map ``A`` and East 4→West 4 map ``B``.  The contexts
    give ``A(3)=44``, ``B(3)=22``, ``A(22)=23``, and ``B(59)=23``.  If ``A``
    and ``B`` commuted, then ``B(44)=A(22)=23=B(59)``.  Since ``B`` is a
    permutation, that would force the distinct labels 44 and 59 to be equal.
    """

    reference_name, reference_start = LAST_REFERENCE
    first_name, first_start = LAST_ONE_STEP
    second_name, second_start = LAST_THREE_STEP
    first = context_mapping(
        reference_name,
        reference_start,
        first_name,
        first_start,
        LAST_CONTEXT_LENGTH,
    )
    second = context_mapping(
        reference_name,
        reference_start,
        second_name,
        second_start,
        LAST_CONTEXT_LENGTH,
    )
    start = 3
    first_middle = first[start]
    second_middle = second[start]
    target = first[second_middle]
    colliding_source = next(
        source for source, value in second.items() if value == target
    )
    return CommutationContradiction(
        start=start,
        first_then_second=(start, first_middle, target),
        second_then_first=(start, second_middle, target),
        colliding_source=colliding_source,
    )
