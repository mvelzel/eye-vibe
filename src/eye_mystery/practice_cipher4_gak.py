"""Packed beam search for practice cipher 4's nonlinear cyclic GAK layer."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from heapq import nlargest
from math import log


MODULUS = 83
UNSET = 255


def normalize_language(text: str) -> tuple[int, ...]:
    """Return uppercase A-Z plus collapsed space as values 0..26."""

    result: list[int] = []
    in_space = True
    for character in text.upper():
        if "A" <= character <= "Z":
            result.append(ord(character) - ord("A"))
            in_space = False
        elif not in_space:
            result.append(26)
            in_space = True
    if result and result[-1] == 26:
        result.pop()
    return tuple(result)


@dataclass(frozen=True)
class CharacterModel:
    order: int
    scores: dict[bytes, float]
    floor: float

    @classmethod
    def train(cls, text: str, order: int = 6) -> "CharacterModel":
        values = bytes(normalize_language(text))
        counts = Counter(
            values[index : index + order]
            for index in range(len(values) - order + 1)
        )
        total = sum(counts.values())
        if not total:
            raise ValueError("language corpus is too short")
        return cls(
            order,
            {gram: log(count / total) for gram, count in counts.items()},
            log(0.01 / total),
        )

    def score_extension(self, suffix: bytes, following: int) -> float:
        gram = suffix + bytes((following,))
        if len(gram) < self.order:
            return 0.0
        return self.scores.get(gram[-self.order :], self.floor)


@dataclass(frozen=True)
class BeamCandidate:
    score: float
    key: bytes
    suffix: bytes
    plaintext: bytes


@dataclass(frozen=True)
class BeamResult:
    completed: int
    candidates: tuple[BeamCandidate, ...]


def plaintext_values(space_position: int) -> tuple[int, ...]:
    """Return A-Z plus one disclosed position for space."""

    if space_position in range(26):
        raise ValueError("space must not collide with A-Z")
    if space_position not in range(MODULUS):
        raise ValueError("space position must lie in Z83")
    return tuple(range(26)) + (space_position,)


def render_plaintext(values: Sequence[int]) -> str:
    return "".join(
        " " if value == 26 else chr(ord("A") + value) for value in values
    )


def signed_band_step(rank: int, convention: str) -> int:
    """Interpret one `0..56` rank as a canonical signed distance."""

    if rank not in range(57):
        raise ValueError("rank must lie in 0..56")
    if convention == "zigzag-negative-odd":
        return rank // 2 if rank % 2 == 0 else -(rank // 2 + 1)
    if convention == "zigzag-positive-odd":
        return -(rank // 2) if rank % 2 == 0 else rank // 2 + 1
    if convention == "centered":
        return rank - 28
    if convention == "centered-reflected":
        return 28 - rank
    raise ValueError(f"unknown signed-band convention: {convention}")


def _oriented(value: int, sign: int) -> int:
    return sign * value % MODULUS


def nonlinear_gak_beam(
    differences: Sequence[int],
    model: CharacterModel,
    *,
    space_position: int,
    beam_width: int,
    ciphertext_sign: int = 1,
    plaintext_sign: int = 1,
    key_on_next: bool = False,
) -> BeamResult:
    """Search ``p' = sign*d + q(selector)`` with packed candidate states.

    Plaintext path bytes are language codes (A-Z=0..25, space=26).  ``key``
    stores the required value of the otherwise arbitrary function ``q`` for
    each of those 27 symbols.  Expansion records retain only a parent index
    until the top beam has been selected, avoiding millions of full-path
    copies at first-use branches.
    """

    if beam_width < 1:
        raise ValueError("beam width must be positive")
    if ciphertext_sign not in (-1, 1) or plaintext_sign not in (-1, 1):
        raise ValueError("signs must be -1 or +1")
    if any(value not in range(MODULUS) for value in differences):
        raise ValueError("differences must lie in Z83")

    actual = plaintext_values(space_position)
    code_by_oriented = {
        _oriented(value, plaintext_sign): code
        for code, value in enumerate(actual)
    }
    empty_key = bytes((UNSET,)) * len(actual)
    beam = [
        BeamCandidate(0.0, empty_key, bytes((code,)), bytes((code,)))
        for code in range(len(actual))
    ]

    completed = 0
    suffix_size = model.order - 1
    for difference in differences:
        expanded: dict[
            tuple[bytes, bytes], tuple[float, int, int, bytes, bytes]
        ] = {}
        signed_difference = ciphertext_sign * difference
        for parent_index, candidate in enumerate(beam):
            current_code = candidate.plaintext[-1]
            if key_on_next:
                next_codes = range(len(actual))
            else:
                key_value = candidate.key[current_code]
                if key_value == UNSET:
                    next_codes = range(len(actual))
                else:
                    following_oriented = (
                        signed_difference + key_value
                    ) % MODULUS
                    following_code = code_by_oriented.get(following_oriented)
                    if following_code is None:
                        continue
                    next_codes = (following_code,)

            for following_code in next_codes:
                following_oriented = _oriented(
                    actual[following_code], plaintext_sign
                )
                required = (
                    following_oriented - signed_difference
                ) % MODULUS
                selector_code = (
                    following_code if key_on_next else current_code
                )
                previous_required = candidate.key[selector_code]
                if previous_required not in (UNSET, required):
                    continue
                if previous_required == UNSET:
                    key = (
                        candidate.key[:selector_code]
                        + bytes((required,))
                        + candidate.key[selector_code + 1 :]
                    )
                else:
                    key = candidate.key
                score = candidate.score + model.score_extension(
                    candidate.suffix, following_code
                )
                suffix = (candidate.suffix + bytes((following_code,)))[
                    -suffix_size:
                ]
                identity = (key, suffix)
                previous = expanded.get(identity)
                if previous is None or score > previous[0]:
                    expanded[identity] = (
                        score,
                        parent_index,
                        following_code,
                        key,
                        suffix,
                    )

        if not expanded:
            break
        selected = nlargest(
            beam_width, expanded.values(), key=lambda item: item[0]
        )
        beam = [
            BeamCandidate(
                score,
                key,
                suffix,
                beam[parent_index].plaintext + bytes((following_code,)),
            )
            for score, parent_index, following_code, key, suffix in selected
        ]
        completed += 1

    return BeamResult(
        completed,
        tuple(sorted(beam, key=lambda item: item.score, reverse=True)),
    )


def encode_nonlinear_gak(
    plaintext: Sequence[int],
    key: Sequence[int],
    *,
    space_position: int,
    ciphertext_sign: int = 1,
    plaintext_sign: int = 1,
) -> tuple[int, ...]:
    """Generate transition differences for a planted current-symbol key."""

    actual = plaintext_values(space_position)
    if len(key) != len(actual) or any(value not in range(MODULUS) for value in key):
        raise ValueError("key must contain 27 values in Z83")
    if any(value not in range(len(actual)) for value in plaintext):
        raise ValueError("plaintext codes must lie in 0..26")
    inverse_ciphertext_sign = ciphertext_sign
    return tuple(
        inverse_ciphertext_sign
        * (
            _oriented(actual[following], plaintext_sign)
            - key[current]
        )
        % MODULUS
        for current, following in zip(plaintext, plaintext[1:])
    )
