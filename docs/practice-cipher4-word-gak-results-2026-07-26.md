# Practice Cipher 4: word-constrained cyclic-GAK result

## Question

Can the recovered `C83` difference stream be decoded by an arbitrary
plaintext-selected rotation

```text
p[i+1] = sign * difference[i] + q(p[selector]) mod 83
```

when the plaintext is ordinary dictionary prose in the straightforward
alphabet used by the related practice puzzles?

This is the strongest remaining literal interpretation of “deck-based” plus
the independently recovered cyclic effective group. The unknown table `q` is
not assumed affine or otherwise simple.

## New solver

The earlier 250,000-state character beam was inadmissible because it lost a
matched English plant at transition 49. The replacement combines:

- exact consistency of the unknown rotation assigned to every plaintext
  symbol;
- a complete word-prefix trie built from the training corpus and the system
  English dictionary;
- character six-gram ranking only among paths that remain valid word
  prefixes;
- current- and next-symbol update timing and both relative orientations;
- explicit natural plaintext positions rather than a fitted substitution.

It supports compact 27, natural-position 27, natural 32
(`A-Z`, space, `.-'?!`), and the complete natural 42 positions including
digits.

## Positive controls

The 27-symbol control that defeated the old character beam is recovered
exactly at rank one.

More importantly, a 102-character natural-position control using spaces,
period, hyphen, apostrophe, question mark, and exclamation mark is recovered
exactly at rank one with a 50,000-state beam:

```text
THE QUICK-BROWN FOX'S PUZZLE IS HARD? YES! THEN ANOTHER CURIOUS DOG WATCHES FROM THE GARDEN AND RESTS.
```

The control exercises the same 32-symbol alphabet and unknown rotation-table
architecture as the promoted real test.

A 42-symbol control that deliberately uses every digit as well as punctuation
is not recovered at 50,000 states; it stops at transition 56. Therefore the
complete 42-symbol real runs are exploratory and cannot exclude that superset.

## Real results

On the first 200 transitions of portion 2, the four genuinely different
natural-32 conventions stop at:

| Selector timing | Relative orientation | Completed |
|---|---:|---:|
| current symbol | same | `49/200` |
| current symbol | reflected | `48/200` |
| next symbol | same | `48/200` |
| next symbol | reflected | `48/200` |

Simultaneously reflecting ciphertext and plaintext coordinates produces the
same language paths with a reflected key, so the nominal eight sign settings
reduce to these four.

Possible word-boundary misalignment was tested under the primary convention.
Starting at every offset `0..16`, no candidate completes a 100-transition
window; the maximum is `57/100` at offset 5. Thus the phase-zero failure is not
explained by beginning in the middle of an ordinary first word.

Finally, increasing the primary real beam from 50,000 to 250,000 states,
generating as many as 2,604,288 distinct candidates at one step, reaches only
`52/200`. It does not show the capacity jump seen when an underpowered model
is widened.

The larger 42-symbol exploratory run reaches `75/200`, but its digit-heavy
tail exploits an uncalibrated part of that model. Apparent openings such as
`WORLD MAGIC BUT HEAVENS` and `ITS FINGER POHYOLA` change with alphabet and
budget and are followed by arbitrary punctuation. They are optimizer
artifacts, not recovered plaintext.

## Exact edit geometry

The shared action blocks also sharpen one fact independently of language.
Portions 2 and 3 take one transition between the shared states around their
first long block. Portion 1 takes two transitions through one extra state and
then rejoins the same 105-transition continuation. Under any deterministic
cyclic-GAK table this is compatible with a one-character plaintext insertion.
The observation supports stateful resynchronization but does not select the
missing codec.

## Decision

This is a calibrated bounded negative for ordinary English dictionary prose
under the natural 32-position arbitrary cyclic-GAK recurrence. It is not a
proof against:

- the complete 42- or 83-symbol plaintext alphabet;
- non-dictionary source text;
- a non-GAK deck whose visible cyclic group is only an outer layer;
- polygraphic, fractionated, or encoded plaintext.

The result removes the reason to enlarge the same language beam again. Cipher
4 should next be reopened by an author hint, a plaintext/source crib, or a
deck invariant qualitatively different from an arbitrary rotation table.

Reproduction:

```text
src/eye_mystery/practice_cipher4_words.py
scripts/search_sdlwdr_cipher4_word_gak.py
tests/test_practice_cipher4_words.py
```
