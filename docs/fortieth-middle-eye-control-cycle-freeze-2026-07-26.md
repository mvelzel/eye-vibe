# Fortieth pass — middle-eye control-cycle freeze

## Question

Do the late equality-class repeats contain a four-direction control cycle on
the middle base-five coordinate?

The three repeated classes that already yielded marker-valued scope
differences are:

```text
5,20,15
```

These are three of the four positive classes whose three-digit base-five form
has only the middle coordinate nonzero:

```text
 5 = 010_5  up
10 = 020_5  right
15 = 030_5  down
20 = 040_5  left
```

The inspected E4 late signature repeats the missing class 10 at position 34,
the exact E4/W4 source-scope conflict boundary. Ordered by repeat position:

```text
class     5  20  15  10
direction 1   4   3   2
position  9  26  29  34
```

Direction order `1,4,3,2` is counterclockwise under the renderer's established
`up,right,down,left = 1,2,3,4` convention.

This was inspected before freezing. Treat controls as conditional
specificity, not prospective discovery p-values.

## Fixed inputs

Freeze:

- independently derived E4 late entry;
- canonical equality classes numbered by first occurrence;
- ordinary three-digit base-five class representation;
- nonzero single-coordinate states on each of the three digit axes;
- immediately repeated occurrence positions;
- renderer direction numbers and physical cyclic order;
- the already promoted E4/W4 conflict boundary 34.

Do not relabel classes, rotate eye-coordinate positions, choose another radix,
skip repeats, or reorder events by numeric class in the primary test.

## Primary statistics

For every positive middle-only class `5*d`, `d=1..4`, report:

- first occurrence;
- first repeat occurrence;
- repeat distance;
- whether the repeat lies inside the common 30-symbol phase or at its first
  E4-only source boundary.

Sort by first repeat position. Test whether the direction sequence is exactly
counterclockwise from up:

```text
1,4,3,2
```

## Axis controls

For each base-five digit axis, form the four positive single-coordinate class
IDs:

```text
first:  25,50,75,100
middle: 5,10,15,20
third:  1,2,3,4
```

Within the available E4 late signature through boundary 34, report:

- how many classes are present;
- how many repeat;
- whether all four repeat;
- repeat-direction order where defined.

The middle axis should not be selected merely because its class IDs fit the
observed range.

## Order controls

Among all 24 permutations of four directions, report:

- exact counterclockwise-from-up count;
- either clockwise/counterclockwise from up;
- any rotation of either physical cyclic order.

These are finite descriptive baselines. The physical direction order is fixed
by the renderer, not learned from the repeat positions.

## Boundary and held-out return

Class 10 must:

- first occur inside the common phase;
- repeat at position 34 in E4;
- be the event that breaks the E4/W4 equality signature;
- complete the missing physical direction.

After establishing that structural selection, inspect class-10 labels under
the already defined source-scope differences. Inventory marker returns without
choosing a direction from their numeric result.

## Calibration and promotion gate

Tests must recover:

- exact class forms `010,020,030,040`;
- repeat positions `(9,34,29,26)` by direction `1,2,3,4`;
- chronological order `(1,4,3,2)`;
- boundary class10 at 34;
- negative or incomplete first- and third-axis controls;
- a synthetic four-direction repeat cycle.

Promote a middle-eye control channel only if:

- it is the unique complete single-coordinate axis;
- the order is a physical cyclic traversal;
- class10 independently coincides with the source-scope exit;
- any numeric marker return is reported as a consequence, not used to select
  the class.

This would identify an operation alphabet inside the equality states, not
plaintext letters.
