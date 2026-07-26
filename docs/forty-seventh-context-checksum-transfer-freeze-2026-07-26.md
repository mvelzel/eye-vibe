# Forty-seventh pass — registered-context checksum transfer freeze

## Discovery/calibration context

The newly promoted branch record is not an arbitrarily chosen suffix. It is
the continuation of the previously registered context:

```text
last-east5
left   E4 start68
right  E5 start69
known isomorphic length30
```

Local equality signatures agree for the registered 30 events. Their first two
closed disagreement windows then have left-minus-right class-sum checks:

```text
+3, +2
```

The ordered header scalar fields are:

```text
left E4  scalar2
right E5 scalar3
```

Thus the observed checksum order is:

```text
right scalar, left scalar
```

This context is calibration and must not be counted as a prospective test.

## Frozen transfer rule

For every other nonliteral `CONTEXT_SPECS` entry, keep its already registered:

- left and right panels;
- left and right start offsets;
- known isomorphic length;
- direction `left - right`.

Canonicalize each complete suffix from its registered start independently by
first occurrence. A **closed disagreement record** is one maximal aligned
unequal run followed by an equal class before either suffix ends.

Prediction:

```text
first closed check   = right panel's header scalar
second closed check  = left panel's header scalar
```

All checks are ordinary sums of local equality-class IDs modulo 83. No
positional weights, class relabeling, window selection, sign reversal, or
offset adjustment are allowed.

For a self-context both scalars are identical. A context with one closed
record can test only the first field. A context with none is untestable, not a
failure or success. Later records are reported but not predicted.

## Frozen test set

The calibration `last-east5` is excluded. Test every other nonliteral entry:

```text
first-gap30
first-cross
first-cross-late
first-gap28
last-west4
last-east3
```

The literal marker-prefix contexts are excluded because they are reset
openings rather than offset isomorphs and supplied the headers used by the
prediction.

## Broad controls

Report:

1. exact field matches and complete two-field matches;
2. all closed-window checks in all seven nonliteral contexts;
3. how many ordered context assignments would pass if panel pairs were
   reassigned while retaining the observed window checks;
4. sign-reversed matches, disclosed only as a robustness boundary;
5. an equality-preserving synthetic plant whose checks are constructed from
   ordered scalar fields.

## Promotion gate

Promote a corpus-wide checksum transducer only if at least one non-calibration
context predicts both fields exactly and the complete transfer is selective
under the declared broad assignment control.

One matched field, an untestable context, or a match found only after reversing
the sign does not pass. Failure leaves the final `last-east5` branch record
intact but closes its direct transfer to the other registered contexts.
