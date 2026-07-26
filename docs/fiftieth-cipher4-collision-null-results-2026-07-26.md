# Cipher 4 collision observation under the cyclic phase null

## Observation and provenance

In the read-only Cipher 4 Discord thread, simplesmiler reported on 23 July
2026 that aligned cross-message IoC was unusually low: only two coincidences
where about 12 were expected. The same message reported high bigram IoC and
attached a standard-order `83×83` distant-bigram heatmap. The attachment has
SHA-256
`71a4c4bf0abe42233fbf5bffe679a8b55d49ebfaf37716448cfbad7f5fa9979f`.

This is a retrospective audit of a community-selected statistic, not a
preregistered discovery test.

## Exact matched null

Cipher 4's established outer layer is a `C83` running state. Adding one
constant modulo 83 to a whole portion changes only its initial state; it
preserves every adjacent difference, repeated action, and exact common action
block.

The audit fixes portion 1 at shift zero and exhausts the `83² = 6,889`
independent shifts of portions 2 and 3. It measures:

1. equal symbols at the same position across each pair of portions;
2. exact adjacent-bigram collisions across pairs of portions;
3. repeated bigrams within each portion, which are invariant under the null.

A planted translated-stream control recovers its complete relative phase.

## Results

The two aligned coincidences are both between portions 2 and 3: value `5` at
zero-based index 340 and value `61` at index 369. The independent-uniform
expectation is `1,051/83 = 12.6627`.

Under the matched phase null:

| Quantity | Observed | Exact null result |
|---|---:|---:|
| aligned unigram collisions | 2 | `86/6,889` are `<=2` |
| corrected lower tail | | `87/6,890 = .012627` |
| cross-message bigram collisions | 183 | mean `180.4578`, range `116..574` |
| corrected bigram upper tail | | `2,168/6,890 = .314659` |
| joint observed-direction tail | | `34/6,890 = .004935` |

There are 102 fixed within-portion repeated-bigram pairs. Adding the 183
cross-portion matches gives 285 pooled collisions among 1,301 bigrams:
IoC `.000337019`, or 2.322 times the independent `83×83` baseline. But the
matched null leaves the 102 within-portion matches fixed and puts the observed
cross-portion count near its mean. The high bigram IoC therefore does **not**
select another layer; it is already explained by the narrow difference band,
its nonuniform action frequencies, and the disclosed shared action blocks.

Among the 86 phase choices with at most two aligned unigram matches, 33 also
meet the observed bigram threshold. Thus the joint tail is driven by the low
unigram count; “high bigram” is ordinary conditional on that selection.

## Interpretation and stop rule

The low aligned-symbol count is mildly suggestive that the three initial deck
states were chosen to avoid collisions between otherwise homologous state
trajectories. It is not unique—86 phase pairs do at least as well, including
two with zero collisions—and it does not identify the plaintext codec.

Retain **primer/initial-state selection** as a possible construction detail,
not a new decryption mechanism. Do not search those 86 phase pairs for
language without an independent crib or rule selecting one of them. The Eye
adjacent-difference/common-block transfer was already performed and was
negative; this result does not justify repeating it.

Reproduction:
[`audit_sdlwdr_cipher4_collisions.py`](../scripts/audit_sdlwdr_cipher4_collisions.py).
