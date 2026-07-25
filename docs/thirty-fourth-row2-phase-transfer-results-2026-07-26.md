# Thirty-fourth pass — row-2 phase transfer results

## Result

The residue-seven phase-budget rule makes an exact-looking row-2 prediction,
but it fails the registered matched-control gate.

The deterministic construction gives:

```text
copied-opening exit                 body index 5
reselected common equality phase   length 6
predicted suffixes                  (4,3,4)
predicted next starts               (15,14,15)
new common equality phase           length 7
```

The Q-West pair W2/W3 is a valid partial bijection through its complete
ten-symbol bridge and first conflicts on the next pair, exactly at its
predicted phase start.

Nevertheless, 50,000 controls show that this architecture is not unusual
enough:

```text
exact joint corrected tail   .021459571
broad joint corrected tail   .400012000
```

Per the preregistered `.01` gate, the row-2 transfer is closed and is not
promoted as a second execution of the final phase ledger.

## Exact observed trace

The row-2 body opening shared by W2, E3, and W3 is:

```text
66,5,49,75,54
```

Starting immediately after it, all three equality signatures agree for six
positions. The header ledger predicts:

```text
row-2 circulation          7
newline preimages          (3,4,3)
suffixes = 7-preimage      (4,3,4)
```

Therefore:

```text
W2  5 + 6 + 4 = 15
E3  5 + 6 + 3 = 14
W3  5 + 6 + 4 = 15
```

At those starts the three canonical equality signatures agree for seven
positions.

For the independently typed Q-West pair:

```text
W2 bridge [5,15)   10 distinct equality classes
W3 bridge [5,15)   10 distinct equality classes
partial map         valid through all 10 positions
first next pair     conflict at position 10
```

This is a genuine deterministic replication of the final record's grammar:
shared phase, typed suffix, map switch, new shared phase.

## Why it does not promote

The matched null preserves:

- exact message lengths and symbol multisets;
- the five-symbol copied opening;
- the no-adjacent-double rule;
- all headers, factoradic classes, circulation seven, and predicted suffixes.

It shuffles only each post-opening body. The common first phase is reselected
from scratch inside every control before suffixes and new starts are applied.

Measured counts:

| Statistic | Exceedances | Corrected tail |
|---|---:|---:|
| new common phase at least 7 | `28545/50000` | `.570908582` |
| typed W2/W3 pair complete | `9262/50000` | `.185256295` |
| first conflict at predicted boundary | `1944/50000` | `.038899222` |
| exact joint event | `1072/50000` | `.021459571` |
| broad maximum phase at least observed 9 | `37638/50000` | `.752764945` |
| broad joint event | `20000/50000` | `.400012000` |

The broad family reruns the complete selector over all six factoradic symbols,
all 22 distinct admissible suffix vectors, and all three pair choices.

The result is understandable under the null. With 83 visible labels, short
segments are commonly all-new. Two all-new segments always admit a temporary
partial bijection; the first repeat can then create a conflict at an
apparently sharp boundary. A seven-symbol common equality prefix is itself
ordinary in these multiset-preserving controls.

## Calibration

The detector:

- derives suffixes `(4,3,4)` from the real headers;
- derives starts `(15,14,15)` from the copied-opening exit and reselected
  common phase;
- recovers a planted two-phase trace and exact boundary switch;
- rejects the plant after one held-out new-phase equality is changed;
- preserves prefix, multiset, length, and no-double nuisances in controls.

The negative is therefore evidentiary rather than an implementation failure.

## Consequence

Retain:

- the exact row-2 descriptive trace;
- the final-row synchronizing bridge and its matched-control promotion;
- the final residue-seven ledger as a local typed consumer.

Reject:

- universal transfer of that ledger to the row-2 copied-opening exit;
- the row-2 `(15,14,15)` starts as designed phase boundaries;
- using this apparent replication to fit a common body decoder.

The next state-machine work should explain or predict the already promoted
final trace itself, or locate another boundary with independent evidence
stronger than a short all-new equality run.

## Reproduction

```text
PYTHONPATH=src python3 scripts/audit_row2_phase_transfer.py --controls 50000
PYTHONPATH=src python3 -m unittest tests.test_row2_phase_transfer
```

Implementation:

- `src/eye_mystery/row2_phase_transfer.py`
- `scripts/audit_row2_phase_transfer.py`
- `tests/test_row2_phase_transfer.py`

