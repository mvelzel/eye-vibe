# Thirty-first pass — Gate `+3` marker-transfer results

> **Status correction, 26 July 2026:** The marker arithmetic is retained as an
> exploratory comparison only. Gate `+3` has not been independently validated
> as an Eye instruction, so these partial transfers do not corroborate the
> Gate theory or the Eye header model.

## Result

The later Gate/WAK `+3` operator has a real but narrow execution on the
original Eye marker grid:

```text
West4  77 + 3 = 80  West1
East5  33 + 3 = 36  East2
```

These are exactly the two non-self increment fields of the established final
anchor record.  The self/total field does not land on a marker:

```text
East4  27 + 3 = 30  absent
```

Among all nonzero shifts `1..82`, `+3` is the **only** shift that completely
transfers the non-self fields of any natural marker row into another natural
row.  This is useful corroboration that the later asset restates a marker
scalar/check operation.

The stronger factoradic-machine prediction fails.  The two transfers do not
apply one common six-symbol permutation on either multiplication side.  The
Gate clue therefore does not currently explain the factoradic header
transducer or justify applying `+3` to Eye bodies.

## Typed digit action

In orthodox base five, the two transfers are:

```text
302_5 = 77  -> 310_5 = 80
113_5 = 33  -> 121_5 = 36
```

Under the established `middle -> first-1` edge reading, both operations:

1. preserve the edge target;
2. advance the edge source by one;
3. change the scalar digit by `-2 mod 5` through the ordinary base-five carry.

Thus:

```text
West4  edge 0->2 -> West1 edge 1->2
East5  edge 1->0 -> East2 edge 2->0
```

The missing self-field result would be:

```text
102_5 = 27 -> 110_5 = 30
edge 0->0       edge 1->0
```

It has the same digit action but no authored marker endpoint.  This makes the
two hits more coherent than arbitrary rank membership, while still leaving
the semantic reason for the final-to-first-row transfer unknown.

## Conditional marker null

The existing graph-conditioned universe fixes every message's first two
base-five coordinates, permutes only the observed scalar multiset
`001122334`, and retains 12,096 assignments with distinct ranks in `0..82`.

Counts are:

| Event | Count | Fraction |
|---|---:|---:|
| exact final-nonself `+3` transfer into row 1 | 372 | `.030753968` |
| same transfer and shifted self absent globally | 283 | `.023396164` |
| any ordered-row complete nonself transfer under `+3` | 492 | `.040674603` |
| any ordered-row pair with at least two `+3` hits | 954 | `.078869048` |

The exact event was inspected before freezing, so these are conditional
descriptive frequencies, not discovery p-values.  Nevertheless, `+3` was
selected outside this grid by the later Gate/WAK assets, and the observed
all-shift inventory is unusually clean:

```text
complete transfers over shifts 1..82:
  +3: final row -> first row, 2/2 non-self fields
```

No other shift and no other ordered row pair completes.

## Factoradic execution: negative

Lexicographically unranking each rank as the established six-symbol
permutation gives:

```text
77 -> 80
  left quotient   (0,2,5,1,4,3)
  right quotient  (0,1,5,4,2,3)

33 -> 36
  left quotient   (0,5,2,4,1,3)
  right quotient  (0,1,3,5,2,4)
```

All four quotients are order-four permutations with one nontrivial 4-cycle,
but the exact left quotients disagree and the exact right quotients disagree.
None is an element of the observed first-row D4 group.

The conditional result is decisive for the preregistered consequence:

```text
372 exact complete-transfer assignments
  0 with a shared left quotient
  0 with a shared right quotient

492 assignments with some broad complete transfer
  0 with a shared quotient on either side
```

The implementation recovers a synthetic two-transfer plant with a shared
quotient, so this negative is not a detector failure.

## Interpretation and stop rule

Promote only this narrow statement:

> The later `+3` clue acts coherently on the two non-self scalar/check fields
> of the original final marker record and carries them to first-row markers.

Do not promote:

- one shared factoradic instruction;
- a body-wide Caesar shift;
- a Finnish plaintext transform;
- the dossier's Type4/Type6 cache machine.

The best current model is that Veska and the later RNG salts restate a compact
marker-layer locale/scalar operation.  That is meaningful construction
vocabulary, but it remains metadata rather than an Eye-body decoder.

## Reproduction

```text
PYTHONPATH=src python3 scripts/audit_gate_plus3_transfer.py
PYTHONPATH=src python3 -m unittest tests.test_gate_plus3_transfer
```

Implementation:

- `src/eye_mystery/gate_plus3_transfer.py`
- `scripts/audit_gate_plus3_transfer.py`
- `tests/test_gate_plus3_transfer.py`
