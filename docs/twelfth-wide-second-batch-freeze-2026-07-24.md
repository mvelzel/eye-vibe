# Twelfth wide horizon — second lateral batch freeze

## Why this batch

The first five novelty screens are negative. Per the original stop rule, this
batch changes mathematical object again instead of adding parameters to those
models. It uses the next five lanes named before the first results were known.

## Frozen tests

| Lane | Exact test | Control and promotion gate |
|---|---|---|
| **F. Visible symbols as line-digraph edges** | Make two nodes `tail(v)` and `head(v)` for each visible label. Every observed transition `u->v` imposes `head(u)=tail(v)`. Compute the equality closure, the number of hidden-state components, and every absent transition that the closure falsely forces. Then train on the independently defined P-header triple and predict new transitions in the six Q panels. | Compare the P→Q precision/recall with all 84 choices of three intact training panels. Exact line-digraph support requires zero forced absent edges; promotion additionally requires the P split to rank in the top 1%. |
| **H. Rejected raw phases** | At every accepted-glyph boundary form the two crossing base-5 trigrams at raw offsets one and two. Freeze the only special indicator as membership in the unused `83..124` range. Count it at the nine marker/body boundaries and at authored row-pair boundaries, separately by phase. | Independently rotate each complete phase-indicator tape within its panel, preserving counts and autocorrelation; use the maximum of the two phases in every control. Also compare total hidden-range occupancy with within-visual-row direction shuffles. Promotion requires corrected familywise tail below `.01` and replication between marker and row boundaries. |
| **I. Nine-panel affine-plane design** | Put the nine panels on a 3×3 `AG(2,3)` grid. For each aligned body column after 25, compute the sums on the three parallel lines in each of the four directions; record when all three sums agree over `F5` and `F83`. Enumerate row order and independent within-row orders consistent with the three natural message rows, choosing a grid on columns 25–60 and scoring it on 61–97. | Shuffle the nine intact values within each column and repeat the complete grid selection. A natural-grid curiosity is descriptive; promotion requires the training-selected grid to predict held-out line classes at corrected tail below `.01`. |
| **J. Bounded physical shuffle actions** | Freeze a named action dictionary on 83 positions: all cuts, reversal, the four odd-deck interleaves, four Monge variants, Josephus deals, their inverses, and powers through eight of the eight interleave/Monge generators. Score whether one common action, or any action per context, completes the seven nonliteral partial maps. | Shuffle targets within each fixed context domain/image and rerun the whole dictionary. Promotion requires at least one exact nonliteral context plus an exceptional common-action held-out score; best partial agreement alone fails. |
| **K. Tiny header-controlled transducer** | Use the independently established `P / Q-west / Q-east` header partition as a three-valued control. A two-register deterministic machine sees the previous two raw eye directions and predicts the next direction from a shared majority table trained on the other two panels in its header class. Evaluate only after each panel's established deepest prefix-leaf exit. | Rank this grouping among all 280 partitions into three triples, with the same fixed suffix starts and deterministic tie/default rules. Also compare with leave-one-out training on all other panels. Promotion requires a top-1% partition rank and suffix accuracy above the unconditioned model. |

## Restrictions

- F tests an exact support factorization, not an arbitrary graph drawing.
- H does not inspect shapes made by the rejected values and does not add
  thresholds after seeing the result.
- I does not choose a modulus outside `5,83`, move the column split, or use a
  degree-nine interpolation.
- J does not add a shuffle named after inspecting a winning permutation.
- K predicts raw five-way directions, not literal 83-symbol plaintext, and its
  suffix starts are frozen from the existing prefix tree.
- Complete all five screens before returning to any survivor.
