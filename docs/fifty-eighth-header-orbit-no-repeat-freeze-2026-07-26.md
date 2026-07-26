# Fifty-eighth pass — orbit obstruction and conditional-rank freeze

**Frozen:** 26 July 2026, before calculating the conditional-rank output.

## Lane C closes before body scoring

The wide horizon proposed selecting one of six coordinates from the header
action on natural row 1, then using its induced panel-equality groups on rows
2–3.

This is non-identifying:

- coordinates `1..4` give three singleton groups on row 1 and therefore no
  equality prediction;
- coordinate `0` gives one all-three group because all nine headers fix the
  center;
- coordinate `5` also gives one all-three group because the three P headers
  fix newline.

Coordinates `0` and `5` become different partitions on the Q rows, but row 1
cannot distinguish them. Choosing between them from Q-body fit would use the
heldout rows to select the model. The exact lane therefore closes as designed,
without scoring aligned body equality.

## Lane D: header-ordered conditional rank

The earlier no-repeat audit used only canonical numeric order. This test adds
one independently decoded input absent there: each message marker's
factoradic five-eye collation.

For each message:

1. order the canonical 83 visible glyphs under the marker's eye order;
2. at each transition, remove the previous glyph from that order;
3. rank the next glyph among the remaining 82;
4. split the rank uniquely as

```text
rank = 41*sheet + magnitude
sheet in {0,1}
magnitude in 0..40
```

The primary output is `magnitude`. This is the canonical two-half quotient,
not a language-selected alphabet. The full conditional rank and sheet are
diagnostics only.

## Frozen context test

Use transitions wholly inside the seven established nonliteral windows; the
first symbol of each window is context only and emits no rank.

Training:

```text
first-gap30
first-cross
first-cross-late
first-gap28
```

Holdout:

```text
last-west4
last-east5
last-east3
```

Try exactly two global routes, header and inverse-header. Select the route by
literal training agreement of magnitudes; a tie chooses header. Score heldout
magnitude agreement once.

Every one of the 6,806 affine permutations of `0..82` globally relabels the
body, preserves the real markers, reselects the route on training, and scores
holdout. This retains every copied prefix, equality isomorph, no-double, and
message-length fact while breaking only the proposed absolute ordered-deck
meaning.

## Decision

Promotion requires:

1. exact heldout upper tail below `.01`;
2. improvement in at least two heldout contexts;
3. a fixed sheet relation or full-rank consequence not used in selection.

Failure closes the marker-ordered version of the static no-repeat enumerative
decoder. It does not reject a changing deck order.
