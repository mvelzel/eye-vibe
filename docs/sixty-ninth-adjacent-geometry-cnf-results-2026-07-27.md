# Sixty-ninth pass — independent CNF hidden-geometry results

## Outcome

The independent CNF encoding decides one of the four formerly UNKNOWN pairs:

```text
pair                              outcome  seconds
first-gap30 + first-cross         UNKNOWN  120
last-west4 + last-east5           UNKNOWN  120
last-west4 + last-east3           SAT        5.458
last-east5 + last-east3           UNKNOWN  120
```

The complete pair census is now:

```text
SAT       18/21
UNSAT      0/21
UNKNOWN    3/21
```

This remains compatibility, not evidence for a hidden wheel.

## Controls

The CNF solver:

- recovered both halves and the union of the planted SAT pair;
- accepted each half of the split `F5` triangle;
- rejected the split triangle's union;
- rejected a forced duplicate coordinate.

Every SAT witness is replayed through the original unsigned-chord checker.

## Exact new witness

The solved pair has 53 constraints, 55 touched labels, and 29 transitive
distance classes. CaDiCaL used 5,754 variables and 892,378 clauses. One
normalized coordinate witness is:

```text
1:60, 2:25, 3:29, 4:43, 5:20, 6:33, 7:14, 9:76, 11:68, 12:46,
16:12, 17:8, 18:82, 19:10, 20:24, 21:22, 22:48, 23:17, 25:55,
26:3, 30:47, 31:38, 33:45, 34:32, 37:61, 38:78, 40:35, 42:31,
43:66, 47:16, 49:59, 51:71, 53:18, 54:50, 56:75, 57:1, 58:34,
59:81, 60:40, 62:37, 63:19, 64:44, 65:49, 66:58, 67:54, 68:67,
69:72, 70:74, 71:13, 73:73, 74:23, 75:80, 77:64, 78:4, 79:0
```

The witness is notable only because both prior arithmetic encodings timed out
on this pair. It does not supply a common wheel for the last family.

## Decision

No pairwise contradiction has been found. Three pairs remain unresolved under
three exact encodings. Before deriving a heavier exact decomposition, run one
fixed one-sided witness search on those three pairs. A complete witness proves
SAT; an incomplete search says nothing.

## Reproduction

With the optional `python-sat` dependency:

```text
PYTHONPATH=src python3 scripts/run_hidden_geometry_cnf.py
PYTHONPATH=src python3 -m unittest tests.test_hidden_geometry_cnf
```

Implementation:

- `src/eye_mystery/hidden_geometry_cnf.py`
- `scripts/run_hidden_geometry_cnf.py`
- `tests/test_hidden_geometry_cnf.py`
