# Waite East-2 sparse XGAK audit — results

## Outcome

The exact Waite/East-2 alignment is feasible under arbitrary-permutation XGAK
with a different fixed output position for every literal character. The fit
has no predictive value: after fitting only the first 73 characters, both the
real next card `25` and the pre-frozen wrong card `26` remain feasible.

```text
deck / text / operations       83 / 81 / 20
output positions               pairwise distinct
planted Eye-scale control      SAT in 60.857 s; exact replay
real Waite / East-2 suffix     SAT in 79.304 s; exact replay
73-character prefix + card25   SAT
73-character prefix + card26   SAT
two held-out checks total      126.198 s
```

One replayable real-fit witness assigns the 20 first-occurrence-ordered
characters `SUBLIME THAWCO,NDKG.` these output positions:

```text
32,82,64,65,31,78,40,74,22,13,39,37,21,9,0,48,28,68,80,36
```

This tuple is one solver witness, not a recovered historical key.

## Method

For each character `s`, let `q_s` be the inverse of its unknown deck
permutation and `o_s` its unknown output position. A tracked card evolves by:

```text
new_position(card) = q_s[old_position(card)]
observed card constraint: new_position(ciphertext_t) = o_s
```

Every visited fragment of each `q_s` is constrained to be a partial bijection.
Any such fragment extends to a full permutation; the solver pairs unused
inputs and outputs, inverts each completed map, and checks the complete
forward replay. Because all `o_s` are unknown, simultaneous relabelling of
deck positions makes the common reset deck identity without loss of
generality. The real test additionally requires all 20 selectors to differ.

This explains why the ordinary-GAK five-output certificate does not transfer.
Ordinary GAK asks all operation words to stabilize the same top point. XGAK
compares character-dependent points, so those stabilizer implications vanish.

## Interpretation

Reject the XGAK fit as evidence for the Waite plaintext. An arbitrary
permutation and a distinct selector per character can fit the complete
candidate while also fitting a frozen incorrect continuation. SAT establishes
only model capacity; it neither prefers Waite nor identifies a key.

This does not reject XGAK as the Eye architecture. It closes this exact
known-plaintext lane unless an independent clue fixes or sharply restricts
the operations, output positions, plaintext-operation quotient, or orbit
partition.

## Reproduction

With `z3-solver` installed:

```bash
PYTHONPATH=src python scripts/run_waite_sparse_xgak.py --timeout-ms 120000
PYTHONPATH=src python -m unittest tests.test_sparse_xgak_sat
```
