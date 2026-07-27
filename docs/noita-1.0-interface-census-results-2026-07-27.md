# Noita 1.0 interface census: results

**Date:** 27 July 2026  
**Freeze:** [`noita-1.0-interface-census-freeze-2026-07-27.md`](noita-1.0-interface-census-freeze-2026-07-27.md)

## Provenance and limit

The public
[Noita Wayback Machine](https://github.com/acidflow-noita/noita-wayback-machine)
lists manifest `2326595580679356504` at 2020-10-15 16:59:04 UTC on
`main`, followed in its chronology by `5246750520913292821` at
2020-07-27 10:41:37 UTC on `fix_20200727`. A second public manifest
[history](https://git.ignore.pl/noita-data-builder/tree/manifests)
independently lists the 1.0 manifest and timestamp.

The Discord report says the former contains all 284 current Eye constants and
the latter none, and reports a WAK delta of 1,402 additions, 145 removals, and
980 changes. Those payload-level results were not reproduced here. The
official DepotDownloader 3.4.0 connected anonymously but correctly reported
that paid depot 881101 was unavailable. Historical download requires an
entitled Steam login; no credentials or Steam session data were inspected.

The audit below therefore concerns current implementations of the report's
retrospectively named candidates. The installed WAK parsed successfully with
14,745 entries. It does not establish that the current bytes equal the 1.0
bytes.

## Candidate results

### Buried Eye

The current mechanism has one binary input: a material-area check for
Teleportatium or Unstable Teleportatium. Success enables a teleporter to fixed
coordinates and, after player use, sets `secret_buried_eye`. The return portal
only retrieves the stored entrance coordinates.

This is a binary secret/teleporter interface. It has no five-direction,
nine-panel, or 83-label alphabet and supplies no operation on an Eye tape.

### Six cave-eye images

The six named PNGs are all `9x5` terrain stamps, but the implementation does
not expose them as six symbols:

- `forest.xml` and `hills2.xml` reference only fixed `eye.png`, with zero to
  three placements;
- `hills.xml` requests exactly three random stamps using
  `eye_0$[1-4].png`;
- no current WAK file references `eye_05.png`.

Thus the apparent six-member set is actually one fixed stamp, a four-choice
random terrain family, and one unreferenced file. It is not five Eye
directions plus a neutral state, and there is no player-readable sequence.

### Rune font and runestones

`font_pixel_runes.xml` is currently a loose font asset rather than a WAK
entry. It defines 240 ordinary character IDs, and `noita.exe` names the XML.
It is a renderer font, not an authored `83 -> character` Eye map.

The six runestone scripts named in the 1.0 report are independent on/off
world effects: projectile replacement, lava emission, projectile deletion,
or slowing. No script consumes an ordered runestone sequence or maps their
effects to Eye directions. A six-item count alone cannot supply the missing
mapping.

### Alchemist key and music

`key_music.lua` polls four tagged music machines. Each newly completed flag
increments a counter; the order is neither recorded nor tested. The resulting
state is merely completion count `0..4`, with a final transition at four.
This cannot consume or order an Eye message.

The separate five-note Kantele interface had already passed a stronger direct
test: no complete Eye row matches any executable song under any real
factoradic header route, and 85 of 120 matched relabeling controls score at
least as high. See
[`fifty-sixth-kantele-header-results-2026-07-26.md`](fifty-sixth-kantele-header-results-2026-07-26.md).

### Mountain-tree pillars

The current tree script treats `secret_buried_eye -> secretbe` as one
independent achievement entry in a much larger persistent-flag ledger. It
draws that flag's fixed pillar tile if present. It does not transform the
Buried Eye input, cave stamps, or Eye Message data.

## Decision

None of the report's named contemporaneous candidates survives the frozen
interface rule. The shortlist contains ordinary secrets, terrain decoration,
a font skin, independent world effects, an unordered completion counter, and
an achievement display. None yields even the first required object: a
complete asset-derived mapping that can make a predeclared Eye prediction.

This is a negative audit of the named shortlist, not of all 1,402 reported
additions. Reopen the broader build lane only with the two entitled historical
payloads or a complete added/changed path list. Do not mine numerical constants
from these named assets or combine their partial resemblances.
