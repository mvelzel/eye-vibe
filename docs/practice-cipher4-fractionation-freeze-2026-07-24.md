# Practice cipher 4: fractionation breadth freeze

## Trigger and prior boundary

After the standard `C83` outer layer, every action lies in a 57-position band.
The exact factorization

```text
rank = 3*q + r,  q in 0..18, r in 0..2
```

separates a structured 19-state quotient from a nearly memoryless ternary
remainder. Earlier work treated `r` as a sign, carry, toggle, accumulator-lane
selector, or prediction target. It also applied fixed positional routes to
`q`. It did **not** ask whether `r` labels several interleaved payload streams
or whether the typed `q/r` coordinates were reassociated before output.

Any fixed permutation of the 57 symbol labels is already subsumed by the
negative arbitrary static-substitution tests. Only operations that change
positional association or stream order are new here.

## Wide portfolio before depth

| Lane | Hypothesis | Bounded first test | Stop / promotion rule |
|---|---|---|---|
| **A. Exact source homophones** | The 200-symbol common block is a static homophonic rendering of a public source. | Use the action equality fingerprint against available English/Finnish corpora with no cap on homophones. | This was executed while inventorying the gap, before the present freeze; report it as exploratory, not preregistered. |
| **B. Selector demultiplexing** | `r` is a lane tag and each subsequence of `q` selected by one `r` is a payload stream. | Score the lanes separately and under all global lane orders/reversals for widths 2 and 3. Shuffle selectors within each portion, reselect the full family on portions 1–2, and test portion 3. | Promote only if the selected model has corrected held-out tail below `.01` and a planted interleaving is recovered. |
| **C. Typed coordinate reassociation** | Within short blocks, quotient and selector coordinates were paired at different offsets. | For periods 2–32, re-pair `q[i]` with a cyclically shifted or reversed `r` from the same block and score the reconstructed 57 ranks label-invariantly. | Reselect period/direction/offset inside every selector-shuffle control; a raw best route does not count. |
| **D. Run-controlled packets** | Selector changes mark packet boundaries; payload order is local to runs rather than fixed blocks. | Test stable run concatenation, within-run reversal, and run-length ordering without assigning letters. | Must predict a held-out portion and beat run-length-matched controls. |
| **E. Typed `3×19` fractionation** | A deck operation transposes coordinate rows while preserving their unequal domains. | Enumerate only type-preserving row/column deals; reject any construction that puts a 0–18 quotient into a ternary slot. | Exact replay and a disclosed deck operation are required; ordinary Bifid mixing is invalid on unequal domains. |
| **F. Quotient digraph packing** | Two or more base-19 payload digits form one larger symbol while `r` gives framing. | Test fixed 2/3-digit packets at every phase for printable-byte or source-signature structure. | Correct for phase and packet-width selection; no arbitrary codebook fitting. |
| **G. Selector as boundary alphabet** | One remainder value marks spaces, punctuation, or case changes while `q` carries a reduced alphabet. | Exhaust three boundary choices and before/after timing with a fixed 19-class reduction. | A planted control must recover, and exact shared blocks must preserve reconstructed boundaries. |
| **H. Edited common template** | The three portions are edits of several lane texts rather than one prose stream. | Align demultiplexed equality signatures and require a lane permutation selected on two portions to predict the third. | A joint alignment without held-out attribution is insufficient. |

## First frozen experiment: lane B

Use the English equality-pattern model already used for the fixed-route audit;
it assigns no letters to quotient values. For each width:

1. split every `(q,r)` stream into stable `q` subsequences by `r`;
2. score either the lanes separately or concatenate them under every global
   lane permutation and every per-lane reversal;
3. select one convention on portions 1 and 2;
4. apply that exact convention to portion 3;
5. in 2,000 controls, shuffle only the selectors within each portion,
   preserving every quotient, selector count, length, and quotient language
   nuisance, then repeat the full train selection and held-out test.

The primary statistic is held-out improvement over the untouched quotient
stream after train-side selection. The plus-one upper tail must be below
`.01`. A width-2 planted control interleaves two independently substituted
English streams using explicit lane tags; the method must select
demultiplexing and improve the held-out score.

If B fails, proceed laterally to C rather than inventing selector-dependent
substitution tables.

## Lane-C metric calibration

The order-8 equality-pattern model used for B failed to recover an exact
planted period-7 selector reassociation, so its first real C score is
inadmissible. Pattern orders `8,10,12,14,16,20` were compared **only on the
planted fixture**. Order 14 is the smallest that selects the planted width-3,
period-7, shift-left inverse exactly and gives positive train and held-out
improvements. Freeze order 14 for lane C before scoring the real stream. The
candidate family is three natural typed routes—one-place shift left,
one-place shift right, and reversal—for every period 2–32 and both widths,
186 candidates total.
