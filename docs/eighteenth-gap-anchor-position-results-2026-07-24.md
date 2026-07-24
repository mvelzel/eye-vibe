# Gap-anchor position/permutation follow-up — results

## Result

The anchor-position permutation passes the frozen broad joint control:

```text
broad joint corrected tail = 1/50001 = .0000199996
```

No control finds both a selection-corrected numeric match and three
consecutive positions in one of the final header orders after searching every
gap `2..30`.

This is another aspect of the already promoted final-row record, not an
independent discovery whose tail can be multiplied by earlier tails.

## Exact position record

The three unique gap-11 anchors occur at trimmed positions:

```text
(E4,W4,E5) = (16,18,17) = 16 + (0,2,1)
```

The final marker edges and their component orders are:

```text
message  marker  control edge  component order
E4       27      0->0          012 (identity convention)
W4       77      0->2          021
E5       33      1->0          102
```

Thus the anchor-position ranks are exactly W4's independently defined order
`021`.

## Positive and matched controls

The short position plant is recovered exactly at gap 11 with anchors
`75,81,48` and positions `0,2,1`.

Across 50,000 new body shuffles:

```text
1612  have one clean gap-11 anchor in every message
   1  has positions equal to one translated 021
   1  satisfies the exact numeric formula
   0  satisfies both exact properties
   0  survives the broad joint gap/order search
```

Plus-one corrected tails are:

```text
exact position only   2/50001 = .0000399992
exact joint           1/50001 = .0000199996
broad joint           1/50001 = .0000199996
```

The one exact-position control and the one exact-numeric control are different
shuffles.

## Interpretation

The same final row now has two reproduced interfaces:

1. full marker values encode the two mod-83 path differences and their
   telescoping total;
2. the W4 marker's control edge encodes the relative position order of the
   three repeated-body landmarks.

This is substantially more specific than saying the first glyphs are generic
checks. It suggests a small typed construction record whose fields choose a
landmark ordering and verify its labels.

The result still does not identify the selector's semantic reason—why a clean
gap of 11 at base position 16—or recover plaintext. Those questions require a
fresh wide follow-up rather than scanning nearby integers.
