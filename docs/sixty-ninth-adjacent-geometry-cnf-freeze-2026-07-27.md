# Sixty-ninth pass — independent CNF hidden-geometry freeze

## Purpose

The arithmetic bit-vector and integer encodings both timed out on four of the
21 two-context unions. This pass changes only the exact solver
representation, not the cryptographic model.

## Frozen CNF

For one unresolved pair, use:

```text
X[label,position]       label occupies this point of the 83-cycle
D[class,magnitude]      edge class has unsigned magnitude 1..41
```

Add:

1. exactly one position for each touched label;
2. at most one touched label at each position;
3. exactly one magnitude for each nonzero chord class;
4. for every class edge, position, and magnitude,
   `D[c,m] AND X[u,p]` implies
   `X[v,p+m] OR X[v,p-m]`, modulo the cycle;
5. the same translation/scaling anchor `X[a,0]` and `X[b,1]`.

Use pairwise exact-one clauses. Add each edge implication in both directions
for propagation. No learned wheel, label order, or extra lag is admitted.

## Frozen targets and budget

Run exactly the four UNKNOWN pairs from the frozen pair census, in canonical
order. Use one fixed bundled SAT backend and 120 seconds per pair.

```text
first-gap30 + first-cross
last-west4 + last-east5
last-west4 + last-east3
last-east5 + last-east3
```

`SAT` must replay through the original chord checker. `UNSAT` is an exact
rejection. Timeout or interruption remains `UNKNOWN`.

## Controls before Eye scoring

- recover the jointly SAT `F7` pair;
- reject only the union of the split equidistant `F5` triangle;
- agree with both old encodings on every individual control fragment;
- reject a deliberately duplicated coordinate through the injection clauses.

## Branching

- Any UNSAT pair rejects the global adjacent-cycle hypothesis. Confirm it
  with an arithmetic encoding at a longer bound and seek a small certificate.
- A SAT result closes that pair as compatible but does not promote a wheel.
- If all four remain unknown, stop generic solver substitution and derive a
  cycle-space or separator decomposition.
