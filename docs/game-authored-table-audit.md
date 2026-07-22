# Game-authored exact-size table audit

## Question

Could a developer-authored Noita table directly supply the missing order or
lookup for the Eye alphabet? This is the most literal form of the “later
lookup table” lane: search the installed data before inventing a transform,
and require an exact domain size rather than an approximate numerical echo.

## Structural inventory

`scripts/scan_game_authored_tables.py` scans balanced Lua table literals, XML
direct-child counts, and nonblank CSV/TSV/TXT line counts in the installed
WAK. The target sizes are 5, 42, 83, and 101. In the 21 July 2026 installed
build it finds:

```text
Lua files                    1,077
Lua table target counts      5:1,011  42:0  83:4  101:0
XML files / parse failures   4,325 / 301
XML child target counts      5:283  42:1  83:0  101:0
text line target counts      5:12  42:0  83:0  101:0
```

All four 83-entry Lua hits are identical copies of `gun_names`:

```text
data/scripts/gun/procedural/gun_procedural.lua
data/scripts/gun/procedural/gun_procedural_better.lua
data/scripts/gun/procedural/gun_utilities.lua
data/scripts/gun/procedural/wand_petri.lua
```

The NUL-joined entry list has SHA-256
`9ef2ead9b050c32b8440930d4ff7480b1c77298f7758c162fca8e5e54daf94ae`.
Its endpoints and the conspicuous 41/42 boundary are:

```text
0 Deadly       40 Special       41 Unique       42 Mega       82 Online
```

This is one authored table copied four times, not four independent clues. Its
ordinary runtime use is also explicit: `gun_names[Random(1,#gun_names)]` adds a
random adjective to a generated wand's UI name. The roll is one-based Lua
indexing and is not retained as a cipher value.

The sole 42-child XML hit is the root of
`entities/animals/maggot_tiny/maggot_tiny.xml`; its children are ordinary
components, not a 42-value lookup. No direct 42- or 101-entry Lua table and no
83- or 101-line text table appears. The 301 XML parse failures limit this to a
structural inventory rather than a proof about every possible authored data
encoding.

## Chronology

The repository labelled `noita-early-access-data` contains the same 83 names,
in the same order and with the same digest. Its complete `gun_utilities.lua`
is byte-identical to the first timestamped public-data copy from 9 February
2021. The early-access snapshot does not contain the Eye payload strings or
the later Eye-building assets found in the current tree.

This strongly supports the list being old enough to be construction material,
but it is not a clean contemporary timestamp: the early-access snapshot's
single Git commit was uploaded on 2 October 2022. Therefore the chronology is
recorded as **construction-eligible if the snapshot label is accurate**, not
as independently proved pre-15-October-2020 publication. It is eligible as a
later decoding clue regardless.

## Bounded cryptographic attacks

### Fixed label-to-letter readings

The table first maps each Eye value to its source-order adjective. Fifteen
global, deterministic reductions were predeclared:

- first, last, two middle letters, and A1Z26 word length;
- the character selected cyclically by each of the three base-five Eye digits,
  counted from either end;
- digit-sum and full-label modulo word length, counted from either end.

Each rule was tested with and without the first marker. An English tetragram
model selected the best of all 30 readings. Every control shuffles the 83
whole names among the 83 labels, reruns the complete family, and preserves the
name multiset, ciphertext, message boundaries, and selection freedom.

The winner is full-label modulo word length counted from the end, with the
marker omitted. Its average score is `-14.515440` per tetragram and its output
is visible gibberish (`LILMOYFENEEKIOAFTSRLOEYE...`). In 2,000 controls the
family-corrected upper tail is:

```text
316 / 2,001 = 0.157921
```

Thus the exact lookup count does not select a natural global letter reading.
Choosing a different character independently at each occurrence is not a
bounded decoder; it can manufacture phrases from the available letters.

### Transferring the solved practice-#5 mechanism

As a method-transfer check, the names were alphabetized to define an external
83-card initial deck. Both alphabetical directions and both marker policies
were decoded with sdlwdr practice cipher #5's exact recursive,
plaintext-selected chunk-reversal shuffle. The selected candidate places
`560/1,027` body outputs in that puzzle's `0..41` plaintext range. Shuffling
the name assignments and reselecting the four variants gives:

```text
240 / 2,001 = 0.119940
```

The learned dynamic-deck method therefore does not turn this table into an
Eye decoder.

## Community provenance

Read-only searches of `silmä-cryptography` and `silmä-novel` show that the
83-name observation is longstanding:

- defektu recorded the count and `wand_petri.lua` copy on 22 August 2022;
- sirreldar explored selecting letters from the indexed names on 10–11
  September 2024;
- sdlwdr mentioned `gun_names` as a possible stored ordering on 19 May 2026.

An exact `gun_names alphabetical` search found no prior hit in either channel,
but search absence is not a novelty claim. The important addition here is the
matched negative calibration, not rediscovery of the table.

## Verdict

The 83-entry table is real, exact, relevant to wand/deck vocabulary, and
probably old enough to be considered. The direct semantic readings and the
most relevant learned dynamic-shuffle transfer are negative. Keep the table
paused as a possible externally selected key only if another authored clue
specifies how to consume it. Do not search arbitrary per-occurrence letter
choices, arbitrary name sorts, or unrestricted 83-card permutations.

## Reproduction

```bash
PYTHONPATH=src python3 scripts/scan_game_authored_tables.py /path/to/data.wak
PYTHONPATH=src python3 scripts/analyze_gun_names_selector.py \
  /path/to/data.wak /path/to/english-corpus-large.txt --controls 2000 \
  --historical-lua /path/to/early/data/scripts/gun/procedural/gun_utilities.lua
```
