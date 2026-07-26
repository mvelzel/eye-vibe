# Forty-second pass — cache/allocator freeze

## Question

Can the common late equality trace drive a small, independently specified
stateful allocator that reproduces the visible ranks?

The trace itself may say when a class is new or repeated. It may not supply a
class-to-rank lookup learned from the answer.

## Fixed data

- Input: the canonical late equality classes.
- Training window: positions `0..29`, common to E4, W4, and E5.
- Output: the actual visible rank in the selected panel.
- Holdout: every symbol after position 29, including the E4/W4 boundary.

## Family A — synchronized adaptive decks

Maintain a source deck of class IDs and a target deck of visible ranks.

For each input class:

1. find its position in the source deck;
2. emit the target card at that position;
3. update each deck independently with one of:
   `none`, move-to-front, move-to-back, swap-left, swap-right,
   reverse-prefix, reverse-suffix.

Initial source order ranges over all 166 rotations/reflections of `0..82`.
Initial target values range first over the same dihedral family and then over
all affine permutations `a*x+b mod 83`, `a != 0`.

This is a deliberately generous adaptive substitution family. Count every
initialization, update pair, slope, and offset as a separate model.

## Family B — identifiability certificate

Prove directly that an equality signature is invariant under every injective
relabeling of its classes. Therefore a deterministic allocator using only
that signature cannot select the observed numeric labels over any other
injective assignment. A successful allocator needs an independent numeric
primitive: another stream, a fixed deck/key, arithmetic state, or a
reproducible asset-derived tape.

## Promotion gate

Promote only if one frozen adaptive-deck model reproduces all 30 training
positions and then predicts at least one post-common value. Partial
best-fitting models are reported but not interpreted.

