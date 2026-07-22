# Tenth pass differential validation — frozen 22 July 2026

## Trigger

Lane K's first screen compares aligned labels belonging to different child
branches of the copied-prefix trie. Across the five least-common-ancestor
branches, mod-101 differences occupy 469 branch-specific support slots over
3,611 comparisons, for repeated mass `3142`. In 1,000 prefix-tree- and
message-sum-preserving suffix controls the range is `3116..3141`. After
reselecting the four frozen difference representations by leave-one-control-out
empirical rank, the corrected tail is `4/1001 = 0.003996`.

The effect is only one support slot beyond the simulated range. It is a screen,
not a mechanism or checksum interpretation.

## Independent relation family

The validation uses the seven nonliteral context maps, not the five trie
branch-pair populations. Each context map is independently selected by an
equality-isomorphic aligned window and provides unique forced edges
`source -> target`.

The representation is now fixed:

```text
delta = (target - source) mod 101
```

For each of the seven maps separately, count its distinct delta support.
The single validation score is total edges minus the sum of those seven
support sizes. Larger means more repeated differences. There is no digit
projection, modulus selection, direction selection, window trimming, or
cross-map pooling.

Controls keep every map's exact domain, image, injectivity, edge count, and
fixed-point count, while shuffling the source/target correspondence. Use 2,000
seeded controls and the plus-one upper tail.

## Decision rule

- Promote the mod-101 differential as a relational clue only if the fixed
  validation tail is below `0.01`.
- A pass still does not supply plaintext. It would justify inspecting a small
  authored difference machine and demanding another external prediction.
- If it fails, record the original branch support as an isolated one-slot
  anomaly and do not inspect missing residues for semantic numbers.
