"""Decode candidates for affine group-autokey actions over F_83."""

from __future__ import annotations

from collections.abc import Callable, Sequence

MODULUS = 83


def decode_affine_gak(
    ciphertext: Sequence[int],
    multiplier_for_plaintext: Callable[[int], int],
    mode: str = "full",
) -> tuple[int, ...] | None:
    """Decode the visible coset coordinate of ``AGL(1, 83)``.

    Write the hidden affine state as ``(a, b)`` and the visible coordinate as
    ``x=b/a``.  Normalize each plaintext operation so its translation-to-
    multiplier ratio is the plaintext value ``t``. Then

    ``t_i = (x_i - x_(i-1)) * a_(i-1)`` and ``a_i = u(t_i)*a_(i-1)``.

    ``mode`` controls whether the first ciphertext value is an ordinary output,
    a visible primer, an ignored indicator, or an initializer for hidden ``a``.
    """
    if not ciphertext:
        return ()
    if mode == "full":
        previous = 0
        hidden = 1
        body = ciphertext
    elif mode == "primer":
        previous = ciphertext[0]
        hidden = 1
        body = ciphertext[1:]
    elif mode == "skip":
        previous = 0
        hidden = 1
        body = ciphertext[1:]
    elif mode == "indicator-hidden":
        previous = 0
        hidden = ciphertext[0] % MODULUS
        body = ciphertext[1:]
    elif mode == "indicator-both":
        previous = ciphertext[0]
        hidden = ciphertext[0] % MODULUS
        body = ciphertext[1:]
    else:
        raise ValueError(f"unknown affine GAK mode: {mode}")
    if hidden == 0:
        return None

    plaintext = []
    for current in body:
        symbol = (current - previous) * hidden % MODULUS
        plaintext.append(symbol)
        multiplier = multiplier_for_plaintext(symbol) % MODULUS
        if multiplier == 0:
            return None
        hidden = hidden * multiplier % MODULUS
        previous = current
    return tuple(plaintext)
