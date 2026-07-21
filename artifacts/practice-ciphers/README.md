# Read-only practice-cipher fixtures

## Qualia's `2-to-26 deck cipher`

`deck_cipher_binary_stripped.json` was downloaded from the attachment in the
read-only [Discord practice thread](https://discord.com/channels/453998283174576133/1529154097729769472),
posted by Qualia on 21 July 2026.  It contains nine ciphertext strings and no
plaintext or key.

```text
bytes: 3221
sha256: 1f0f10ffc3999fe4c470a87af296f22bebcb5e9b8772e7d4e20060db4cbd95d4
```

The author's stated model has a binary plaintext alphabet, a 26-card
ciphertext alphabet, one arbitrary initial hidden-state permutation, and one
arbitrary `S26` operation for each plaintext bit.  The binary streams encode
natural English sentences over a 27-symbol alphabet.  The serialization from
that alphabet to bits is not yet established locally.
