# Desert paired-record quotient on held-out contexts — results

## Result

The frozen record-local use of the historical transform is decisively
negative.

```text
x²+y training             11 / 96
x²+y held out              6 / 129
exact training contexts    0 / 4
exact held-out contexts    0 / 3

global-label controls      50,000
controls at least real     48,175
inclusive empirical tail   48,176 / 50,001
                           = .963500730
promotion threshold        .01
```

The natural base-five coordinates do not make the held-out nonliteral records
agree unusually often. They perform near the low end of equality-preserving
global relabelings.

## Per-context scores

The squared quotient gives:

```text
first-gap30        1 / 27
first-cross        2 / 27
first-cross-late   3 / 27
first-gap28        5 / 15

last-west4         2 / 45
last-east5         2 / 45
last-east3         2 / 39
```

No transformed context is exact.

The lossless `5x+y` sanity reading is also negative:

```text
training    4 / 96
held out    3 / 129
exact       0 / 7
```

Its few agreements occur because output coordinates can partially agree when
only one member of an input pair changes; completely copied input pairs were
excluded from both transforms.

## Component-order check

With the documented `y=021` order fixed, the six possible `x` orders score on
held out:

```text
x=012   16
x=021    9
x=102   10
x=120    6   <- historical document
x=201   11
x=210   14
```

The historical `x=120` order is uniquely last, rank `6/6`. This is
descriptive rather than a separate p-value, but it points in the same negative
direction as the preregistered control.

## Matched control

Each control globally permuted accepted labels `0..82` before extracting the
same seven records. This preserved every exact label equality, context
boundary, partial isomorphism, message length, alphabet frequency, local pair
reset, and odd-record zero pad. It broke only the natural base-five coordinate
of each label.

With seed `0xD1A607`, the complete held-out distribution is:

```text
 1:7     2:35    3:210   4:492   5:1081  6:2024
 7:3333  8:4503  9:5615 10:5991 11:6100 12:5671
13:4594 14:3686 15:2504 16:1681 17:1099 18:645
19:391  20:164  21:99   22:44   23:17   24:7
25:3    26:3    27:1
```

The real score `6` is tied or exceeded by `48,175/50,000` controls.

## Validation

A planted record demonstrates the intended lossy collision:

```text
source pair  y=111, x=000
target pair  y=000, x=111

x²+y source  1,1,1
x²+y target  1,1,1
```

All three coordinates agree although both accepted input labels change. The
same fixture has zero `5x+y` agreements. Separate tests verify odd-record
padding, copied-pair exclusion, natural rank-to-trigram conversion, split
denominators, and preservation of all equalities under global relabeling.

Implementation:

```text
src/eye_mystery/diamond_context.py
scripts/run_diamond_context_audit.py
tests/test_diamond_context.py
```

## Decision

Close the record-local desert quotient. Do not choose another formula,
component order, pair phase, context subset, label map, or substitution
alphabet after this result.

The three equally weighted desert assets and the reproducibility of defektu's
historical transform remain factual. What fails is the prospective claim that
the lossy squared reading consumes the known nonliteral Eye-record structure.
Return to the twenty-third wide portfolio rather than deepening this
representation.

