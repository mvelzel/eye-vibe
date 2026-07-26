# Thirty-seventh pass — terminal-repeat row-2 record results

> **Status correction, 26 July 2026:** The row-2 repeat record is retained as
> an Eye-only observation. The later “complete marker-layer interpretation”
> in this document depends on unvalidated Gate `+3` and is not promoted.

## Outcome

Promote marker row 2 as a terminal-repeat pointer record for the late common
phase:

```text
West3 34 + terminal position 29 = East3 63
East3 63 + repeat distance 13   = West2 76
```

In the row's reverse-cycle traversal:

```text
34 -> 63 -> 76
increments 29,13
```

This explains the two row-2 marker values that remained unresolved after the
phase/header closure.

## Selected body event

The independently derived common 30-symbol equality signature is:

```text
0,1,2,3,4,5,6,7,8,5,9,10,11,12,13,14,15,16,0,17,
18,19,20,21,22,23,20,1,24,15
```

Its repeat events are:

```text
position  previous  distance  class
       9         5         4      5
      18         0        18      0
      26        22         4     20
      27         1        26      1
      29        16        13     15
```

The phase ends in a repeat. Therefore position `29` and distance `13` require
no search or language interpretation.

## Fixed conditional audit

Across the same 12,096 graph-conditioned scalar assignments:

| Event | Count | Fraction |
|---|---:|---:|
| West3 is boundary 34 | 1,620 | `.133928571` |
| plus `34+29=East3` | 468 | `.038690476` |
| plus `East3+13=West2` | 126 | `.010416667` |

The exact record frequency is `1/96`. It was discovered before freezing and
is a conditional specificity measure, not a prospective p-value.

## Broad controls

The broadened searches allow:

1. any ordering of row 2 and any of the five repeat events;
2. any ordering of any marker row and any repeat event;
3. additionally, either sign for each increment.

Conditional counts are:

```text
row 2, any order/event       291/12096 = .024057540
any row/order/event          291/12096 = .024057540
any row/order/event/sign     727/12096 = .060102513
```

On the observed marker grid, all three inventories contain exactly one hit:

```text
row 2
order West3, East3, West2
terminal event (position29, distance13)
signs +,+
```

No other row, ordering, earlier repeat, or signed variant fits.

## Joint phase topology

Crossing the fixed terminal record with the previously frozen phase/header
construction gives nested counts:

```text
terminal record + full phase repair        2/12096
+ source-pair delta 50                     1/12096
+ source-boundary topology                 1/12096
```

The unique survivor is the observed scalar assignment:

```text
message order:
E1 W1 E2 W2 E3 W3 E4 W4 E5

scalars:
 0  0  1  1  3  4  2  2  3
```

The terminal record alone also selects this assignment from the two complete
factoradic survivors. The phase repair independently makes the same
selection. These routes share marker coordinates, so their counts are not
multiplied, but their agreement removes the old duplicate-edge ambiguity.

## Complete marker-layer interpretation

All nine first trigrams now have verified control-plane roles:

```text
row 1  50,80,36  output of final-row +3 and E4 bridge repair
row 2  76,63,34  terminal-repeat distance, position, source boundary
row 3  27,77,33  gap-anchor checksum/difference record
```

The connecting program is:

1. row 3 defines the anchor/check fields and directed control edges;
2. equality state follows the common-target scope for `17+3=20`;
3. the map switches to the common-source scope for `30+4=34`;
4. Gate `+3` and bridge 20 generate row 1;
5. row 2 starts at boundary 34 and points to the terminal repeat at
   positions `16,29`.

This is a complete header/control decode, not yet a body-label or plaintext
decode.

## Next falsification target

The row-2 record selects class 15 at positions 16 and 29 in every late panel.
Use the already fixed source scope E4/W4 and its established direction to
make one body-label prediction before trying other classes or pairings.

A successful operation should return a known control state, phase boundary,
or map edge without fitting a numeric transform.

## Reproduction

```bash
PYTHONPATH=src python scripts/audit_terminal_repeat_record.py
PYTHONPATH=src python -m unittest tests.test_terminal_repeat_record
```

Implementation:

- `src/eye_mystery/terminal_repeat_record.py`
- `tests/test_terminal_repeat_record.py`
- frozen protocol:
  `docs/thirty-seventh-terminal-repeat-record-freeze-2026-07-26.md`
