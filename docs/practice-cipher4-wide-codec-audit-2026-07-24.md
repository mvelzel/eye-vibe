# Practice cipher 4: wide codec and factor audit — 24 July 2026

## Frozen question

After removing Cipher 4's standard cyclic outer state, the three adjacent-
difference streams have lengths `330,388,583`. All 1,301 actions lie in the
exact interval `22..78`; subtracting 22 gives `0..56`, with only ranks
`1,3,51,53` absent. This pass began wide: test several unrelated
representations cheaply, then deepen only a family that survives a positive
control or a label-invariant structural test.

The author-thread facts were re-read directly. The puzzle is “deck-based”;
the three portions share much plaintext; all use the same, “very
straightforward” initial PTA order. The only disclosed group result is that
the effective group is cyclic and the equivalent ciphertext order is
standard. Nothing in the thread says the inner object is Base64, prose, or a
57-character alphabet.

## Breadth screen

| Family | Exact question | Result |
|---|---|---|
| Printable characters | Can the 53 actions inject into any printable ASCII character, with each first ciphertext value treated only as state? | Rejected by a planted control and a 10,762-score real/control gap. |
| Base64 under substitution | Are the action symbols an arbitrary relabeling of unpadded Base64 digits? | Rejected at the natural phase by a locally exact optimizer and planted Base64 prose. |
| Contiguous quotient/remainder | Does the numeric order split each rank into a structured high component and a low selector? | Survives structurally at widths 2 and 3; neither high component is direct English/Finnish substitution text. |
| Repeated cumulative layers | Is a surviving quotient itself another running cyclic state? | Negative: the un-differenced quotient is uniquely most nonuniform; further finite differences rapidly approach uniformity. |
| Known-source equality | Does a quotient reproduce a passage up to symbol renaming? | No 24-symbol window match in 1.39M normalized English characters or 1.16M normalized Finnish characters. |

## Printable and Base64 exclusions

The complete printable-ASCII pool contains 95 characters, so it strictly
contains all earlier 57- and 83-character prose pools. An injective
53-to-95 mapping was optimized on the differences only. Three 100,000-step
restarts gave:

```text
planted control: score -11284.89, accuracy 0.999231, clean prose
real best:       score -22047.26, seed-unstable mixed punctuation
```

This rejects ordinary prose under any static injective printable-ASCII map.

The difference lengths are all legal unpadded Base64 lengths: `330 mod 4 = 2`,
`388 mod 4 = 0`, and `583 mod 4 = 3`. Their flat frequency profile also
resembles encoded text. I therefore tested the stronger model in which all
53 observed actions may map injectively to arbitrary members of the 64-value
Base64 alphabet. Swaps are rescored exactly at the affected quartets.

At the real lengths, the same search recovers a planted substitution to
`96.820513%` byte accuracy. Its best result scores `-883.47`, all `975/975`
decoded bytes are printable, and the output is clean literary prose. Across
eight real 100,000-step restarts the best score is `-18200.56`; only `691/975`
bytes are printable, and every portion is binary gibberish. This closes the
natural fixed-phase Base64 family. It does not claim to exclude a format with
hidden leading digits, an interposed transposition, or a non-Base64 six-bit
codec.

## The width-2 and width-3 structural survivors

Every contiguous width from 2 through 28 was screened. For each width `w`,
write a rank as

```text
rank = w * quotient + remainder.
```

First-order mutual information was measured separately for the quotient and
remainder. Five hundred controls independently shuffled each portion while
preserving its exact rank frequencies. Width 3 is the unique smallest
remainder excess; width 2 is second:

| Width | Quotient states | Remainder states | Quotient MI | Quotient excess over null | Remainder MI | Remainder excess over null |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 19 | 3 | 0.788949 | +0.595282 | 0.001320 | -0.000899 |
| 2 | 29 | 2 | 1.480049 | +1.047748 | 0.024551 | +0.024024 |
| 5 | 12 | 5 | 0.393611 | +0.323167 | 0.035885 | +0.026663 |
| 7 | 9 | 7 | 0.262352 | +0.226836 | 0.122595 | +0.101978 |

The full 27-width table is emitted by the reproduction script. This ranking
was not obtained by trying to spell words: it uses only the authored numeric
order and sequential dependence.

### Width 2: 29-state payload plus parity

The 29-state quotient has entropy `4.572764` bits and normalized IoC
`1.350156`. Its serial MI is `1.480049`, compared with a frequency-preserving
null mean near `0.434`. The quotient/parity coordinate MI is `0.140885`; only
`97/10000` random assignments of the fixed 57 label frequencies to numeric
positions are as low (corrected lower tail `98/10001 = 0.009799`). Thus the
adjacent-pair grouping is unusually close to frequency-independent, although
the parity stream retains a small but significant serial dependence.

Two obvious “straightforward PTA” readings were calibrated and rejected:

| Static 29-character alphabet | Control score / accuracy | Best real score | Result |
|---|---:|---:|---|
| English `A-Z`, space, period, comma | `-10839.25 / 100%` | `-20881.91` | unstable gibberish |
| Finnish `A-Z`, `Ä`, `Ö`, space | `-11112.01 / 100%` | `-20011.46` | unstable gibberish |

An exact first-occurrence-signature scan also finds no 24-symbol window in the
large English corpus, Finnish *Seven Brothers*, or Finnish *Kalevala*, with
and without spaces. Width 2 is therefore a genuine structural lead, not a
plaintext solution.

### Width 3: 19-state payload plus ternary selector

The 19-state quotient has entropy `4.028140` bits and normalized IoC
`1.263304`. Its pooled serial MI is `0.788949`; all 5,000 within-portion
shuffles are lower. The ternary remainder has entropy `1.573749` of a maximum
`log2(3)=1.584963`, normalized IoC `1.013660`, and serial MI `0.001320`; its
upper tail is ordinary (`0.673065` in the 5,000-control run). The authored
triple grouping's quotient/remainder MI has random-label lower tail
`0.025897`.

That clean structure/selector separation is interesting, but the quotient is
not direct monoalphabetic English in the available test. A constrained
19-symbol control reached only `83.5511%`, so its optimizer is not strong
enough for a hard general exclusion; the real score nevertheless remained
about 10,960 units worse and seed-unstable. More decisively, neither the
19-state quotient nor its alternative mod-19 projection has a 24-symbol
equality-pattern match in the 1.39M-character English corpus.

## Verdict and next boundary

Cipher 4 remains unsolved. The printable and natural-phase Base64 lanes are
closed. The useful survivor is numeric: the exact 57-rank band admits
unusually clean consecutive pair/triple quotients, especially a 29-state
payload plus parity and a 19-state payload plus a nearly memoryless ternary
selector. Static English and Finnish character readings of the stronger
29-state quotient are excluded.

The next depth pass must explain *why* a deck construction would lift 29 or 19
payload states into consecutive pairs or triples. It should test a bounded
state/control law or a small route transposition and require replay across all
three exact shared blocks. Treating the quotients as arbitrary new
substitution ciphers, or extending the rejected language annealers, is not
justified.

Reproduction:

```text
scripts/analyze_sdlwdr_cipher4_factor.py
scripts/solve_sdlwdr_cipher4_base64.py
scripts/solve_sdlwdr_cipher4_case_bijection.py
scripts/scan_sdlwdr_cipher4_isomorph_sources.py
```
