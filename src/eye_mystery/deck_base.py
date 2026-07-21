"""Deck cipher with a fixed affine shuffle plus one plaintext-dependent swap."""

from __future__ import annotations

from collections.abc import Sequence


def decode_affine_base_swap(
    ciphertext: Sequence[int],
    multiplier: int,
    offset: int,
    modulus: int = 83,
    secondary: str = "none",
) -> tuple[int, ...]:
    """Recover swap positions for ``base shuffle; swap(top, k); emit top``.

    The fixed base shuffle is represented by ``new[j] = old[a*j+b]``.
    A lazy affine coordinate system makes each state update constant-time.
    The initial card order is the canonical ``0..modulus-1`` ordering.
    """
    multiplier %= modulus
    offset %= modulus
    if multiplier == 0:
        raise ValueError("multiplier must be invertible")
    inverse = pow(multiplier, -1, modulus)

    coordinate_of = list(range(modulus))
    card_at_coordinate = list(range(modulus))
    scale = 1
    shift = 0
    plaintext = []

    def swap_positions(left: int, right: int) -> None:
        if left == right:
            return
        inverse_scale = pow(scale, -1, modulus)
        left_coordinate = (left - shift) * inverse_scale % modulus
        right_coordinate = (right - shift) * inverse_scale % modulus
        left_card = card_at_coordinate[left_coordinate]
        right_card = card_at_coordinate[right_coordinate]
        coordinate_of[left_card], coordinate_of[right_card] = (
            right_coordinate,
            left_coordinate,
        )
        card_at_coordinate[left_coordinate], card_at_coordinate[right_coordinate] = (
            right_card,
            left_card,
        )

    for card in ciphertext:
        # Applying new[j] = old[a*j+b] moves old position x to
        # j = a^-1 * (x-b).
        scale = inverse * scale % modulus
        shift = inverse * (shift - offset) % modulus
        position = (scale * coordinate_of[card] + shift) % modulus
        plaintext.append(position)

        swap_positions(0, position)

        if secondary == "none":
            pass
        elif secondary == "one-k":
            if position not in (0, 1):
                swap_positions(1, position)
        elif secondary == "adjacent":
            other = (position + 1) % modulus
            if position != 0 and other != 0:
                swap_positions(position, other)
        elif secondary == "mirror":
            other = -position % modulus
            if position != 0 and other != 0:
                swap_positions(position, other)
        elif secondary == "double":
            other = 2 * position % modulus
            if position != 0 and other != 0:
                swap_positions(position, other)
        elif secondary == "half-turn":
            other = (position + modulus // 2) % modulus
            if position != 0 and other != 0:
                swap_positions(position, other)
        elif secondary == "fixed-1-2":
            swap_positions(1, 2)
        else:
            raise ValueError(f"unknown secondary swap: {secondary}")
    return tuple(plaintext)
