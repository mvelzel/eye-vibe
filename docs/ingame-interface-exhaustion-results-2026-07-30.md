# In-game interface exhaustion — 2026-07-30

## Scope and rule

This audit asks whether an ordinary player-facing or developer-facing Noita
interface supplies a source-selected ordering, 83/101 table, or state machine
that could explain the Eye corpus's canonical trigram isomorphs.  It is an
isolated screen: no partial match is combined with another theory.  A proposed
deck order had to be determined from the shipped source before looking at Eye
output; every dynamic transition had to replay a planted rank stream exactly;
the Eye score used six registered training contexts and one withheld context.

The reproducible screen is [`scripts/audit_ingame_interfaces.py`](../scripts/audit_ingame_interfaces.py).
It parsed the installed `data.wak` (14,745 entries), the loose runic font, and
`data/translations/common.csv`.  It constructed 31 deduplicated orders from:

- 469 material declarations (`CellData`/`CellDataChild`);
- 491 action IDs in `gun_actions.lua`;
- 147 unique persistent/run flags;
- 201 magic-number names;
- 308 debug keycode names;
- 3,630 unique translation keys;
- WAK path families for books (46 paths), music/kantele/ocarina/runes (131),
  and intro assets (53);
- runic-font glyph widths and atlas positions (240 glyphs, first 83 used).

For each source, source order, lexical order, length order, and reversals were
tested where at least 83 entries existed.  Fourteen small reversible
move/swap/rotate/reverse/transpose transitions were tested in both label-decode
and rank-instruction directions: 31 × 14 × 2 = 868 dynamic rows.

## Result

No candidate preserved all seven registered equality signatures.  The best
dynamic result is:

```text
training isomorphs  5/6
held-out isomorph   1/1
literal re-syncs    0/6 + 0/1
```

This is the same rank-instruction `swap-front` artifact seen in the earlier
source-deck screen and occurs for many unrelated source orders; it therefore
does not identify an alphabet or mechanism.  There are no exact full-context
rows.  The omitted identity operation is a deliberate tautology: a fixed
relabeling preserves equality signatures but supplies no decoding information.

As a residual font check, [`scripts/audit_rune_font_windows.py`](../scripts/audit_rune_font_windows.py)
also screened every contiguous 83-glyph window of the full 240-glyph runic
atlas, six stored metrics (`id`, width, atlas-x, offsets, height), both
orientations, and the same 14 dynamic families in both directions.  This is
318 deduplicated decks and 8,904 calibrated rows.  It has the same non-specific
best `(5,1,0,0)` rank-instruction `swap-front` artifact and zero exact rows.

## Direct interface census

### Cessation, Void Liquid, and material reactions

`data/biome_impl/static_tile/puzzle_logic_barren.lua` is the complete shipped
Cessation trigger.  A successful material-area check creates the `CESSATION`
card, sets `card_unlocked_cessation`, converts a rectangular temple-slab area
to holy grass, and plays sounds.  No cauldron, calendar, or cycle code is in
the current WAK.

`data/materials.xml` contains 468 cell declarations.  `void_liquid` is the
156th declaration (zero-based index 156), a child of `water`, not an 83- or
101-entry table.  There are 330 material reaction records; only three mention
`void_liquid`: the radioactive-liquid/fungus creation and two inert-preserving
reactions.  No reaction records a sequence, day, panel, direction, or Eye data.
The release executable likewise contains `POLYMORPH_CESSATION` symbols but no
`cauldron`, `calendar`, or `void_liquid` string.  This cannot rule out an
obfuscated or historical implementation, but it rules out a plainly named
current interface.
The Cessation/cauldron lead therefore remains a separate historical or engine
provenance question, not a current Lua decoder interface.

### Music, instruments, and the Alchemist key

`kantele.lua` and `ocarina.lua` each implement four hard-coded songs.  Notes are
matched left-to-right; one mismatch clears the current song; completion fires
one of four effects and sets a per-instrument secret flag.  There is no shared
song order, permutation, numeric output, or read of Eye arrays.  The separate
`music_machine_00.lua` … `_03.lua` files each play an indexed sound and set
`musicmachine1` … `musicmachine4`; `key_music.lua` only increments an Alchemist
key status from 0 to 1 to 2.  These are independent counters, not a cipher
state machine.

The five-note Kantele route was already screened against executable songs and
the real factoradic headers; this audit finds no additional music interface.

### Runestones, altars, and orb rooms

The seven runestone scripts call `runestone_activate`, which only toggles a
per-entity `active` integer between 0 and 1 and enables/disables tagged
components.  They do not consume a sequence.  Moon/dark-moon altars test a
fixed conjunction of four essence flags (`fire`, `air`, `water`, `laser`) and
emit fixed effects.  Their extra route creates six fixed touch-material cards
in spatial order; neither route references Eye values.

The shared `orb_list` is an 11-pair coordinate list.  `orb_map_update` merely
serializes those pairs to `ORB_MAP_STRING`; orb rooms 00–11 load corresponding
orb/book assets.  It has no checksum, alphabet, or state derived from player
actions.  The altar-tablet script tracks independent persistent flags and a
tablet count; the mountain-tree pillar display groups 76 flag labels into six
visual rows.  Neither is an 83-card source or an Eye consumer.

### Debug and intro interfaces

`data/debug_keys.txt` and `_debug/debug_menu.lua` expose editor controls only:
spawn perks/events, teleport, material tests, fungal-shift conversions, and a
button that spawns the 12 emerald-tablet books.  No Eye, glyph, message, or
decoder action exists in this menu.  The 20 intro constellation XMLs each
select a static PNG animation (`00_00` through `03_03`, plus logos); no runtime
data or ordering is computed from them.

### Residual eye/rune/symbol assets and lore payloads

The path-name sweep also covered every shipped `eye`, `rune`, `symbol`, `wall`,
`secret`, and `text` asset.  The six 9×5 `biome_impl/caves/eye*.png` files are
grayscale eye-appearance variants referenced only by the forest/hills biome
templates; `eyespot_a`–`e` merely select the five `$item_book_s_*` scrolls when
the player has the tripping effect.  The eight `gatesymbol_*.png` files are
random particle sprites emitted by `keyshot.xml`, while `buildings_gfx/runes`
is an unused, commented-out biome spawn.  Neither family carries a table or
state transition.

`orb_plan.txt` and the hidden/trailer mountain-text PNGs are static lore.  The
orb text has fixed room labels, quotations, and reward comments; the six eye
variants, 12 orb books, and all text images are never consumed by a decoder.
This closes the residual named-asset route without treating visual similarity
as evidence.

The remaining date-sensitive hooks are ordinary seasonal Easter eggs:
Christmas Santa/drunk spawns, Halloween pumpkins, Finnish Jussi/Mammi/sima
items, and New Year props.  They return booleans or select fixed entities and
do not read Eye values or maintain an ordered state.

## Boundary and remaining live leads

This closes the ordinary shipped Lua/XML interfaces listed above for the
screened developer-sized family.  It does **not** close:

1. the historical cauldron calendar payload or an entitled pre-release depot;
2. an arbitrary offline authoring transform not shipped in the current WAK;
3. a complete, independently specified `S_83` transition outside the tested
   small deck family;
4. a native engine routine not reached by the renderer call-site audit.

Those are the only remaining in-game/engine directions after this census; no
current player-facing interface supplies an identified 83/101 key or a
complete Eye decoder.
