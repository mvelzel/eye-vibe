# Gate Guardian cyclical-sieve theory: ground-up audit

**Status:** Interesting later clue, not a decoder.  Several direct observations
survive independent reconstruction, but the claimed Type4/Type6 execution still
depends on unpublished masks, scope assignments, and a missing fresh-value
allocator.  No Eye plaintext or held-out value has been recovered.

The 26 KB Discord dossier `eye_messages_focused_state_dossier_2026-07-21.md`
was read in full, together with the surrounding discussion.  It is used here
only to generate falsifiable questions.  Measurements below start from the
installed game data and the canonical Eye corpus.

## Raw Gate construction

The relevant installed data are fully externalized.  The dormant gate is
controlled by:

```text
entities/buildings/wizardcave_gate.xml
scripts/buildings/wizardcave_gate.lua
entities/buildings/wizardcave_gate_monster_spawner.xml
particles/image_emitters/wizardcave_gate_ornaments.png
```

and the awakened parts by fourteen PNG/XML/Lua files under
`entities/animals/boss_gate/`.  The Lua code has one explicit activation rule:
consume three unheld entities tagged `egg_item`.  The surface artwork is known
to hint this rule, so deliberate pictography in the asset is an established
fact rather than speculation.

The egg reading can also be checked without relying on the wiki or Discord.
The dormant `wizardcave_gate_ornaments.png` openly draws an egg-shaped circle
with a jagged break through it, while the shipped opening sequence contains a
different red line-art progression from whole egg to broken shell and emerging
triangle.  The concepts match, but the pixels and composition do not.  This is
good evidence that the Gate art communicates its three-egg awakening rule; it
is not evidence that an exact intro-frame mask or numeric key was copied into
Veska.

The four static sprites tile naturally using only their dimensions and aligned
bottom edges:

```text
Seula                   57×55 at (34, 0)
Molari                  37×71 at ( 0,50)
Veska                   52×66 at (37,55)
Mokke                   37×71 at (89,50)
assembled extent       126×121
```

This reconstructs the dormant triangle: Seula is the top, Molari and Mokke are
the left and right wings, and Veska is the center.  The derived assembly is
[`assembled-static.png`](../artifacts/gate-guardian/assembled-static.png).

The executable awakening order is also explicit and differs from an inferred
functional arrow.  The spawner schedules:

```text
frame 220  Veska   at (  0,  0)
frame 225  Molari  at (-52, -8)
frame 230  Mokke   at ( 52, -8)
frame 235  Seula   at ( -8,-60)
```

On death the same A/B/C/D order becomes random-card seed offsets `0,1,2,3`.
The only runtime interaction among living parts is mutual physical repulsion.
There is no Lua/XML operand routing, cache, sieve, Type4/Type6 dispatch, or Eye
lookup.  Current `noita.exe` and `noita_dev.exe` strings contain the four
`gate_monster_*` identifiers only inside the ordinary enemy/progress registry;
the gate-specific behavior lives in the files above.  Decompiling the generic
physics/entity engine would not recover a hidden Gate operation absent from
those data-driven definitions.

## Direct Eye facts reproduced

Complete-message sums modulo 101 in canonical physical row-major order are:

```text
        E1  W1  E2       0  84   7
        W2  E3  W3  ->  53   0   1
        E4  W4  E5      32  88   0
```

The three odd-East checksums occupy the main diagonal and are zero.  Circular
off-diagonal magnitudes under the four ordinary reflection axes are:

| Axis | Magnitudes | Total |
|---|---|---:|
| main diagonal | `31,25,14` | **70** |
| anti-diagonal | `0,18,35` | 53 |
| horizontal | `32,4,7` | 43 |
| vertical | `7,49,32` | 88 |

For three independent uniform mod-101 pair differences, the exact fixed-axis
probability of total 70 is:

```text
15036 / 101^3 = 0.014593793
```

This independently agrees with the dossier's reported scale.  It is a real,
percent-level fit, not a decoder and not an independent probability that may
be multiplied into discoveries made from the same corpus.

A later breadth-first prefix-trie test finds another Eye-derived 70: after the
lower six bodies' shared five-symbol prefix, their distinct descendant edges
sum to 70 modulo 101.  This is a concrete same-corpus echo of the mirror total,
but it is not Gate-asset corroboration and was noticed after the target 70 was
known.  It does not supply the missing Seula sprite mask described below.

The dossier's three Q-C edges are also literal adjacent transitions:

```text
east4 index54  68->69 = 233_5->234_5
west4 index51  23->24 = 043_5->044_5
east5 index55  30->31 = 110_5->111_5
```

They preserve the first two eyes and increment the third without carry.  The
whole corpus contains seven such adjacent edges, so the direct observation is
“three grammar-selected edges out of seven,” not “the only three successors.”
The claimed Monte Carlo significance of the grammar selection cannot be
reproduced from the dossier alone because its complete scope census and label
permutation harness were not attached.

## Sprite claims

### Veska's 72 pixels

Veska does contain exactly 72 opaque pixels of the dedicated color
`(60,57,65,255)`.  The upper and lower pictograms are visually and digitally
plausible:

