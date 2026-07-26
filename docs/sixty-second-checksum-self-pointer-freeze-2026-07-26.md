# Sixty-second pass — checksum-quotient self-pointer freeze

## Question

The complete orthodox trigram sums of the three odd-East messages are:

```text
E1  4040 = 40 * 101
E3  5656 = 56 * 101
E5  4545 = 45 * 101
```

Call the integer quotient `q`. Does each message contain its own `q` at a
position whose distance from `q` names an independently established
construction quantity?

This is a self-pointer test, not a plaintext test. The quotient is derived
from the already known mod-101 checksum and the coordinate is the accepted
zero-based full-array index, including the first glyph at position zero.

## Observed discovery record

All occurrences of `q` are:

```text
message  q   zero-based positions  absolute |position-q|
E1       40  27,33                 13,7
E3       56  45,69,118             11,13,62
E5       45  75                    30
```

The discovered selection is therefore:

```text
E1  40 - 33 = 7    row-2 phase-width budget
E3  56 - 45 = 11   final clean-repeat gap
E5  75 - 45 = 30   late common-phase length
```

The quantities `7`, `11`, and `30` were established before this observation.
However, choosing one occurrence per message, taking absolute rather than
signed distance, assigning the three quantities to messages, and choosing
this particular three-quantity subset were retrospective.

## Frozen statistics

Let `D_m` be the set of absolute distances `|position-q_m|` over every body
occurrence of `q_m`.

1. **Exact typed event**

   ```text
   7 in D_E1 and 11 in D_E3 and 30 in D_E5
   ```

2. **Three-target permutation event**

   The three messages can be bijectively matched to the three fixed targets
   `{7,11,30}`, with each matched target present in that message's `D_m`.
   This charges the assignment of targets to messages and every occurrence
   choice.

3. **Construction-ledger calibration**

   Report each observed distance against this fixed list of previously used
   structural lengths:

   ```text
   6,7,9,11,15,16,17,18,20,21,25,26,28,29,30,34
   ```

   This is descriptive calibration only. It cannot promote the lead because
   the list is broad and contains correlated quantities from the same
   construction record.

## Conditional null

For each message independently:

- keep the first glyph fixed;
- keep the full trigram multiset and therefore the full sum and quotient;
- condition on the observed number of body occurrences of `q`;
- place those occurrences uniformly without replacement among all body
  positions.

Only the positions of `q` affect these statistics, so this conditional
position model is exactly equivalent to the relevant part of a uniform body
shuffle. Enumerate the small position-subset spaces exactly rather than use a
Monte Carlo estimate.

## Decision rule

This pass can retain a checksum self-pointer as a serious construction lead
if the exact and permutation events are rare under their stated conditional
null. It cannot promote a decoder or a fully authored `7|11|30` record without
an independent rule explaining:

- why these three structural quantities are the consumers;
- why absolute distance is used;
- why E1/E3 use `q-position` while E5 uses `position-q`.

No alternate modulus, indexing convention, quotient family, target subset,
or nearby position may be scanned in this pass.

## Secondary coordinate-graph freeze

This section records a second observation made after executing the primary
`7|11|30` audit but before executing any control for this graph statistic.
It is not independent of the distance result because it uses the same
occurrence positions.

The positions selected above are themselves members of established typed
field classes:

```text
E1 quotient positions 27,33  = two members of final headers {27,77,33}
E3 quotient position 45      = one member of checksum quotients {40,56,45}
E5 quotient position 75      = one member of final anchors {75,81,48}
```

Freeze three field sets:

```text
H = {27,77,33}  final-row headers
Q = {40,56,45}  odd-East checksum quotients
A = {75,81,48}  final-row gap-11 anchor labels
```

Report:

1. **Exact typed coordinate event:** every E1 quotient occurrence is in `H`,
   at least one E3 occurrence is in `Q`, and at least one E5 occurrence is in
   `A`.
2. **Any-hit assignment event:** after allowing all six assignments of
   `H,Q,A` to `E1,E3,E5`, every message has at least one quotient occurrence
   in its assigned field set.
