"""Key-independent certificates for Wadsworth-style cipher clocks.

A classical cipher clock has a plaintext ring of size ``m`` and a mixed
ciphertext ring of size ``n``.  Every plaintext character advances both rings
by between one and ``m`` positions.  Consequently, if both ciphertext digrams
``u,v`` and ``v,u`` occur, their two clockwise distances sum to ``n`` and
``m >= ceil(n / 2)`` regardless of the mixed-ring key.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass


AKI_DISK_INPUT_RING = (
    "01234bdmagickefhijlnopqrstuvwxyz56789 "
    "bcke0dmagi1fhij234lvtuke0dmahwxpqrsyznoij234gipqrs85679 "
    "bc1znotufy85lvwx679 "
)


@dataclass(frozen=True)
class DigramOccurrence:
    message: str
    position: int


@dataclass(frozen=True)
class ReciprocalDigramWitness:
    first: int
    second: int
    forward: tuple[DigramOccurrence, ...]
    reverse: tuple[DigramOccurrence, ...]


def reciprocal_digram_witnesses(
    messages: Mapping[str, Sequence[int]],
) -> tuple[ReciprocalDigramWitness, ...]:
    """Return every unordered pair observed in both directed orders."""

    occurrences: dict[
        tuple[int, int], list[DigramOccurrence]
    ] = defaultdict(list)
    for name, message in messages.items():
        for position, (first, second) in enumerate(
            zip(message, message[1:])
        ):
            if first != second:
                occurrences[(first, second)].append(
                    DigramOccurrence(name, position)
                )

    result = []
    for first, second in sorted(occurrences):
        if first >= second or (second, first) not in occurrences:
            continue
        result.append(
            ReciprocalDigramWitness(
                first,
                second,
                tuple(occurrences[(first, second)]),
                tuple(occurrences[(second, first)]),
            )
        )
    return tuple(result)


def reciprocal_plaintext_ring_lower_bound(
    messages: Mapping[str, Sequence[int]], output_ring_size: int
) -> int:
    """Lower-bound a cipher clock's plaintext ring from reciprocal digrams."""

    if output_ring_size < 2:
        raise ValueError("output ring must contain at least two symbols")
    if not reciprocal_digram_witnesses(messages):
        return 1
    return (output_ring_size + 1) // 2


def affine_output_positions(
    size: int, multiplier: int, offset: int
) -> tuple[int, ...]:
    """Map output symbols to positions in an affine-ordered ring."""

    if size < 2:
        raise ValueError("ring must contain at least two positions")
    positions = tuple(
        (multiplier * value + offset) % size for value in range(size)
    )
    if len(set(positions)) != size:
        raise ValueError("multiplier does not define a permutation")
    return positions


def wadsworth_decode(
    ciphertext: Sequence[int],
    input_ring: str,
    output_positions: Sequence[int],
    *,
    initial_offset: int = 0,
) -> str:
    """Decode with the next-occurrence semantics of Aki's cipher clock."""

    if not input_ring:
        raise ValueError("input ring cannot be empty")
    output_size = len(output_positions)
    if set(output_positions) != set(range(output_size)):
        raise ValueError("output positions must be a permutation")
    mechanism_offset = initial_offset
    plaintext = []
    for symbol in ciphertext:
        if symbol not in range(output_size):
            raise ValueError("ciphertext symbol is outside the output ring")
        target = output_positions[symbol]
        shift = (target - mechanism_offset % output_size) % output_size
        if shift == 0:
            shift = output_size
        mechanism_offset += shift
        plaintext.append(input_ring[mechanism_offset % len(input_ring)])
    return "".join(plaintext)
