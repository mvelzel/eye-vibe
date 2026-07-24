# Eleventh wide horizon — first mixed batch results

## Result

The batch yields one genuinely useful new primitive and no decoder:

- ciphertext-only ordinary-GAK feasibility is exactly decidable on tiny decks,
  and the reported eight-/nine-symbol parent/orphan pair reproduces;
- the recent index-25 entropy/music claim is directly false on the real data
  and its relaxed finite family is null-typical after selection;
- the proposed Finnish syllable pair was constructed to share an opening and
  does not reproduce the later Eye equality runs;
- the no-double observation puts no finite capacity bound on ordinary GAK;
- every retained project curiosity still has an identifiable carrier, and none
  predicts a genuinely new body context.

The GAK oracle is promoted as calibration infrastructure, not to an 83-card
deep search. Its factorial operation-set growth fails the required scaling
gate.

## A. Universal entropy or periodicity pivot

The attachment `Entropy-Based Analysis of Noita Eye Transmissions.pdf` claims
that glyph index 25 divides a high-variance header from a perfectly balanced,
lag-five-periodic payload. The actual block at glyphs 25 through 49 was checked
on all distinct natural five-valued trigram projections:

1. first eye;
2. middle eye;
3. third eye;
4. the three-eye sum modulo five.

There are 36 projection/message rows. Exactly `0/36` have five copies of every
residue, and `0/36` repeat perfectly at lag five. For example, East 1's third
eye has counts `(6,5,4,4,6)` and only `3/20` lag-five matches. East 4's middle
eye has `0/20` matches. This is an exact contradiction, not a significance
judgment.

The weaker family was also scanned rather than dismissed:

| selected family | observed best | glyph-shuffle controls | corrected upper tail |
|---|---:|---:|---:|
| lag 5; choose projection and cut | `62/180`, first eye, cut 42 | min 50, median 60, max 76 | `402/1001 = 0.401598` |
| lags 2–10; choose projection, lag, and cut | `77/207`, first eye, lag 2, cut 55 | min 62, median 70, max 86 | `55/1001 = 0.054945` |

Each control shuffles complete trigrams within each message, preserving its
trigram multiset and all within-glyph component relations, and reselects the
entire projection/lag/cut family. Neither scan promotes. The plotted exact
post-pivot sequence in the PDF is not a representation of the accepted Eye
corpus.

**Decision:** close the exact index-25/music claim. A future change-point claim
must name a different representation and statistic before looking at the
messages.

## B. First-glyph checksum field

The recent Discord summary restates a real result already audited in this
project. Complete sums are:

```text
4040  4124  4754
4295  5656  4748
5385  4936  4545
```

East 1, East 3, and East 5 are the main diagonal/odd-East family and are
multiples of 101. Their first glyphs `50,63,33` are exactly the additive check
values for their bodies. The other six first-glyph offsets are
`84,7,53,1,32,88`; there is no all-nine additive check rule.

The prior exact conditional control remains the right attribution. Holding all
nine bodies and the observed marker multiset fixed, `720/362880 = 1/504`
marker assignments make this fixed triple close; the same corpus also supplied
the choice of modulus and scope, so this is not an independent decryption
probability.

**Decision:** retain “three markers are ciphertext checks/order metadata.”
Do not retest generic checksum formula families until an external rule predicts
the six nonzero offsets or the diagonal scope.

## C/D. Ciphertext-only GAK feasibility and minimum-operation curve

The frozen ordinary GAK is:

```text
new_deck[i] = old_deck[operation[plaintext_symbol][i]]
ciphertext   = new_deck[0]
initial deck = identity
operation[0] != 0
the operations' source positions at index 0 are distinct
```

The last condition makes every used operation bring a non-top card to the top.
Distinct source positions make the plaintext operation recoverable when the
current deck and next ciphertext are known. Plaintext is unknown.
Plaintext-symbol names are irrelevant, so the exact tiny solver enumerates
unordered operation sets and performs dynamic reachability over deck states.

For `A=0, B=1, C=2, D=3`, the reported community pair reproduces:

```text
BCBDBCDA   SAT    after 45/108 two-operation sets
BCBDBCDAC UNSAT  after all 108/108 two-operation sets
```

One exact witness for the parent is:

```text
plaintext:  aababaaa
operation a: (1,2,3,0)
operation b: (3,1,0,2)
replay:     BCBDBCDA
```

The minimum operation alphabet for prefixes of the orphan is:

```text
length 1  2  3  4  5  6  7  8  9
minimum 1  1  2  2  2  2  2  2  3
```

This demonstrates a ciphertext-only falsifier and a complexity curve without
guessing plaintext. It also demonstrates the scaling wall:

