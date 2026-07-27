# Waite East-2 sparse ordinary-GAK audit — results

## Outcome

The exact Waite suffix is impossible under ordinary GAK, even with arbitrary
deck permutations and an arbitrary starting deck.

The sparse solver first passed the frozen positive control:

```text
deck / text / operations     83 / 81 / 20
planted control              SAT in 40.899 s
control forward replay       exact
real Waite / East-2 suffix   UNSAT in 6.327 s
```

The first 73 aligned characters have a replayable model; adding character 74,
the space at suffix offset 73 / raw East-2 offset 110, is UNSAT. More
importantly, a five-observation fixed-point certificate proves the rejection
without relying on SMT.

## Exact certificate

For ordinary GAK, each plaintext word composes fixed permutations of deck
positions. Equal ciphertext cards at the endpoints of a word mean that the
word's composite fixes the top position; different cards mean that it does
not.

The Waite alignment gives:

```text
suffix offsets   word          endpoint cards   consequence
20 -> 25         " THE "       10 -> 10          A fixes top
64 -> 68         "EST,"        25 -> 44          C does not fix top
64 -> 73         "EST, THE "   25 -> 25          C then A fixes top
```

But the permutations fixing one point form a subgroup. Since `A` fixes the
top and `C` followed by `A` fixes the top, `C` must also fix the top. The
observed `25 -> 44` says it does not. This is a contradiction.

An exhaustive word-span scan finds four certificates; the shortest uses only
ciphertext observations `10,10,25,44,25` at suffix offsets
`20,25,64,68,73`. Planted contradictory text is detected, while a valid random
ordinary-GAK fixture produces no certificate.

## Scope

Reject:

- the literal 81-character Waite sentence at raw East-2 offsets `37..117`;
- any deck size and any arbitrary starting deck;
- arbitrary fixed permutation operations;
- any context-free relabelling or merging of its characters that retains one
  fixed update and one output per aligned character.

Do not reject:

- the Waite source under XGAK, an output selector, context-dependent
  tokenization, extra memory, or a postprocessor;
- other Waite passages;
- arbitrary GAK as a general Eye architecture without this known plaintext.

The source was selected retrospectively, so passing its earlier isomorphism
checks was never positive decryption evidence. This exact rejection closes
the source-backed ordinary-GAK residual rather than advancing a plaintext.

## Reproduction

The certificate needs no optional solver:

```bash
PYTHONPATH=src python scripts/check_waite_gak_fixed_point.py
```

The calibrated SMT cross-check requires `z3-solver`:

```bash
PYTHONPATH=src python scripts/run_waite_sparse_gak.py --timeout-ms 60000
PYTHONPATH=src python -m unittest \
  tests.test_gak_fixed_point tests.test_sparse_gak_sat
```
