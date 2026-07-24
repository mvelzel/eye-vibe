# Fourteenth horizon: shared linear-generator result

## Outcome

The shared linear-generator lane is exactly negative.

After deleting the known copied openings, none of eight predeclared
representations of the three P-header panels obeys one common linear recurrence
of any order from 1 through 32. At order 32 every coefficient matrix has full
column rank 32 while its augmented matrix has rank 33. Thus the training
equations themselves are inconsistent; no coefficient vector exists to test
or tune on Q.

This is a finite-field proof, not a language or Monte Carlo result.

## Frozen representations

The scan covers:

1. accepted trigram ranks directly over `F83`;
2. adjacent rank differences over `F83`;
3. the raw base-five eye stream over `F5`, serialized under all six fixed
   component orders:

```text
012  021  102  120  201  210
```

For order `k`, one coefficient vector is shared by every training panel:

```text
x[t] = c1*x[t-1] + c2*x[t-2] + ... + ck*x[t-k]  (mod p)
```

Each panel may have an independent seed/reset. The first 25 body glyphs are
removed from the P panels and the first six from Q, matching the selector
audit's protection against known copied openings.

## Positive control

Three coefficients over `F83` were planted:

```text
(c1,c2,c3) = (2,5,7)
```

Every panel received an independent three-value seed. Fitting only P recovers
the planted vector uniquely and predicts all Q equations:

```text
consistent:       yes
unique:           yes
solution:         (2,5,7)
Q matches:        462/462
```

The solver therefore distinguishes different initial states from a different
generator and enforces the intended cross-panel constraint.

## Eye result

No representation has a consistent P fit at any order through 32. The final
order gives:

| Representation | P equations at order 32 | Coefficient rank | Augmented rank |
|---|---:|---:|---:|
| `rank-f83` | 146 | 32 | 33 |
| `difference-f83` | 143 | 32 | 33 |
| `digits-012-f5` | 630 | 32 | 33 |
| `digits-021-f5` | 630 | 32 | 33 |
| `digits-102-f5` | 630 | 32 | 33 |
| `digits-120-f5` | 630 | 32 | 33 |
| `digits-201-f5` | 630 | 32 | 33 |
| `digits-210-f5` | 630 | 32 | 33 |

For every row, rank 33 of the augmented system versus coefficient rank 32
proves that some linear combination of the recurrence equations requires
`0 = nonzero` in the corresponding field.

## Interpretation

The Eye bodies are not resets of one order-at-most-32 LFSR/linear recurrence
under these natural rank, difference, or raw-component serializations.

This does not reject:

- a nonlinear generator;
- a linear generator of order above 32;
- an externally driven stream cipher in which plaintext changes the state;
- a recurrence after an unknown nonlinear relabeling;
- the body being encrypted prose rather than a generated sequence.

Increasing the order after an exact failure would eventually interpolate the
finite P data and lose predictive value. The frozen branch therefore moves
lateral to canonical dictionary automata rather than searching higher orders.

## Reproduction

```bash
PYTHONPATH=src python scripts/run_fourteenth_linear.py
PYTHONPATH=src python -m unittest tests.test_fourteenth_linear -v
```

Definitions are in
[`fourteenth_linear.py`](../src/eye_mystery/fourteenth_linear.py).
