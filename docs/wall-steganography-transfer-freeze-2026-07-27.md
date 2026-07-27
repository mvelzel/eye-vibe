# Wall-steganography transfer — freeze

## Corpus

The transfer corpus is the 12 translated Secret Messages on the current
Noita Wiki `Game Lore` page:

<https://noita.wiki.gg/wiki/Game_Lore#Secret_Messages>

The page warns that its missing punctuation and grammatical errors reproduce
the original glyphs for one-to-one comparison. The exact English text
inspected before decoding is frozen in
[`../artifacts/noita-wall-messages-en.txt`](../artifacts/noita-wall-messages-en.txt).
Map IDs preserve the page's ordering. Wiki layout line breaks are ignored;
punctuation, words, apostrophes, and capitalization are retained. The editorial
`[sic]` in G11 is removed before decoding because it is not in the glyph text.

## Predeclared transfer

Apply the practice-puzzle rule unchanged and independently to each message:

1. split Morse-character groups after every run of `. , ? !`;
2. within a resulting clause, split before every capitalized word except the
   first;
3. map each alphabetic carrier word of length 1–3 to dot and length 4+ to dash;
4. decode each group with standard International Morse.

No bit repair, threshold change, boundary deletion, message concatenation,
reordering, reversal, or language-scored retuning is allowed after output is
seen.

## Readout and gate

For every map ID report:

- carrier-word and Morse-group counts;
- raw decoded string, with `?` for invalid Morse groups;
- number of valid groups and longest contiguous alphabetic run.

An unchanged positive transfer requires a complete intelligible secondary
message and must explain conspicuous carrier choices. Isolated words or
fragments fail. If no message passes, record a scoped negative: Lymm's practice
construction is not a literal second layer in the English Wall translations
under the recovered rule. This says nothing about other steganographic rules,
the Finnish glyph tape, or the Eye ciphertext.
