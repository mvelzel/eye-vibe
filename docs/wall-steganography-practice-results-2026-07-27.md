# Wall Messages steganography practice — results

## Outcome

The cover has a deterministic word-length Morse layer. It recovers the full
63-letter message with two opposite carrier-bit defects:

```text
VISIONS OF ETERNITY LIE AHEAD
FULL OF HOPELESSNESS
RUBEDO JUST OUT OF REACH
```

The visible rule is exact at 168 of 170 carrier words. Because neither defect
has an independently visible exception rule and the author has not confirmed
one, this is a highly constrained recovery rather than an exact source replay.

## How the layer was found

The frozen breadth-first portfolio included word lengths and punctuation
groups. Treat a run of `. , ? !` as the end of one Morse character. A
conspicuous capital inside a clause also begins a new character. Map each
alphabetic word as:

```text
1–3 letters  .
4+ letters   -
```

Then decode every group as International Morse. With only the visible rule,
the 170 words form 63 groups and read:

```text
VISIONSOFETERNIEYLIEAHEAD?ULLOFHOPELESSNESSRUBEDOJUSTOUTOFREACH
```

This was not selected from a large free-form codec search. Screening the
natural word-length cutoffs in both polarities makes cutoff 3 uniquely
language-bearing; it gives 62 valid Morse groups and the exact tail
`RUBEDOJUSTOUTOFREACH`. Cutoff 4 makes all groups valid but yields
`VISIUNSOFETESII...`, while the other cutoffs are gibberish. Splitting at the
otherwise anomalous internal capitals then explains all those capitals and
completes the group boundaries.

Examples:

```text
Who do you worship        ...-  V
Who is                    ..    I
The one god               ...   S
Truly understand anything ---   O
See who god is            ....  H
even you are of           -...  B
Our                       .     E
Vision and eye            -..   D
```

## Minimal defect certificate

Aligning the proposed 63 characters to their standard Morse codes preserves
every group length. Exactly two of the 170 bits disagree:

| group | plaintext | carrier | observed | required |
|---:|:---:|---|:---:|:---:|
| 16 | `T` | word 37, `yet` | `.` | `-` |
| 26 | `F` | word 64, `this` | `-` | `.` |

Changing only those two classifications gives the full message above. The
bits are complementary, and the indices happen to sum to 101, but neither
fact supplies a visible extraction rule; they are not promoted as intended.

The executable certificate is
[`../scripts/solve_wall_steganography_practice.py`](../scripts/solve_wall_steganography_practice.py)
with the reusable decoder in
[`../src/eye_mystery/wall_steganography.py`](../src/eye_mystery/wall_steganography.py).

## Transfer to Noita

The recovered rule was frozen unchanged and applied independently to the 12
English Wall Message translations. Across 98 groups, only 46 are valid Morse;
52 are invalid. No message has an alphabetic run longer than three characters,
and none produces intelligible secondary text. Exact output and protocol are
in
[`wall-steganography-transfer-results-2026-07-27.md`](wall-steganography-transfer-results-2026-07-27.md).

The transferable lesson is methodological: meaningful cover prose can encode
a second message through the combination of structural delimiters and a coarse
word feature, so repeated plaintext need not create repeated carrier text.
The literal construction does not transfer to Noita's English Wall Messages
and has no direct input interface on the Eye trigrams.
