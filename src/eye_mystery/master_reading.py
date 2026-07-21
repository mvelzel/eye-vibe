"""The Sampo-document's parity-dependent 125-symbol Eye transform.

The stored corpus has already put each visual triangle into the canonical
83-symbol order.  This module first reconstructs left/centre/right visual
positions, then applies Patrick O'Callahan's proposed Master rules:

* downward triangles swap right- and left-facing eye values (2 and 4);
* upward triangles swap up- and down-facing eye values (1 and 3);
* downward triangles read visual positions 1,2,0;
* upward triangles read visual positions 1,0,2.

This is an alternative ciphertext interpretation, not a decryption.
"""

from __future__ import annotations

from collections.abc import Sequence


def visual_triangles(message: Sequence[int]) -> tuple[tuple[int, int, int], ...]:
    """Undo the canonical 021/201 ordering into visual left/centre/right."""

    if len(message) % 3:
        raise ValueError("eye stream length must be divisible by three")
    triangles = []
    for index, start in enumerate(range(0, len(message), 3)):
        grouped = message[start : start + 3]
        if index % 2 == 0:  # downward; canonical visual order 0,2,1
            triangles.append((grouped[0], grouped[2], grouped[1]))
        else:  # upward; canonical visual order 2,0,1
            triangles.append((grouped[1], grouped[2], grouped[0]))
    return tuple(triangles)


def master_rule_values(message: Sequence[int]) -> tuple[int, ...]:
    """Apply the proposed parity rules and return values in ``0..124``."""

    values = []
    for index, visual in enumerate(visual_triangles(message)):
        downward = index % 2 == 0
        substitutions = {2: 4, 4: 2} if downward else {1: 3, 3: 1}
        changed = tuple(substitutions.get(value, value) for value in visual)
        order = (1, 2, 0) if downward else (1, 0, 2)
        values.append(
            25 * changed[order[0]]
            + 5 * changed[order[1]]
            + changed[order[2]]
        )
    return tuple(values)
