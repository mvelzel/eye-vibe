# Thirty-seventh pass — terminal-repeat row-2 record freeze

## Question

Does marker row 2 encode the terminal repeat event of the promoted late common
phase?

The previous pass independently established:

```text
late common phase length          30
late E4/W4 source-pair boundary   34 = West3 marker
```

The common equality signature ends at zero-based position 29. Its final class
last appeared at position 16, so the terminal back-reference distance is 13.

The inspected row-2 equations are:

```text
West3 34 + terminal position 29 = East3 63
East3 63 + repeat distance 13   = West2 76
```

Equivalently, reading the reverse control cycle from its boundary:

```text
34 -> 63 -> 76
increments 29,13
```

The observation was made before this freeze. Counts are conditional
specificity measures, not prospective discovery p-values.

## Fixed inputs

Freeze:

- orthodox marker values modulo 83;
- natural marker rows and message identities;
- the established row-2 reverse-cycle control edges;
- late entry points derived from the published final contexts;
- the maximal three-panel equality-signature prefix, not numeric body labels;
- the source-pair boundary 34 promoted in the previous pass;
- zero-based positions, because equality signatures are indexed that way;
- distance to the immediately previous occurrence of the terminal class.

Do not vary the phase start, truncate the signature, skip an occurrence, use a
one-based position, reverse the back-reference, or apply an affine transform
in the primary test.

## Primary staged statistics

For every one of the 12,096 graph-conditioned scalar assignments, count:

1. `boundary`: West3 equals the measured late source-pair boundary 34;
2. `position`: boundary plus terminal index 29 equals East3;
3. `record`: East3 plus terminal repeat distance 13 equals West2.

Also cross the complete record with:

- the previously promoted full phase/header repair;
- its source-delta and boundary topology;
- the two full factoradic scalar survivors.

Nested counts are reported separately and never multiplied.

## Broad controls

Extract every repeat event in the common 30-symbol signature as:

```text
(current position, distance to immediately previous occurrence)
```

Report three broadened conditional events.

### Row-2 ordering

Keep row 2 fixed, but allow:

- any of its three markers as the base;
- either ordering of the remaining two;
- any repeat event in the phase.

Require `base+position=middle` and `middle+distance=end` modulo 83.

### Any marker row

Additionally allow any of the three marker rows and any ordering.

### Signed broad event

Additionally allow each of the two increments to have either sign. This is
the broadest event and discloses ordinary three-number arithmetic fits.

On the observed marker grid, inventory every matching row, order, event, and
sign. The fixed terminal record should be identified explicitly among them.

## Calibration and promotion gate

Tests must recover:

- the complete late equality signature;
- repeat events `(9,4)`, `(18,18)`, `(26,4)`, `(27,26)`, `(29,13)`;
- terminal event `(29,13)`;
- exact observed record `34->63->76`;
- a synthetic planted record;
- failure after changing one target marker.

Promote row 2 as a terminal-repeat pointer record only if:

- the fixed record is rare in the conditional universe;
- the broad event inventory is reported;
- combining it with the already frozen topology selects a unique scalar
  assignment;
- no alternate repeat event gives an equally natural fixed-role record.

A positive result explains marker-layer control fields. It does not yet
decode visible labels or prove that the bodies contain prose.