```text
deck        top-changing permutations    unordered pairs
4           18                           108
5           96                           3,456
6           600                          144,000
7           4,320                        7,776,000
8           35,280                       533,433,600
```

At 83 cards, direct enumeration is unusable. Shrinking an Eye prefix to the
labels it happens to contain would change the hidden deck and is not a valid
test.

**Decision:** promote the exact oracle as a calibration target for a future
symbolic/constraint-propagation solver. Do not call an Eye prefix SAT or UNSAT
until the same implementation passes a predeclared scaling gate on planted
decks.

## H. Finnish syllable-token fingerprint

A deterministic orthographic syllabifier was implemented from the
[Kielitoimiston general rules](https://kielitoimistonohjepankki.fi/ohje/tavutus-yleisperiaatteet/):
the final consonant before a vowel begins the next syllable; adjacent vowels
split unless they form a long vowel or an allowed diphthong; `ie`, `uo`, and
`yö` are diphthongs only in the first syllable. Official examples such as
`ka-la`, `lui-ta`, `ai-no-a`, `puo-lu-ei-ta`, and `pa-pe-ri-en` are locked in
tests.

The two Discord strings tokenize to 48 syllables each. Their aligned
literal-equality runs are:

```text
same 24, different 2, same 6, different 2, same 14
```

East 1 and West 1 after their distinct markers instead begin:

```text
same 24, different 4, same 4, different 4, same 13
```

The shared opening is exact; the claimed later pattern is not. The example is
also not a located verbatim source. It edits the public Kanteletar poem *Aholla
itkijä*: among other changes, `Paistavalla` becomes `Paukkovalla`, `pahoin`
becomes `pahon`, `Siskoko` becomes `Sikkoko`, and the common `Ken sua pahoin
pitävi` line is omitted. The original is available in the public-domain
[Kanteletar edition](https://www.gutenberg.org/cache/epub/7078/pg7078-images.html).

Under arbitrary GAK, plaintext syllable equality does not directly imply
ciphertext equality, so even a perfect literal run match would need a
mechanism-specific bridge.

**Decision:** reject this pair as source evidence. Retain syllable-token
search only after a planted GAK/source experiment identifies an invariant that
the ciphertext should preserve.

## J. Carrier attribution matrix

The retained observations were classified by the data that actually carries
them:

| observation | exact carrier | genuinely new body-context prediction? |
|---|---|---|
| shared openings | copied full labels at the same positions | no |
| six nonliteral isomorphs | equality/repetition skeleton in selected windows | no |
| factoradic/D4/S5 header structure | the nine first trigrams only | no |
| cyclic BWT `Fi!` | unused digits of the nine markers plus the marker trail | no |
| odd-East mod-101 checks | selected full-body sums and their first markers | no |
| merged-trie mod-101 closure | deduplicated prefix-trie edge labels | no held-out consumer |
| first/third-eye order residue | seven selected isomorph contexts; post-hoc feature family | no |
| Gate mirror total 70 | later sprite residual and an Eye-derived grid statistic | no; retrospective corroboration |
| cipher-4 selector score | exact repeated plaintext-rank bigrams/trigrams | `0/23`, `0/42` on new rank bigrams |

This does not make the observations unreal. It says what each can currently
support. The header results support metadata; the checks support deliberate
numeric construction; the Gate supports possible shared construction
vocabulary. None currently executes a body transform on an unseen context.

**Decision:** any next body model must report its score separately on new full
labels, new equality contexts, copied-prefix exits, and renderer boundaries.

## F. No-double capacity

The proposed finite-capacity interpretation is false for ordinary GAK. A
single rotation

```text
(1,2,3,...,82,0)
```

has `operation[0] != 0` and can be repeated forever. A committed 83-card
fixture emits 1,028 symbols with zero adjacent doubles using only that one
operation.

The observation still constrains every actually used operation to avoid a top
fixed point under this model. It reduces the candidate permutation count from
`d!` to `(d-1)(d-1)!`; it does not bound message length or plaintext alphabet
size.

**Decision:** close the capacity lane. Keep the no-top-fixed constraint inside
GAK feasibility models.

## Batch decision

No plaintext or body decoder results. The useful advance is methodological:
ordinary GAK is not universally capable of generating arbitrary ciphertext at
fixed alphabet sizes, so a ciphertext-only no-parent proof is possible in
principle. The immediate obstacle is solver representation, not a missing
crib.

Before deepening that lane, the next pass should remain mixed: test
reconvergence collision inference, reset-state identifiability, renderer-width
counterfactuals, and one independently specified in-game interface. A stronger
GAK backend earns depth only by crossing a planted-deck scaling threshold.
