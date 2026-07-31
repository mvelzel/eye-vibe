# Hail Mary 01: connected-gap ordinary GAK — results

## Outcome

The previously unresolved exact finite-completion question is now SAT.

One seven-action, 83-position ordinary GAK key exactly carries all three
frozen `THAT WHICH` occurrences through their complete intervening segments.
The three traces use independent start decks and one shared operation per
literal phrase character. All 123 emitted trigrams replay exactly.

This is a constructive compatibility result, not plaintext evidence. The
intervening action strings were selected retrospectively from random trial
452 and read as gibberish under the phrase alphabet. No source, in-game clue,
or language model selects them.

## Frozen instance

Action labels are:

```text
0=T  1=H  2=A  3=space  4=W  5=I  6=C
```

The complete action strings are:

```text
East 1  THAT WHICHAITWHTHHHHHATAA CTTHAT WHICH
West 1  THAT WHICH TWTTIC HHAIHCT CWCATHAT WHICH
East 2  THAT WHICHCWWTCC WHWTHACTC  CIIHTWCTHAT WHICH
```

Because the pinned phrase itself uses seven distinct actions, `K=7` is the
minimum possible alphabet size in the frozen nested family. The exact witness
therefore resolves the requested `K=7..42` ladder at its first bound.

## Construction

Trial 452 had:

```text
31 same-card interval words
2,442 different-card interval words
98-state Stallings core
0 forced nonmember contradictions
```

The previously frozen congruence search quotiented that core to 34 states and
172 signed transition records while preserving every observed endpoint
status. Earlier random completion tried 500,000 fills and found none.

The new completion model:

1. builds one shared prefix trie of every reversed interval word;
2. represents each of seven actions as a complete permutation of 83 states;
3. pins the 34-state quotient's positive transitions;
4. constrains every same-card endpoint to state zero and every different-card
   endpoint away from zero;
5. uses CP-SAT to complete the remaining permutation entries;
6. reconstructs each independent start deck from the solved origin states;
7. replays the result with the separate forward GAK implementation.

The successful completion took 23.5 seconds in the recorded run.

## Controls and verification

- The impossible one-action output orbit `A B B` is UNSAT.
- Small symbolic plants are recovered by the Z3 and CP-SAT formulations.
- Same-length fixed-schedule plants at 10 and 83 positions replay exactly
  when their hidden operations are supplied as nonbinding solver hints.
- Unguided same-shaped symbolic recovery still times out; no timeout is
  interpreted as evidence.
- The frozen witness is independently replayed without Z3 or OR-Tools.

The full key, all three decks, and action strings are in
[`../artifacts/that-which-connected-gap-gak-witness-2026-07-31.json`](../artifacts/that-which-connected-gap-gak-witness-2026-07-31.json).
Its tuple digest is:

```text
943ff9645d8bca04b6ce33fd7de84d1a1b032a0e1eb34b258eeccb6e442fc89b
```

Reproduce the independent check with:

```bash
PYTHONPATH=src python scripts/verify_that_which_candidate452_witness.py
```

## Interpretation

Promote only this boundary:

> The three connected `THAT WHICH` windows are exactly compatible with an
> ordinary seven-action GAK on 83 cards.

This removes finite feasibility as an objection to that crib. It does not
increase the crib's probability: arbitrary gap actions and independent decks
give the model enough freedom to realize a retrospectively chosen random
schedule. The completed permutations are one solver-chosen realization and
their cycle structure has no evidential status.

Further work on this lane must add information the compatibility witness does
not use: a source-selected gap continuation, a shared/reset-state constraint,
an independently authored operation family, or a held-out prediction.
