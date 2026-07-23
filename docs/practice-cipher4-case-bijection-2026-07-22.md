# Practice cipher 4: case-sensitive bijection test — 22 July 2026

## Frozen question

The standard `C83` reduction of sdlwdr's fourth puzzle uses 53 values inside
the exact contiguous band `22..78`, a span of 57 positions.  Earlier attacks
case-folded those values and forced them into either fixed two-homophone slots
or an unrestricted many-to-one map.  They did **not** test the distinct
hypothesis suggested by the author's “very straightforward initial PTA” hint:

> the 57 positions are a conventional case-sensitive character alphabet, and
> the 53 observed actions are a one-to-one substitution of 53 distinct
> plaintext characters.

This is compatible with cyclic CTAK: adjacent ciphertext differences recover
the injective plaintext action map, after which only a monoalphabetic
substitution remains.

## Finite experiment

1. Preserve upper/lower case, ordinary word spaces, and punctuation while
   training a character four-gram model on the frozen English corpus already
   used for the other practice attacks.
2. Search injective maps from the 53 observed actions into each of these
   conventional character pools:
   - `A-Z`, `a-z`, and ` .,?!`;
   - `A-Z`, `a-z`, and ` .,'-`;
   - `A-Z`, `a-z`, and ` .;:-`;
   - `A-Z`, `a-z`, and ` .,:;`.
3. Allow observed symbols to swap with unused pool characters, so the four or
   five absent plaintext characters are not fixed in advance.
4. Run the identical optimizer on planted case-sensitive prose at the real
   total length.  Record recovered character accuracy and score.
5. Repeat the real search across independent seeds.  A solution must be
   readable across all three portions, preserve their exact shared blocks,
   and recur up to symbols that are genuinely underdetermined.

## Decision rule

- **Promote** only if several seeds converge to the same readable plaintext
  and the planted control verifies that the optimizer can recover this model.
- **Reject this family** if the control recovers while the real candidates
  remain seed-unstable gibberish with a large calibrated score gap.
- Do not reinterpret a best-scoring pseudo-word string as a partial solution.

This test does not cover a second transposition/encoding layer or a plaintext
alphabet outside the listed conventional families.  Those remain separate
hypotheses if this one fails.

## Result

The planted control succeeds and the real puzzle fails by a wide, stable
margin:

| Character pool | Control score | Control accuracy | Best real score | Real restarts |
|---|---:|---:|---:|---:|
| `A-Z a-z .,?!` | -11,001.74 | 99.9233% | -21,951.41 | 4 × 150,000 |
| `A-Z a-z .,'-` | -11,097.55 | 99.9233% | -21,714.64 | 8 × 200,000 |
| `A-Z a-z .;:-` | -10,984.01 | 99.9233% | -21,793.14 | 4 × 150,000 |
| `A-Z a-z .,:;` | -11,041.51 | 99.9233% | -21,821.69 | 4 × 150,000 |

The one control error out of 1,304 characters is on an underdetermined rare
character; the prose itself is clean and the best control solution recurs
across independent seeds.  The real candidates differ radically between
seeds and pools.  Their isolated fragments such as `hints`, `wind`, or
`ampLing` move to unrelated token assignments and are surrounded by mixed-case
gibberish.  They are optimizer artifacts, not partial plaintext.

## Verdict

Reject the declared case-sensitive monoalphabetic family.  The 57-wide band
is real, but it is not a bijection onto any of the four conventional
case-sensitive prose alphabets under this calibrated model.  This narrows the
remaining boundary to either a nonlinear/second layer, an unconventional
source alphabet, or non-prose plaintext.  Merely increasing the same
annealing budget is not justified.

## Superset follow-up

On 24 July the test was widened to all 95 printable ASCII characters and each
first ciphertext value was omitted as a possible primer rather than a
plaintext action. Three 100,000-step restarts recover a matched control to
`99.9231%` at score `-11284.89`; the best real run is unstable gibberish at
`-22047.26`. This stronger superset closes ordinary static printable prose,
not merely the four pools above. The subsequent encoded-format and quotient
screen is recorded in
[`practice-cipher4-wide-codec-audit-2026-07-24.md`](practice-cipher4-wide-codec-audit-2026-07-24.md).
