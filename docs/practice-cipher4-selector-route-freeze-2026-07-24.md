# Practice cipher 4: selector/route breadth freeze — 24 July 2026

**Result:** A–G are complete and negative as mechanisms. The selector
predictor is significant but is carried entirely by exact full-rank bigram
reuse; the route improvements are null-ordinary. Lane H was not opened because
no executable invariant survived. Full results are in
[`practice-cipher4-selector-route-results-2026-07-24.md`](practice-cipher4-selector-route-results-2026-07-24.md).

## Why this pass exists

The first wide codec pass found two ordered decompositions of the recovered
57-rank action band:

```text
rank = 2*q + r    q in 0..28, r in 0..1
rank = 3*q + r    q in 0..18, r in 0..2
```

The quotients have strong sequential structure. The small remainders have much
less, especially the ternary stream. Static English and Finnish readings of
the 29-state quotient fail. The next question is therefore mechanical:
whether `q` is a distance/state input and `r` is a control, or whether a small
route operation hides a static reading.

This document freezes a broad family before inspecting its best candidates.

## Independent lanes

| Lane | Model | Cheap necessity test | Promotion gate |
|---|---|---|---|
| A. Quotient walk | Accumulate `q+offset` on a plaintext ring. | Exhaust ring sizes and small offsets. | Readable output under a disclosed straightforward alphabet and recovery of a planted walk. |
| B. Signed selector | Each `r` chooses the sign of `q+offset`. | Exhaust all sign tables. | Same sign table and alphabet family work across all portions. |
| C. Selector carry | Each `r` selects a small `0/1` correction to `q`. | Exhaust all Boolean correction tables. | Stable language gain beyond the unsigned walk and planted recovery. |
| D. Direction toggle | Selected remainder values reverse a persistent traversal direction. | Exhaust nonempty toggle subsets and both initial directions. | One fixed toggle law works across portions and preserves copied action blocks up to predicted state. |
| E. Lane accumulators | Maintain one accumulator per remainder value; update and emit only the selected lane. | Exhaust widths 2 and 3, plausible rings, and small offsets. | Language and shared-block behavior both improve; no per-position choices. |
| F. Small route family | Undo odd/even, rail, rectangular, snake, and fixed-block routes on each quotient stream. | Score equality-pattern n-grams before assigning letters. | Selection-corrected structure beats matched shuffles, then an exact source-signature or calibrated substitution test. |
| G. Selector transducer | Predict `r` from current/neighboring `q`, prior `r`, transition, or short position phase. | Cross-validated conditional entropy with copied blocks deduplicated. | Held-out gain over marginal and shuffled-selector controls. |
| H. Two-cycle lift | Treat adjacent pairs as an interleaving of 29- and 28-position lanes, analogous only in shape to earlier practice cycles. | Derive an explicit reversible state law; do not infer one from the count alone. | Exact action replay and an independently predicted plaintext equality. |

## Search boundaries

- Widths 2 and 3 are both tested. The earlier ranking does not license
  committing to one.
- The standard 42-character plaintext order from sdlwdr's solved puzzles is a
  disclosed community-puzzle prior, not evidence about Noita or an automatic
  key for Cipher 4.
- Per-portion starting rotations may be reported diagnostically, but a
  promoted mechanism must explain them from reset/update state or remove them.
- Language score is never sufficient by itself. A planted positive control at
  the real lengths is required for every optimizer.
- Shared copied blocks are not independent samples. Selector-prediction nulls
  must deduplicate or preserve them.
- No arbitrary permutation table, unrestricted transposition, or unconstrained
  state machine is allowed in this pass.

## Stop rules

- Close A–E if planted quotient walks recover and all real candidates remain
  seed-free but unreadable by a large score margin.
- Close F if every fixed route has equality-pattern likelihood ordinary under
  selection-matched shuffles.
- Close G if no declared context improves held-out selector likelihood after
  family-wise selection.
- Open H only after A–G identify a concrete lane/toggle invariant. The visual
  resemblance `57 = 29 + 28` is not enough.
