# Practice cipher 3 — mechanism breadth freeze

## Why reopen it

The only deeply tested model for sdlwdr cipher 3 was

```text
c[i] = P^i(S[p[i]]).
```

That position-progressive premise was introduced by this project, not located
in an author hint. Its single-`C83` form is exactly impossible and its two
fixed multi-cycle relaxations look poor under a calibrated heuristic. Those
results do not justify treating the puzzle itself as a progression cipher.

Cipher 3 contains eighteen author-labelled reset streams in three length
groups, A/B/C. Like the other sdlwdr exercises, it uses all 83 ciphertext
labels and has no adjacent doubles. The solved exercises provide several
different *methods*, not one presumed shared key. This pass tests those methods
side by side before deepening any favorite.

The available Discord session currently requires a fresh login. The locally
preserved public input remains the ciphertext attachment, its A0 correction,
and the absence of a locally recorded author mechanism hint.

## Frozen horizon

| Lane | Exact finite question | Promotion gate |
|---|---|---|
| **A. Recovered `C82` wheel transfer** | Map every non-`J` label through the exact 82-position ciphertext wheel independently recovered from sdlwdr ciphers 1 and 2. Enumerate traversal direction, the two parity sheets, and bounded `J` control semantics (ignore/emit, parity flip, direction flip, accumulator reset). Select the global semantics on group A while allowing only a per-message plaintext-wheel rotation; score B/C once. | A complete-family heldout tail below `.01`, readable text in more than one group, and exact replay under one control schedule. A best per-message rotation is charged inside every control. |
| **B. Standard `C83` action stream** | Apply both standard-order adjacent differences and accumulations used to expose cipher 4. Screen every contiguous quotient width `2..42`, selecting only on A and measuring the same frozen frequency/serial-dependence statistics on B/C. | The selected width must replicate on B and C under global-label controls and expose either a bounded second state or readable output. A conspicuous factor alone fails. |
| **C. Fixed position drift** | On each of the known `C82` and standard `C83` coordinates, remove every linear position drift `k*i`, both signs, with true reset-relative positions. Select `k` on A by decoded support and score the number of heldout B/C states without refitting. | At most 42 heldout states and an exact planted recovery. This is a fixed-coordinate test, not another arbitrary-permutation progression solver. |
| **D. Standard physical deck updates** | Exhaust the existing named 83-card base dictionary and the seven selected-card updates. Decode all streams from reset. Select a single base/action/marker policy on A by rank support and score B/C without changing the model. | Every heldout rank must lie in `0..41`, followed by readable text or exact source compatibility. In-sample small support fails. |
| **E. Cipher-5 recursive operation transfer** | Use the exact solved recursive increasing-chunk reversal as the 83 plaintext-selected updates, under the identity/raw order and the independently recovered cipher-1/2 wheel order. Test emit-then-update and the uniquely decodable update-before-emission convention. | One global convention must keep all eighteen streams inside the known 42-symbol plaintext alphabet and replay exactly. Partial low-rank mass fails. |
| **F. Label-invariant isomorph maps** | Inventory repeated equality patterns without numeric labels. Convert independent occurrence pairs into partial bijections, compose compatible maps, and ask whether one low-order operation predicts heldout edges or exceptional positions. | A map must predict an edge not used to construct it and beat frequency/no-double matched position controls. Describing an in-sample cycle is insufficient. |
| **G. Source/language closure** | Only after A–F selects a finite action stream, test the solved 42-character plaintext ordering and broad English/Finnish source fingerprints. | Language ranks candidates but cannot create the mechanism. A solve requires readable full plaintext plus re-encryption, source confirmation, or author confirmation. |

## First mixed batch

The first implementation batch is A, C, D, and E:

1. the known 82-wheel is the strongest cross-puzzle construction transfer;
2. fixed drift distinguishes that concrete transfer from the discarded
   arbitrary progression premise;
3. physical selected-card models generalize the previous one-message scan to
   a train/heldout corpus test;
4. the solved recursive update is an exact, unrelated dynamic-deck family.

Lane B and the label-invariant lane F remain active regardless of first-batch
failure. No language optimizer may be introduced until a mechanism predicts
heldout structure.

## Controls and stop rules

- A is training; B and C are held out. Per-message resets and rotations allowed
  by the model are rerun inside every control.
- Global label permutations preserve all message lengths, label frequencies,
  reset points, and absence of adjacent doubles. When a distinguished `J`
  control is tested, its positions are held fixed and the other 82 labels are
  permuted.
- Every dynamic-deck candidate is replayed from reset. A plaintext-range hit
  is necessary but not sufficient.
- A lane closes after its exact heldout gate fails. Parameters may not be
  repaired from B/C.
