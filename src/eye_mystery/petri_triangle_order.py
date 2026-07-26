"""Bound a reading-order transfer from Petri Purho's 2015 triangle renderer."""

from __future__ import annotations

from collections.abc import Mapping


Point = tuple[int, int]
OrderedTriangle = tuple[Point, Point, Point]


# Source/procedural_triangles.cpp, commit 02f7bf1, lines 143-145 and 174-176.
# Coordinates are multiplied by two and translation is discarded.
PETRI_SOURCE_ORDERS: Mapping[str, OrderedTriangle] = {
    "up": ((0, 2), (1, 0), (2, 2)),
    "down": ((1, 0), (2, 2), (3, 0)),
}

# visual_rows.py reconstructs top=(a,b,f), bottom=(c,e,d).  Staggered integer
# coordinates therefore make the two accepted trigrams a,b,c and d,e,f.
EYE_ACCEPTED_ORDERS: Mapping[str, OrderedTriangle] = {
    "down": ((0, 0), (2, 0), (1, 2)),
    "up": ((5, 2), (3, 2), (4, 0)),
}


def signed_double_area(triangle: OrderedTriangle) -> int:
    """Return the exact oriented area numerator for an ordered triangle."""

    (ax, ay), (bx, by), (cx, cy) = triangle
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)


def orientation_signature(
    triangles: Mapping[str, OrderedTriangle],
) -> Mapping[str, int]:
    """Return -1/+1 winding signs, rejecting degenerate input."""

    signature: dict[str, int] = {}
    for name, triangle in triangles.items():
        area = signed_double_area(triangle)
        if area == 0:
            raise ValueError(f"degenerate triangle: {name}")
        signature[name] = 1 if area > 0 else -1
    return signature


def global_orientation_matches() -> tuple[tuple[str, int], ...]:
    """List pairings/determinant signs that pass the global-winding condition.

    ``determinant_sign`` is +1 for an orientation-preserving global symmetry
    and -1 for a reflection.  Both same-orientation and swapped-orientation
    pairings are checked.
    """

    source = orientation_signature(PETRI_SOURCE_ORDERS)
    eye = orientation_signature(EYE_ACCEPTED_ORDERS)
    pairings = {
        "same": (("up", "up"), ("down", "down")),
        "swapped": (("up", "down"), ("down", "up")),
    }
    matches = []
    for name, pairs in pairings.items():
        for determinant_sign in (1, -1):
            if all(
                eye[eye_name] == determinant_sign * source[source_name]
                for source_name, eye_name in pairs
            ):
                matches.append((name, determinant_sign))
    return tuple(matches)
