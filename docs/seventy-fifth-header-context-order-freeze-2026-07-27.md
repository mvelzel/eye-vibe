# Seventy-fifth pass — header/context finite-order freeze

## Question

Could the factoradic header control a repeated-body isomorphism even if its
action on the 83 visible labels is hidden by an arbitrary relabeling?

This is weaker than applying the six-symbol header permutation directly to the
base-five eye coordinates.  Suppose one observed context map is the image of a
header element under **any** permutation representation on the 83 labels.  The
image's order must divide the header element's order.  This survives every
renaming of the visible alphabet.

## Frozen contexts

Use only the five established **cross-panel, nonliteral** context maps:

```text
first-cross       W1[34:52] -> E2[39:57]
first-cross-late  W1[34:52] -> E2[74:92]
last-west4        E4[68:98] -> W4[71:101]
last-east5        E4[68:98] -> E5[69:99]
last-east3        E4[73:98] -> E3[64:89]
```

Do not use copied openings or self-contexts.

## Frozen header associations

Audit exactly three global conventions:

1. the source panel's unranked factoradic header;
2. the target panel's unranked factoradic header;
3. `target * source^-1`.

No per-context choice, inverse choice, component order, body relabeling, or
language score is allowed.  Inversion would not change element order.

## Exact discriminator

For a partial injection, decompose its observed directed graph into paths and
cycles.  A completion whose exponent divides `m` must:

- place every forced cycle in a cycle whose length divides `m`;
- close every forced path inside such a cycle;
- use no more wholly unobserved labels than the 83-label alphabet supplies.

Compute exact feasibility by grouping forced paths into cycles of divisor
length and minimizing the required unobserved filler vertices.

One incompatibility rejects the corresponding global convention.  Feasibility
is only compatibility, not evidence that the header actually supplies the
body action.

## Controls and stop rule

Unit tests must cover a planted finite-order completion, multiple forced paths
sharing one cycle, an incompatible forced cycle, and a path longer than the
claimed exponent.  No random null is needed for an exact contradiction.

Stop after the three frozen conventions.  Do not fit arbitrary powers,
products of unrelated headers, context-specific associations, or larger
orders after a failure.
