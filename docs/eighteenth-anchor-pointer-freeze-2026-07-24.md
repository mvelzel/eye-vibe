# Final anchor record pointer/gauge follow-up — freeze

## Seen exact closure

E4 is the unique self-edge panel in the final marker row. Its clean gap-11
repeat has trimmed start/end positions:

```text
16 -> 27
```

The endpoint is exactly its marker:

```text
trimmed endpoint = 27 = h_E4
```

The full array contains one marker plus the copied 20-symbol opening before
the trimmed body. Converting the same endpoint to a full-array zero-based
index gives:

```text
1 + 20 + 27 = 48 = a_E5
```

E5 is not selected after the fact by value. Under E4's identity order `012`,
the source-minus-remaining slot rule uses E4 as component 0 and E5 as the
remaining component 2:

```text
h_E4 = a_E4 - a_E5
```

The pointer therefore fixes the additive gauge and the marker record
reconstructs every anchor:

```text
a_E5 = 1 + prefix20 + h_E4 = 48
a_E4 = a_E5 + h_E4 = 75
a_W4 = a_E4 - h_W4 = 81
h_E5 = a_W4 - a_E5 = 33  (check)
```

This was discovered retrospectively. Index/value coincidences need an
especially broad control.

## Exact statistic

At target gap 11 require:

1. one clean anchor per final panel;
2. the unique component-slot rule `source - remaining`;
3. E4's zero-based trimmed endpoint equals `h_E4`;
4. that endpoint plus the fixed marker/opening frame `21` equals the E5
   anchor selected by E4's remaining component;
5. all reconstructed anchors and the E5 check are exact.

## Broad pointer family

Run 50,000 new matched shuffles with seed `0x18e09`, preserving each trimmed
body's length, multiset, and no-adjacent-double condition.

Every control may search all gaps `2..30`. At a gap with one clean anchor per
panel, first require the previously broadened numeric difference relation.
Then allow:

- any of the three panels as the pointer carrier;
- repeat start or repeat endpoint;
- any of the three marker values for the first index equality;
- any of the three anchor values for the second equality;
- independently for each equality, coordinate offsets
  `{0,1,20,21}`.

These offsets cover zero/one-based trimmed, post-opening body, and full-array
coordinates. A broad pointer match requires the same selected start/end
position to equal a marker under one permitted offset and an anchor under
another.

This family deliberately forgets the self-edge, remaining-component, and
exact frame choices. It charges the entire visible index convention menu,
not just the elegant real route.

Use plus-one corrected tails. A synthetic plant with positions
`16,18,17`, gap 11, and anchors `75,81,48` must pass first.

## Gate

Promote the pointer/gauge closure only if the broad corrected tail is below
`.01`. Do not multiply it with earlier shared-anchor tails. A positive result
would make the final row a closed self-describing record rather than a check
requiring one arbitrary additive seed.
