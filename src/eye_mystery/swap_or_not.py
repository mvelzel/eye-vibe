"""Endpoint constraints for the swap-or-not shuffle on ``Z_83``.

One round with key ``k`` either leaves a value ``x`` alone or reflects it to
``k - x``.  The round's Boolean swap function decides which paired positions
actually exchange.  Ignoring those pair-consistency constraints gives a
necessary endpoint condition: after a fixed key sequence, every source-target
edge must be one of a small set of affine forms ``y = sign*x + constant``.

Failure of this deliberately relaxed test therefore rules out the exact
low-round construction in the visible numeric coordinates.  Passing it would
only justify a stronger pair-consistency test.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import product
from typing import Sequence

from eye_mystery.affine_embedding import Context


MODULUS = 83


@dataclass(frozen=True)
class EndpointAudit:
    """Best relaxed endpoint fit for one context and round count."""

    rounds: int
    matched: int
    total: int
    exemplar_keys: tuple[int, ...]
    full_key_tuples: int

    @property
    def compatible(self) -> bool:
        return self.matched == self.total


@lru_cache(maxsize=None)
def endpoint_forms(
    keys: tuple[int, ...], *, modulus: int = MODULUS
) -> frozenset[tuple[int, int]]:
    """Return all ``(sign, constant)`` endpoint forms for ``keys``.

    ``(1, c)`` denotes ``y = x + c`` and ``(-1, c)`` denotes
    ``y = -x + c``, all modulo ``modulus``.
    """

    forms: set[tuple[int, int]] = {(1, 0)}
    for key in keys:
        if not 0 <= key < modulus:
            raise ValueError("round keys must be residues modulo the modulus")
        forms |= {
            (-sign, (key - constant) % modulus)
            for sign, constant in tuple(forms)
        }
    return frozenset(forms)


def edge_matches_forms(
    left: int,
    right: int,
    forms: Sequence[tuple[int, int]] | frozenset[tuple[int, int]],
    *,
    modulus: int = MODULUS,
) -> bool:
    """Return whether one relaxed endpoint form maps ``left`` to ``right``."""

    return any(
        (sign * left + constant) % modulus == right
        for sign, constant in forms
    )


def audit_endpoint_fit(
    context: Context,
    rounds: int,
    *,
    modulus: int = MODULUS,
) -> EndpointAudit:
    """Exhaust all visible-coordinate key tuples for ``rounds``.

    The result is a necessary-condition audit only: it does not enforce that
    two tracked cards occupying one round pair make the same swap decision.
    """

    if rounds < 1:
        raise ValueError("rounds must be positive")
    if not context.pairs:
        raise ValueError("context must contain at least one mapping")
    if any(
        not 0 <= value < modulus for pair in context.pairs for value in pair
    ):
        raise ValueError("context labels must be residues modulo the modulus")

    best_matched = -1
    exemplar: tuple[int, ...] = ()
    full_key_tuples = 0
    for keys in product(range(modulus), repeat=rounds):
        forms = endpoint_forms(keys, modulus=modulus)
        matched = sum(
            edge_matches_forms(left, right, forms, modulus=modulus)
            for left, right in context.pairs
        )
        if matched > best_matched:
            best_matched = matched
            exemplar = keys
        if matched == len(context.pairs):
            full_key_tuples += 1
    return EndpointAudit(
        rounds,
        best_matched,
        len(context.pairs),
        exemplar,
        full_key_tuples,
    )
