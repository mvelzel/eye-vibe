# Forty-sixth pass — axis-typed branch-machine results

## Outcome

Promote a new **label-invariant branch record**, but reject its direct transfer
to visible-label arithmetic.

The final header row types a two-branch conformance program:

```text
headers                 E4 102₅   W4 302₅   E5 113₅
header scalar               2         2         3
scope                    loop    source mate target mate

third-axis role          common  source      target      absent
class/direction               1       2           3           4

closed loop/target checks             +3, +2
                                      target, source
```

This is the first exact consumer found for the final row's scalar digits:
source-pair scalar `2` selects third-axis class 2, target scalar `3` selects
class 3, and the two closed divergence records return those scalars in
reciprocal order.

It does not identify the visible labels or plaintext.

## A — third-axis branch roles: positive

Second occurrences across the already frozen scopes classify classes `1..4`
without consulting numeric labels:

```text
class1  repeats in all panels at position27       common
class2  repeats in E4/W4 at position30            source pair
class3  repeats in E5 at position31               target mate
class4  never repeats                             absent
```

The role order is exactly:

```text
1,2,3,4 = up,right,down,left
```

That is one clockwise physical direction cycle from up. It complements the
already established middle-axis counterclockwise cycle
`1,4,3,2`.

The positive digit set in the three final headers is exactly `{1,2,3}`;
direction 4 is absent from both the header row and the third-axis repeat
program.

## B/C — paired checks and carry rewrite: positive

The header-selected loop E4 and target mate E5 have exactly two closed
disagreement windows in the late phase:

```text
positions  source/loop word    target word       loop-target sum
30..32     2,25,20             25,3,16                 +3
34..35     10,12               13,7                     +2
```

Thus:

```text
observed checks  = (3,2)
header scalars   = (source2,target3)
predicted order  = (target3,source2)
```

The first record has an exact base-five rewrite:

```text
002 + 100 + 040
100 + 003 + 031
```

Cancel the common `100`:

```text
source residual  002 + 040 = 22
target residual  003 + 031 = 19
coordinate delta             (0,+1,-2)
weighted base-five delta     5 - 2 = +3
```

The repair class `3` is simultaneously:

- the target branch's third-axis direction;
- the target header scalar;
- the first checksum deficit;
- the later Gate/Veska `+3` operation.

A deliberately broad four-term baseline over distinct classes `0..24` has
`7,568/303,600 = .024927536` assignments with difference `+3`.
Only `1,092/303,600 = .003596838` both have difference `+3` and contain a
term 3. These are post-inspection conditional frequencies, not p-values.

## D — strict stack/queue/deque: closed

The five first-to-second occurrence intervals in the common 30-event phase
have:

```text
repeat order  5,0,20,1,15
first order   0,1,5,15,20
```

- Intervals cross, so they are not a laminar call stack.
- Repeat order is not FIFO.
- Class 5 is the first repeat but is neither endpoint of the first-order list,
  so even a one-shot deque fails at the first operation.

This closes strict access discipline. It does not reopen the already negative
adaptive-cache family.

## E — systematic `5×5` code: closed

For each of the nine base-five output digits in the three class-to-label
tables, every affine map

```text
output = a*middle + b*third + c mod5
```

was trained on 23 classes with classes 10 and 24 held out.

The best columns fit only `9..11/23`. No co-best model predicts both
holdouts. Among all pair projections involving an output column, the maximum
coverage is `19/25`; no output pair is an orthogonal `25/25` coordinate.

The planted affine control recovers `23/23` and both holdouts exactly.

## F — transition cover: descriptive only

The common trace has:

```text
30 events
25 classes
29 directed transitions
29 distinct directed transitions
```

It is an edge-simple trail, but that is not independently surprising enough
at this length. The typed branch record, not edge uniqueness, is the promoted
conformance evidence.

## Prospective visible-label holdout: negative

Before reading class-2 and class-3 labels, two transfers were frozen from the
known middle-axis operations.

### Direction inheritance

```text
class2 W4->E4 predicted77, actual50
class3 E4->E5 predicted27, actual32
score 0/2
```

### Scope inheritance

```text
class2 W4->E4 predicted77, actual50
class3 E5->E4 predicted36, actual51
score 0/2
```

The complete held-out label inventory is:

```text
class2  E4=4   W4=37  E5=60
class3  E4=56  W4=19  E5=5
```

Broadening after the failure finds three marker differences, all at class 2:

```text
E4->W4  +33  E5 marker
W4->E4  +50  E1 marker
E5->E4  +27  E4 marker
```

Class 3 has none. These broad hits were not predicted and do not rescue either
model.

## Interpretation boundary

Promoted:

- final header scalar digits type source and target branch classes;
- third-axis direction roles form a clockwise scope cycle;
- two closed branch windows carry reciprocal `(target,source)` checks;
- the first check is an exact base-five `+3` carry rewrite, echoed by Gate.

Rejected:

- direct copying of middle-axis visible-label subtraction to the third axis;
- strict stack, queue, or deque execution;
- affine/orthogonal static `5×5` allocation.

The result advances the control-plane reconstruction but leaves the
approximately 154-bit fresh-label carrier unresolved. The next admissible
consumer must use the header-typed branch record to predict another equality
boundary or record outside these two windows; fitting visible labels remains
closed.

## Reproduction

```bash
PYTHONPATH=src python scripts/audit_novel_branch_machine.py
PYTHONPATH=src python -m unittest tests.test_novel_branch_machine
```

Implementation:

- `src/eye_mystery/novel_branch_machine.py`
- `tests/test_novel_branch_machine.py`
- freeze:
  `docs/forty-sixth-wide-novel-machine-horizon-2026-07-26.md`
- prospective label freeze:
  `docs/forty-sixth-axis-branch-marker-freeze-2026-07-26.md`
