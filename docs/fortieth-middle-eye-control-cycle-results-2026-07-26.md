# Fortieth pass — middle-eye control-cycle results

## Outcome

Promote a four-direction control wheel in the late equality states.

The positive middle-eye-only class IDs are:

```text
class  base5    direction
 5     010      up
10     020      right
15     030      down
20     040      left
```

All four repeat by the E4/W4 source boundary. Their chronological repeat order
is:

```text
up -> left -> down -> right
 1      4       3       2
```

This is exactly one counterclockwise circuit starting from up.

## Repeat records

Derived from the E4 late equality signature through position 34:

```text
direction  class  first  repeat  distance
up           5      5       9       4
right       10     11      34      23
down        15     16      29      13
left        20     22      26       4
```

Sorted by repeat position:

```text
class 5,20,15,10
positions 9,26,29,34
directions 1,4,3,2
```

The first three events are inside the shared 30-symbol phase. The fourth
completes the missing physical direction at the exact E4/W4 conflict boundary.

## Axis controls

The corresponding single-coordinate inventories are:

```text
axis    class IDs       present by34   repeated by34
first   25,50,75,100          1              0
middle   5,10,15,20           4              4
third    1,2,3,4              4              2
```

Only the middle axis supplies a complete four-direction repeat cycle. This
rejects the simple objection that any single-coordinate base-five axis would
look similar.

## Direction-order specificity

Among all 24 permutations of four directions:

```text
exact counterclockwise from up        1/24
clockwise or counterclockwise from up 2/24
any rotation of either physical cycle 8/24
```

The renderer fixes the physical meanings of `1,2,3,4`. These counts are
descriptive after inspection and are not multiplied with the axis result.

## Boundary completion

Class 10 first occurs at position 11 in the common phase. At position 34:

```text
E4 repeats class10
W4 introduces new class27
```

That is exactly the first E4/W4 equality-signature conflict. Thus the missing
right-direction control state is the phase-exit event, not a repeat found by
searching elsewhere.

The existing class-10 maps are:

```text
E4 class10 -> visible67
W4 class10 -> visible73
```

Inventorying both source directions gives:

```text
E4->W4: 73-67 = 6     no marker
W4->E4: 67-73 = 77    West4 marker
```

This is a fourth marker-valued control return outside the original common
five-repeat inventory. It matches the mate-to-loop direction already seen for
class5. Numeric labels were inspected only after class10 had been selected by
the axis cycle and boundary.

## Interpretation

The equality classes are not merely anonymous repeat labels. At least one
base-five coordinate carries a physical four-operation alphabet:

```text
middle coordinate 1,2,3,4
        = up,right,down,left
```

The machine visits those operations in a counterclockwise cycle. The final
right operation changes the source-pair map and exits the phase.

This suggests the common late phase is a state/allocation table whose
canonical class IDs are meaningful coordinates. The visible ranks remain
panel-specific mapped values; the control wheel says how to approach that map
without treating them as direct substitution ciphertext.

## Next falsification target

Build the `0..24` late classes as a `5×5` `(middle,third)` state table. Freeze
small D4/control-wheel operations on one row or column, then withhold:

- the class10 phase exit;
- one marker-valued cross-panel difference; or
- one first-seen allocation.

Promote a table operation only if it predicts held-out map behavior. Merely
plotting the 25 values or choosing a symmetry after inspection fails.

## Reproduction

```bash
PYTHONPATH=src python scripts/audit_middle_eye_cycle.py
PYTHONPATH=src python -m unittest tests.test_middle_eye_cycle
```

Implementation:

- `src/eye_mystery/middle_eye_cycle.py`
- `tests/test_middle_eye_cycle.py`
- frozen protocol:
  `docs/fortieth-middle-eye-control-cycle-freeze-2026-07-26.md`
