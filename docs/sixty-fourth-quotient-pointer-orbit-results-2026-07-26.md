# Sixty-fourth pass — quotient-addressed 83-state tables

## Result

The checksum quotient is not only present as a value in its own message. It
also acts as a highly structured address into a parameter-free functional
table:

```text
q = floor(sum(all panel values) / 101)
f(i) = panel[i], for i in 0..82
start at q and follow f until a state repeats
```

Every accepted Eye value is a valid address in `0..82`, so the first 83
full-array values—including the exceptional header at address zero—define
`f: Z83 -> Z83` without a key, relabeling, or fitted operation.

This is the strongest current evidence that the mod-101 quotient is an
executable pointer rather than a retrospective scalar coincidence. It is not
yet a plaintext decoder.

## Complete reproduction

`tail|cycle` below splits each path immediately before the first repeated
state.

```text
panel q  r   forward path                                      tail|cycle
E1    40  0   40,47 -> 47                                        1|1
W1    40 84   40,47 -> 47                                        1|1
E2    47  7   47,64,81,72,66,34,57,10,42 -> 47                   0|9
W2    42 53   42,53,78,35,62,52,47,43,82,1,66 -> 62              4|7
E3    56  0   56,60,22,45 -> 56                                  0|4
W3    47  1   47,32,62,8,11,26,19,28 -> 19                       6|2
E4    53 32   53,58,38,48,75 -> 75                               4|1
W4    48 88   48,64,71,63,50,81,23,80,66,14,59,68,8,29,35,27,16
               -> 68                                            11|6
E5    45  0   45,10,2,5,54,32,79,12,9,40,55,30,60,34 -> 12       7|7
```

The orbit sizes in physical message order are:

```text
2,2,9 | 11,4,8 | 5,17,14
```

They total exactly `72`.

## Eye phase and header consumers

The mod-101-closing family is exactly `E1,E3,E5`. Its three orbits give:

```text
tail nodes                      1+0+7 = 8
cycle nodes                     1+4+7 = 12
orbit nodes with multiplicity           20
distinct union nodes                    17
overlap excess                     20-17 = 3
ordered cycle lengths                  1,4,7
```

Thus the same fixed operation recovers the independently established Eye
phase split `17+3=20`. The cycle lengths form an ordered `+3` progression.

Their pairwise intersection sizes in `E1,E3,E5` order are:

```text
E1∩E3 = 0
E1∩E5 = 1  ({40})
E3∩E5 = 2  ({45,60})
```

The nonempty-mask matches the established header-edge composability pattern
for `0->1, 2->1, 1->0`: the first two edges do not compose with each other,
while each composes with the third. The mask alone is common under the null
and is corroboration, not a discovery statistic.

Across all nine orbits, 51 labels are visited and 32 are omitted:

```text
83 - |union(all nine orbits)| = 32 = E4 checksum remainder
```

E4 is independently the final loop/pivot panel. Allowing every nonzero
checksum remainder barely changes the matched-null rate, because the other
remainders are mostly outside the natural omitted-count range.

## Exact Gate correspondence and its boundary

The quotient orbits partition as:

```text
closing cycles                         12
other nonclosing orbits                43
sole nonclosing orbit with no tail      9  (E2)
closing tails                           8
                                      --
                                      72
```

This is exactly the Gate dossier's proposed Veska partition
`12 outer + 43 crack + 9 upper + 8 lower`.

The ground-up sprite audit prevents overclaiming:

- Veska objectively has 72 authored-color pixels.
- Its separated upper and lower pictograms objectively have 9 and 8 pixels.
- Simple spatial separation of the remaining pixels gives `11+44`, not
  `12+43`.
- The dossier did not publish the extra mask that moves one pixel between
  those groups.

Therefore `72|9|8` is independent later-asset evidence. The pointer model's
`12|43` is a sharp prospective prediction of the missing mask, not evidence
that the mask exists.

## Matched conditional null

One million trials independently randomize each panel's first-83 table while
preserving:

1. its exact table multiset, full checksum, quotient, and remainder;
2. the marker and every panel's longest independently established copied
   prefix;
3. every in-table occurrence of its quotient, including all positions used
   by the preceding self-pointer result;
4. the complete absence of adjacent equal values, including the boundary
   between positions 82 and 83.

The null does not preserve every later nonliteral isomorph, so its rates are
not universal corpus-preserving probabilities. A synthetic 83-table fixture
with unrelated labels and the planted `8|12|9|43`, `20|17`, and `1|4|7`
structure triggers every detector before the real-data result is asserted.

The fixed seed is `0x5645534b41`.

The typed Gate rows use the natural semantic assignment
`cycle->outer, mixed->crack, pure-cycle->upper, tail->lower`. Because that
assignment was noticed retrospectively, the broad rows also allow the
objective `8/9` pair—or the complete four counts—to occupy any of the four
pointer categories. The broad rows govern the evidence assessment.

| Frozen event | Hits / 1,000,000 | Add-one corrected rate |
|---|---:|---:|
| all-nine orbit total `72` | 5,829 | `.005829994` |
| typed objective Gate `72|9|8` | 18 | `.000018999981` |
| broad-category objective Gate `72|9|8` | 102 | `.000102999897` |
| typed predicted `12|43|9|8` | 1 | `.000001999998` |
| any-category predicted `12|43|9|8` | 4 | `.000004999995` |
| closing orbit total/union `20|17` | 4,022 | `.004022996` |
| ordered cycle lengths `1|4|7` | 493 | `.0004939995` |
| any ordered cycle `+3` progression | 2,548 | `.002548997` |
| header composability overlap mask | 124,479 | `.1244799` |
| omitted count equals typed E4 remainder | 34,884 | `.03488497` |
| omitted count equals any checksum remainder | 34,966 | `.03496697` |
| total `72` and omitted count `32` | 343 | `.0003439997` |
| Eye `20|17` and typed Gate `72|9|8` | 0 | `<.000001` |
| Eye `20|17` and broad Gate `72|9|8` | 1 | `.000001999998` |
| preceding broad joint plus cycles `1|4|7` | 0 | `<.000001` |

These are overlapping views of one pointer structure and must not be
multiplied. They are conditional rates, not project-wide discovery
probabilities; the operation was found retrospectively after substantial
exploration.

## Convention audit

The address convention is unusually rigid. Using the body-only table
`panel[1:84]` instead gives:

```text
all total 76
closing total/union 25/24
closing cycles 10,8,2
```

It satisfies none of the bridge events. Scanning every common contiguous
83-cell window start `0..16`, only start zero has the Gate, phase, cycle, or
typed partition events. This selects the exceptional header as table address
zero rather than treating it as discarded framing.

## Decision and next falsifier

Promote the following construction lead:

> The nine panels contain quotient-addressed `83`-state functional tables.
> Their orbit decomposition connects the mod-101 checksums, the `17+3=20`
> phase machine, and the later Veska `72|9|8` artwork.

Do not yet promote:

- the dossier's unpublished `12/43` pixel mask;
- a body-wide cipher or allocation rule;
- plaintext, Finnish or otherwise;
- alternate seeds, moduli, table lengths, window offsets, or aggregate
  ledgers chosen after this result.

The next valid advance must be prospective: recover an objective Veska mask
that yields `12/43` without using the target, find an authored interface that
selects this quotient-pointer operation, or use the frozen orbit partition to
predict an uninspected Eye transition/value.

Reproduction:
[`audit_quotient_pointer_orbits.py`](../scripts/audit_quotient_pointer_orbits.py);
implementation:
[`quotient_pointer_orbits.py`](../src/eye_mystery/quotient_pointer_orbits.py).
