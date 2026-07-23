# Practice cipher 4: selector and route results — 24 July 2026

## Question and boundary

The preceding width screen found two ordered descriptions of Cipher 4's
recovered `0..56` action ranks:

```text
rank = 2*q + r    q in 0..28, r in 0..1
rank = 3*q + r    q in 0..18, r in 0..2
```

This pass tested the bounded mechanism families frozen in
[`practice-cipher4-selector-route-freeze-2026-07-24.md`](practice-cipher4-selector-route-freeze-2026-07-24.md).
It asked whether `q` is a distance and `r` a control, whether `r` follows a
small transducer, or whether a conventional fixed route hides a static
reading. It did not add arbitrary state tables after inspecting the output.

## A–E: quotient walks and selector controls

There are 67 declared laws at width 2 and 139 at width 3:

- direct quotient;
- unsigned quotient accumulation with offsets `-1,0,+1`;
- every selector-to-sign table;
- every selector-to-Boolean-carry table;
- every nonempty direction-toggle subset, both initial directions, and
  before/after timing;
- one accumulator per selector lane.

Every law was rendered under ring reflection and rotation on the plausible
sizes `19,27,28,29,30,36,37,41,42`, using both a space-first alphabet and
sdlwdr's disclosed alphabet convention. Independent portion rotations favor
the model; a shared-rotation run was also checked at size 29.

The planted unsigned width-2 walk decodes cleanly. At size 29 its
space-preserving control scores `-8.389512` log units per modeled gram, and the
unspaced sdlwdr control scores `-9.303360`. On the real data the untouched
quotient beats every one of the 205 state/control alternatives. Representative
best real scores are:

| Alphabet/ring | Best real law | Score per gram |
|---|---|---:|
| English `A-Z + space + . ,`, 29 | direct width-2 quotient | `-18.011651` |
| Finnish `A-Z + Ä + Ö + space`, 29 | direct width-2 quotient | `-17.106584` |
| sdlwdr natural 42 | direct width-2 quotient | `-18.189788` |

Changing the selector into a sign, carry, toggle, or lane choice never
improves the direct quotient. A–E are therefore closed within the frozen
families.

## G: a significant selector predictor that is not a transducer

The first selector-prediction audit looked promising. It used leave-one-
portion-out training and excluded every held-out position whose centered
nine-quotient window occurred in training. The same selection over 39
predeclared contexts was repeated on 1,000 controls.

| Width | Best context | Gain, bits/symbol | Accuracy | Marginal baseline |
|---:|---|---:|---:|---:|
| 2 | previous `q`, current `q`, previous `r` | `0.328318` | `0.814961` | `0.624016` |
| 3 | previous `q`, current `q`, previous `r` | `0.551030` | `0.662698` | `0.339286` |

Both effects have corrected upper tail `1/1001` under each of four nulls:

1. shuffle selectors independently;
2. shuffle selectors only within their current-quotient class;
3. circularly offset each selector stream, preserving its run structure;
4. shuffle intact quotient/selector rank pairs.

That significance does **not** establish a control law. The held-out
predictions can be attributed exactly:

| Width | Seen context and exact rank bigram | Seen context but new rank bigram | Unseen context |
|---:|---:|---:|---:|
| 2 | `304/322` correct | `0/23` | `110/163` |
| 3 | `295/317` correct | `0/42` | `39/145` |

Exact rank trigrams account for `188/194` and `180/189` correct cases,
respectively. In other words, the coarse context succeeds when it acts as a
compact index for a full action bigram already present in another portion.
It fails every time that coarse context collides with a genuinely new action
bigram. The statistic detects the author's disclosed shared plaintext beyond
the removed nine-symbol blocks; it does not predict new actions and is not an
executable selector transducer.

## F: fixed route transpositions

A label-invariant English model was trained on canonical equality patterns of
eight-character windows. It assigns no letters to quotient symbols. The
complete 396-route catalog contains:

- identity and reversal;
- global odd/even splits and inverses;
- ragged rectangular column, snake-row, and snake-column reads and inverses
  for widths `2..32`;
- rail-fence orders and inverses for `2..10` rails;
- fixed-block odd/even, reversal, and alternating reads for widths `2..32`.

The measured quantity is the best nonidentity improvement over identity. Each
of 200 controls shuffles positions within every portion and repeats the full
396-way selection.

| Quotient | Best nonidentity route | Improvement | Null range | Corrected upper tail |
|---:|---|---:|---:|---:|
| width 2 | eight-wide alternating/snake rows | `+0.527047` | `+0.158099..+1.281532` | `0.651741` |
| width 3 | 21-wide block odd/even | `+1.099294` | `+0.135315..+1.610905` | `0.179104` |

A planted ragged seven-column transposition is identified exactly and inverted
exactly, with improvement `+3.478690`. The real improvements are ordinary
best-of-family effects. No fixed route is promoted.

## Verdict

Cipher 4 remains unsolved. The ordered pair/triple quotients are real
descriptive statistics, but this pass finds no small walk, sign, carry,
toggle, lane, selector-transducer, or fixed-route mechanism behind them. The
most significant apparent survivor is completely carried by exact rank
bigram reuse from the known shared plaintext. Therefore the speculative
two-cycle lift is not opened: `57 = 29 + 28` alone supplies no state law.

The transferable result is methodological. A projection can produce an
extremely significant held-out statistic while adding no predictive
information beyond copied or homologous full symbols. Attribution by exact
carrier—not merely a stronger shuffle—is required before treating such a
projection as a cipher component.

Reproduction:

```text
scripts/analyze_sdlwdr_cipher4_selector_walks.py
scripts/analyze_sdlwdr_cipher4_selector_prediction.py
scripts/analyze_sdlwdr_cipher4_routes.py
```
