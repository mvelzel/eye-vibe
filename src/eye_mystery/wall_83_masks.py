"""Derive the source-selected 83-entry binary masks in the Wall Messages."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from .wall_baconian import tokenize_wall


WORLD_VERTICAL_ORDER = (
    "G9",
    "G7",
    "G6",
    "G10",
    "G8",
    "G11",
    "G12",
    "G1",
    "G2",
    "G3",
    "G4",
    "G5",
)
ASSET_XML_ORDER = tuple(f"G{index}" for index in range(1, 13))
THAT_WHICH_WINDOWS = (
    ("east1:40", (47, 44, 48, 42, 19, 48, 13, 47, 19, 49)),
    ("east1:68", (71, 11, 74, 56, 4, 74, 19, 71, 4, 51)),
    ("west1:40", (47, 44, 48, 42, 19, 48, 13, 47, 19, 49)),
    ("west1:70", (68, 46, 17, 36, 13, 17, 21, 68, 13, 9)),
    ("east2:45", (6, 13, 64, 29, 49, 64, 63, 6, 49, 31)),
    ("east2:80", (41, 72, 57, 20, 23, 57, 65, 41, 23, 18)),
)


@dataclass(frozen=True)
class WallMask:
    name: str
    bits: tuple[int, ...]

    @property
    def weight(self) -> int:
        return sum(self.bits)


@dataclass(frozen=True)
class WindowMaskScore:
    mask_name: str
    agreements: int
    comparisons: int
    exact_common_tape: bool
    tapes: tuple[tuple[int, ...], ...]


def _ordered_text(
    lines_by_id: Mapping[str, Sequence[str]],
    order: Sequence[str],
) -> str:
    return " ".join(" ".join(lines_by_id[map_id]) for map_id in order)


def wall_masks(
    lines_by_id: Mapping[str, Sequence[str]],
) -> tuple[WallMask, ...]:
    result = []
    for order_name, order in (
        ("world-y", WORLD_VERTICAL_ORDER),
        ("asset-xml", ASSET_XML_ORDER),
    ):
        text = _ordered_text(lines_by_id, order)
        period_question = tuple(
            1 if character == "?" else 0
            for character in text
            if character in ".?"
        )
        period_comma_apostrophe = tuple(
            0 if character == "." else 1
            for character in text
            if character in ".,'"
        )
        if len(period_question) != 83 or sum(period_question) != 33:
            raise ValueError("period/question mask is not 50+33")
        if (
            len(period_comma_apostrophe) != 83
            or sum(period_comma_apostrophe) != 33
        ):
            raise ValueError("period/comma-apostrophe mask is not 50+33")
        words = tuple(
            word
            for map_id in order
            for word in tokenize_wall(map_id, lines_by_id[map_id])
        )
        you_form = tuple(
            0 if word.normalized == "you" else 1
            for word in words
            if word.normalized.startswith("you")
        )
        if len(you_form) != 83 or sum(you_form) != 22:
            raise ValueError("expanded-you mask is not 61+22")
        for family_name, bits in (
            ("period-question", period_question),
            ("period-comma-apostrophe", period_comma_apostrophe),
            ("you-versus-extension", you_form),
        ):
            result.append(WallMask(f"{order_name}/{family_name}", bits))
            result.append(
                WallMask(f"{order_name}/{family_name}/reverse", tuple(reversed(bits)))
            )
    return tuple(result)


def score_mask_on_windows(mask: WallMask) -> WindowMaskScore:
    tapes = tuple(
        tuple(mask.bits[value] for value in values)
        for _, values in THAT_WHICH_WINDOWS
    )
    agreements = sum(
        left_bit == right_bit
        for left_index, left_tape in enumerate(tapes)
        for right_tape in tapes[left_index + 1 :]
        for left_bit, right_bit in zip(left_tape, right_tape, strict=True)
    )
    return WindowMaskScore(
        mask.name,
        agreements,
        15 * len(THAT_WHICH_WINDOWS[0][1]),
        len(set(tapes)) == 1,
        tapes,
    )


def simple_base5_masks() -> Mapping[str, tuple[int, ...]]:
    result: dict[str, tuple[int, ...]] = {}
    values = tuple(range(83))
    digits = {
        value: (value // 25, (value // 5) % 5, value % 5)
        for value in values
    }
    for position in range(3):
        for digit in range(5):
            result[f"eye{position}=={digit}"] = tuple(
                int(digits[value][position] == digit) for value in values
            )
        for threshold in range(1, 5):
            result[f"eye{position}<{threshold}"] = tuple(
                int(digits[value][position] < threshold) for value in values
            )
        result[f"eye{position}-even"] = tuple(
            int(digits[value][position] % 2 == 0) for value in values
        )
    for threshold in range(1, 12):
        result[f"digit-sum>={threshold}"] = tuple(
            int(sum(digits[value]) >= threshold) for value in values
        )
    result["digit-sum-odd"] = tuple(
        int(sum(digits[value]) % 2 == 1) for value in values
    )
    result["value-odd"] = tuple(value % 2 for value in values)
    result["value<33"] = tuple(int(value < 33) for value in values)
    result["value>=50"] = tuple(int(value >= 50) for value in values)
    result["contains-zero"] = tuple(
        int(0 in digits[value]) for value in values
    )
    result["all-distinct"] = tuple(
        int(len(set(digits[value])) == 3) for value in values
    )
    return result


def hamming_up_to_complement(
    left: Sequence[int],
    right: Sequence[int],
) -> int:
    if len(left) != len(right):
        raise ValueError("mask lengths differ")
    direct = sum(a != b for a, b in zip(left, right, strict=True))
    return min(direct, len(left) - direct)
