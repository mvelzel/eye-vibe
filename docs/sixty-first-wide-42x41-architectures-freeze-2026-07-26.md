# Sixty-first horizon — `42+41` machine architectures

**Frozen:** 26 July 2026, before any real score was calculated.

## Why this is a new breadth pass

The body still has 83 visible labels and the practice-cipher construction
genealogy still makes a 42-symbol plaintext alphabet plausible. The identity

```text
83 = 42 + 41 = 2*42 - 1
```

has previously been read as signed magnitudes, reflection quotients, and
two-sheet homophony. It has not been read as the exact object counts of either
a path or a full binary tree:

- a path on 42 vertices has 41 edges;
- a full binary tree with 42 leaves has 41 internal nodes.

The promoted header/phase facts add another independent factorization:

```text
42 = 6*7
```

The headers are genuine `S6` elements and seven is an independently promoted
phase-width budget. These facts motivate two finite architectures without
fitting an arbitrary 83-to-42 map.

A third lane executes the retained first-`N` packet proposal. It is a
different dynamic-deck mechanism and receives no parameters from the two
static architectures.

## Lane A — six-by-seven incidence tape

Interpret the 83 visible labels as 42 ordered cells interleaved with their 41
dividers. Two canonical endpoint conventions are admitted:

```text
end singleton:    (0,1),(2,3),...,(80,81),82
start singleton:  0,(1,2),(3,4),...,(81,82)
```

Each pair and the singleton maps to one rank `0..41`. Write that rank as

```text
7*group + phase,  group in 0..5, phase in 0..6.
```

For each message, unrank its real factoradic header and use either the
permutation or its inverse to transform `group`; `phase` is unchanged. No
other group conjugation, phase shift, or label permutation is admitted.

The first four registered nonliteral contexts select one of the four global
endpoint/header-route variants. The last three contexts are held out. Score
literal equality after projection. The 6,806 affine relabellings
`x -> ax+b mod83` preserve all equality, copied-prefix, and header facts;
each control reselects the variant on training and scores holdout once.

Promotion requires an exact heldout upper tail below `.01`, improvement in at
least two heldout contexts, and a second consequence such as a stable
42-symbol support or a new branch equality.

## Lane B — balanced 42-leaf binary tree

Build the unique recursively balanced ordered full binary tree with 42 leaves:
split every `n`-leaf subtree into `floor(n/2)` and `ceil(n/2)` leaves. It has
exactly 83 nodes.

Label its nodes `0..82` under four canonical traversals:

```text
breadth-first, preorder, inorder, postorder
```

For every aligned adjacent-transition pair in the seven nonliteral contexts,
ask whether source and target transitions have the same tree distance. The
first four contexts select one traversal; the last three are untouched
holdout. The same 6,806 affine global relabellings reselect the traversal.

A planted pair of walks related by recursive child swaps must preserve every
tree distance and pass the scorer. Promotion requires a heldout tail below
`.01` and agreement in more than one heldout context. A depth or node-role
statistic may not be added after seeing the result.

This lane is distinct from the earlier six-leaf Catalan prefix decoder: the
six symbols there were renderer symbols; the 83 symbols here are nodes of one
42-leaf state object.

## Lane C — first-`N` packet XGAK

Execute the previously retained packet proposal on a canonical 83-card deck.
The finite family is:

```text
N                    26,27,36,42
initial deck          ascending, descending
eligible packet       prefix, suffix
packet collection     preserve, reverse
output timing         before update, after update
```

At each event the observed card must lie in the eligible packet; its rank
inside that packet is the decoded plaintext value. The whole eligible packet
then moves to the opposite end, preserving or reversing its internal order.
Every message resets to the same initial deck.

The positive control encrypts random rank streams with every boundary rank
represented and must replay exactly. On the Eyes, report the complete valid
prefix of every panel for all 64 candidates. Promotion requires one candidate
to decode every event with one global convention. Partial prefix length or
language score cannot promote.

This closes only the canonical packet family. A hidden initial deck is not
fitted after failure.

## Stop rule

Run all three cheap screens before deepening any survivor. If none promotes,
record the finite exclusions and return to breadth; do not add variants to
the best-looking lane.
