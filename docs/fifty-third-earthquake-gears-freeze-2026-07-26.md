# Earthquake-gear Wadsworth audit — freeze

## Why this branch is executable

The existing Earthquake-circle horizon left physical wheel timing open.
Read-only Discord archaeology recovered Lymm's concrete version rather than a
generic resemblance:

- [23 December 2024](https://discord.com/channels/453998283174576133/1063583558154854521/1320773804779241594):
  two wheels with three Earthquake gears, producing isomorphs, no doubles, and
  the same value distribution;
- [30 July 2025](https://discord.com/channels/453998283174576133/1063583558154854521/1400196919162310766):
  the complete modified Wheatstone/Wadsworth operation;
- [gear sizes](https://discord.com/channels/453998283174576133/1063583558154854521/1399944903588315220):
  `17`, `20`, and `24` teeth, all advancing at the same tooth rate;
- [outer gear](https://discord.com/channels/453998283174576133/1063583558154854521/1400227647015096541):
  every outer eye is open, preventing the three gears from all disengaging.

Lymm also [clarified in January 2024](https://discord.com/channels/453998283174576133/817530812454010910/1199191007913320458)
that the cipher does not depend on the sprite's spacing/rounding defects. It
uses the ring contents, especially the extra tooth that breaks the inner
four-step repetition. This matters because a contemporary claim that the
visual spacing was a graphics-package rounding error does not invalidate the
actual mechanism.

## Reconstructed machine

The fixed tapes, at an arbitrary starting phase, are:

```text
outer 24       111111111111111111111111
middle 20      10101010101010101010
inner 17       11110111011101110
```

The plaintext and ciphertext disks have arbitrary symbol orders and initial
states. To encrypt the next plaintext symbol:

1. rotate positively to it on the plaintext disk;
2. use a full lap rather than distance zero when the symbol repeats;
3. for every unit plaintext step, advance all three tapes by one tooth;
4. add a fixed weight to the ciphertext rotation for every currently open
   tape;
5. output the ciphertext symbol at the landed-on position.

With weights `(w24,w20,w17)`, phase `p`, and plaintext distance `d`, the
ciphertext increment is

```text
d*w24 + open20(p,d)*w20 + open17(p,d)*w17  mod 83.
```

The visible tape output has period `lcm(2,17)=34`; the nominal 24-tooth gear
is constant. Before/after-step timing is absorbed by the free phase. Reversing
the irregular tape is the only nontrivial direction ambiguity.

## Community diagnostics preserved

Two later Lymm attachments were acquired read-only:

| message | attachment | dimensions | SHA-256 |
|---|---|---:|---|
| [14 Nov 2025](https://discord.com/channels/453998283174576133/817530812454010910/1438675110893457571) | `gear-cipher-imperfection-2.png` | `833×547` | `436c6a4a40b997f1e0a3cc81c672903eebccd7fde39d197eb7981f34053e72b0` |
| [19 Nov 2025](https://discord.com/channels/453998283174576133/817530812454010910/1440825900240338994) | `image.png` | `1401×745` | `40dd60ce875e6f6c990c106278c74a1df4febf7fcb82b5f350c2d128f298712d` |

The first plots sampled isomorph-imperfection scores by sequence length and
repeat count. The second shows a quick generated-text isomorph test
(`219` patterns, `905` instances in the displayed run). Lymm's accompanying
assessment was negative: the mechanism produces many isomorphs, but a given
pattern recurs substantially less often than in the Eyes. These are useful
calibration and provenance, not raw data for a new probability claim.

## Frozen tests

### A. Equal-weight arithmetic-progression disk

Use the visible trigram ranks as ciphertext coordinates up to one global
nonzero affine scale. Translation cancels in deltas. Test both tape directions,
all `82` scales, and plaintext alphabet sizes `26` and `29`. Give every
context occurrence an independent initial phase and every transition any
distance `1..m`.

### B. Every fixed weight on that disk

Normalize the always-open weight to one; this is lossless because `83` is
prime and the outer weight is nonzero. Exhaust every

```text
(scale, w20/w24, w17/w24) in (1..82) × Z83 × Z83.
```

For an especially permissive necessary condition, give *each transition*
fresh independent source/target phases and a fresh common plaintext distance.
Intersect compatible parameter triples in corpus order. Empty intersection
rejects the real continuous machine for this whole disk-order family.

### C. Arbitrary hidden ciphertext disk

Respect Lymm's original allowance for any permutation of the 83 ciphertext
symbols. For equal weights, first drop phase continuity but require both
occurrences of every aligned transition to use increments available at one
common plaintext distance. Keep all 71 observed labels at distinct hidden
coordinates. For `m=26` this admits 159 increment pairs; for `m=29`, 181.

Run independent linear-integer and seven-bit encodings, with positive planted
controls. A solver timeout is recorded as unknown, never as rejection.

## Promotion and stop rules

- A visible/arithmetic-progression model must survive the necessary weight
  intersection before any language work.
- A hidden-disk SAT result is compatibility only; it still needs a
  decoder-independent disk order and exact phase-continuous replay.
- An UNSAT hidden relaxation would reject the equal-weight original despite
  its deliberately excessive freedom.
- Do not fit an arbitrary ciphertext permutation and then call it an in-game
  key. The disk order must come from independent evidence.
