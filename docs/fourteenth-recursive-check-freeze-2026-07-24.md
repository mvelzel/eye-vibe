# Fourteenth horizon: recursive branch-check freeze

## Purpose

The ordinary body prefix trie remains the strongest breadth-first positive:
its 918 transition labels sum to zero modulo 101. The minimal-dictionary and
failure-link automata did not supply an independent confirmation.

This lane asks a stricter question: does one tiny bottom-up check rule make the
five independently present branch nodes self-validating and then predict the
unscored trie root? The exact family and held-out protocol are fixed here
before any coefficient is evaluated.

## Canonical tree and check value

Use the marker-stripped body prefix trie. A branch node is exactly a trie node
with outdegree at least two. The existing hierarchy predicts five such nodes;
no unary nodes, leaves, failure links, compressed-edge endpoints, or selected
depths are added.

For every node `v`, compute bottom-up:

```text
R(v) =
    a * incoming_label(v)
  + b * sum(R(child) for child of v)
  + c * outdegree(v)
  + d * depth(v)
  mod 101
```

The trie root has incoming label zero and depth zero. Children are a set, so
their traversal order is irrelevant.

The finite rule family is:

```text
a in {-1,+1}
b,c,d in {-1,0,+1}
```

There are exactly 54 rules. Requiring `a != 0` prevents a label-free topology
rule from masquerading as a checksum. The ordinary transition sum is the
included rule `(a,b,c,d)=(1,1,0,0)`, but it receives no preference.

## Prediction protocol

The branch-check hypothesis says `R(v)=0` at every branch node.

For each of the five branches in turn:

1. hold that branch out;
2. select the rule with the most zero checks on the other four;
3. break ties by lexicographic coefficient tuple, without consulting the held
   branch;
4. score whether the fixed rule gives zero on the held branch.

The primary score is the number of correct held-out branches, `0..5`.

Separately, select one rule on all five branches by the same criterion and ask
whether it gives `R(root)=0`. The root is not part of branch-rule selection.

Promotion requires all three:

1. exact `5/5` branch leave-one-out prediction;
2. the all-branch-selected rule closes at the root;
3. a corrected joint matched-control upper tail below `.01`.

Anything less than `5/5` or a nonzero root stops immediately. A near-best
coefficient, one lucky branch, or the already known root-sum rule does not
promote.

## Positive control

Before the Eye result is admissible, construct a finite trie whose edge labels
are generated to make one rule close at every branch and root. The evaluator
must recover 5/5 held-out checks and the root. A toy that merely evaluates one
known coefficient without selection is insufficient.

## Matched controls

If the exact data gates pass, draw 2,000 uniform global relabelings from the
existing subgroup that:

- preserves the complete Eye equality/prefix trie;
- preserves the East 1/East 3/East 5 complete numeric sums exactly;
- fixes all nine marker labels.

For every control, recompute all 54 recursive tapes, all five leave-one-out
selections, and the all-branch root prediction. The joint event is:

```text
control leave-one-out score >= observed
AND control selected root is zero
```

Do not multiply a branch-score probability by the old root-checksum
probability. The same labels carry both.

## Boundaries

This is not a decoder. A survivor would identify a compact checksum grammar
that could then be compared with an independently authored recursive
game/Gate interface. It would not authorize assigning plaintext to node
values.

If the lane fails, do not expand coefficients beyond `{-1,0,1}`, add
node-type-specific rules, choose a different modulus, or treat leaves as extra
training checks. Those repairs would turn five branch observations into a
fitted formula.
