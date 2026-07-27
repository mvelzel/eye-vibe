# Practice cipher 3 — six-stream route freeze

**Date:** 27 July 2026
**Status:** controls complete; real-route scoring still unopened

## Question

Each author-labelled group contains six streams. This pass asks whether those
streams are rows or ragged fragments of one continuous state path, presented
under a shared route. It does not assume plaintext or fit a substitution.

## Frozen route catalog

Every route uses one global row order from `S6` and either retains or removes
the first value of every stream.

### Row concatenations

Concatenate rows under four direction schedules:

```text
all forward
all reverse
alternating, first forward
alternating, first reverse
```

Catalog size:

```text
2 trims * 6! orders * 4 schedules = 5,760
```

### Ragged column routes

Place the six rows left- or right-aligned. Read columns left-to-right or
right-to-left, and read rows within each column either in one fixed order or
as a snake alternating that order. Opposite vertical direction is already
represented by reversing the `S6` order.

Catalog size:

```text
2 trims * 6! orders * 2 alignments * 2 column directions * 2 vertical modes
= 11,520
```

The complete declared catalog therefore contains 17,280 routes. Reversal or
ragged-layout symmetries are reported as equivalence classes rather than
claimed as independently identified routes.

## Two frozen selectors

### Broad, label-invariant selector

For the routed path, count distinct directed edges and audit its effective
uniform outgoing-choice count. More edge reuse is expected if one of at most
42 plaintext actions selects the next visible state.

Select on A by:

```text
minimum distinct directed edges
then minimum effective uniform choices
then a fixed lexical route order
```

This tests a predecessor-visible-state action path without using the numeric
labels.

### Narrow, visible-C83 selector

Count the support of:

```text
(next-current) mod 83
```

Select the smallest A support, then the broad score and fixed route order.
This adds a visible cyclic-translation assumption. It is a separate,
narrower result and cannot validate the broad model.

Both A-selected routes are applied unchanged to B and C. A route/action model
passes the necessary heldout gate only if both groups remain within 42
effective choices or 42 modular steps, respectively.

Control calibration exposed a ragged-snake parity ambiguity: two parameter
routes can produce exactly reversed coordinate orders on A yet cease to be
reversals when the maximum row length changes. The frozen staged treatment is:

1. select one route on A by the declared score;
2. retain the complete catalog class whose A coordinate order is exactly that
   path or its reversal;
3. use B only to filter class members by the 42-action gate;
4. make no choice inside the surviving class from C; report every C result.

This is a set-valued prediction, not permission to rescan arbitrary routes on
B. Class and survivor counts must be disclosed.

## Positive controls

Plant one row route and one ragged-column snake route at the real A/B/C row
lengths. Generate each routed path from 42 fixed nonzero modular steps with a
strongly nonuniform action schedule. When scattering paths back into supplied
rows, reject choices that would create adjacent doubles, preserving the
corpus's no-double fact.

Search the complete 17,280-route catalog without disclosing the planted
route. A selector is operational only if:

1. the true route lies in the A-selected exact coordinate-equivalence class;
2. B retains a true/global-equivalent member at the 42-action gate;
3. every claimed C prediction comes from the frozen B survivor set;
4. the supplied rows contain no adjacent doubles.

If the row control is not identifiable because permutations alter only five
joins, preserve that as a capacity result and do not interpret real row-route
winners. Column routes may proceed only if their own control passes.

## Frozen control outcome

The complete-catalog controls were run once with the declared seed.

- The planted row route ranked 177th under the broad selector and 18th under
  the additive selector. Neither A-selected class contained it. Row routes are
  non-identifiable here and are removed from the real pass.
- Both column selectors selected the planted A coordinate order up to global
  reversal. That A class contained two parameter routes.
- The broad B gate retained both routes and both passed C. It is only a
  two-member set-valued capacity diagnostic.
- The additive B gate retained one route: the globally correct planted route.
  Its B/C step supports were `27/29`, both within 42. The column/additive
  selector is operational.

The real pass is therefore frozen to the 11,520 column routes. It will report
the broad survivor set but interpret only the calibrated staged additive
test. No route, tie-break, threshold, or field will be changed after opening
the real scores.

## Promotion and stop gates

Promote a real route only if its unchanged B and C scores both cross the
corresponding 42-action gate and it exposes a new transition prediction or
replayable action stream.

If a planted selector passes but the real heldout groups return toward the
full 82/83-choice support, close only that selector's route/action family.
Failure of the visible-C83 selector does not reject arbitrary permutation
actions, and failure of the broad occupancy selector does not reject a route
whose state is hidden or larger than the preceding visible value.
