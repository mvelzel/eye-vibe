# Thirty-sixth pass — phase-marker closure results

> **Status correction, 26 July 2026:** The phase measurements remain Eye-only
> observations, but the claimed closure imports the unvalidated Gate `+3`
> interpretation. It is therefore not a promoted construction record. The
> numerical closure is preserved as retrospective provenance only.

## Outcome

Promote a complete phase/header construction record:

```text
final row                    27  77  33
Gate shift +3               30  80  36
repair self by bridge 20    50  80  36
row 1                       50  80  36
```

The previously “absent” shifted self value `30` is exactly the independently
measured length of the second three-panel equality phase. The E4 bridge length
is `20`, and `20+30=50` repairs that phase pointer into the remaining row-1
marker.

This upgrades Gate `+3` from a two-field marker coincidence to an executable
header/state repair. It still does not justify shifting body labels or promote
the dossier's unproved Type4/Type6 allocator.

## Derived measurements

All phase lengths are derived from the canonical corpus:

```text
old bridge lengths:          E4 20, W4 21, E5 20
old three-panel common:      17
old pair LCPs:               E4/W4 17, E4/E5 20, W4/E5 17

late three-panel common:     30
late pair LCPs:              E4/W4 34, E4/E5 30, W4/E5 30
```

No numeric body label is used to measure these boundaries. Each phase is
canonicalized independently by equality signature.

## Fixed closure

The four exact equations are:

```text
27+3  = 30  late common-phase length
20+30 = 50  East1 marker
77+3  = 80  West1 marker
33+3  = 36  East2 marker
```

Equivalently, `+3` converts the final self field into a phase pointer and the
two non-self fields directly into row-1 markers. Adding the self panel's old
bridge length dereferences the pointer and completes row 1.

## Conditional marker audit

The fixed 12,096-assignment universe preserves every header's first two
base-five coordinates, permutes only the observed scalar multiset, and
requires distinct ranks in `0..82`.

Staged counts are:

| Event | Count | Fraction |
|---|---:|---:|
| aligned non-self `+3` relations | 372 | `.030753968` |
| plus `E4+3=late phase 30` | 66 | `.005456349` |
| plus `E1=bridge 20+phase 30` | 22 | `.001818783` |

Incrementally:

```text
P(self points to phase | non-self) = 66/372 = .177419355
P(full closure | self-to-phase)    = 22/66  = .333333333
P(full closure | non-self)         = 22/372 = .059139785
```

These are nested descriptions, not independent factors, and must not be
multiplied. The closure was inspected before freezing, so `.001818783` is a
conditional specificity measure rather than a prospective p-value.

## Broad correction and shift scan

Keeping the measured phase lengths and `+3`, but allowing:

- every ordered pair of marker rows;
- every possible self position;
- bridge length `20` or `21`;
- either natural target positions or any target permutation;

gives:

```text
natural-position repair: 34/12096 = .002810847
permuted-target repair:   34/12096 = .002810847
```

On the observed grid, a diagnostic scan of every nonzero shift `1..82` under
both broad families has exactly one hit:

```text
shift +3
source row 3 -> target row 1
self position E4
bridge length 20
```

Target permutation introduces no second solution.

Of the two full factoradic scalar survivors, only the observed assignment
satisfies the fixed closure:

```text
001134223
```

This is a body-facing resolution of the earlier duplicate-edge scalar
ambiguity, independent of the locale checksum.

## Target-to-source scope switch

The first two header digits already encode directed control edges:

```text
E4  0->0  loop
W4  0->2  same source as E4
E5  1->0  same target as E4
```

The phase topology follows those types exactly:

```text
before map switch:
  longest pair = E4/E5 = common target group
  17 + 3 = 20

after map switch:
  longest pair = E4/W4 = common source group
  30 + 4 = 34
```

The loop E4 is the pivot shared by both scopes. The extension magnitudes
`3,4` match the old typed suffixes of the target mate E5 and source mate W4.
This is direct evidence that the header edge routes equality-state scope:
the machine changes from grouping by control target to grouping by control
source.

The same topology closes two further quantities:

```text
old target-pair boundary 20 + late common 30 = 50
W4-E4 = 77-27 = 50 mod83
```

Thus `50` is simultaneously the East1 marker, the two-phase path length, and
the source-pair rank delta.

Adding the source-delta condition leaves `4/12096` assignments. The unique
late source-pair boundary is:

```text
34 = West3 marker
```

Adding that retrospective boundary match leaves `2/12096`. These nested
counts reuse the inspected topology and are not additional p-values.

## Interpretation

The compact machine model is now:

1. final headers are typed directed control edges around a loop;
2. the old equality phase groups the loop with its target mate;
3. a map switch changes scope to the loop and its source mate;
4. typed suffix widths `3` and `4` schedule the two extensions;
5. Gate `+3` converts final record fields into a late-phase pointer and row-1
   fields;
6. the E4 bridge dereferences the pointer to complete row 1.

This is substantially stronger than “some numbers match.” It integrates
independently derived equality boundaries, header types, marker arithmetic,
and the later Gate operator in one low-capacity construction.

It remains a control-plane decode. The meaning of the visible body labels,
the remaining row-2 fields `76,63`, and the plaintext—if the bodies contain
prose at all—remain unresolved.

## Next prediction target

Use the target-to-source scope switch without fitting numeric body labels to
predict one of:

- the roles of row-2 markers `76` and `63`;
- the next scope after the E4/W4 boundary at 34;
- an old/new map edge other than the known `7->24`;
- the allocation rule for first-seen values.

The strongest immediate test is to treat the three header coordinates as a
scope-routing program and derive the next pair or boundary before inspecting
another body segment.

## Reproduction

```bash
PYTHONPATH=src python scripts/audit_phase_marker_closure.py
PYTHONPATH=src python -m unittest tests.test_phase_marker_closure
```

Implementation:

- `src/eye_mystery/phase_marker_closure.py`
- `tests/test_phase_marker_closure.py`
- frozen protocol:
  `docs/thirty-sixth-phase-marker-closure-freeze-2026-07-26.md`
