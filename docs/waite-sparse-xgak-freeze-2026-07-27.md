# Waite East-2 sparse XGAK audit — freeze

## Question

Does the exact 81-character Waite sentence aligned to raw East-2 offsets
`37..117` remain feasible when ordinary GAK is broadened only by assigning
each literal plaintext character its own fixed output position?

## Frozen model

- one common 83-card reset deck, set to identity without loss of generality
  because every output position is unknown;
- one arbitrary fixed permutation per distinct literal character;
- one fixed output position per character;
- all 20 output positions pairwise distinct;
- update first, then emit from that character's output position;
- no context memory, token merging, postprocessor, normalization, alignment
  shift, or multiple orbit partition.

The inverse-position SMT encoding tracks only observed cards. Every satisfying
model must be completed to full 83-position permutations and replay the exact
ciphertext under the forward implementation.

## Calibration and held-out test

1. Generate an 83-card, 81-character planted XGAK instance with 20 arbitrary
   permutations and 20 distinct output positions from seed `270728`.
2. Require SAT and exact forward replay before testing the Eye candidate.
3. Test the full Waite/East-2 alignment under the unchanged model.
4. If it is SAT, refit only offsets `0..72` and test both the observed card at
   offset 73 and the frozen alternative `(observed + 1) mod 83`.

Offset 73 is fixed because it is the character that first completes the
shortest ordinary-GAK contradiction. The alternative rule is fixed before the
XGAK run.

## Interpretation

- `UNSAT`: reject the exact candidate under this transitive,
  distinct-selector XGAK model.
- `SAT` with exact replay but two feasible held-out cards: compatibility is
  non-predictive and supplies no evidence for Waite; close the XGAK crib as an
  evidential lane unless an external clue restricts its operations or output
  positions.
- `SAT` with the observed held-out card forced against the frozen alternative:
  test all other 81 alternatives before considering a prediction.
- `unknown`: record a computational boundary, not evidence.
