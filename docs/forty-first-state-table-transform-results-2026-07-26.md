# Forty-first pass — state-table transform results

## Outcome

Reject direct geometric/substitution transfer between the three late `5×5`
class-to-visible-label tables.

The middle-eye control wheel is real, but it does not mean that one panel's
visible labels are obtained from another by a D4 grid motion, toroidal shift,
or physical eye rotation/reflection.

## Coordinate-table screens

For every ordered panel pair:

| Family | Models | Best exact cells | Best fixed-offset cells |
|---|---:|---:|---:|
| 8 square D4 transforms | 48 | 1/25 | 3/25 |
| D4 plus 25 toroidal shifts | 1,200 | 3/25 | 5/25 |

The translated family's best exact fits are six unrelated three-cell models.
The best modal offsets are two unrelated five-cell fits. Neither includes a
shared operation selected by the control classes or phase boundaries.

## Visible-eye geometry screens

Each visible rank was decoded into three eye directions. Tested transforms:

| Family | Models | Best exact cells |
|---|---:|---:|
| eye-position permutation + one shared physical D4 | 288 | 1/25 |
| eye-position permutation + independent D4 per eye | 18,432 | 3/25 |

The independent-eye family's four co-best models all match the same unrelated
classes `0,6,24` between E4 and E5. Three matches after searching 18,432
models fails the frozen capacity gate.

## Held-out control failure

Using control classes `5,15,20` as the only training cells:

```text
shared physical D4:
  maximum training matches       0/3
  class10 held-out predictions   0

independent-eye D4:
  maximum training matches       1/3
  co-best models                 256
  co-best class10 predictions    0
```

Thus even the broad physical family cannot learn the known control states and
predict the class10 boundary event.

## Interpretation

The `5×5` plane is an operation/state coordinate system, not a static
substitution square. The visible mappings must be updated statefully, allocated
from another structure, or compared through selected cache events.

This negative narrows the next model:

- retain canonical class coordinates and the counterclockwise control wheel;
- retain selected directed differences at repeated states;
- reject a single D4 transform of coordinates or visible eye trigrams;
- require a cache/allocator or transducer to predict fresh mapped labels.

It modestly increases the relevance of the Gate dossier's cache vocabulary,
but supplies none of its missing eight-role allocator by itself.

## Next test

Treat the late signature as an allocation/reference tape:

```text
25 first-seen allocations
5 common-phase references
1 boundary reference in E4
```

Use the control wheel to classify reference operations and freeze a
deterministic cache update. Withhold class10 and at least one first-seen value.
Per-cell transformations and arbitrary label-table completions remain closed.

## Reproduction

```bash
PYTHONPATH=src python scripts/audit_state_table_screen.py
PYTHONPATH=src python -m unittest tests.test_state_table_screen
```

Implementation:

- `src/eye_mystery/state_table_screen.py`
- `tests/test_state_table_screen.py`
- frozen protocol:
  `docs/forty-first-state-table-transform-freeze-2026-07-26.md`
