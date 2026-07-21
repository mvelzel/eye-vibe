"""Search simple stateful cipher families over the prime field F_83."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass

from .metrics import index_of_coincidence

MODULUS = 83


@dataclass(frozen=True)
class FieldResult:
    family: str
    parameters: tuple[int, ...]
    unique: int
    ioc: float
    length: int


def _result(family: str, parameters: tuple[int, ...], values: Sequence[int]) -> FieldResult:
    unique = len(set(values))
    return FieldResult(
        family=family,
        parameters=parameters,
        unique=unique,
        ioc=index_of_coincidence(values, unique),
        length=len(values),
    )


def affine_recurrence(
    messages: Iterable[Sequence[int]], max_lag: int = 32
) -> list[FieldResult]:
    """Test ``p[i] = c[i] - a*c[i-lag] (mod 83)``."""
    messages = tuple(messages)
    results = []
    for lag in range(1, max_lag + 1):
        for multiplier in range(MODULUS):
            residuals = [
                (message[index] - multiplier * message[index - lag]) % MODULUS
                for message in messages
                for index in range(lag, len(message))
            ]
            results.append(_result("affine-recurrence", (lag, multiplier), residuals))
    return results


def two_lag_recurrence(
    messages: Iterable[Sequence[int]],
) -> list[FieldResult]:
    """Test ``p[i] = c[i] - a*c[i-1] - b*c[i-2] (mod 83)``."""

    messages = tuple(messages)
    results = []
    for first in range(MODULUS):
        for second in range(MODULUS):
            residuals = [
                (
                    message[index]
                    - first * message[index - 1]
                    - second * message[index - 2]
                )
                % MODULUS
                for message in messages
                for index in range(2, len(message))
            ]
            results.append(
                _result("two-lag-recurrence", (first, second), residuals)
            )
    return results


def polynomial_position_mask(messages: Iterable[Sequence[int]]) -> list[FieldResult]:
    """Test all quadratic positional masks ``c[i] - a*i - b*i^2``."""
    messages = tuple(messages)
    results = []
    indexed = tuple((index, value) for message in messages for index, value in enumerate(message))
    for linear in range(MODULUS):
        for quadratic in range(MODULUS):
            residuals = [
                (value - linear * index - quadratic * index * index) % MODULUS
                for index, value in indexed
            ]
            results.append(_result("quadratic-position", (linear, quadratic), residuals))
    return results


def shifted_ratio(messages: Iterable[Sequence[int]]) -> list[FieldResult]:
    """Test ``p[i] = (c[i]+s)/(c[i-1]+s)`` on the projective line.

    The value 83 is used for the point at infinity when a denominator is zero.
    """
    messages = tuple(messages)
    results = []
    for shift in range(MODULUS):
        ratios = []
        for message in messages:
            for previous, current in zip(message, message[1:]):
                numerator = (current + shift) % MODULUS
                denominator = (previous + shift) % MODULUS
                ratios.append(
                    MODULUS
                    if denominator == 0
                    else numerator * pow(denominator, -1, MODULUS) % MODULUS
                )
        results.append(_result("shifted-ratio", (shift,), ratios))
    return results


def tangent_difference(messages: Iterable[Sequence[int]]) -> list[FieldResult]:
    """Test a one-parameter projective group law.

    ``p[i] = (c[i]-c[i-1]) / (1+k*c[i]*c[i-1])``.  This includes ordinary
    finite differences at ``k=0`` and is the finite-field analogue of the
    tangent subtraction identity.  Undefined denominators map to infinity.
    """
    messages = tuple(messages)
    results = []
    for factor in range(MODULUS):
        residuals = []
        for message in messages:
            for previous, current in zip(message, message[1:]):
                numerator = (current - previous) % MODULUS
                denominator = (1 + factor * current * previous) % MODULUS
                residuals.append(
                    MODULUS
                    if denominator == 0
                    else numerator * pow(denominator, -1, MODULUS) % MODULUS
                )
        results.append(_result("tangent-difference", (factor,), residuals))
    return results


def best(results: Iterable[FieldResult], limit: int = 10) -> tuple[FieldResult, ...]:
    """Rank for plaintext-like collapse: few symbols first, then high IoC."""
    return tuple(sorted(results, key=lambda item: (item.unique, -item.ioc))[:limit])
