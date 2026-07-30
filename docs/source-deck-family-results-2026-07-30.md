# Source-selected alphabet/deck screen — 2026-07-30

## Question

Could a developer-sized initial 83-card order, chosen from a real Noita or
ordinary alphabet source, make a small adaptive deck operation preserve the
Eye's registered repeated passages?  This is a finite mechanism screen, not a
plaintext search.  The source order is fixed before looking at Eye output and
no candidate is fitted to it.

## Frozen candidate family

`scripts/screen_source_deck_families.py` constructs 21 distinct orders:

- identity/reverse ASCII+32 (`0..82`);
- first-occurrence keyed ASCII orders for `BDMAGICK`, `A BAD MAGIC CARD
  TRICK`, `MAGICK`, `NOITA`, `EYES`, the two in-game eye strings, `FI358`,
  `FINNISH`, `FIBONACCI`, and `KANTELE`;
- stable ASCII category orders (case, digits, punctuation);
- first-83-element periodic-table orders by element name and name length;
- first-occurrence letters from the Finnish Orb lore, English Wall Messages,
  and the installed `common.csv` translation table.

The runic font's actual `QuadChar` source order is the sequential Unicode
order; it therefore duplicates the identity ASCII-prefix order and is not
counted as a separate permutation.  Every order is checked to be a complete
permutation of 83 cards.

Each order is tested under 14 nontrivial, fully specified reversible updates:
move-to-front/back, swap-with-front, reverse-prefix, rotate-to-front, and
transpose distances `1,2,3,4,5,8,13,21,41`.  Both interpretations are run:
the Eye values are emitted card labels, or they are rank instructions whose
updated card labels are emitted.  A planted rank stream is replayed exactly
through every candidate before any Eye stream is scored.

## Frozen tests

The seven registered nonliteral contexts in `CONTEXT_SPECS[6:]` are compared
after decoding.  The first six are the training count; `last-east3` is held
out.  A context passes when its equality signature matches the canonical
signature; literal equality is reported separately.  The marker-inclusive
coordinates used by the repository are retained.

The screen covers 588 dynamic combinations (`21 × 14 × 2`).  No dynamic
combination preserves all seven equality signatures.  The best result (obtained
by every initial order under swap-with-front in rank-instruction direction) is:

```text
training isomorphs   5/6
held-out isomorph     1/1
literal re-syncs      0/6 + 0/1
```

Its one training failure is `first-cross-late`; it is therefore not a complete
replay.  The best result for every other operation is at most two of the six
training contexts (and no held-out context), except the label/rank swap-
with-front cases.  No candidate has a full literal E4/E5 re-sync either.

The static identity operation is intentionally shown as a control: all seven
equality signatures survive because any fixed relabeling preserves equality.
That tautology is not a cipher result and supplies no plaintext.

## Interpretation

This closes the named BDMAGICK/trailer, runic/Unicode, ASCII, periodic-table,
Noita lore/book, and translation-table initial orders for this small dynamic
deck family.  It does **not** reject an arbitrary `S83` state machine, a
different source-selected operation, or a hidden initial state.  Such a model
needs a complete transition rule and must first pass an exact planted replay,
then all seven contexts including the withheld one.  The source orders and
the operation screen are reproducible with:

```text
PYTHONPATH=src python scripts/screen_source_deck_families.py
```
