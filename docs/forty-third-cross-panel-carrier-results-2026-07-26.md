# Forty-third pass — cross-panel carrier results

## Result

The other two synchronized final panels do not provide a simple numeric
allocator for the third.

All frozen families fail complete replay and every co-best family fails the
two held-out classes.

## Mod-83 record arithmetic

For each target, the first family exhausted `571,787` models:

```text
target = a*source1 + b*source2 + c mod 83
```

Every target has the same maximum, `5/23` training classes. There are five
co-best models per target and none predicts both holdouts.

Adding the equality-class index:

```text
target = a*source1 + b*source2 + d*class + c mod 83
```

expands the family to `47,458,321` models per target. Each target has one
co-best model at `7/23`; all six withheld predictions are wrong:

| Target | class10 predicted/actual | class24 predicted/actual |
|---|---:|---:|
| E4 | `23/67` | `54/69` |
| W4 | `17/73` | `13/17` |
| E5 | `17/22` | `1/31` |

The isolated W4 class24 near miss is still wrong and was selected from more
than 47 million models.

## Base-5 three-eye arithmetic

The second family exhausted `675,000` models per target:

- independent eye order in both sources and the target;
- shared coefficients `a,b` modulo five;
- three independent fixed output-eye offsets.

Every target peaks at only `4/23`:

| Target | Co-best models | Both holdouts correct |
|---|---:|---:|
| E4 | 54 | 0 |
| W4 | 54 | 0 |
| E5 | 18 | 0 |

Several co-best models also emit ranks above 82 on a holdout. The family was
left broad; imposing the visible-alphabet bound cannot rescue it.

## Independent-carrier inventory

The negative result leaves the other carrier categories:

| Carrier | Current objective content | Why it cannot yet allocate |
|---|---|---|
| factoradic headers | nine exact `S6` states and marker ranks | direct consumers are negative; no authored PRNG/update rule |
| Gate assets | objective `153`, `+3`, paired panels, control-layer cycle | proposed 8-digit tape/masks are not independently defined; first-seen branch remains missing |
| procedural-wand branch | exact `0..82` outcome set inside `0..100` | selected value is not retained or used as an 83-state walk |
| `gun_names` table | one concrete 83-entry deck | no selected consumption rule; direct and practice-transfer tests are negative |
| Cessation/earthquake | reproducible in-game tapes/masks | frozen transfers to Eye contexts are negative |
| game RNG | many calls and seeds | eligible Lua exposes no generator implementation or header-seed rule |

This is a necessity result, not a claim that no hidden carrier exists.
It says that none of the currently reproducible candidates supplies the
missing fresh-value information without adding an unselected algorithm.

## Consequence

Further cache fitting is not identifiable. Progress now requires one of:

1. a newly discovered authored carrier or operation schedule;
2. construction archaeology that recovers the developers' offline tool/key;
3. a fully solved practice cipher that supplies a concrete, replayable
   allocation mechanism;
4. a plaintext/source anchor selected independently of Eye fit.

The most efficient next actions are a read-only Silmä delta focused on new
carrier claims and renewed mechanism acquisition from practice cipher 4.

## Reproduction

```bash
PYTHONPATH=src python3 scripts/audit_cross_panel_carrier.py
```

Implementation:
`src/eye_mystery/cross_panel_carrier.py`.

