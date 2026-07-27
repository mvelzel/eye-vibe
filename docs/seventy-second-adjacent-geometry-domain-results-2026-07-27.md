# Seventy-second pass — finite-domain geometry results

## Outcome

The finite-domain solver passed its primitive controls but failed the required
full-scale positive gate:

```text
scale pair     last-west4 + last-east3
known status   SAT from the independent CNF witness
domain result  UNKNOWN after 180.000 s
nodes          73,079
backtracks     73,059
```

Per the freeze, the three unresolved Eye pairs were not opened.

## Controls

The solver:

- recovered the jointly SAT `F7` plant;
- rejected the injection-only split `F5` equal-distance star;
- rejected the algebraically impossible `F5` triangle in unit tests.

These checks support correctness at small scale. Failure to recover the
55-label known witness shows that the registered propagation and branching are
not adequate for the intended instances.

## Decision

Stop this solver lane without tuning. The exact adjacent-pair state remains:

```text
SAT       18/21
UNSAT      0/21
UNKNOWN    3/21
```

No common hidden wheel, contradiction, plaintext, or decoder was recovered.
Further work on adjacent geometry requires a genuinely different cycle-space
method or a new independently authored label relation, not another generic
encoding or longer timeout.

## Reproduction

```text
PYTHONPATH=src python3 scripts/run_hidden_geometry_domain.py
PYTHONPATH=src python3 -m unittest tests.test_hidden_geometry_domain
```

Implementation:

- `src/eye_mystery/hidden_geometry_domain.py`
- `scripts/run_hidden_geometry_domain.py`
- `tests/test_hidden_geometry_domain.py`
