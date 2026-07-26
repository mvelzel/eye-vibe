# Swap-or-not card-shuffle audit — results

## Outcome

The direct visible-coordinate construction fails its relaxed necessary
condition for every accepted Eye context at one, two, and three rounds. There
is no exact low-round survivor to test for pair consistency.

## Exact fits

The entries are the maximum number of distinct context mappings covered by any
round-key tuple. `full_keys` is zero in every cell.

| context | mappings | one round | two rounds | three rounds |
|---|---:|---:|---:|---:|
| `first-gap30` | 13 | 2 | 4 | 7 |
| `first-cross` | 13 | 2 | 4 | 7 |
| `first-cross-late` | 13 | 1 | 4 | 6 |
| `first-gap28` | 6 | 1 | 3 | 4 |
| `last-west4` | 25 | 2 | 6 | 10 |
| `last-east5` | 25 | 3 | 7 | 11 |
| `last-east3` | 22 | 2 | 5 | 8 |

For three rounds the eight possible paths reduce exactly to four translation
and four reflection relations:

```text
y-x in {0, k2-k1, k3-k1, k3-k2}
x+y in {k1, k2, k3, k1-k2+k3}
```

Every key triple in `Z_83^3` was exhausted.

## Matched null

Full three-round compatibility among 1,000 deranged injective controls per
context was:

| context | compatible controls |
|---|---:|
| `first-gap30` | 0/1,000 |
| `first-cross` | 0/1,000 |
| `first-cross-late` | 0/1,000 |
| `first-gap28` | 33/1,000 |
| `last-west4` | 0/1,000 |
| `last-east5` | 0/1,000 |
| `last-east3` | 0/1,000 |

Thus complete three-round fits are already rare for the longer random partial
maps. The Eye rejection is a useful exact bound, not an anomalous positive
signature.

## Interpretation

Reject the linked shuffle as a one-, two-, or three-round transform of the
accepted context maps in the ordinary trigram-rank coordinates.

Do **not** reject:

1. four or more rounds;
2. an independently motivated hidden relabeling of the 83 glyphs;
3. a stateful or tweaked construction with a supplied key schedule;
4. the paper's general many-round format-preserving cipher.

Those larger models currently make no held-out Eye prediction. Allowing an
independent pseudorandom permutation for every context explains the
isomorphisms only in the generic sense that any monoalphabetic substitution
preserves repetition. The historical lead should therefore remain archived
until an in-game or cryptographic clue selects its missing state machinery.

## Reproduction

```bash
PYTHONPATH=src python scripts/audit_swap_or_not.py \
  --rounds 3 --null-trials 1000
PYTHONPATH=src python -m unittest tests.test_swap_or_not
```
