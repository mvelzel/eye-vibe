# Runic-font 83-window screen (2026-07-30)

The installed runic font has 240 authored glyph records. This screen treated
every contiguous 83-glyph window, both orientations, and six source-authored
metrics (ID, width, atlas X, offsets, and height) as possible deterministic
deck orders. It then applied the already-calibrated 14 small reversible deck
transitions in both directions, with planted replay checks before Eye scoring.

Reproducer: scripts/audit_rune_font_windows.py.

Verified result:

    glyphs=240
    unique_decks=318
    dynamic_rows=8904
    best training/held-out/literal = 5/1/0/0

The best row is the same non-specific rank-instruction swap-front artifact
found for unrelated source orders. No candidate preserves all seven registered
equality signatures or any literal re-sync. This closes the finite
font-window/deck family; it does not reject an independently selected
non-window glyph operation or an offline authoring transform.
