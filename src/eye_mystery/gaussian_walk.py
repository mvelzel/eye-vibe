"""Natural eye-direction walks over the quadratic field ``F_83[i]``.

Because 83 is 3 modulo 4, ``x^2 + 1`` is irreducible over ``F_83``.  The five
eye directions therefore have the literal interpretation ``0, ±1, ±i`` in the
field with 83² elements.
"""

from __future__ import annotations

from collections.abc import Sequence

MODULUS = 83
Gaussian = tuple[int, int]

EYE_VECTORS: tuple[Gaussian, ...] = (
    (0, 0),
    (0, 1),
    (1, 0),
    (0, MODULUS - 1),
    (MODULUS - 1, 0),
)


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return ((left[0] + right[0]) % MODULUS, (left[1] + right[1]) % MODULUS)


def multiply(left: Gaussian, right: Gaussian) -> Gaussian:
    real = left[0] * right[0] - left[1] * right[1]
    imaginary = left[0] * right[1] + left[1] * right[0]
    return real % MODULUS, imaginary % MODULUS


def norm(value: Gaussian) -> int:
    return (value[0] * value[0] + value[1] * value[1]) % MODULUS


def inverse(value: Gaussian) -> Gaussian:
    if value == (0, 0):
        return value
    scale = pow(norm(value), -1, MODULUS)
    return value[0] * scale % MODULUS, -value[1] * scale % MODULUS


def transform_center(value: Gaussian, mode: str) -> Gaussian:
    real, imaginary = value
    if mode == "identity":
        return value
    if mode == "negation":
        return -real % MODULUS, -imaginary % MODULUS
    if mode == "conjugation":
        return real, -imaginary % MODULUS
    if mode == "inversion":
        return inverse(value)
    if mode == "rotate-left":
        return -imaginary % MODULUS, real
    if mode == "rotate-right":
        return imaginary, -real % MODULUS
    raise ValueError(f"unknown center mode: {mode}")


def observe(value: Gaussian, mode: str) -> int | Gaussian:
    real, imaginary = value
    if mode == "state":
        return value
    if mode == "real":
        return real
    if mode == "imaginary":
        return imaginary
    if mode == "norm":
        return norm(value)
    if mode == "slope":
        return (
            MODULUS
            if real == 0
            else imaginary * pow(real, -1, MODULUS) % MODULUS
        )
    if mode == "unit-phase":
        if value == (0, 0):
            return value
        # z^(q-1) lies in the norm-one subgroup of size q+1.
        result = (1, 0)
        base = value
        exponent = MODULUS - 1
        while exponent:
            if exponent & 1:
                result = multiply(result, base)
            base = multiply(base, base)
            exponent >>= 1
        return result
    raise ValueError(f"unknown observation mode: {mode}")


def trace_gaussian_walk(
    message: Sequence[int],
    *,
    center_mode: str,
    observation: str,
    up_order: tuple[int, int, int] = (0, 1, 2),
    down_order: tuple[int, int, int] | None = None,
    initial: Gaussian = (0, 0),
) -> tuple[int | Gaussian, ...]:
    if len(message) % 3:
        raise ValueError("eye stream length must be divisible by three")
    down_order = up_order if down_order is None else down_order
    value = (initial[0] % MODULUS, initial[1] % MODULUS)
    output = []
    for offset in range(0, len(message), 3):
        order = up_order if (offset // 3) % 2 == 0 else down_order
        trigram = message[offset : offset + 3]
        for index in order:
            eye = trigram[index]
            if eye == 0:
                value = transform_center(value, center_mode)
            else:
                value = add(value, EYE_VECTORS[eye])
        output.append(observe(value, observation))
    return tuple(output)
