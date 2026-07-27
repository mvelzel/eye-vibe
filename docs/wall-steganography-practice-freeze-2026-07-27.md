# Wall Messages steganography practice — freeze

## Source and object

Lymm posted the practice puzzle in the read-only Silmä Secrets Storehouse:

<https://discord.com/channels/453998283174576133/1227024108286644284/threads/1530349632884838572>

The exact cover text is frozen in
[`../artifacts/practice-wall-steganography.txt`](../artifacts/practice-wall-steganography.txt).
Capitalization, punctuation, apostrophes, repeated words, and spacing are part
of the object.

The author describes it as a steganographic puzzle designed to resemble the
content of Noita's Wall Messages. The only author hint inspected before this
freeze is:

```text
It's not a Baconian
```

At retrieval, the eight-message thread contained attempts but no posted
solution. No further hint or solution will be consulted before the frozen
attack portfolio is exhausted.

## Frozen attack portfolio

Run breadth-first, without language-directed retuning:

1. anomalous capitalization and its word/sentence coordinates;
2. sentence, clause, and punctuation-delimited initials/finals;
3. word-length, parity, and alphabetic-rank tapes;
4. repeated carrier words and the words immediately around them;
5. lexical anomalies, including repeated fillers and conspicuous phrasing;
6. rectangular/ragged layouts selected only by objective text counts.

For binary observables, report standard byte orders and offsets but do not
expand into arbitrary encodings. Baconian five-bit grouping is excluded by the
author hint.

## Solution gate

A solution must provide:

- a deterministic extraction rule fixed by visible features;
- a complete intelligible hidden message, not a language-scored fragment;
- an explanation of the cover text's conspicuous choices;
- exact reproduction from the frozen artifact.

Only after that gate passes may the recovered method be tested on the actual
Wall Messages. The Eye test must be declared before inspecting its output and
must use the same feature family without bespoke edits.
