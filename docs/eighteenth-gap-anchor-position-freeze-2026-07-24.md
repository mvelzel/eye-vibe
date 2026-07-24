# Gap-anchor position/permutation follow-up — freeze

## Seen observation

The promoted clean gap-11 anchors occur after the copied opening at positions:

```text
E4,W4,E5 = 16,18,17 = 16 + (0,2,1)
```

The final marker control edges are:

```text
E4  0->0  identity order 012
W4  0->2  component order 021
E5  1->0  component order 102
```

Thus the position-rank permutation is exactly the W4 header's independently
defined component order `021`. This was noticed after the positions were
printed, so it needs a new full selection correction.

## Frozen matched controls

Run 50,000 new independently seeded controls (`0x18c05`). Shuffle each final
post-opening body while preserving exact length, symbol multiset, and no
adjacent doubles.

Report:

1. number with one clean gap-11 anchor per message;
2. number whose three gap-11 positions are exactly one translated `021`;
3. number that also satisfy the exact reported numeric formula;
4. a broad joint count.

For the broad count, allow every gap `2..30`. At a gap with exactly one clean
anchor per message, require:

- the fully broadened numeric header-difference match, allowing every anchor
  order and ignoring edge assignment;
- three distinct consecutive positions;
- their rank permutation to be any one of the three final marker orders
  `{012,021,102}`.

Every control reselects the gap. Use plus-one corrected tails.

## Gate

Promote the position permutation as another authored part of the same
final-row record only if the broad joint corrected tail is below `.01`.
Because it uses the same anchors and headers as the prior result, do not
multiply its tail with any earlier tail.

A positive result would suggest that marker control orders select not just an
arithmetic relation but the relative placement/read order of the body
landmarks. It would still not identify plaintext.
