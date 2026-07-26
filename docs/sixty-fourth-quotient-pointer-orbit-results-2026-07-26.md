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

This defines a compact, parameter-free operation worth testing. It is not yet
evidence that the developers intended the quotient as a pointer, and it is not
a plaintext decoder. The operation was found retrospectively.

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

Thus the same fixed operation numerically reproduces the independently
established Eye phase split `17+3=20`. The cycle lengths form an ordered `+3`
progression.

Their pairwise intersection sizes in `E1,E3,E5` order are:

```text
E1∩E3 = 0
E1∩E5 = 1  ({40})
E3∩E5 = 2  ({45,60})
```

The nonempty-mask matches the established header-edge composability pattern
for `0->1, 2->1, 1->0`: the first two edges do not compose with each other,
while each composes with the third. The mask alone is common under the null
and is descriptive rather than positive evidence.

Across all nine orbits, 51 labels are visited and 32 are omitted:

```text
83 - |union(all nine orbits)| = 32 = E4 checksum remainder
```

E4 is independently the final loop/pivot panel. Allowing every nonzero
checksum remainder barely changes the matched-null rate, because the other
remainders are mostly outside the natural omitted-count range.

## Eye-only observations

Two relations can be stated without referring to Gate Guardian or any other
fringe theory.

First, the only tail-free walks are E2 and E3. They are also exactly the two
panels whose promoted header source digit is `2`:

```text
tail-free panels = {E2,E3} = panels with source digit 2
```

This named equality is not selective after accounting for other simple unary
header classifications: it occurs in `173,963/1,000,000` matched controls.
It is useful description, not positive evidence.

Second, summing orbit sizes by physical row gives:

```text
row 1: 2+2+9   = 13
row 2: 11+4+8  = 23
row 3: 5+17+14 = 36
13+23 = 36 = E2 header value
```

The typed relation occurs in `81/1,000,000` controls. Allowing any physical
row to equal the sum of the other two and any observed header to equal that
balanced value gives `895/1,000,000`, add-one corrected `.000895999`.
This is the best Eye-internal anomaly produced by the operation. It remains
retrospective and is derived from the same orbit sizes as the other relations.

The broad conjunction of the unary classification and row balance occurs in
`155/1,000,000`, corrected `.000155999844`. The two events are not independent
and this joint is not multiplied by any other rate.

## Separate Veska comparison and its failure

The quotient orbits partition as:

```text
closing cycles                         12
other nonclosing orbits                43
sole nonclosing orbit with no tail      9  (E2)
closing tails                           8
                                      --
                                      72
```

This numerically matches the Gate dossier's proposed Veska partition
`12 outer + 43 crack + 9 upper + 8 lower`. That comparison motivated an
audit; it does not validate the pointer operation.

The ground-up sprite audit does not reproduce the claimed partition:

- Veska objectively has 72 authored-color pixels.
- Its separated upper and lower pictograms objectively have 9 and 8 pixels.
- Simple spatial separation of the remaining pixels gives `11+44`, not
  `12+43`.
- The dossier did not publish the extra mask that moves one pixel between
  those groups.

Therefore the current Veska construction hypothesis fails its complete
reproduction requirement. The raw asset supplies a total and two counts that
can be compared with the orbit output, but no authored rule maps all 72 pixels
to the four orbit categories. The missing `12/43` split must not be treated as
a prediction whose later recovery would retrospectively validate this model:
many target-aware masks could manufacture it.

Veska remains a binary, standalone lead. It can return only if an objective
asset-derived rule independently yields a complete executable mapping and a
held-out consequence. Its partial numerical overlap contributes zero weight
to the quotient-orbit hypothesis.

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
structure also plants the source/tail-free and physical-row relations and
triggers every detector before the real-data result is asserted.

The fixed seed is `0x5645534b41`.

The typed Veska-comparison rows use the proposed semantic assignment
`cycle->outer, mixed->crack, pure-cycle->upper, tail->lower`. Because that
assignment was noticed retrospectively, the broad rows also allow the
objective `8/9` pair—or the complete four counts—to occupy any of the four
pointer categories. These rows document the explored comparison; they do not
enter the Eye-only evidence assessment.

### Eye-only audit

