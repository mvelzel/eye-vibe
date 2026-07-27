# Sixty-eighth pass — adjacent hidden-geometry pair census results

## Outcome

The frozen pair census found no pairwise contradiction:

```text
SAT       17/21
UNSAT      0/21
UNKNOWN    4/21
```

Every SAT result includes an exact injective wheel witness checked against all
constraints. The four timeouts remain unresolved:

```text
first-gap30 + first-cross
last-west4 + last-east5
last-west4 + last-east3
last-east5 + last-east3
```

The adjacent-only hidden-cycle hypothesis therefore remains open.

## Controls

Both exact encodings passed before Eye scoring.

```text
control              left   right   union
joint SAT plant      SAT    SAT     SAT
split F5 triangle    SAT    SAT     UNSAT
```

The second control verifies the purpose of the census: two individually
compatible contexts can have an exact obstruction visible only in their
union.

## Complete canonical census

Each solver received 15 seconds. The integer encoding ran only after a
bit-vector timeout.

```text
pair                                      constraints labels  BV       Int      final
first-gap30 + first-cross                         34     31   UNKNOWN  UNKNOWN  UNKNOWN
first-gap30 + first-cross-late                    34     35   SAT      -        SAT
first-gap30 + first-gap28                         25     29   SAT      -        SAT
first-gap30 + last-west4                          46     55   SAT      -        SAT
first-gap30 + last-east5                          46     55   SAT      -        SAT
first-gap30 + last-east3                          41     52   SAT      -        SAT
first-cross + first-cross-late                    34     33   SAT      -        SAT
first-cross + first-gap28                         25     26   SAT      -        SAT
first-cross + last-west4                          46     52   SAT      -        SAT
first-cross + last-east5                          46     52   SAT      -        SAT
first-cross + last-east3                          41     50   SAT      -        SAT
first-cross-late + first-gap28                    25     28   SAT      -        SAT
first-cross-late + last-west4                     46     52   SAT      -        SAT
first-cross-late + last-east5                     46     54   SAT      -        SAT
first-cross-late + last-east3                     41     53   SAT      -        SAT
first-gap28 + last-west4                          37     46   SAT      -        SAT
first-gap28 + last-east5                          37     50   SAT      -        SAT
first-gap28 + last-east3                          32     47   SAT      -        SAT
last-west4 + last-east5                           58     54   UNKNOWN  UNKNOWN  UNKNOWN
last-west4 + last-east3                           53     55   UNKNOWN  UNKNOWN  UNKNOWN
last-east5 + last-east3                           53     54   UNKNOWN  UNKNOWN  UNKNOWN
```

## Interpretation

The 17 witnesses rule out a cheap pairwise obstruction in most of the
incidence structure. They are compatibility results, not evidence that the
developers used a hidden wheel. The four UNKNOWN pairs cannot be called
positive or negative.

The next exact step is an independently encoded finite-domain CNF model on
only those four unresolved pairs. If that also stalls, further solver budget
needs a new mathematical decomposition rather than another timeout increase.

## Reproduction

```text
PYTHONPATH=src python3 scripts/run_hidden_geometry_pair_census.py
PYTHONPATH=src python3 -m unittest \
  tests.test_hidden_geometry_pairs tests.test_hidden_geometry
```

Implementation:

- `src/eye_mystery/hidden_geometry_pairs.py`
- `scripts/run_hidden_geometry_pair_census.py`
- `tests/test_hidden_geometry_pairs.py`
