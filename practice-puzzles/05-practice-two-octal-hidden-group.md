# Practice `two` — solved (octal hidden-group cipher)

Source data and the independently reproducible attack are public in the
[Noita eye scratchpad](https://github.com/hansborr/noita-eye-puzzle-scratchpad/tree/main/research/data/practice-puzzles).
The recovered plaintext was frozen before the repository maintainer compared
it with withheld ground truth and confirmed its content on 6 July 2026.

## Cracking method

The 698-symbol ciphertext uses only `A..L`.  The first structural observation
is that a symbol is never followed by one in the same modulo-three class.  More
importantly, long repeated **equality patterns** exist even when the literal
symbols differ.  Align each such pair and record the induced symbol bijection,
or *column map*.  Four complete maps close under composition to a transitive
order-48 permutation group on the 12 labels, preserving three four-symbol
blocks.  This recovers hidden-state geometry directly in the observed labeling;
no arbitrary relabeling search is needed.

All strong repeats have even gaps.  They therefore expose only an index-two
shadow of the author-reported order-96 group—a useful warning that group closure
is a lower bound when the observations have a parity restriction.

The attack then proceeds as follows:

1. Trim two symbols from both ends of every long isomorph.  The visible pattern
   matches overextend the true repeated plaintext slightly; using the raw
   boundaries as hard constraints eliminates the real key.  A planted control
   distinguishes that boundary error from solver failure.
2. Parameterize a key inside the recovered order-48 shadow by one of 48 initial
   states and one of four stabilizer-fibre choices for each of eight legal
   actions: `48 × 4^8 = 3,145,728` candidates.  Evolve each candidate on the
   **full 12-symbol stream** and require its hidden eight-class action sequence
   to agree across the trimmed repeat anchors.
3. Hard anchors reduce the search to 104,096 distinct action streams.  Score 17
   shorter repeats softly rather than risking another boundary exclusion.  The
   maximum leaves 96 streams, or 24 canonical patterns after quotienting the
   arbitrary names of the eight actions.
4. Read each pattern as pairs of octal digits.  Exhaust the `8!` digit
   relabelings, both digit orders, and a small set of six-bit character tables.
   Language scoring produces a 26-symbol, space-bearing intermediate layer.
5. Solve that last layer as a monoalphabetic substitution, with a
   space-position-preserving shuffled null.  It yields the octal/decimal and
   Proto-Indo-European passage.  Punctuation and the malformed first letter are
   restored afterward from grammar and source alignment, not claimed as cipher
   output.

## Solution

```text
Would an octal number system have come before the decimal number system? It has been suggested that the reconstructed Proto-Indo-European word for "nine" might be related to the Proto-Indo-European word for "new". Based on this, some have speculated that proto-Indo-Europeans used an octal number system, though the evidence supporting this is slim.
```

## Verification and transfer

The maintainer confirmed the frozen candidate against withheld plaintext, so
the content is solved.  The repository does not contain the original
generator, key, codec, or punctuation artifacts, so this is **not** an exact
original-generator round trip; the pure computational result stops at the
letter layer.

The most valuable transfers to the eyes are methodological:

- extract and compose symbol maps from isomorphs instead of recording only
  their locations;
- trim empirical repeat boundaries and validate the trimming rule on a dirty
  planted control;
- treat a recovered closure as a subgroup when every anchor shares a parity or
  phase restriction;
- avoid an attractive low-alphabet projection until proving that it preserves
  the group signal; this solve required the full symbol stream;
- keep hard structural filtering, soft language ranking, matched nulls, and
  final verification as separate stages.
