# Discarded A–Z initial-state audit — freeze

## Lead

In a read-only `silmä-cryptography` message from 9 January 2026, Lymm proposed
that the deliberately awkward 26-trigram render width may instruct an
unwritten initialization pass: encrypt `A-Z`, possibly in the Trailer Altar
keyed order, discard those outputs, and begin the visible Eye ciphertext from
the resulting state.

Source:
<https://discord.com/channels/453998283174576133/817530812454010910/1459246201940738193>

This exact construction was not found in the repository. Existing keyword
searches place a keyword directly into the initial deck; they do not execute
26 cipher updates and discard their outputs.

## Frozen interpretations

The ordinary alphabet and the exact already-audited Trailer Altar order
`ABDMGICRTKEFHJLNOPQSUVWXYZ` give three directional readings:

1. standard `A-Z` positions `0..25`;
2. keyed letter order expressed as standard `A-Z` positions;
3. standard `A-Z` expressed as positions in the keyed order.

No reversals, rotations, per-message sequences, digits, or invented keywords
are admitted.

The canonical empty warm-up is reported beside the three candidates as a
control. It is not counted as another interpretation of the lead.

## Frozen cipher families

1. The four structured affine-GAK multiplier families already used by
   `search_affine_gak.py`, with visible marker modes `full`, `skip`, and
   `primer`.
2. Every affine `F83` base plus every named 83-card base from
   `standard_base_candidates`, followed by the existing plaintext-selected
   top swap. The marker is either ordinary (`full`) or excluded without a
   state update (`skip`).

Each message receives the same reset and the same deterministic 26-step
warm-up. Arbitrary `S83` operations and optimized plaintext are forbidden.

## Promotion gate

Both warm-up implementations must first recover a planted continuation that
the canonical reset does not. On the Eyes, a candidate must decode all frozen
repeated-plaintext contexts with zero mismatches. Fewer than 37 decoded
symbols is supportive but cannot rescue any mismatch. A nonzero optimum
rejects only these bounded operation families, not arbitrary GAK/XGAK or the
general possibility of an unwritten initializer.
