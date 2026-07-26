# Fifty-seventh follow-up — visible-codebook rerank freeze

**Frozen:** 26 July 2026, after the omission-count result and before this
follow-up was calculated.

## Trigger and independence

Lane B's omission count missed its promotion threshold and exposed a coarse
zero-bucket degeneracy. This follow-up executes lane A from the pre-result
wide candidate table:

```text
sort the fixed visible glyph set 0..82 under the marker's five-eye order
replace each glyph by its position in that ordered 83-word codebook
```

Unlike omission count, this is a bijection on all 83 labels for every panel.
It cannot create equality merely by collapsing many values into one bucket.
It asks whether each header is a per-message collation key that transports the
seven established context maps into one canonical label space.

## Frozen model and controls

- Routes: real header or its inverse, globally.
- No complement, offset, component order, or per-panel choice.
- Training contexts: `first-gap30`, `first-cross`,
  `first-cross-late`, `first-gap28`.
- Holdout contexts: `last-west4`, `last-east5`, `last-east3`.
- Score: literal aligned equality after visible-codebook reranking.
- Selection: maximum training agreement; a tie chooses `header`.
- Controls: all 6,806 global affine permutations of `0..82`; reselect the
  route on training and score holdout once.

The control preserves all equality/isomorph structure and changes only the
absolute base-five association used by the proposed codebook order.

## Decision

Promote only below the exact `.01` heldout upper tail, with improvement in at
least two heldout contexts. One fitted partial map or a readable rendering is
insufficient. Failure closes the exact static per-message codebook transport,
not every stateful use of marker collation.
