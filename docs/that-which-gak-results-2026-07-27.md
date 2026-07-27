# `THAT WHICH` ordinary-GAK stabilizer audit — results

## Outcome

The six proposed `THAT WHICH` windows are exactly compatible with ordinary
GAK when each window may begin in an arbitrary deck state. One shared set of
seven arbitrary position permutations reproduces all 60 ciphertext outputs
exactly.

This is a compatibility result, not plaintext evidence. The arbitrary-state,
arbitrary-permutation model has high capacity and does not connect the two
occurrences through their unknown intervening plaintext.

## Exact observations

```text
phrase='THAT WHICH' length=10
east1:40   47 44 48 42 19 48 13 47 19 49   A.B.CB.AC.
east1:68   71 11 74 56  4 74 19 71  4 51   A.B.CB.AC.
west1:40   47 44 48 42 19 48 13 47 19 49   A.B.CB.AC.
west1:70   68 46 17 36 13 17 21 68 13  9   A.B.CB.AC.
east2:45    6 13 64 29 49 64 63  6 49 31   A.B.CB.AC.
east2:80   41 72 57 20 23 57 65 41 23 18   A.B.CB.AC.
```

All 270 nonempty operation-word spans were compared across traces:

```text
same-word fixes/does-not-fix conflicts   0
point-stabilizer subgroup contradictions 0
```

The repeated endpoint cards imply exactly three distinct composite operation
words in the top stabilizer:

```text
T W
WHIC
HAT WHI
```

For example, the first and eighth ciphertext cards match in every window, so
the updates between them—`HAT WHI`—compose to a permutation fixing the top
position. No factorization of any observed word conflicts with subgroup
closure.

## Exact extension

The sparse solver gives:

```text
traces=6
characters per trace=10
shared character operations=7
deck size=83
status=SAT
forward replay=exact
```

It assigns an independent initial position to every tracked ciphertext card
in each window, while every occurrence of a plaintext character shares one
partial position bijection across all windows. Each partial bijection is
completed to a full 83-position permutation, each partial state to a full
deck, and the resulting witness is replayed with the ordinary forward GAK
implementation. Thus `SAT` is constructive rather than a necessary-condition
screen.

The displayed solver choice of initial card `0` in each trace is unconstrained
gauge, not an Eye observation.

## Calibration note

The fixed-point implementation passed a contradictory cross-trace plant, a
cross-trace subgroup-closure plant, and a valid random-GAK trace before the
Eye readout. The arbitrary-state solver passed a generic six-state planted
fixture before the real run. The freeze had more strictly requested a plant
with the same ten-character equality pattern; that matched-pattern fixture was
added immediately after the real result and is now the first solver test.

This sequencing lapse is disclosed rather than rewritten. It cannot create
the positive result because the extracted real witness is independently
forward-replayed exactly, but the matched control was not prospective.

## Scope

Promote only:

- the literal ten-character core has no top-stabilizer obstruction;
- its six local traces extend to shared ordinary-GAK operations;
- any future ordinary-GAK construction for this crib must realize the three
  top-fixing words above.

Do not promote:

- `THAT WHICH` as plaintext;
- a common eleventh character—the six equality patterns already split after
  ten positions;
- feasibility of complete messages, a common reset state, XGAK, or a source
  text.

## Reproduction

The certificate without optional dependencies:

```bash
PYTHONPATH=src python scripts/check_that_which_gak_fixed_point.py
```

The constructive witness requires `z3-solver`:

```bash
PYTHONPATH=src python scripts/run_that_which_arbitrary_state_gak.py
PYTHONPATH=src python -m unittest \
  tests.test_gak_fixed_point tests.test_arbitrary_state_sparse_gak
```
