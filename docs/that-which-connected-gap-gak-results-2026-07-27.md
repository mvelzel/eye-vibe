# `THAT WHICH` connected-gap ordinary-GAK test — results

## Outcome

The connected-gap test did not produce a key or reject the crib. Its exact
finite result is unresolved.

All seven constant fillings of the unknown gaps are UNSAT. Among 1,000 frozen
random seven-action fillings, 574 pass a new exhaustive free-group
top-stabilizer test. One retrospectively selected survivor can be folded from
98 to 34 partial states without violating any observed endpoint relation, but
neither exact solver found a full permutation completion. `unknown` is not
evidence for or against `THAT WHICH`.

## Frozen segments

```text
East 1   40 -> 68   length 38   unknown gap 18
West 1   40 -> 70   length 40   unknown gap 20
East 2   45 -> 80   length 45   unknown gap 25
```

The two ten-character ends are both fixed to `THAT WHICH`. Its literal
character alphabet, including space, has seven shared actions. The three
segments have independent starting decks but share all operations.

## Stronger exact necessary test

Every pair of output positions supplies an operation word that either fixes
top position zero or does not. Instead of checking only directly observed
factorizations, the new screen uses Stallings folding:

1. reverse each chronological fixed word to match GAK composition order;
2. generate the complete free subgroup of all fixed words;
3. reject if any observed nonfixed word belongs to that subgroup.

This is exhaustive subgroup closure, not the earlier three local factorization
rules. It rejects the planted `A B B` repeated-action orbit, accepts known
forward-encrypted GAK fixtures, and closes relations such as
`<A²,A³>` containing `A`.

For seed `27072026`, 1,000 random gap schedules give:

```text
free-subgroup compatible                    574 / 1,000
all folded-core states, min/median/max       1 / 105 / 110
compatible cores, min/median/max            98 / 105 / 110
best compatible trial                       452
best trial endpoint spans                 31 fixed, 2,442 nonfixed
```

Core size is not a deck-size lower bound: adding further unobserved stabilizer
relations can quotient it. Random congruence folding reduces trial 452 to 34
states while preserving all 2,473 observed statuses. This proves only a
partial group action.

## Candidate used for finite completion

The symbol order is:

```text
0=T  1=H  2=A  3=space  4=W  5=I  6=C
```

The selected unknown gaps are:

```text
East 1  2 5 0 4 1 0 1 1 1 1 1 2 0 2 2 3 6 0
West 1  3 0 4 0 0 5 6 3 1 1 2 5 1 6 0 3 6 4 6 2
East 2  6 4 4 0 6 6 3 4 1 4 0 1 2 6 0 6 3 3 6 5 5 1 0 4 6
```

This schedule was selected because it minimized core size in the frozen random
batch. It has no linguistic or in-game support.

## Finite completion

Three exact fixed-schedule completion runs each reached their 120-second
timeout:

```text
83 positions, quotient target 50      unknown
83 positions, quotient target 25      unknown
36 active positions, 34-state core,
then fixed-point extension to 83       unknown
```

The 36-position reduction is valid because the largest trace contains 36
distinct output cards; any recovered action would be extended by 58 untouched
positions before exact 83-card replay. No solver returned SAT or UNSAT.

Separately, 500,000 random completions of the 34-state core inside 36 active
positions produced zero exact replays. This is a heuristic null, not a
rejection.

The same-shaped symbolic planted recovery timed out before the real query, so
solver timeout was never promoted. Smaller positive and negative controls
pass, and every returned SAT model in the implementation is independently
forward-replayed.

## Interpretation and stop rule

Promote the exhaustive free-subgroup closure test as a reusable ordinary-GAK
crib screen. Do not promote the random schedule, its quotient, `THAT WHICH` as
plaintext, or finite GAK compatibility.

The connected-gap branch should reopen only with a source-selected gap
schedule, a faster finite-cover solver with a passed same-shaped plant, or a
different explicitly frozen architecture such as XGAK. More arbitrary
seven-symbol schedule sampling has no evidential value.

## Reproduction

```bash
PYTHONPATH=src python scripts/run_that_which_connected_gap_gak.py
PYTHONPATH=src python scripts/run_that_which_connected_gap_gak.py \
  --constant-screen --solve
```
