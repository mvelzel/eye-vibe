"""Additive synchronization tests for unequal-length edit paths.

If visible values encode increments ``value - neutral`` in a cyclic group,
two alternative paths that leave and re-enter the same state must satisfy

``sum(left) - len(left) * neutral ==
  sum(right) - len(right) * neutral``.

The helpers here solve that constraint exactly and find short literal edit
diamonds without assigning language to the symbols.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class AdditiveDiamond:
    """Two alternative visible paths between the same proposed states."""

    left: tuple[int, ...]
    right: tuple[int, ...]

    def neutral_solutions(self, modulus: int) -> tuple[int, ...]:
        """Return every neutral value that makes the paths rejoin."""

        if modulus < 2:
            raise ValueError("modulus must be at least two")
        coefficient = len(self.left) - len(self.right)
        target = sum(self.left) - sum(self.right)
        common = gcd(abs(coefficient), modulus)
        if target % common:
            return ()
        reduced_modulus = modulus // common
        if reduced_modulus == 1:
            return tuple(range(modulus))
        reduced_coefficient = coefficient // common
        reduced_target = target // common
        base = (
            reduced_target
            * pow(reduced_coefficient % reduced_modulus, -1, reduced_modulus)
        ) % reduced_modulus
        return tuple(
            sorted(base + offset * reduced_modulus for offset in range(common))
        )

    def residual(self, neutral: int, modulus: int) -> int:
        """Return the modular displacement mismatch at one neutral."""

        left = sum(value - neutral for value in self.left)
        right = sum(value - neutral for value in self.right)
        return (left - right) % modulus


@dataclass(frozen=True)
class LiteralEditDiamond:
    """One short unequal branch bracketed by two copied contexts."""

    left_name: str
    right_name: str
    left_start: int
    right_start: int
    context_length: int
    left_path: tuple[int, ...]
    right_path: tuple[int, ...]

    @property
    def additive(self) -> AdditiveDiamond:
        return AdditiveDiamond(self.left_path, self.right_path)


def literal_edit_diamonds(
    streams: Mapping[str, Sequence[int]],
    *,
    context_length: int,
    maximum_gap: int,
) -> tuple[LiteralEditDiamond, ...]:
    """Find copied-context diamonds whose branch lengths differ by one.

    Both boundary contexts are literal and non-overlapping.  The search is
    exhaustive over unordered stream pairs, gaps ``1..maximum_gap``, and both
    possible one-symbol length differences.
    """

    if context_length < 1 or maximum_gap < 1:
        raise ValueError("context length and maximum gap must be positive")
    names = tuple(streams)
    results: list[LiteralEditDiamond] = []
    for left_index, left_name in enumerate(names):
        left = tuple(streams[left_name])
        for right_name in names[left_index + 1 :]:
            right = tuple(streams[right_name])
            right_contexts: dict[tuple[int, ...], list[int]] = {}
            for right_start in range(len(right) - context_length + 1):
                context = right[
                    right_start : right_start + context_length
                ]
                right_contexts.setdefault(context, []).append(right_start)
            for left_start in range(len(left) - context_length + 1):
                context = left[left_start : left_start + context_length]
                for right_start in right_contexts.get(context, ()):
                    left_branch_start = left_start + context_length
                    right_branch_start = right_start + context_length
                    for left_length in range(1, maximum_gap + 1):
                        left_end = left_branch_start + left_length
                        if left_end + context_length > len(left):
                            continue
                        for right_length in (left_length - 1, left_length + 1):
                            if not 1 <= right_length <= maximum_gap:
                                continue
                            right_end = right_branch_start + right_length
                            if right_end + context_length > len(right):
                                continue
                            if (
                                left[left_end : left_end + context_length]
                                != right[
                                    right_end : right_end + context_length
                                ]
                            ):
                                continue
                            results.append(
                                LiteralEditDiamond(
                                    left_name,
                                    right_name,
                                    left_start,
                                    right_start,
                                    context_length,
                                    left[left_branch_start:left_end],
                                    right[right_branch_start:right_end],
                                )
                            )
    return tuple(results)
