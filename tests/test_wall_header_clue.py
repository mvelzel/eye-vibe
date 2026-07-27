from fractions import Fraction
from pathlib import Path

from eye_mystery.noita_wall_messages import load_wall_message_lines
from eye_mystery.wall_header_clue import (
    direct_context_table_audit,
    expanded_you_contexts,
    fixed_ordered_word_probability,
    natural_context_reads,
    odd_east_checksums,
    wall_header_counts,
)
from eye_mystery.wall_83_masks import WORLD_VERTICAL_ORDER


ROOT = Path(__file__).parents[1]
TEXT_PATH = ROOT / "artifacts/noita-wall-messages-en.txt"


def _lines():
    return dict(load_wall_message_lines(TEXT_PATH))


def test_wall_counts_match_the_odd_east_headers_only_after_two_repairs():
    counts = wall_header_counts(_lines())
    assert counts.header_tuple == (50, 63, 33)
    assert counts.literal_you == 61
    assert counts.omitted_you == 2
    assert counts.expanded_you == 83

    checksums = odd_east_checksums()
    assert tuple(record.header for record in checksums) == counts.header_tuple
    assert tuple(record.total for record in checksums) == (4040, 5656, 4545)
    assert tuple(record.quotient for record in checksums) == (40, 56, 45)
    assert all(record.remainder == 0 for record in checksums)


def test_zero_based_world_y_previous_read_is_and_created_god():
    contexts = expanded_you_contexts(_lines(), WORLD_VERTICAL_ORDER)
    assert len(contexts) == 83
    reads = natural_context_reads(_lines())
    target = next(
        read
        for read in reads
        if (
            read.order_name,
            read.indexing,
            read.direction,
        )
        == ("world-y", "zero-based", "previous")
    )
    assert target.indices == (50, 63, 33)
    assert target.words == ("and", "created", "god")
    assert tuple(context.map_id for context in target.contexts) == (
        "G1",
        "G2",
        "G1",
    )


def test_sensitivity_family_and_post_hoc_multiset_calculation_are_exact():
    reads = natural_context_reads(_lines())
    assert len(reads) == 16
    assert sum(read.phrase == "AND CREATED GOD" for read in reads) == 1
    assert fixed_ordered_word_probability(
        _lines(),
        ("and", "created", "god"),
    ) == Fraction(1, 10209)


def test_direct_context_table_fails_the_canonical_isomorph_check():
    previous = direct_context_table_audit(_lines(), field="previous")
    assert previous.unique_outputs == 42
    assert previous.expected_pattern == "A.B.CB.AC."
    assert previous.preserved_windows == 2
    assert not previous.common_pattern

    following = direct_context_table_audit(_lines(), field="following")
    token = direct_context_table_audit(_lines(), field="token")
    assert (following.unique_outputs, token.unique_outputs) == (40, 4)
    assert not following.common_pattern
    assert not token.common_pattern
