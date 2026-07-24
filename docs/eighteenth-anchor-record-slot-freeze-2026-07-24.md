# Anchor-record slot/target follow-up — freeze

## Retrospective algebraic observation

Use the independently established final component orders, with the identity
convention for E4's self edge:

```text
E4  012
W4  021
E5  102
```

For an order `(source,target,remaining)`, test the six directed differences
between distinct slots. Exactly one reproduces all three markers:

```text
h_message = a[order[0]] - a[order[2]] mod 83
```

That is, subtract `source - remaining` and omit the control target:

```text
slot pair  outputs on anchors 75,81,48
0-1        77,27,6
0-2        27,77,33   <- markers
1-0        6,56,77
1-2        33,50,27
2-0        56,6,50
2-1        50,33,56
```

The omitted target components across the three panels are:

```text
(1,2,0)
```

The ascending ranks of the three anchor values in message order are also:

```text
rank(75,81,48) = (1,2,0)
```

This rank equality was noticed after the values were known. It is not a fresh
prediction and needs a full reselection control.

## Frozen controls

Run 50,000 new matched body shuffles using seed `0x18d07`, preserving each
post-opening body's exact length, multiset, and no-adjacent-double condition.

Report targeted gap-11 counts for:

1. one clean anchor per message;
2. anchor ranks exactly `(1,2,0)`;
3. the exact ordered numeric formula;
4. both rank and numeric formula.

For the broad statistic, reselect every gap `2..30`. Require one clean anchor
per message, the fully broadened numeric difference relation, and an anchor
rank pattern equal to either:

```text
target column ascending:  (1,2,0)
target column descending: (1,0,2)
```

Allowing both directions charges the retrospective choice of ascending rank.
The target column itself is not selectable: among the three final-order
columns it is the only column that is a permutation of `0,1,2`.

Use plus-one corrected tails. The detector must pass a plant in which the
slot rule and target-rank column are both exact.

## Gate

Promote the omitted target column as another field of the same record only if
the broad corrected tail is below `.01`. Do not multiply it with earlier
tails. A positive result would give the final marker orders three linked
roles:

- slots 0 and 2 choose subtraction operands;
- slot 1 records anchor value ranks;
- W4's complete order records anchor position ranks.

It would still not explain the gap/base selector or plaintext.
