# Thirty-third pass — residue-seven phase-ledger results

## Result

The previously unexplained row-2 circulation `7` has a concrete body
consumer. It types the transition suffix between the two promoted equality
phases:

```text
message  phase suffix  header newline preimage  sum
E4       3             4                        7
W4       4             3                        7
E5       3             4                        7
```

The generic rule recomputes row-2 circulation for every header-scalar
assignment. Among 12,096 admissible assignments, 159 satisfy the exact ledger:

```text
159 / 12096 = .013144841
```

Allowing any of the six factoradic symbols adds no assignments and no
alternative symbol: every fixed-suffix match uses the already established
newline symbol.

The rule also distinguishes the remaining full-header ambiguity. Of the two
unchanged factoradic-header survivors, only the observed scalar assignment
satisfies the phase ledger.

This promotes a typed residue-seven phase ledger as structural evidence. The
broader symbol-plus-suffix tail is `.057374339`, so the result does not by
itself prove a unique transition algorithm.

## Fields derived without fitting

The body-side values come from the synchronizing-bridge result:

```text
common equality phase     17
complete bridge lengths   20,21,20
suffix lengths             3, 4, 3
```

The header-side values come from ordinary lexicographic unranking:

```text
header ranks              27,77,33
newline preimages          4, 3, 4
```

The ledger constant is recomputed from the second marker row:

```text
76 + 63 + 34 = 173 = 7 mod83
```

No constant seven, suffix placement, or symbol identity is inserted into the
generic conditional enumeration.

## Conditional audit

The frozen broadenings give:

| Event | Count | Fraction |
|---|---:|---:|
| exact newline, exact suffixes, equals row-2 circulation | 159 | `.013144841` |
| exact ledger and final scalar sum equals circulation | 12 | `.000992063` |
| any common factoradic symbol, exact suffixes | 159 | `.013144841` |
| newline, any permutation of suffix multiset `(3,3,4)` | 273 | `.022569444` |
| any symbol and any suffix permutation | 694 | `.057374339` |
| any symbol gives one common constant, ignoring row 2 | 1,413 | `.116815476` |
| any symbol/suffix gives a common constant, ignoring row 2 | 4,803 | `.397073413` |

The exact and any-symbol assignment sets are identical. Across every exact
fixed-suffix witness, the symbol is newline.

The final scalar sum is also seven:

```text
2 + 2 + 3 = 7
```

Its 12-assignment conjunction is reported because that equality was already
in the marker ledger before this pass. It is not multiplied with the primary
count, and it is not promoted as an independent p-value.

## Observed witness inventory

Searching all six symbols and all three distinct suffix assignments, while
even ignoring row 2, finds exactly one uniform-sum witness in the observed
headers:

```text
symbol     newline (5)
suffixes   (3,4,3)
constant   7
row2       matches
```

Thus the verbal interpretation is not hiding another symbol, suffix
placement, or constant on the observed record.

## Factoradic ambiguity resolution

The unchanged full factoradic filter has two scalar survivors:

```text
001134223   observed   ledger passes
001234213   W2/W4 duplicate-edge exchange   ledger fails
```

The locale checksum already selected the first survivor. The body phase
ledger now selects it through a different consumer: newline preimages and
body suffix lengths.

These two selectors share the same header scalars and are not statistically
independent. Their agreement nevertheless strengthens the interpretation
that the precise scalar placement, not merely its graph-isomorphism class,
was authored.

## Interpretation

The result supplies a role for three previously disconnected facts:

1. the factoradic header's newline-preimage field;
2. the row-2 nonzero circulation residue;
3. the side-dependent suffix between two body equality phases.

A compact state interpretation is:

```text
row-2 circulation = phase-width budget
body suffix length = budget - header newline preimage
```

For Q-East, `7-4=3`; for Q-West, `7-3=4`.

The word “newline” should remain operational rather than textual. It is the
sixth renderer symbol in the factoradic model and may mean delimiter, reset,
or phase transition. Nothing here shows plaintext line breaks or assigns
semantic characters to body labels.

## Boundary and next prediction

Promote:

- residue seven as an executed phase-width budget;
- newline preimage as a body-schedule field;
- the observed scalar assignment as the one compatible with that schedule.

Do not promote:

- a complete finite-state transition;
- a per-label decryption;
- a Gate Type4/Type6 role table;
- multiplication of the `.0131` conditional frequency with prior dependent
  header counts.

The next useful test must use this budget rule to predict an unused exit,
suffix, or phase boundary in another header/context family. Refitting a new
constant or choosing another symbol after seeing the body is forbidden.

## Reproduction

```text
PYTHONPATH=src python3 scripts/audit_phase_ledger.py
PYTHONPATH=src python3 -m unittest tests.test_phase_ledger
```

Implementation:

- `src/eye_mystery/phase_ledger.py`
- `scripts/audit_phase_ledger.py`
- `tests/test_phase_ledger.py`

