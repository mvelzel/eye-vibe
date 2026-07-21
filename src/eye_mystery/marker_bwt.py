"""Burrows-Wheeler interpretation of the nine initial-marker payloads."""

from __future__ import annotations

from collections import Counter
from itertools import permutations

from eye_mystery.corpus import MESSAGE_ORDER
from eye_mystery.initials import initial_digits, perfect_successor_rotation


def stable_lf_mapping(last_column: tuple[int, ...]) -> tuple[int, ...]:
    """Map each occurrence in a BWT last column to its sorted occurrence."""

    starts: dict[int, int] = {}
    position = 0
    counts = Counter(last_column)
    for symbol in sorted(counts):
        starts[symbol] = position
        position += counts[symbol]
    seen: Counter[int] = Counter()
    result = []
    for symbol in last_column:
        result.append(starts[symbol] + seen[symbol])
        seen[symbol] += 1
    return tuple(result)


def inverse_cyclic_bwt(
    last_column: tuple[int, ...], primary_index: int
) -> tuple[int, ...]:
    """Invert a cyclic BWT using its primary row index."""

    if not last_column:
        raise ValueError("last column cannot be empty")
    if primary_index not in range(len(last_column)):
        raise ValueError("primary index is outside the last column")
    lf = stable_lf_mapping(last_column)
    row = primary_index
    reversed_plaintext = []
    for _ in last_column:
        reversed_plaintext.append(last_column[row])
        row = lf[row]
    return tuple(reversed(reversed_plaintext))


def cyclic_bwt(
    plaintext: tuple[int, ...]
) -> tuple[tuple[int, ...], int]:
    """Return the last column and primary index of sorted cyclic rotations."""

    if not plaintext:
        raise ValueError("plaintext cannot be empty")
    rotations = sorted(
        plaintext[index:] + plaintext[:index]
        for index in range(len(plaintext))
    )
    return tuple(rotation[-1] for rotation in rotations), rotations.index(
        plaintext
    )


def marker_last_column() -> tuple[int, ...]:
    """Read the third marker digits in the East-5-first trail order."""

    trail = perfect_successor_rotation()
    if trail is None:
        raise ValueError("markers do not define a unique trail rotation")
    digits = dict(zip(MESSAGE_ORDER, initial_digits(), strict=True))
    return tuple(digits[name][2] for name in trail)


def marker_bwt_lf_order() -> tuple[str, ...]:
    """Return message rows encountered by LF from the East 5 primary row."""

    trail = perfect_successor_rotation()
    if trail is None:
        raise ValueError("markers do not define a unique trail rotation")
    lf = stable_lf_mapping(marker_last_column())
    order = []
    row = 0
    for _ in trail:
        order.append(trail[row])
        row = lf[row]
    return tuple(order)


def marker_bwt_plaintext_order() -> tuple[str, ...]:
    """Return message identities associated with the restored BWT digits."""

    return tuple(reversed(marker_bwt_lf_order()))


def base5_trigram_values(digits: tuple[int, ...]) -> tuple[int, ...]:
    if len(digits) % 3:
        raise ValueError("digit count must be divisible by three")
    if any(digit not in range(5) for digit in digits):
        raise ValueError("digits must be in 0..4")
    return tuple(
        25 * digits[index] + 5 * digits[index + 1] + digits[index + 2]
        for index in range(0, len(digits), 3)
    )


def marker_bwt_summary() -> dict[str, object]:
    last_column = marker_last_column()
    restored = inverse_cyclic_bwt(last_column, 0)
    values = base5_trigram_values(restored)
    return {
        "last_column": last_column,
        "first_column": tuple(sorted(last_column)),
        "lf_mapping": stable_lf_mapping(last_column),
        "lf_order": marker_bwt_lf_order(),
        "plaintext_order": marker_bwt_plaintext_order(),
        "restored_digits": restored,
        "values": values,
        "ascii32": "".join(chr(value + 32) for value in values),
        "round_trip": cyclic_bwt(restored) == (last_column, 0),
    }


def marker_bwt_multiset_null_counts() -> dict[str, int]:
    """Enumerate all distinct orderings of the observed payload multiset."""

    multiset = tuple(sorted(marker_last_column()))
    seen: set[tuple[int, ...]] = set()
    counts = {
        "permutations": 0,
        "single_cycle": 0,
        "valid_0_82": 0,
        "punct_upper_lower": 0,
        "case_insensitive_fi_suffix": 0,
        "exact_bang_fi": 0,
    }
    for last_column in permutations(multiset):
        if last_column in seen:
            continue
        seen.add(last_column)
        counts["permutations"] += 1
        lf = stable_lf_mapping(last_column)
        row = 0
        visited = set()
        for _ in last_column:
            visited.add(row)
            row = lf[row]
        if len(visited) != len(last_column) or row != 0:
            continue
        counts["single_cycle"] += 1
        restored = inverse_cyclic_bwt(last_column, 0)
        values = base5_trigram_values(restored)
        if any(value > 82 for value in values):
            continue
        counts["valid_0_82"] += 1
        text = "".join(chr(value + 32) for value in values)
        counts["punct_upper_lower"] += (
            text[0] in "!?." and text[1].isupper() and text[2].islower()
        )
        counts["case_insensitive_fi_suffix"] += text[1:].lower() == "fi"
        counts["exact_bang_fi"] += text == "!Fi"
    return counts


def marker_bwt_trail_assignment_counts() -> dict[str, int]:
    """Calibrate BWT outputs among observed-marker assignments on the trail."""

    markers = initial_digits()
    trail = (8, 0, 1, 2, 3, 4, 5, 6, 7)
    counts = {
        "fixed_trail": 0,
        "single_cycle": 0,
        "valid_0_82": 0,
        "exact_bang_fi": 0,
    }
    for assignment in permutations(range(9)):
        if not all(
            markers[assignment[trail[index]]][0] - 1
            == markers[assignment[trail[index + 1]]][1]
            for index in range(8)
        ):
            continue
        counts["fixed_trail"] += 1
        last_column = tuple(
            markers[assignment[message]][2] for message in trail
        )
        lf = stable_lf_mapping(last_column)
        row = 0
        visited = set()
        for _ in last_column:
            visited.add(row)
            row = lf[row]
        if len(visited) != len(last_column) or row != 0:
            continue
        counts["single_cycle"] += 1
        values = base5_trigram_values(
            inverse_cyclic_bwt(last_column, 0)
        )
        if any(value > 82 for value in values):
            continue
        counts["valid_0_82"] += 1
        counts["exact_bang_fi"] += (
            "".join(chr(value + 32) for value in values) == "!Fi"
        )
    return counts
