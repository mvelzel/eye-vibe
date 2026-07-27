# Practice cipher 3 — six-stream route results

**Date:** 27 July 2026  
**Outcome:** calibrated negative; no plaintext recovered

## Tested family

The six streams in each author-labelled group were treated as rows of one
continuous path. The frozen catalog contained:

```text
5,760  row concatenations
11,520 ragged column/snake routes
17,280 total
```

Two A-only selectors were calibrated:

- a label-invariant score minimizing distinct directed edges and estimating
  the effective number of uniform outgoing choices;
- an additive score minimizing the support of
  `(next-current) mod 83`.

Exact coordinate-order reversals were retained as one A equivalence class.
B alone filtered that class at the necessary 42-action bound. C could be
inspected only for B survivors.

## Positive controls

Controls preserved the real A/B/C row lengths and no-adjacent-double property,
while hiding one route and a weighted stream of 42 fixed nonzero modular
actions.

The row plant was not identifiable: it ranked 177th under the broad selector
and 18th under the additive selector. That subfamily was discarded before the
real pass.

Both column selectors recovered the planted A coordinate order up to reversal.
The A class contained two routes. The broad B gate retained both, so it was
only a set-valued diagnostic. The additive B gate retained only the globally
correct route, whose untouched B/C supports were:

```text
B 27
C 29
```

Thus only the 11,520-member column catalog and staged additive test were
operational.

## Real corpus

The real column catalog was opened once. The initial command stopped after
printing the broad A winner because the reporting function lacked its length
argument. The argument was supplied and the identical frozen command rerun;
no route, score, threshold, or tie-break changed.

```text
selector   selected A route                         A score
broad      trim1, order520314, snake, right/R       K=20.602936
additive   trim1, order214503, snake, right/L       support=78
```

Each selected A coordinate class contained two reversal-equivalent routes.
Their B results were:

```text
selector   column direction   B effective K   B step support
broad      L                    114.298419          83
broad      R                     91.610723          83
additive   L                     76.332129          83
additive   R                     68.551556          83
```

No member passed its B `<=42` gate. Under the frozen protocol there was
therefore no C prediction, and C was not scored for these candidates.

## Decision

Close this literal six-stream row/column route family. A detector that
recovers the planted ragged-snake route and its hidden 42-step action set finds
no transferable route in the real corpus. In particular:

- row concatenation order is not identifiable at these lengths;
- the best real column route already needs 78 visible modular steps on A and
  all 83 on B;
- the apparent low broad A choice count does not transfer to B.

This does not exclude a transposition with a hidden or larger state, nonlinear
actions, variable routes between groups, or a layout outside the declared
row/column catalog. It supplies no solution text.
