from eye_mystery.wall_baconian import (
    baconian_values,
    decode_values,
    tokenize_wall,
)


def test_baconian_grouping_and_orientations():
    bits = tuple(character == "B" for character in "AAAAA" "AAAAB" "BAAAA")
    assert baconian_values(bits) == (0, 1, 16)
    assert baconian_values(bits, reverse_bits=True) == (0, 16, 1)
    assert baconian_values(bits, inverted=True) == (31, 30, 15)
    assert decode_values((0, 1, 25, 26, 31)) == "ABZ??"


def test_wall_tokenization_preserves_contractions_and_suffixes():
    words = tokenize_wall("G0", ("You don't. Why?",))
    assert [word.normalized for word in words] == ["you", "don't", "why"]
    assert [word.suffix for word in words] == [" ", ". ", "?"]
