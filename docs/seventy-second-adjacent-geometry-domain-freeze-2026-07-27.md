# Seventy-second pass — finite-domain geometry solver freeze

## Purpose

The remaining pair instances have no cheap graph separator, but every chord
constraint is a small ternary relation:

```text
distance(z[u], z[v]) = d[class]
```

This pass uses direct finite-domain propagation instead of bit-blasting,
arithmetic disjunctions, or post-hoc collision cuts.

## Frozen exact CSP

- Each touched label has an 83-bit coordinate domain.
- Each transitive chord class has a 41-bit magnitude domain.
- Fix the first constrained edge at coordinates `0,1`, as before.
- Enforce generalized arc consistency on every chord edge by cyclic bitset
  rotations:
  - remove coordinates with no partner at any allowed magnitude;
  - remove magnitudes with no endpoint pair support.
- Propagate singleton coordinates through global injection.
- Reject a node if the remaining coordinate domains have no complete
  bipartite matching.
- Branch deterministically on the smallest non-singleton domain, breaking ties
  by constraint degree and then canonical variable order.
- Try values in ascending numeric order.

The search is complete if allowed to finish. Returned SAT assignments are
replayed with the original checker. Exhaustion is exact UNSAT. A wall timeout
is UNKNOWN.

## Gates and targets

Before the unknown pairs:

1. recover the jointly SAT `F7` plant;
2. reject the injection-only split `F5` star;
3. recover the previously CNF-solved
   `last-west4 + last-east3` 55-label witness.

Then run the three unresolved pairs in canonical order with 180 seconds each:

```text
first-gap30 + first-cross
last-west4 + last-east5
last-east5 + last-east3
```

## Stop rule

- Any SAT or UNSAT result is exact.
- A timeout remains unknown irrespective of nodes or domain reductions.
- Do not tune branching, value order, or propagation per target.
- If the scale gate fails or all targets time out, stop this lane and return
  to a different cryptographic object.