3. **All-hit assignment event:** after the same six assignments, every
   quotient occurrence in every message lies in its assigned field set.

Use the same exact conditional position null. The any-hit event corrects the
typed field assignment and occurrence selection. The all-hit event measures
the unusually specific fact that both E1 occurrences are final headers, but
is not a fair replacement for the any-hit result because the all-occurrences
rule was noticed from E1.

This graph may justify the three primary distance consumers only if it
survives assignment correction. It still cannot be counted as independent
evidence or multiplied by the primary probability.

## Tertiary all-occurrences packet freeze

This section records a cleaner formulation noticed after the coordinate-graph
audit but before executing packet controls. It uses every quotient occurrence
and therefore makes no within-message occurrence selection.

Reduce a full-array position modulo 83 and define its shortest circular
distance from the quotient:

```text
d83(position,q) = min((position-q) mod 83, (q-position) mod 83)
```

The mod-83 circle is independently established by the final gap-anchor
record. In stream order the complete distance packets are:

```text
E1  (13,7)
E3  (11,13,21)
E5  (30)
```

Every value belongs to this fixed pre-observation ledger of executed
state-machine scalars:

```text
3,4,6,7,11,13,15,17,20,21,25,28,29,30,34
```

The ledger includes the `+3/+4` operators, row-2 phases `6/7`, gap `11`,
return increment `13`, terminal class `15`, common phase `17`, bridge widths
`20/21`, registered context width `25`, positions `28/29`, late phase `30`,
and source boundary `34`.

The packet sums are:

```text
E1  13+7       = 20  E4 bridge width
E3  11+13+21   = 45  E5 checksum quotient
E5  30         = 30  late common-phase width
```

Freeze:

1. **Ledger containment:** all six circular distances lie in the fixed scalar
   ledger.
2. **Exact typed packet sums:** the three sums are exactly `(20,45,30)` in
   `(E1,E3,E5)` order.
3. **Packet-sum permutation:** allow all six assignments of the fixed target
   multiset `{20,45,30}` to the three message packets.

Enumerate the same conditioned quotient-position subsets exactly. The packet
statistics are retrospective and are not independent of the earlier
distance and coordinate observations. Their value is mechanistic: unlike the
primary test, they consume every occurrence and produce a compact candidate
payload.

Do not scan another modulus, directed distance, raw distance for E3's final
occurrence, alternate aggregation, target sum, or scalar ledger in this pass.

## Six-panel holdout freeze

Before inspecting them, apply the same extractor without alteration to the
six messages whose sums do not close modulo 101:

```text
W1,E2,W2,W3,E4,W4
```

For each, use Euclidean division `full_sum = 101*q + r`, locate every body
occurrence of the integer quotient `q`, and emit the same shortest circular
mod-83 distances.

Report:

- quotient, remainder, occurrence positions, and complete distance packet;
- whether the packet is nonempty;
- whether every emitted distance belongs to the already frozen machine-scalar
  ledger;
- the conditional probability of the observed all-distance containment,
  given each observed quotient-occurrence count.

Do not derive a new packet-sum target from the holdout remainders. If any
message has no quotient occurrence or emits an out-of-ledger distance, the
universal nine-message form fails. That does not refute a typed odd-East
checksum subsystem, because only the odd-East messages have zero remainder.

## Header-residual interpretation freeze

This interpretation was noticed after the all-occurrences packet audit and
before executing its assignment correction. It is algebraically the same
exact event as the typed packet sums, not additional evidence.

Subtract each packet sum from its message's already established first glyph:

```text
E1  50 - 20 = 30  late common-phase width
E3  63 - 45 = 18  hidden modulus gap, 101-83
E5  33 - 30 = 3   Gate/phase repair operator
```

Freeze:

1. the exact typed residual vector `(30,18,3)`;
2. a broad residual-assignment event allowing all six assignments of the
   fixed residual set `{30,18,3}` to headers `(50,63,33)`.

For each assignment, the target packet sum is ordinary integer
`header-residual`. Do not use modular subtraction, change the header set,
introduce another residual, or count the exact result separately from the
already reported packet-sum event.
