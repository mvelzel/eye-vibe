# Thirty-eighth pass — terminal source-state return freeze

## Question

Does the row-2 terminal pointer close the header/phase machine by returning a
body state to the E4 loop header?

The previous pass selects late class 15 at positions 16 and 29. The established
post-switch scope is the common-source pair:

```text
E4 loop        0->0
W4 source mate 0->2
```

The source-pair direction is already fixed as loop to mate; the same directed
header delta was `W4-E4=50`.

At the selected terminal class, the inspected visible labels are:

```text
E4 40
W4 67
E5 21
```

The candidate return is:

```text
W4-E4 = 67-40 = 27 mod83 = E4 loop header
```

This observation was made before freezing. Report conditional specificity,
not a prospective discovery p-value.

## Fixed inputs

Freeze:

- the late common 30-symbol equality signature;
- the terminal repeat event selected by row 2;
- class 15, without moving to another class or occurrence;
- E4/W4 as the common-source scope;
- directed mate-minus-loop subtraction modulo 83;
- the E4 loop marker as the return target;
- orthodox numeric labels only after all structural selections above.

Do not try sums, products, XOR, affine maps, reversed subtraction, another
panel pair, or another marker in the primary statistic.

## Matched relabeling null

For each panel, preserve exactly:

- the complete late equality signature;
- every class multiplicity;
- the late visible-label multiset;
- whether a new class reuses a visible label from the old phase.

Class 15 is a multiplicity-two class whose value is fresh relative to the old
phase in both E4 and W4. Its compatible reassignment pools are therefore all
fresh multiplicity-two late classes in the corresponding panel.

Enumerate every E4/W4 compatible class pair and count:

```text
W4_label - E4_label = E4_header mod83
```

This finite count is the exact primary relabeling probability.

## Broad controls

Report increasingly broad observed inventories:

1. fixed E4/W4 direction and target 27, every repeated late class;
2. fixed source pair, either direction, any marker target;
3. every panel pair, either direction, every repeat class, any marker target;
4. every late class of the same multiplicity/reuse type, not only repeat
   events selected by their occurrence.

Record every hit with class, pair, direction, difference, and matching marker.
The primary terminal hit must be identified explicitly among them.

Also count conditional scalar assignments in which the fixed returned value
27 equals the E4 marker, and cross it with the previously promoted full
topology. These are nested descriptions and are not multiplied.

## Calibration and promotion gate

Tests must recover:

- terminal labels `(40,67,21)`;
- compatible E4 and W4 class pools;
- the exact difference `27`;
- a synthetic planted directed return;
- failure after reversing or perturbing the mate value;
- complete broad-hit inventories.

Promote a cyclic source-state return only if:

- the fixed hit is unique across repeated classes in its source scope;
- the exact matched probability is below `.1`;
- broad searches do not make the selected return vacuous;
- the returned `27` connects directly to an already promoted next operation.

A positive result closes a control cycle. It still does not assign plaintext
meaning to arbitrary visible labels.
