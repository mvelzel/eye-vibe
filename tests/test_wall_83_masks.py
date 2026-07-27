from pathlib import Path

from eye_mystery.noita_wall_messages import load_wall_message_lines
from eye_mystery.wall_83_masks import (
    hamming_up_to_complement,
    score_mask_on_windows,
    wall_masks,
)


ROOT = Path(__file__).parents[1]


def test_wall_masks_have_the_source_selected_cardinalities():
    lines = dict(
        load_wall_message_lines(ROOT / "artifacts/noita-wall-messages-en.txt")
    )
    masks = wall_masks(lines)
    assert len(masks) == 12
    assert {len(mask.bits) for mask in masks} == {83}
    assert {mask.weight for mask in masks} == {22, 33}


def test_window_score_and_complement_invariant_distance():
    lines = dict(
        load_wall_message_lines(ROOT / "artifacts/noita-wall-messages-en.txt")
    )
    mask = wall_masks(lines)[0]
    score = score_mask_on_windows(mask)
    assert score.comparisons == 150
    assert score.agreements >= 10  # East-1:40 and West-1:40 are identical.
    assert hamming_up_to_complement(mask.bits, mask.bits) == 0
    assert hamming_up_to_complement(
        mask.bits,
        tuple(1 - bit for bit in mask.bits),
    ) == 0
