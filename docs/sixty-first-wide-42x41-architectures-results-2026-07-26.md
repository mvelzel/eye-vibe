# Sixty-first pass — `42+41` machine architectures

## Result

All three frozen mechanisms close at their first discriminator. No plaintext
or body decoder was recovered.

```text
lane                         strongest real result
S6 x 7 incidence tape        0/63 training equality; holdout tail .451513
42-leaf balanced tree        12/82 holdout distances; tail .138701
first-N packet XGAK          30/1036 valid events; 0/64 complete models
```

The exact identities `83=42+41` and `42=6*7` remain true construction
possibilities. These results reject only the finite canonical consumers
frozen in advance.

## A. Six-by-seven incidence tape

The four endpoint/header variants give:

```text
endpoint         route             training  holdout
end singleton    header               0/63      2/85
end singleton    inverse header       0/63      1/85
start singleton  header               0/63      0/85
start singleton  inverse header       0/63      3/85
```

The declared tie rule selects end-singleton/header on training. Among all
6,806 affine global relabellings, 3,073 score at least its `2/85` holdout:

```text
tail = 3073/6806 = .451513371
control maximum = 10
```

More importantly, every variant has zero training equality. The real `S6`
header does not turn the known nonliteral contexts into one common six-block,
seven-phase tape under either canonical `42+41` endpoint convention.

**Decision:** close this exact `S6 x 7` incidence projection. Do not add a
group conjugation, phase shift, or arbitrary pairing.

## B. Balanced 42-leaf full binary tree

The recursively balanced tree has the required 42 leaves, 41 internal nodes,
and 83 total nodes. Structural tests verify that its root-subtree swap is a
true isometry under all four numberings.

Real aligned-transition distance scores are:

```text
layout          training  holdout
breadth-first      8/59     12/82
preorder           1/59      4/82
inorder            3/59      7/82
postorder          5/59      9/82
```

Training selects breadth-first. In 6,806 affine global relabellings:

```text
tail = 944/6806 = .138701146
control maximum = 20
```

The selected layout has contributions in all three heldout contexts, but its
total is ordinary and below many matched controls.

**Decision:** close exact tree-distance preservation for the four canonical
balanced-tree numberings. Do not introduce depth, ancestor, or node-role
scores after distance fails.

## C. First-`N` packet XGAK

All 64 combinations of packet size, initial direction, eligible side, packet
reversal, and output timing pass exact planted round trips, including ranks
zero and `N-1`.

No real candidate decodes a complete panel, let alone all nine. The best
equivalent pair of models reaches:

```text
N=26, ascending, prefix, reverse, after
valid prefixes = (6,0,6,0,0,6,6,0,6)
total = 30/1036
```

The `N=27` reverse-packet analogue ties at `30/1036`. Every other model is
lower; all 64 fail the complete-corpus gate.

**Decision:** close the canonical first-`N` packet family. The result does not
test a hidden initial deck, but failure does not license fitting one.

## Transfer

- Exact cardinality identities should generate a complete interface, not
  merely an appealing partition.
- Genuine header and phase fields can still fail when composed; the zero
  training score is more informative than their independent plausibility.
- A tree-state hypothesis should first preserve its cheapest invariant under
  known isomorphs before a language decoder is attached.
- Dynamic deck proposals can often be killed by eligibility alone, before
  optimizing plaintext.

Reproduction:

```text
PYTHONPATH=src python3 -m unittest tests.test_sixty_first_architectures
PYTHONPATH=src python3 scripts/run_sixty_first_architectures.py
```
