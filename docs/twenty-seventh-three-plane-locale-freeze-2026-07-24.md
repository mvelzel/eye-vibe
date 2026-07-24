# Twenty-seventh pass — three-plane calling-code / locale freeze

## New observation

Treat all three eye coordinates symmetrically. For each coordinate plane,
lay its nine digits out in canonical 3×3 engine order and sum down the three
columns. The resulting decimal rows are:

```text
first-eye plane   6,8,3  -> +683  Niue       region NU
middle-eye plane  0,3,4  ->  +34  Spain      region ES
third-eye plane   3,5,8  -> +358  Finland/
                                      Åland   regions FI, AX
```

The [ITU E.164 assigned-code list](https://www.itu.int/itudoc/itu-t/ob-lists/icc/e164.pdf)
contains `+683`, `+34`, and `+358`. The scalar third plane is also the only
plane with the already fixed one-cycle BWT payload `!Fi`.

This was noticed after `+358`; it is not independent evidence and is not
assigned a discovery p-value. The useful next question is generic rather than
target-specific:

> Across the frozen graph-conditioned scalar assignments, does a plane's
> column-sum calling code name the same region as its fixed-trail BWT suffix?

## Fixed calling-code map

Use the generated `CountryCodeToRegionCodeMap.java` from Google's
libphonenumber at commit:

```text
f7e3e88c92b905c8d6edb81f336dbe25edc05b52
```

Source:
`java/libphonenumber/src/com/google/i18n/phonenumbers/CountryCodeToRegionCodeMap.java`.
It maps each assigned calling code to one or more two-character region codes;
notably `358 -> (FI,AX)`. Vendor the generated factual map with its Apache-2.0
provenance so the audit is reproducible and network-free. Non-geographic
region `001` cannot match a two-letter suffix.

No country name, language model, or hand-selected list is admitted.

## Frozen conditional universe

Reuse exactly the twenty-fifth graph-conditioned assignments:

1. hold every first/second header digit at its observed message coordinate;
2. assign the multiset `001122334` to the nine third-digit slots;
3. reconstruct orthodox ranks and retain only all-in-`0..82`, nine-distinct
   assignments;
4. retain the East-5-first trail, stable LF mapping, and primary row zero.

The expected universe is again 12,096 assignments.

## Decimal parser

For a 3×3 third-digit grid, calculate the three ordinary column sums. A view
is eligible only when every sum is one decimal digit `0..9`. Parse the three
digits as one integer, allowing leading zero solely as fixed-width padding:
`034 -> 34`.

An eligible code is geographic when the fixed map has at least one
two-letter region. The BWT text is eligible only after the existing
single-cycle and `0..82` filters and when its final two ASCII characters are
letters.

The primary semantic event is:

```text
upper(BWT text[1:]) is one of the regions assigned to the column-sum code
```

The first BWT character is not interpreted. Report separately how many
semantic matches also have the observed exclamation mark.

## Registered geometry and factoradic cross-checks

For every admissible assignment, report:

- natural-view assigned geographic codes;
- natural-view BWT texts with two-letter suffixes;
- natural semantic matches;
- natural semantic matches beginning `!`;
- the same semantic events when any of the eight D4 grid views may provide
  the code;
- the codes, regions, and BWT texts of every semantic match.

Then apply the unchanged full factoradic predicate and report the same fields
for its two expected survivors. No new factoradic condition is added.

The natural semantic match is primary. D4 is the single registered geometric
broadening. Exact `358`, exact `Fi`, and the three-plane country triple are
descriptive consequences rather than separate tails.

## Calibration and stop

Synthetic tests must cover:

- leading-zero parsing (`034 -> 34`);
- multi-region matching (`358 -> FI,AX`);
- rejection when a column sum exceeds nine;
- case-insensitive region comparison;
- natural and D4-only matches.

This audit can promote only a locale-check interpretation of the marker
payload. It cannot prove Finnish body plaintext or license a key.

If the observed assignment is not unique under the natural generic semantic
event, retain the exact `!Fi/+358` observation but close the broader checksum
claim. If it is unique, record that as structural corroboration with the same
post-hoc warning; do not multiply it by prior counts.

No enumeration result was inspected before this freeze.
