# Native Eye call-graph census — 2026-07-30

## Scope

This is a read-only comparison of the installed `noita.exe` and
`noita_dev.exe`, going beyond the earlier packed-row and five-frame-atlas
checks.  It asks whether another native entry point, a debug-only branch, a
seed/coordinate input, or PE metadata could alter the Eye values at runtime.
The binaries and the CrossOver installation were not modified.

The reproducer is:

```text
PYTHONPATH=src:scripts python scripts/audit_binary_callgraph.py \
  "/path/to/noita.exe" "/path/to/noita_dev.exe"
```

For instruction context, the same build can be inspected with:

```text
objdump -D -Mintel --start-address=0x61e880 \
  --stop-address=0x620220 "/path/to/noita.exe"
```

The first command uses direct `E8 rel32` edges only.  It does not pretend to
recover optimized C++ function names from the unavailable PDB.

## Build and symbol metadata

| build | SHA-256 | COFF timestamp | CodeView record |
|---|---|---|---|
| `noita.exe` | `808d2a0ab51ea0b46e9ad2aeb3327a4b0ce3feae04f32ba26326bf585b5779bd` | `0x6794ee3c` = 2025-01-25 13:59:24 UTC | GUID `1d4e62673b7e5c42994a84880a48f02b`, age 1 |
| `noita_dev.exe` | `d2f7dbeff72b785bdadd068870343d2821cf4bd2f6c58125fe6a90a1b0900285` | `0x6794ed4f` = 2025-01-25 13:55:27 UTC | GUID `ba0417e33fd24441a0a4b07b1fb3ce31`, age 1 |

Both CodeView records point to the same build-machine path,
`D:\Projects\NollaGames\FallingEverything\Build\VC12\ReleaseUnity\falling_everything.pdb`.
That PDB is not present in the local installation, and neither PE exposes a
useful public symbol table.  The dev executable is therefore a real build
control, not a symbol-rich source reconstruction.

## Release call graph

The exact direct edges in the release build are:

```text
0x620129  -> 0x61ed60   message initializer (the only direct caller)
0x61fe2e  -> 0x61ec60   renderer (the initializer's only renderer call)
0x61ecd1  -> 0x61e880   five-frame atlas setup
0x61ece0  -> 0x61eaf0   row/character parser
0x61ecf0  -> 0x61e5c0   draw/emit routine
```

Each of `0x61e880`, `0x61eaf0`, and `0x61e5c0` has exactly one direct caller,
the renderer at `0x61ec60`; no other direct call sites occur in the `.text`
section.  The initializer's direct callees are the vector append helper,
the generic unsigned division helper, formatting/string helpers, the single
renderer edge above, and cleanup/security-cookie code.  There is no second
initializer, alternate panel loop, or direct edge from a debug subsystem.

At `0x61ed60`, the first instructions copy `EDX` and `ECX` to stack locals and
read the third argument (`[EBP+8]`) as the panel selector.  Its branches are
the nine static panels; the packed words are then appended to a local vector.
After construction, the loop at `0x61fd20` divides each 64-bit word by the
literal divisor 7, emits base-seven digits, and calls `0x61ec60`.  No world
seed, RNG state, file input, locale, or player coordinate is read by this
initializer.  The renderer receives only `(x, y, message-string)`; its parser
maps bytes `'0'..'4'` to the five direction values and `'5'` to a row break.

This is a stronger negative than a raw constant search: there is one native
producer, one native consumer, and the consumer's complete local dataflow is
position/panel plus the static corpus.  The calls to the generic helpers are
ordinary string/vector/allocator operations, not hidden cipher state.

As a separate indirect-call check, the raw image contains no little-endian VA
or RVA pointer for any of the five Eye functions (`0x61ed60`, `0x61ec60`,
`0x61e880`, `0x61eaf0`, `0x61e5c0`).  Thus there is no obvious function-pointer
table or relocation-backed alternate entry that the direct `E8` census would
miss.

## Dev-build control

The dev executable has zero hits for all fourteen instruction-aware atlas
signature fields (the five obfuscated words plus XOR/add masks).  It also has
no contiguous 150-word packed-row initializer.  Its only direct native
strings relevant to this audit are ordinary shared assets and achievement or
debug names:

```text
data/particles/eye.xml
ThreeEyesAreWatchingYou
SecretsOfTheAllSeeing
DEBUG_TEST_SYMBOL_CLASSIFIER
```

The Eye XML reference is in a generic particle/gameplay routine, and the two
achievement strings are used by the same statistics/achievement code in both
builds.  Neither is an Eye-message decoder.  The dev binary retains many
source-path and debug-setting strings, but no Eye corpus, atlas signature,
trigram/rank table, or decryptor-specific string.

## PE resources and hidden branches

Both executables have the same ordinary PE shape: `.text`, `.rdata`, `.data`,
detour/TLS sections, a small `.rsrc`, and relocations.  The resource root has
one `RT_MANIFEST` (type ID `24`) with a standard XML application manifest; no
icon, version-info payload, custom data resource, or embedded script carries
Eye data.  The CodeView debug directory contains only the RSDS record above.

The imported DLL set is also ordinary engine/runtime support (`KERNEL32`,
`USER32`, `lua51`, `SDL2`, `fmod`, Steam, sockets, and C/C++ runtimes).  The
dev build additionally imports `dbghelp.dll` for crash dumps.  Neither image
imports a cryptography library or a separate data/decoder DLL.

The only unusual debug-adjacent string found in both builds,
`DEBUG_TEST_SYMBOL_CLASSIFIER`, is a configuration/debug toggle.  Its xrefs
lead to debug-settings registration and lookup; it is not referenced by the
Eye renderer or initializer call chain.  No Eye-specific strings matching
`cipher`, `trigram`, `glyph`, `checksum`, `Finnish`, `Kalevala`, or a decoder
name occur in either native image; generic engine strings such as `message`
are abundant and are not evidence for the Eye path.

## Result and boundary

This sweep finds no alternate native Eye producer, hidden dev-only renderer,
runtime key/seed input, PE resource payload, or debug branch that could change
the nine displayed messages.  It does not prove how the corpus was authored:
the only remaining binary avenue is an unavailable historical/offline source
or an earlier build whose executable is not in the installation.  Any future
binary lead therefore needs a pre-release executable, PDB, or source artifact;
more disassembly of these two 2025 images is unlikely to reveal the cipher
key.
