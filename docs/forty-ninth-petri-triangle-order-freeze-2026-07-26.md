# Forty-ninth pass — Petri triangle-order provenance freeze

## Motivation

Petri Purho's public `CardBackGenerator` repository contains a staggered
alternating-triangle renderer committed on 15 June 2015, more than five years
before the Eye Messages:

<https://github.com/gummikana/CardBackGenerator/blob/02f7bf1252ae0e3702ec9c15f052fc3310239ba4/Source/procedural_triangles.cpp#L108-L205>

This is relevant only because NollaArvi directly attributed the Eye secret to
Petri. A triangular renderer by the Eye author can corroborate a construction
habit, but visual resemblance cannot select a decoder.

## Frozen question

Test one narrow, language-free claim:

> Does one global symmetry of the triangular plane carry Petri's authored
> vertex order into the accepted Eye trigram order for both triangle
> orientations?

The comparison uses only source order and the already accepted Eye
interleave. It does not score plaintext, marker arithmetic, or any later
Noita asset.

### Petri source order

After multiplying coordinates by two, `TrianglesLine()` inserts:

```text
up:   bottom-left, top, bottom-right = (0,2), (1,0), (2,2)
down: top-left, bottom, top-right    = (1,0), (2,2), (3,0)
```

### Accepted Eye order

For consecutive digits `a..f`, the accepted reconstruction is:

```text
top:    a b f
bottom:  c e d
```

Placing the staggered rows at consecutive lattice positions gives:

```text
down: a,b,c = top-left, top-right, bottom = (0,0), (2,0), (1,2)
up:   d,e,f = bottom-right, bottom-left, top = (5,2), (3,2), (4,0)
```

## Exact acceptance rule

For each ordered triple, compute the sign of twice its oriented area.
Every global rotation preserves both signs and every global reflection
reverses both signs. Cyclically choosing another starting vertex does not
change a sign.

Accept the provenance claim only if either the orientation-preserving or the
orientation-reversing case matches both triangle orientations, allowing both
possible pairings of source up/down with Eye up/down.

This is a necessary condition, not a sufficient proof of common construction.
Failure rejects only literal transfer of the authored vertex order. It does
not reject the shared alternating-triangle topology or a later, separately
chosen Eye reading convention.

## Result

The exact winding signatures are:

```text
Petri source: up +1, down -1
accepted Eye: up +1, down +1
```

There are zero matches under both same-orientation and swapped-orientation
pairings, for determinant signs `+1` and `-1`.

Petri's code alternates the winding of its inserted polygon vertices; the Eye
reading keeps one winding across the two orientations. No single global
rotation or reflection can transfer the source order. This remains true if a
common or independent cyclic starting-vertex change is allowed, because
cyclic changes preserve winding.

The source therefore corroborates only a pre-existing Petri habit of building
staggered alternating-triangle fields. It neither derives the orthodox Eye
trigram order nor supplies a body transform. The source order was written for
drawing polygons, so even a positive match would have been weak provenance
rather than a decoder.

Server-wide Discord searches for `CardBackGenerator`, `gummikana`, and
`procedural_triangles` returned no results. That suggests this exact source
comparison has not been preserved in the server discussion, but it is not
proof that nobody previously considered it elsewhere.

## Bounded pre-Eye source census

The other exact, authored mechanisms in the public pre-2020 repository sample
do not yet expose an Eye interface:

- `NoMoreMeat` defines four packet operations: Select, Shuffle, Mystery, and
  Backwards. Its packets have player-dependent size, and nothing selects a
  mapping from these four operations to an Eye header or control class.
- `qr_test` detects symmetric five-run QR markers by requiring outer run
  pairs to match and the center run to be wider. It removes and replaces QR
  corners; it does not implement a text cipher or usable Eye permutation.
- `GameOf20`, `NoMoreMoney`, its Monte Carlo simulator, the Cold War card
  prototype, and the combinatorial abstract game expose ordinary game/deck
  operations but no fixed 83-state, five-direction, or nine-message
  mechanism.
- Exact `83` text hits in the two larger source trees are third-party image
  compression tables, font metrics, or ASCII labels, not Petri-authored
  state sizes.

The four `NoMoreMeat` operations remain a low-priority construction vocabulary
only. Testing all assignments against the Eyes would fit an arbitrary model
after seeing the target, so no search is authorized without a new fixed
packet-to-header correspondence.

## Decision

Close literal transfer of Petri's 2015 triangle vertex order. Preserve the
alternating-triangle topology as independent author provenance, not as new
cryptographic evidence. Reopen Petri archaeology only for a mechanism with a
fixed Eye-facing interface or a held-out prediction.
