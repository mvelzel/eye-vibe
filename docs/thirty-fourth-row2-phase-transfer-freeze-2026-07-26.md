# Thirty-fourth pass — prospective row-2 phase transfer freeze

## Question

Does the residue-seven/newline ledger predict a second body phase transition
outside the final anchor record?

The row-2 family is:

```text
W2, E3, W3
```

Its exact copied body opening has length five. Its factoradic newline
preimages are `(3,4,3)`, so the already frozen budget rule predicts:

```text
7 - (3,4,3) = (4,3,4)
```

as the three transition-suffix lengths.

## Canonical boundary rule

Start at the independently established copied-opening exit, markerless body
index 5.

From that fixed position:

1. canonicalize the remaining body of each panel by first-occurrence equality
   classes;
2. take the longest common prefix of all three signatures as the first shared
   phase;
3. add the fixed predicted suffix `(4,3,4)` panelwise;
4. treat the resulting three coordinates as the predicted next-phase starts.

The common-prefix length is recomputed by the same rule in every control. No
numeric value, phase length, or start position is inserted by hand.

## Inspected observation

The real initial common phase has length six. The rule therefore predicts:

```text
message  opening exit  common phase  suffix  next start
W2       5             6             4       15
E3       5             6             3       14
W3       5             6             4       15
```

The same-type Q-West pair W2/W3 has identical complete equality signatures
over its ten-symbol bridge `[5,15)`. Its induced partial bijection is valid
through all ten symbols; adding the pair at body index 15 produces its first
conflict at position ten.

At the three predicted starts `(15,14,15)`, all three equality signatures
share a new prefix of length seven.

These outputs were inspected before this freeze. Their matched-control counts
are conditional evidence, not prospective discovery p-values.

## Primary statistics

For the fixed newline-derived suffix vector:

1. `old_common`: length of the canonically reselected initial shared phase;
2. `typed_pair_complete`: whether W2/W3 remain a partial bijection through
   their equal-length old phase plus suffix;
3. `typed_pair_switch`: whether adding their first predicted-phase pair gives
   the first conflict;
4. `new_common`: three-way equality-signature prefix length at the predicted
   starts;
5. `joint`: typed pair complete, exact switch, and `new_common >= 7`.

The Q-West pair is primary because the factoradic header classifier
independently puts W2 and W3 in the same side class while E3 is Q-East.

## Matched controls

Generate 50,000 controls. For each row-2 panel:

- preserve its exact markerless length and complete symbol multiset;
- preserve the five-symbol copied opening literally;
- uniformly shuffle only the post-opening suffix;
- reject adjacent doubles, including the opening/suffix boundary;
- leave headers unchanged.

For each control, recompute the initial common equality phase, apply the fixed
suffix vector, and evaluate the predicted starts. Reject a control only if a
predicted start lies outside a body.

This preserves the boundary selector, body lengths/multisets, copied prefix,
no-double constraint, header classes, row-2 circulation, and newline
preimages. It breaks only the proposed phase schedule.

Report inclusive plus-one tails for `new_common`, pair completion, switch,
and their joint event. Do not multiply dependent tails.

## Broad correction

In every observation and control, rerun the complete selection process over:

- each of the six common factoradic symbols in place of newline, with suffix
  `7 - preimage(symbol)` when all three lengths are nonnegative;
- all distinct assignments of the resulting suffix multiset to the three
  panels;
- all three choices of same-length/truncated panel pair.

The opening exit, forward direction, budget seven, equality representation,
and “common phase then suffix” grammar remain fixed.

For each candidate, the initial common phase is reselected before its starts
are calculated. Score the maximum new-phase prefix and whether any candidate
has a complete pair, first-symbol switch, and prefix at least seven.

No position shifts, alternate budget, reversal, numeric-label relation, or
per-panel symbol may be admitted.

## Controls and stop rule

The implementation must:

1. derive `(4,3,4)` from the actual row-2 headers and budget rule;
2. derive starts `(15,14,15)` from the corpus;
3. recover a synthetic two-phase plant;
4. reject it when one new-phase equality is broken;
5. reproduce copied-prefix preservation and no doubles in controls.

Promote cross-row transfer only if:

- the exact joint corrected tail is below `.01`;
- the broad corrected tail is below `.01`;
- the plant passes;
- no start was selected after seeing a favorable body value.

A positive result establishes a repeated header-controlled state schedule. It
does not identify state labels, plaintext, or the update operation.