| Frozen event | Hits / 1,000,000 | Add-one corrected rate |
|---|---:|---:|
| all-nine orbit total `72` | 5,829 | `.005829994` |
| closing orbit total/union `20|17` | 4,022 | `.004022996` |
| ordered cycle lengths `1|4|7` | 493 | `.0004939995` |
| any ordered cycle `+3` progression | 2,548 | `.002548997` |
| header composability overlap mask | 124,479 | `.1244799` |
| omitted count equals typed E4 remainder | 34,884 | `.03488497` |
| omitted count equals any checksum remainder | 34,966 | `.03496697` |
| total `72` and omitted count `32` | 343 | `.0003439997` |
| source digit 2 exactly selects tail-free panels | 38,554 | `.038554961` |
| any simple unary header class selects tail-free panels | 173,963 | `.173963826` |
| typed physical-row balance and E2 header `36` | 81 | `.000081999918` |
| any physical-row balance and any observed header | 895 | `.000895999104` |
| typed source/tail-free plus typed row balance | 7 | `.000007999992` |
| broad unary/tail-free plus broad row balance | 155 | `.000155999844` |

### Exploratory Veska-comparison audit

| Frozen event | Hits / 1,000,000 | Add-one corrected rate |
|---|---:|---:|
| typed proposed `72|9|8` categories | 18 | `.000018999981` |
| broad-category proposed `72|9|8` | 102 | `.000102999897` |
| typed proposed `12|43|9|8` | 1 | `.000001999998` |
| any-category proposed `12|43|9|8` | 4 | `.000004999995` |
| Eye `20|17` plus typed Veska comparison | 0 | `<.000001` |
| Eye `20|17` plus broad Veska comparison | 1 | `.000001999998` |
| preceding broad comparison plus cycles `1|4|7` | 0 | `<.000001` |

These are overlapping views of one pointer structure and must not be
multiplied. They are conditional rates, not project-wide discovery
probabilities; the operation was found retrospectively after substantial
exploration. In particular, the Veska-comparison rows cannot strengthen the
Eye-only rows.

## Convention audit

The address convention is unusually rigid. Using the body-only table
`panel[1:84]` instead gives:

```text
all total 76
closing total/union 25/24
closing cycles 10,8,2
```

It satisfies none of the recorded events. Scanning every common contiguous
83-cell window start `0..16`, only start zero has the physical-row balance,
phase, cycle, or explored partition events. This favors the exceptional
header as table address zero within this hypothesis rather than treating it
as discarded framing.

## Decision and next falsifier

Retain the following as a bounded Eye-only hypothesis:

> The nine panels contain quotient-addressed `83`-state functional tables.
> Their orbit decomposition may relate the mod-101 checksum fields to the
> physical message layout.

The physical-row balance is sufficiently unusual under the matched null to
justify one prospective test. It is not sufficient to promote a construction
mechanism because the operation and the balance were both found
retrospectively and no decoded symbol, transition, or asset instruction
selects the walk.

Do not promote:

- any Veska corroboration or the dossier's unpublished `12/43` pixel mask;
- a body-wide cipher or allocation rule;
- plaintext, Finnish or otherwise;
- alternate seeds, moduli, table lengths, window offsets, or aggregate
  ledgers chosen after this result.

The quotient lane advances only by predicting an uninspected Eye
transition/value or by finding an independently authored Eye interface that
selects quotient addressing. The Veska lane advances separately only through
a complete target-blind asset rule with a held-out consequence. Success in
one lane cannot be used as partial support for the other.

## Holdout audit

No honest corpus-internal holdout remains. The first-83 tables, all nine
seeds, complete orbits, headers, and physical row assignment were inspected
before the row balance was recognized. Recasting E5's known orbit size or
E2's known header as a “prediction” would be retrospective reconstruction.
Likewise, inventing a relation to the unconsumed suffix after seeing the
orbits would introduce a new operation rather than test this one.

The lane therefore stops here. It can reopen only when an independently
authored Eye interface selects quotient addressing before exposing another
target. The `.000896` broad row-balance anomaly remains logged, but without
that selector it is not a construction claim.

Reproduction:
[`audit_quotient_pointer_orbits.py`](../scripts/audit_quotient_pointer_orbits.py);
implementation:
[`quotient_pointer_orbits.py`](../src/eye_mystery/quotient_pointer_orbits.py).
