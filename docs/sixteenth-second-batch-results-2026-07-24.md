# Sixteenth wide horizon — second batch results

## Outcome

All three frozen B/H/I mechanisms close after their positive controls pass:

- no exceptional outer-`S6` renderer action is even syntactically exact on P;
- no header ordering/direction places any Eye tape at its canonical necklace
  cut;
- no `GF(125)` field/Frobenius representation makes any of the seven repeated
  contexts Möbius.

The exceptional group and field constructions are implemented and validated,
so these are failures of their declared Eye consumers rather than failures to
construct the mathematics.

Reproduce with:

```bash
PYTHONPATH=src python scripts/run_sixteenth_second_batch.py
PYTHONPATH=src python -m unittest tests.test_sixteenth_second -v
```

The complete Z3-enabled suite passes 512 tests.

## B. Exceptional outer-`S6` renderer action

### Construction validation

The code independently enumerates:

```text
15 duads
15 synthemes
 6 pentads
```

The induced action on pentads is a homomorphism `S6->S6`. It sends a
single transposition to cycle type `(2,2,2)`, proving it is not inner. The
consumer enumerates all 720 inner conjugates and header/inverse route:

```text
1440 candidates
```

### Positive-control calibration

The first arbitrary planted gauge, `c137-header`, exposed an identifiability
fact before real scoring. Newline masks observe only which renderer symbol
becomes newline; the three P headers left 96 candidates exact. The frozen
lexicographic tie-break consequently selected `c001-header`, not the planted
gauge, and failed Q.

No real score had been calculated. The plant gauge alone was changed to the
canonical representative `c000-header`; the catalog, score, P/Q split, and
tie-break were unchanged. The canonical control then gives:

```text
target/selected: c000-header
P: 0/977 mismatches
Q: 0/2190 mismatches
exact P candidates: 24
```

This passes the frozen requirement—recover an exact P candidate that decodes
Q—but does not pretend the newline mask uniquely identifies an outer gauge.
That ambiguity makes the real exact gate more important, not less.

### Eye result

No candidate is exact on P. The deterministic winner is:

```text
c003-header
P:  53/977 newline-mask mismatches
Q: 364/2190 newline-mask mismatches
exact P candidates: 0
```

Per panel:

```text
P:
east1   0
west1  53
east2   0

Q:
west2  41
west3  58
west4  63
east3 123
east4  79
east5   0
```

The exact East 1/East 2 and East 5 panels do not repair West 1 or the other
five Q panels. Since the training family itself has 53 syntax errors, the
abstract outer-automorphism relation supplies no direct renderer key.

**Boundary:** the factoradic headers do not act on renderer tapes through any
inner conjugate of the canonical exceptional outer automorphism, under
header/inverse route, while preserving authored newline syntax. The
factoradic metadata and every other possible outer-`S6` consumer remain
logically distinct; a new one now requires an independently authored
interface.

## H. Header-defined necklace/Lyndon cuts

### Positive control

Nine primitive words are rotated to their unique least rotations under
`header-forward`. The detector selects that convention on P and predicts:

```text
P: 3/3 canonical
Q: 6/6 canonical
```

### Eye result

All four candidates give zero canonical panels:

```text
candidate          P       Q
header-forward     0/3     0/6
header-reverse     0/3     0/6
inverse-forward    0/3     0/6
inverse-reverse    0/3     0/6
```

All nine tapes are primitive and borderless, so the failure is not caused by
ambiguous periodic rotations. Under the selected convention:

```text
panel   least rotation / length   Duval factors
east1        63 / 302                  7
west1       169 / 314                  7
east2       223 / 361                  7
west2       243 / 311                  7
west3       285 / 379                  8
west4        11 / 367                  5
east3       217 / 420                  7
east4        11 / 364                  4
east5        11 / 349                  5
```

The three P factor counts all equal seven, but factor count was explicitly
diagnostic, not a promotion statistic; Q is mixed and no header prediction
was frozen for the number seven. It is retained only as an observation.

**Boundary:** the authored renderer start is not the least necklace rotation
under header/inverse alphabet order and forward/reverse direction. Arbitrary
cut selection and language-scored rotations remain forbidden.

## I. `GF(125)` Möbius/Frobenius contexts

### Positive control

The implementation enumerates all:

```text
40 monic irreducible cubics over F5
 3 Frobenius powers
--------------------------
120 representations
```

Seven independent planted contexts use local fractional maps in

```text
t^3 + t + 1, Frobenius power 1.
```

The complete training scan uniquely selects that representation:

```text
P: 4/4 exact contexts
Q: 3/3 exact contexts
exact P representations: 1
```

### Eye result

No representation makes even one training context exact. After fitting every
local map from every admissible three-edge subset, the training winner is:

```text
t^3 + 2t^2 + 2t + 3
Frobenius power 1
P exact: 0/4
Q exact: 0/3
exact P representations: 0
```

Best per-context agreement under that fixed representation is:

```text
first-gap30        8/18
first-cross        6/18
first-cross-late   9/18
first-gap28        6/9
last-west4         7/30
last-east5         7/30
last-east3         7/25
```

Three agreements are consumed by fitting, so values like `7/30` do not
constitute a near solution. Every context has an explicit fourth-or-later
contradiction.

**Boundary:** none of the 120 canonical `GF(125)` field/Frobenius
representations supports the seven context maps as local Möbius actions.
Literal affine `F5^3` was already rejected separately. Higher rational
degree, per-context field choices, and hidden infinity symbols are not
licensed repairs.

## Decision

No second-batch mechanism earns depth. Do not:

- treat the guaranteed outer `S5` action as evidence after its renderer
  consumer fails;
- choose the observed least-rotation offsets as keys;
- promote the diagnostic Duval factor count seven;
- add rational degree to repair `GF(125)`.

The next move returns to breadth across universal reset semantics, predictive
Hankel state, graph covering, finite-state enumerative coding, executable
archaeology, and practice-puzzle method transfer. The original trie checksum,
lag-one wheel, factoradic metadata, Gate construction vocabulary, source
ancestry, and chronology leads remain active.
