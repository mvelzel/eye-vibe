# Fourteenth horizon: failure-link sieve freeze

## Why this remains distinct

The minimal dictionary automaton found no internal suffix-equivalent states.
That does not settle Aho–Corasick failure links. A failure link points from one
trie prefix to its longest proper suffix that is also *any* trie prefix; the
complete continuation languages need not be equal.

This document fixes lane E's exact serializer and external structural join
before either is calculated on the Eyes.

## Canonical automaton

Use the nine marker-stripped trigram bodies as the pattern dictionary.

1. Build their ordinary prefix trie.
2. Traverse every node's outgoing edges in numeric label order.
3. Construct standard Aho–Corasick failure links breadth first.
4. Retain exactly those non-root nodes whose failure target is also non-root,
   equivalently whose longest proper prefix-suffix match has positive length.

For every retained node record:

```text
incoming edge label
node depth
failure-target depth
depth drop = node depth - failure-target depth
```

The primary checksum is the sum of retained incoming labels modulo 101. A
label is counted once per retained trie node, not once per failure-chain step
or completed transition.

The depth-drop word lists retained nodes in the same numeric-label BFS order.
No alternate DFS, message order, failure-chain expansion, or sorted-depth
variant will be inspected.

## Frozen external join

The only structural word tested is the already decoded prefix-hierarchy word:

```text
BEXIT = (2,5,24,9,20)
```

Ask whether that complete five-value sequence occurs contiguously in the
depth-drop word. No substring, reversal, cyclic rotation, A1Z26 alternative,
or Gate-derived word will be chosen after inspection.

Promotion requires **both**:

1. incoming-label sum `0 mod 101`; and
2. one exact contiguous `BEXIT` depth-drop occurrence.

Either failure closes the lane. A checksum alone is another selected mod-101
event; a word alone can arise from ordering a long depth tape.

## Controls and capacity

The Aho–Corasick topology, retained-node count, failure-depth histogram, and
un-ordered depth drops depend only on the equality skeleton. Global label
permutations preserve them.

If the checksum closes, calibrate its exact probability in the subgroup that
preserves the complete East 1/East 3/East 5 sums and fixes all nine markers,
using the retained incoming-label multiplicities.

If both requirements pass, estimate their joint event by drawing uniform
relabelings from that same subgroup, rebuilding numeric-label BFS order, and
rechecking both criteria. The complete joint control must be run; separate
checksum and word probabilities may not be multiplied.

No language score or plaintext rendering is authorized by this lane. A
survivor would first need an independently authored failure/cache interface,
such as a later in-game construction that actually consumes the retained
records.
