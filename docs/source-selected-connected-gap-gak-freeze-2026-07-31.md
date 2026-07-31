# Source-selected connected-gap GAK — freeze

## Question

Do literal *Hermetic Museum* continuations between source occurrences of
`THAT WHICH` realize the three Eye connected segments under one ordinary GAK?

This test adds information that the successful random-gap witness did not use.
It does not search arbitrary plaintext or score English-looking solver output.

## Source and normalization

The fixed corpus is the public Internet Archive OCR for Waite's two-volume
*Hermetic Museum*:

```text
b24927363_0001
b24927363_0002
```

Before inspecting finite feasibility:

- undo alphabetic line-wrap hyphens;
- collapse every whitespace run to one space;
- uppercase;
- preserve OCR punctuation and spacing otherwise;
- find every pair of literal `THAT WHICH` starts separated by exactly
  `28`, `30`, or `35` normalized characters.

This yields source-only candidate counts `5`, `4`, and `2`. Test all
`5×4×2 = 40` triples; do not preselect on the Eye ciphertext.

## Cipher model

For each triple:

- take the complete source substring from the first phrase start through the
  end of the second phrase;
- assign one shared action label to each literal normalized character;
- use canonical Eye trigram segments at raw offsets `40->68`, `40->70`, and
  `45->80`;
- allow independent arbitrary 83-card start decks;
- share one complete position permutation per source character;
- emit after every action;
- allow no reset, selector layer, token merge, or postprocessor inside a
  segment.

The literal character alphabet, rather than an arbitrary `K`, fixes the action
count for each triple.

## Test ladder

1. Apply exhaustive free-subgroup closure to every triple.
2. For each survivor, quotient its fixed-word core to at most 83 states
   without forcing any registered nonmember.
3. Complete the quotient with the CP-SAT interval-trie solver.
4. Independently replay every returned key and deck.
5. Record the following source character after each second phrase as a
   pre-frozen extension. Report whether the fitted action predicts an already
   observed card, a wrong observed card, or an unconstrained fresh card.

Failure to find a quotient or solver timeout is `unknown`, not rejection.
Free-group contradiction or exact 83-state UNSAT rejects that literal triple.

## Interpretation

All 40 triples rejected would close this exact anthology-continuation route
under ordinary GAK. SAT would be stronger than a random schedule but still not
decryption: occurrence selection is a 40-model family and independent start
decks retain substantial capacity.

Promotion requires more than SAT: a source-selected triple must produce a
nontrivial pre-frozen extension consequence or another independently authored
Eye match not used in selecting it.
