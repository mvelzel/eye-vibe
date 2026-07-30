# Wider second tranche — results (2026-07-30)

This tranche opened three independent lanes: native executable archaeology,
small reversible dynamic-deck models, and the install layers omitted by a
`data.wak`-only census. No lane was allowed to combine partial matches with a
different clue theory.

## Native executable and renderer path

The installed executable is SHA-256
`808d2a0ab51ea0b46e9ad2aeb3327a4b0ce3feae04f32ba26326bf585b5779bd`.
The static initializer at VA `0x61ed60` contains the complete packed corpus:
150/150 low halves, 146/146 nonzero high halves, and four zero-high words. Its
only direct callsite passes `x`, `y`, and panel `0..8`; the side-parity filter
routes East versus West. No key, state, or message argument is supplied.

Disassembly of the post-constant loop shows generic division by seven,
base-seven digit extraction, temporary-string construction, and the ordinary
renderer call. It does not contain a decryptor or a cipher-state update.

Relevant PE strings are limited to `ThreeEyesAreWatchingYou`,
`SecretsOfTheAllSeeing`, and `data/particles/eye.xml`; they sit beside stats
and achievement identifiers. Exhaustive aligned permutation scans found no
contiguous `0..82`, `0..100`, or `0..124` sequence as raw bytes or little-/
big-endian 16/32-bit integers.

**Result:** this materially strengthens the “offline-authored ciphertext,
runtime renderer only” boundary. It does not prove that no information was
hidden in an authoring tool or an unrecovered build, but it closes the current
binary as a source of a direct Eye key/table.

## Dynamic deck / Holdswap family

The public Holdswap proposal was formalized into small reversible fixtures:

- a deck permutation `D`;
- a per-plaintext hold-card array `H` or fixed partner rule;
- output sampled before or after the swap;
- optional whole-deck rotation by `0,+1,-1`;
- identity/reverse initial decks and a few affine/reverse hold arrays.

Every implementation first passed a planted replay. It was then tested against
the seven nonliteral isomorph contexts and the E4/E5 shared body. The result is
sharp:

- fixed-partner swaps preserve all contexts only for the identity/no-op rule;
  nontrivial partners preserve at most 5/7 and fail the deeper E4/E5 latent
  equality check;
- output-after per-plaintext hold-card emission collapses to a static
  substitution (or a tautological equality replay), not a dynamic cipher;
- output-before nontrivial hold arrays preserve at most 1/7 contexts, while
  the identity/reverse array is again just a static/no-op mapping.

This is not a rejection of arbitrary `S83` Holdswap designs: the public idea
still leaves initial state, swap timing, and the exact hold-box transition
underspecified. It is a rejection of the smallest complete interpretations,
and gives the next implementation a concrete target: any full model must
avoid collapsing to static substitution while preserving the withheld
isomorph/equality constraints.

## Install layers outside `data.wak`

The installed game also contains 25 font files, official translation tables,
159 generated schemas, 25 FMOD banks (~1.28 GB), and `mods/translation_fi`.
These were audited directly.

- `mods/translation_fi/README.txt` explicitly calls the mod an example,
  work-in-progress Finnish translation. It contains ordinary book/lore rows,
  including *Secretorum Hermetis*, but no Eye-message, cipher, 83, or 101
  material. The Finnish strings are visibly mixed-language machine-quality
  translations, not a canonical developer source.
- `statusdesc_rainbow_farts` is ordinary four-line flavor text (“Open your
  eyes, I see …”), with no direction/rank/checksum structure.
- `font_pixel_runes.png/xml` is a generic sequential Unicode atlas used by the
  shipped example mod; it has no Eye-specific mapping or 83-entry table.
- FMOD strings contain ordinary rune, eye, orb, Kantele, and Ocarina events,
  but no cipher/message/glyph/checksum event.
- Schemas expose normal `eye_offset`, Book, Orb, and SymbolTextLog components,
  not a hidden Eye data structure.
- Four generic 83-entry `gun_names` lists are ordinary random wand adjectives;
  they already exist in the first 2021 public data commit and have no Eye
  context.

The apparent `gatesymbol_1..8` clue is also closed: each 9×9 sprite is used by
`keyshot.xml` as a cosmetic projectile particle, with no Eye or decoder caller.
The 2021 history places these assets together with the Alchemist and cave-eye
assets, establishing chronology but not intent.

## Fresh public ideas screened

The new punch-card/absence and stereogram discussion does not yet specify a
deterministic projection, grid origin, or decode rule. The reported odd/even
column alternation is consistent with the renderer’s alternating row offsets,
so it is not currently an independent cipher consequence. Conway/falling-sand
suggestions likewise lack a specified embedding or rule and cannot be tested
without introducing arbitrary choices. They remain unpromoted idea seeds,
not evidence.

## Bottom line

This tranche increased coverage substantially but produced no decoder or
plaintext. It closes the remaining obvious current-install source/key surfaces
and the smallest dynamic Holdswap models. The technically live frontier is
now narrower: a fully specified, nontrivial `S83`-scale state machine or an
independently authored external ordering/operation that predicts an unseen
Eye consequence.
