# Thirty-fifth pass — phase-overlap update freeze

## Question

Does the promoted final-row phase switch preserve one ledger-selected state
correspondence across the reset?

This test operates only on equality classes and cross-phase label reuse. It
does not interpret the numeric label values.

## Fixed phases and class coordinates

Use the final bridge and late 30-symbol phase exactly as promoted in the
thirty-second pass. Canonicalize each phase independently by first occurrence.

Old-phase class counts:

```text
E4  16 classes over 20 positions
W4  17 classes over 21 positions
E5  16 classes over 20 positions
```

The new phase has the same 25-class equality signature in all three panels.

Three independently promoted fields select one class transition:

```text
row-2 phase budget          7
shared old phase length    17
East newline preimage       4
```

Therefore:

```text
old class                  7
new class                  7+17 = 24
new first-occurrence index 24+4 = 28
```

The new signature indeed introduces class 24 at position 28, its last new
class.

## Inspected observation

List an edge `old_class -> new_class` when the same actual visible label
occurs in both phases of one panel.

Observed edges:

```text
E4: 0->7, 7->24, 8->0, 14->23, 15->20
W4: 1->9, 10->12, 12->10, 14->20
E5: 7->24, 10->21
```

The exact edge `7->24` occurs in both East panels, using different actual
labels:

```text
E4 label 69
E5 label 31
```

It is absent from W4. It is also the only equality-class edge shared by any
two panels.

Equivalently, this edge is the sole E4/E5 cross-panel mapping preserved from
the old partial bijection into the new one. That equivalence is a restatement
of the same event, not independent evidence.

The observation was inspected before this freeze. Counts are conditional
specificity measures, not prospective discovery p-values.

## Matched overlap null

For each panel, preserve exactly:

- the complete old and new equality signatures;
- every old/new class multiplicity;
- the number of visible labels reused across phases;
- the complete multiset of reuse types
  `(old multiplicity, new multiplicity)`.

Observed reuse-type profiles are:

```text
E4  3×(1,1), 2×(1,2)
W4  3×(1,1), 1×(1,2)
E5  2×(1,1)
```

Generate 50,000 controls independently per panel:

1. for every reuse token, choose a distinct old class with the required old
   multiplicity;
2. choose a distinct new class with the required new multiplicity;
3. pair the chosen endpoints through the fixed type tokens.

This randomizes only which multiplicity-compatible classes are connected.
It preserves all overlap opportunities, counts, and equality structures.

## Primary statistics

Report:

1. `east_target`: both E4 and E5 contain exact edge `7->24`;
2. `east_only`: `east_target` and W4 does not contain it;
3. `shared_offset17`: any panel pair shares an edge `c->c+17`;
4. `any_shared_edge`: any panel pair shares any exact class edge.

Use inclusive plus-one tails. These events are nested and their tails are not
multiplied.

## Broad controls

The broadest event allows:

- any old class;
- any positive or negative class offset;
- any of the three panel pairs.

That is exactly `any_shared_edge`.

Also inventory all offsets of shared observed edges and all candidate
`c->c+17` edges. No modulus, reversed edge, class permutation, phase shift,
or numeric-label transform is allowed.

The primary target remains justified by the already fixed budget, common
phase length, and East newline field. The broad event discloses how easy it
would have been to notice some shared edge after inspection.

## Controls and promotion gate

Tests must:

- derive the old/new segments and class IDs from the canonical corpus;
- recover observed edge sets and target `7->24`;
- verify first occurrence of new class 24 at position 28;
- recover a synthetic overlap plant;
- preserve every multiplicity-type profile in randomized controls.

Promote a constrained phase-update cache only if:

- `east_target` corrected tail is below `.01`;
- `shared_offset17` remains below `.01`;
- the broad `any_shared_edge` result is reported and does not make the exact
  target interpretation vacuous.

A positive result would identify one preserved state correspondence across
the reset. It would not supply the other new mappings, plaintext, or the
Gate dossier's eight-entry cache allocator.

