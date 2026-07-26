# Forty-fourth pass — read-only Silmä delta

## Scope

Read-only review of recent `silmä-cryptography`, `silmä-novel`, and linked
messages, focused on independent numeric carriers, allocator rules, and
construction provenance.

No messages, reactions, calls, or other Discord actions were sent.

## 1. No new allocator was supplied

Recent messages in `silmä-teollinan-älly` describe Eye isomorphs as a role
program that allocates temporary numeric identities and later fetches them.
The surrounding discussion is appropriately skeptical:

- the proposed “root allocator” was an AI-generated interpretation;
- no reason was given that it corresponds to plaintext;
- no rule was supplied that selects first-seen ranks.

This matches the local identifiability result. A role trace can preserve
equality while renaming values, but it does not generate the approximately
153.6 bits needed to select the observed 25 fresh ranks.

## 2. Non-transitive XGAK is now better defined, not more identified

On 25–26 July 2026, `silmä-cryptography` clarified a non-transitive XGAK as
several independent ciphertext orbits/decks. The worked example uses decks of
sizes five and three, with plaintext choosing which deck rotates. The state
group is `C5 × C3`, and different orbits have different point stabilizers.

This is useful formal vocabulary. It does not currently yield an Eye test:

- no Eye alphabet partition is selected;
- no output-index or plaintext schedule is supplied;
- ciphertext reconvergence is already known not to identify XGAK actions;
- the arbitrary initial order in each orbit retains the missing numeric
  information.

A multiple-orbit model should not be fitted until an in-game object, practice
cipher, or plaintext anchor independently selects the orbit partition and
operations.

## 3. Developer attribution narrows later-clue archaeology

A linked message in `noita-spoilers` is materially stronger than community
speculation. On 27 July 2023, the account `NollaArvi`, carrying the
`Noita Developers` role, said that his own additions would not concern the
Eye or cauldron mysteries, adding:

> if something about them gets added, it'll be Petri's work

This does not prove who created the October 2020 ciphertext. It does narrow
later decoding-clue archaeology: additions intended to extend the Eye or
cauldron mysteries should first be tested for Petri Purho authorship or
ownership. Gate Guardian, later RNG salts, and other post-Eye assets gain
evidentiary value only if their Petri provenance and executable relation can
be established.

## 4. Void-liquid render layer

Recent `silmä-novel` discussion notes that void liquid is rendered on a
different layer from ordinary materials and behind many backgrounds. This is
a concrete engine property but not yet an Eye carrier. It may matter when
reconstructing the Cessation/cauldron visual route; it supplies no numeric
schedule by itself.

## Decision

The delta produces no decoder or fresh-value carrier. It does produce one
high-value provenance lead: audit Petri-specific post-Eye additions and
construction habits, rather than treating every later Noita asset as equally
likely to be an intended clue.
