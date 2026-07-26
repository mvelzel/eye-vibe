# Forty-sixth pass — axis-branch marker holdout

## Prospective question

The branch audit selected third-coordinate classes without consulting their
visible labels:

```text
class1  common repeat
class2  source-pair operation
class3  target-mate operation
class4  absent
```

Their role order is the physical clockwise direction cycle `1,2,3,4`. The two
closed loop/target divergence windows independently have checksum deficits
`3,2`, the target and source controls in reciprocal order.

This freeze asks whether the already established *middle-coordinate*
cross-panel operations transfer to the new third-coordinate controls. The
class-2 and class-3 visible labels have not been consulted for this test.

## Frozen panels and directions

Header topology fixes:

```text
loop         E4
source mate  W4
target mate  E5
```

The middle-coordinate controls already execute:

```text
direction2 / source boundary:
  class10  W4 -> E4  = marker77

direction3 / terminal source return:
  class15  E4 -> W4  = marker27

target-to-loop scope:
  class20  E5 -> E4  = marker36
```

Two natural transfers are frozen. They share the source prediction and differ
only in whether the target operation inherits physical direction or scope.

### Model D — inherit the physical-direction operation

```text
third class2: W4 -> E4  predicts marker77
third class3: E4 -> E5  predicts marker27
```

The first line copies the direction-2 source operation. The second copies the
direction-3 loop-to-mate operation, substituting the target mate selected by
the third-axis role.

### Model S — inherit the branch scope

```text
third class2: W4 -> E4  predicts marker77
third class3: E5 -> E4  predicts marker36
```

The first line is unchanged. The second copies the already observed
target-to-loop scope.

## Complete reporting

After this freeze:

- reveal all three panel labels for classes 2 and 3;
- report both directed differences for every panel pair;
- identify every difference equal to one of the nine header markers;
- score Models D and S exactly;
- report a broad baseline over all ordered panel pairs for the two held-out
  classes, without replacing either frozen model.

## Promotion gate

- A model passes only if both exact predicted marker values match.
- One of two predictions is suggestive but fails the complete transfer.
- If both models fail, retain the label-invariant branch checksums but do not
  infer a cross-panel numeric decoder.
- No third orientation, panel substitution, offset, or marker target may be
  added after seeing the labels.