```text
upper: 9 pixels, 8-neighbour component sizes 1,5,3
lower: 8 pixels, one five-pixel plus and three singletons
```

The complete `12 outer + 43 crack + 9 upper + 8 lower` partition is not yet
objective.  Simple spatial separation of the raw mark layer gives:

```text
11 remainder + 44 middle + 9 upper + 8 lower = 72
```

Reaching `12+43+9+8` requires moving one middle pixel to “outer” under an
additional mask rule.  The dossier does not state that rule.  Consequently the
`9|8=17` split is an attractive reading of two real pictograms, while the
claimed no-leftover four-way partition remains under-specified.

Likewise, `145 OR (1<<3)=153` is arithmetically exact once bit 3 and the input
byte are chosen, but the sprite-to-bit selection is the evidentiary step.  The
dossier says direct use of the Boolean descriptor on raw Eye windows is
negative.

### Seula's “70-pixel residual”

No simple raw-sprite symmetry produces 70.  Seula has a perfectly symmetric
opaque silhouette.  Comparing the two halves gives these mismatch-pair counts
for each individual opaque color:

```text
dark 411, authored-mark 4, midtone 302, light 109
all RGBA values 480, alpha 0
```

Thus “70-pixel residual” requires a further scaffold subtraction, palette
collapse, or mask.  None is defined in the dossier.  Until that residual mask
is published and frozen independently of the target 70, the sprite/checksum
match cannot be reproduced.

### Molari and Mokke

Molari and horizontally mirrored Mokke are both 37×71.  Their opaque
silhouettes differ at exactly one pixel, `(3,69)`, although their internal
colors and glyphs differ extensively.  This is strong direct evidence that
they were authored as a paired visual carrier.  It does not identify an XNOR
selector or the Eye labels `9,17,68,69,72,73` by itself.

The claimed seven-pixel side tape and its 25 repetitions need a path, palette
mapping, start point, and direction.  Those definitions are absent from the
dossier and surrounding Discord post.  Reconstructing them after seeing the
desired labels would not be an independent audit.

## Type6 cache branch

The dossier reports tape `12100220`, pointer magnitudes
`4,2,4,1,1,4,8,4`, four forward and four backward references, an XNOR
source-side selector, and eight exactly reconstructed cached targets.  It also
states the unresolved part plainly:

```text
8 source-cache roles
8 first-seen allocation roles
1 local repeat
```

The local repeat is checkable only after the role table is supplied; the eight
first-seen labels still have no generation rule.  A mechanism that recovers
cached values but cannot choose any new value is a partial structural model,
not a cipher.  The dossier also marks the full interval update
`[68,72)->[69,73)` negative and calls the full Type6 byte provisional.

## Chronology

The early-access data archive contains no `wizardcave_gate` or `gate_monster`
files.  Contemporary community evidence places the awakened boss on Noita's
beta branch by 14–15 December 2020; a 29 January 2021 discussion explicitly
distinguishes the dormant gate in main from the boss in beta.  This is after
the Eye Messages' October 2020 appearance, so the Gate cannot have been needed
to construct the original renderer.  It remains chronologically eligible as a
later decoder hint, exactly as the user noted.

The public Noita data Git history starts in February 2021 and cannot establish
the exact first asset build.  An anonymous Steam request for the 15 October
2020 depot was denied because Noita requires an owning account; no credentials
were requested or handled.  Historical retrieval would sharpen the asset
timeline, but it would not fill the missing masks or fresh allocator.

## Assessment and falsification target

The strongest surviving interpretation is modest: the Gate may deliberately
repeat visual vocabulary useful for thinking about paired scopes, a third-eye
successor operation, and a `9|8`/17-role boundary.  Three things support taking
that seriously: authored paired side panels, genuine activation pictography,
and the exact Q-C successor edges.  The raw game code does **not** execute the
proposed record machine, and several central numerical joins are currently
retrospective and under-specified.

The Gate theory should be promoted only after one frozen, prospective result:

1. publish the exact Seula residual and Veska/side-band masks;
2. reproduce every intermediate value from raw PNGs and canonical Eye data;
3. freeze all orientations, scope roles, selectors, and bit conventions;
4. predict one of the eight first-seen Type6 residues, an unseen Q-C role, or
   a historical asset quantity not used during model discovery.

Anything short of that is useful construction-language evidence, not an Eye
solution.

## Reproduction

Run:

```bash
PYTHONPATH=src python scripts/analyze_gate_guardian.py \
  --assets /path/to/data/entities/animals/boss_gate \
  --data-root /path/to/data \
  --assembly-output artifacts/gate-guardian/assembled-static.png
```

The script reads installed assets only and does not launch or modify Noita.

Public chronology/context sources:

- [Gate Guardian — Noita Wiki](https://noita.wiki.gg/wiki/Gate_Guardian)
- [14 December 2020 beta-branch boss discussion](https://www.reddit.com/r/noita/comments/kd8iot/)
- [15 December 2020 red-triangle investigation](https://www.reddit.com/r/noita/comments/kdbvh4/)
- [29 January 2021 main/beta distinction](https://www.reddit.com/r/noita/comments/l7lbz6/)
