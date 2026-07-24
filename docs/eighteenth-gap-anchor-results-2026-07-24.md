# Eighteenth focused lead — gap-anchor/header results

## Result

The final-row gap-anchor/header relation survives the frozen full selection
correction and is promoted as a real construction link.

```text
exact targeted corrected tail     1 / 50001 = .0000199996
broad gap/order corrected tail   56 / 50001 = .0011199776
```

This is not plaintext and does not show that modular subtraction is applied
at every cipher step. It is positive evidence that the three final markers
are coupled to an independently selected equality landmark in their bodies.

## Exact reproduction

After deleting each marker and the copied 20-symbol opening, the unique clean
gap-11 endpoint repeat occurs at:

```text
message  trimmed position  full-array position  anchor
E4       16                37                   75
W4       18                39                   81
E5       17                38                   48
```

Each window has equality signature `A..........A`: the endpoints agree, all
ten interior values are distinct, and none equals the endpoint.

The orthodox marker values are:

```text
(h_E4,h_W4,h_E5) = (27,77,33)
```

They reproduce exactly:

```text
75 - 48 = 27 mod 83
75 - 81 = 77 mod 83
81 - 48 = 33 mod 83
```

Using only E4's identity-panel anchor and the marker values predicts both
nonreference anchors:

```text
a_W4 = 75 - 77 = 81 mod 83
a_E5 = 75 - 27 = 48 mod 83
```

## Controls

The detector first recovers a short planted triple with the same clean
gap-11 anchors and exact formula.

Fifty thousand controls independently shuffle each post-opening body while
preserving its exact length, symbol multiset, and no-adjacent-double
condition. Of them:

```text
1616  have exactly one clean gap-11 anchor in every message
   0  also satisfy the exact reported formula
  55  find any match after searching gaps 2..30 and all six anchor orders
```

The broad statistic also ignores header-to-edge assignment by comparing
multisets. It therefore charges the visible retrospective choices much more
heavily than the original observation.

## Interpretation

In message order `E4 -> W4 -> E5`, the relation is a telescoping difference
record:

```text
h_W4 = a_E4 - a_W4
h_E5 = a_W4 - a_E5
h_E4 = a_E4 - a_E5 = h_W4 + h_E5 mod 83
```

This fits the independently developed view that the first glyphs are typed
ordering/check fields rather than encrypted ordinal numbers. It also gives a
concrete consumer for the final row's factoradic header classes: the identity
panel carries the total difference and the two adjacent-transposition panels
carry the two path increments.

That interpretation remains provisional. The calculation proves association
under the frozen null, not why gap 11 was chosen or how the first two header
rows operate.

## Next tests

Before treating the natural `0..82` arithmetic as authored rather than an
accidental label assignment, run two separately frozen equality-preserving
controls:

1. globally permute all 83 body labels while keeping the three markers fixed;
2. globally permute the shared 83-label alphabet in both markers and bodies.

Then work outward from the established final-row consumer. Do not scan
arbitrary arithmetic over the first two rows. First derive candidate landmark
selectors from their already established equality-isomorph families, and
require a row-typed rule to predict withheld anchors under full reselection.
