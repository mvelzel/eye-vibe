# `THAT WHICH` connected-gap ordinary-GAK test — freeze

## Question

Can one ordinary one-update-per-character GAK model carry each first
`THAT WHICH` occurrence through the actual intervening ciphertext to the
second occurrence?

The three zero-based raw-trigram pairs are fixed before the real solve:

```text
East 1   40 -> 68   start gap 28   segment length 38
West 1   40 -> 70   start gap 30   segment length 40
East 2   45 -> 80   start gap 35   segment length 45
```

`THAT WHICH` occupies the first and last ten positions of every segment.
The intervening plaintext is wholly unknown.

## Frozen model

- orthodox trigram ranks are 83 ciphertext cards;
- each plaintext symbol selects one fixed permutation of deck positions;
- an update is followed by emission of the new top card;
- the three segments may begin in independent arbitrary deck states;
- position permutations are shared across all three segments;
- the seven literal symbols in `THAT WHICH`, including the space, have
  fixed shared action labels;
- every intervening position chooses any action in the tested total alphabet;
- no reset, XGAK selector, context memory, token merging, or postprocessor.

For total alphabet size `K`, test exact feasibility from `K=7` upward through
the community-scale ceiling `K=42`. Stop at the first constructive witness.
Because unused actions are allowed, a first SAT at `K` proves a minimum under
this nested family if every smaller test is UNSAT.

## Frozen controls

Before the Eye query:

1. recover and exactly replay a planted three-segment instance with the same
   lengths and phrase placements, independent starting decks, seven pinned
   phrase actions, and two additional gap actions;
2. reject an impossible repeated-action orbit whose outputs are `A B B`.

Every SAT witness must be completed to full 83-position permutations and full
decks, then reproduced with the independent forward GAK implementation.

The same-shaped symbolic planted recovery subsequently timed out before the
Eye run. It was therefore not treated as a passed control: finite-completion
timeouts below remain `unknown`, never negative evidence. A smaller
partially-known plant, the impossible orbit, exact known-key replays, and the
free-subgroup closure implementation do pass.

## Interpretation

UNSAT through 42 rejects this literal crib in the frozen ordinary-GAK family.
A low minimum would be compatibility, not plaintext evidence: arbitrary
permutations, arbitrary gap plaintext, and independent starting states have
substantial capacity. The useful output would be the exact minimum and any
forced gap schedule or operation structure. `unknown` leaves the tested bound
unresolved.
