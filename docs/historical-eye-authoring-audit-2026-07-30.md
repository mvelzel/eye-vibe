# Historical Eye authoring audit — 2026-07-30

## Scope and provenance

This lane checked the public `vexx32/noita-data` history, the public Noita
Wayback Machine manifest/release-note index, and a dated independent
decompilation of the Eye renderer.  The historical depot payloads themselves
were not downloaded: the public downloader reports that the paid depot needs
an entitled Steam session.

## Independent 2021 binary reconstruction

Xkeeper's public gist was created 28 April 2021 and contains a decompiled
renderer initializer plus a small decoder:
[noita-eyes.php](https://gist.github.com/Xkeeper0/a6eda18571ef889be291822c400cc6c8).
It stores nine branches of 64-bit words as two 32-bit halves.  Its only data
operation is to reverse the words, divide by seven once (the zero padding
digit), read base-seven remainders, subtract one to recover symbols `0..5`,
and reverse the resulting stream.  There is no key, plaintext, state update,
or external input in this routine.

I parsed all 150 word pairs from the gist and compared them with the
repository's independently reconstructed `corpus_packed_words()` output:

```text
word count:       150 == 150
all 150 words:    exact equality
SHA-256 (u64 LE): 5de6ccb3a045218827b7ddaad0f1493254f501b08addd1929495ce060242de94
```

Decoding all nine branches reproduces `storage_stream(name)` byte-for-byte;
the branch stream lengths including row separators are
`305,317,364,314,423,382,367,370,352`.  After removing row-separator symbol
`5`, these are `297,309,354,306,411,372,357,360,342`, exactly the nine
canonical streams.
The public decompilation therefore independently reproduces the same static
ciphertext corpus found in the installed 2025 executable.  This is a strong
historical stability result, but the gist does not identify its exact game
build and is not an authoring source.

## Public data-history chronology

The earliest `vexx32/noita-data` commit (9 February 2021) already contains
the cave-eye terrain stamps, gate symbols, temporary symbol sprites, intro
assets, hidden mountain text, and ordinary book/lore assets.  Their history
does not contain a source-side Eye key or decoder.  The separate
`eyespot_a`–`eyespot_e` entities and `eye_check.lua`/`eyespot_check.lua` first
appear in commit `a1cf190` (22 February 2021).  The patch places five eye
spots at fixed coordinates and, only when the player is tagged
`tripping_extreme`, loads `book_s_a`–`book_s_e`; these scripts toggle particles,
load books, and teleport/secret-check, but never consume the Eye-message
arrays or a direction/rank stream.  This is a later, separate eye-themed
secret, not an Eye cipher mechanism.

The Wayback index exposes a pre-1.0 manifest (27 July 2020) and the 1.0
manifest (15 October 2020).  The corresponding [pre-1.0
notes](https://raw.githubusercontent.com/acidflow-noita/noita-wayback-machine/main/NOITA_BUILDS_RELEASE_NOTES/5246750520913292821/_release_notes.txt)
and [1.0 notes](https://raw.githubusercontent.com/acidflow-noita/noita-wayback-machine/main/NOITA_BUILDS_RELEASE_NOTES/2326595580679356504/_release_notes.txt)
only say `FEATURE: New secrets..`; neither names an Eye message, key, or
decoder.
Without the entitled depot payloads, this establishes chronology only, not a
byte-level pre-release delta.

Additional public chronology checks covered the [2019-10-23 release
notes](https://noitagame.com/release_notes/20191023/), the 2020-06-24 and
2020-07-15 notes, and the [1.0 release
notes](https://noitagame.com/release_notes/20201015/); they likewise use only
generic “new secrets” wording. [GOGDB product
1310457090](https://www.gogdb.org/product/1310457090) lists exact 2019–2020
builds, while the [SteamDB depot
manifests](https://steamdb.info/depot/881101/manifests/) remain entitlement
gated. Public Internet Archive candidates were checked for provenance: the
Noita ZIP is an April/May 2021 build (version hash
`49826289ea5895d7869f52af3e16ca4519eb6315`), the `noita-setup` SFX is dated
December 2021, and a 5.6-GB ISO is dated April 2021. None is a verified
pre-1.0 snapshot, so these mirrors cannot answer whether the Eye payload
predates the 2020 release.

One historical payload target is now reproducible without guessing the build:
[GOGDB's exact 2020-05-20 build metadata](https://www.gogdb.org/product/1310457090/build/53351147046566224)
identifies the game's data.wak MD5 as
`3129ee3e8b556477147a866017ead0b4` (three raw chunk MD5s beginning
`4915ed...`, `3c0691...`, and `e7ad0e...`) and noita.exe SHA-256
`c5e8a689...`. The public GOG metadata endpoint exposes these hashes, but the
payload download requires an OAuth secure link and returned 401; no
entitlement bypass was attempted. This is the strongest remaining historical
lead: an entitled copy of that exact build could settle whether the Eye
initializer/data existed before the 2020 translation question.

The official localization chronology also constrains the Finnish-book lead:
the [30 March](https://noitagame.com/release_notes/20210330/) and
[2 April 2021](https://noitagame.com/release_notes/20210402/) release notes
announce “100% Finnished localization (Options, Language).” That is months
after 1.0 and after the 23 March 2021 Eye video, so this in-game Finnish
translation cannot be required to construct the original Eye ciphertext.
It remains eligible only as a later decoding clue.
Discovery chronology is separate from authoring chronology. The Reddit
submission kdx9iq (15 December 2020, preserved by
https://api.pullpush.io/reddit/search/submission/?ids=kdx9iq) shows that players
were already discussing Eye runes in parallel worlds immediately after 1.0,
but its comments do not date the developer's construction. The first public
Eye Messages wiki article was created 4 April 2021, and the earliest
well-known mystery video was uploaded 23 March 2021
(https://www.youtube.com/watch?v=4lSPZWmmoS8). These dates establish only that
the community's documented solving effort is post-release; they neither
support nor rule out a pre-2020 Finnish source or an offline developer key.

## Result

The dated independent decompilation closes a major historical uncertainty:
the 150-word payload and base-seven renderer serialization were already fixed
by April 2021 and exactly match today's corpus.  It gives no developer-sized
ordering or key and no evidence that the later eyespot/book machinery decodes
the Eye Messages.  A pre-1.0 payload comparison remains blocked on an entitled
historical depot download; no speculative key is promoted.
