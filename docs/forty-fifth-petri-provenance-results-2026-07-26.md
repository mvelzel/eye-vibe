# Forty-fifth pass — Petri provenance boundary

## Question

Can the Gate Guardian or another post-Eye construction be attributed to Petri
Purho strongly enough to promote its operations as an intended Eye clue?

## What is attributable

The strongest direct statement remains NollaArvi's 27 July 2023 Discord
message: if anything were added concerning the Eye or cauldron mysteries, it
would be Petri's work. This makes Petri authorship a justified search filter
for *later decoding clues*. It does not identify the author of the October
2020 ciphertext or attribute every later secret to Petri.

There is also public evidence that Petri was actively speaking for Noita at
release: the official 15 and 16 October 2020 Steam posts are published under
`petri.purho`. The 15 October notes advertise unspecified new secrets, while
the 29 October notes, published as Nolla Games, add “a new (WIP) challenge.”
Neither post names the Eye Messages or Gate Guardian.

Sources:

- [Noita October 2020 Steam posts](https://store.steampowered.com/news/posts/?appids=881100&enddate=1608660048&feed=steam_community_announcements)
- [Petri Purho's public GitHub profile](https://github.com/gummikana)
- [Petri's Kloonigames archive](https://www.kloonigames.com/blog/about)

## What the public data history can establish

The `vexx32/noita-data` history is a game-data mirror. Gate files are already
present in its first 9 February 2021 snapshot:

- `entities/buildings/wizardcave_gate.xml`
- `scripts/buildings/wizardcave_gate.lua`
- `entities/animals/boss_gate/*`
- `particles/image_emitters/wizardcave_gate_ornaments.png`

The history records subsequent Gate changes through 19 March 2021. Every
relevant commit is authored by mirror maintainer Jens Palmqvist. This dates
mirror observations; it does not expose Nolla's internal commits or individual
asset authors.

The snapshot does preserve explicitly named experimental files such as
`snowcave_petri.lua`, `wand_petri.lua`, and
`coalmine_petri_experiment.png`. Those files also enter through the mirror's
initial commit. Their names show that explicit Petri labels sometimes survived
into shipped data, but they cannot turn the mirror author into the original
author. No Gate filename, comment, or source string names Petri, Arvi, or
another Nolla developer.

Repository:
[vexx32/noita-data](https://github.com/vexx32/noita-data).

## Executable content

The raw Gate scripts implement:

- three eggs to activate the encounter;
- four boss entities;
- simple spawn delays and physical repulsion;
- reward seeds with offsets `0..3` and base `10 + parallel_world`;
- no operation over the Eye arrays and no `5`, `9`, `83`, or `101` interface.

This does not invalidate geometric information authored into the sprites. It
does mean that Petri provenance cannot presently select the dossier's proposed
masks, record types, allocator, or arithmetic from the raw code.

## Public construction habits

Petri's public repositories, gists, and Kloonigames archive contain many small
game, board-game, card, and procedural experiments. They establish an interest
in compact rule systems, not a characteristic cipher construction. No public
Eye/Gate source, precomputed 83-symbol table, or reusable cryptographic
implementation was found. Theme-level resemblance is not a decoder key.

## Decision

Petri-specific archaeology was a valid lead and is now bounded:

1. NollaArvi's statement supports Petri as the first author to investigate for
   intended *later* Eye/cauldron clues.
2. Public Steam authorship places Petri at the 1.0 release but does not
   attribute the ciphertext.
3. The public data mirror cannot attribute the Gate Guardian to any Nolla
   developer.
4. No Petri-attributed fixed operation exists to test prospectively on a
   held-out Eye quantity.

The Gate theory is not rejected. Its provenance promotion gate remains unmet.
Reopen this branch only with an internal-author statement, source-history
artifact, or a fixed Gate operation that predicts an unseen Eye value.
