# Eighteenth wide horizon — the final-row anchor record

## Why widen now

A recent Discord observation has survived three independently structured
control families. In the final message row:

```text
clean gap-11 anchors       a = (75,81,48)
trimmed positions          p = (16,18,17) = 16 + (0,2,1)
markers                    h = (27,77,33)

h_E4 = a_E4-a_E5 = 27
h_W4 = a_E4-a_W4 = 77
h_E5 = a_W4-a_E5 = 33
h_E4 = h_W4+h_E5 mod 83
```

The broad matched-body tail is `.001119978`; body-only and joint global-label
tails are `.001999960` and `.000079998`; the broad joint position tail is
`.0000199996`. These tails share anchors and are not multiplied.

This is the first well-calibrated consumer of both the full marker values and
a marker-derived component order. It warrants depth, but the user explicitly
asked novel work to start wide. The map below separates plausible consumers
before another rule is fitted.

## Exact algebraic form

The markers are a discrete gradient of three vertex labels:

```text
      [ 1  0 -1 ]             [27]
B a = [ 1 -1  0 ] [75,81,48] =[77]  mod 83
      [ 0  1 -1 ]             [33]
```

`B` has rank two and `h_E4-h_W4-h_E5=0`. Equivalently, W4 and E5 carry two
path increments and E4 carries their telescoping endpoint difference.

Independently, the first six marker control edges enumerate both orientations
of the complete three-vertex cycle:

```text
row 1: 0->1, 1->2, 2->0
row 2: 0->2, 2->1, 1->0
```

The final row is `0->0,0->2,1->0`; W4's `0->2` edge names component order
`021`, exactly the anchor-position rank order.

## Wide map

| Lane | Different object | First falsifiable test | Promotion gate |
|---|---|---|---|
| **A. K3 coboundary record** | The nine markers describe vertices, directed edges, and a final exact 1-coboundary/check record. | Enumerate only incidence maps selected by the established six control edges and final self/edge types. Ask whether one convention explains both the numeric gradient and `021` position order without an arbitrary edge permutation. | The convention must predict one unused sign, edge assignment, or anchor field. Merely rewriting the observed subtraction matrix fails. |
| **B. Row-typed landmark records** | Opposite-cycle rows and the final self/edge row use different check schemas over equality-selected body landmarks. | Derive one canonical landmark selector per header topology from the existing prefix/isomorph tree, then train no arithmetic menu on the values. | A topology-selected schema must predict withheld anchors in another row under complete selector controls. The final row alone is not enough. |
| **C. Synchronizing 11-loop** | `A..........A` is a designed state-return probe: all three machines return to the same visible state after 11 steps, at header-ordered start offsets. | Treat the three windows as reset-local loop traces. Test whether their internal equality/transition exits predict later strong isomorph entry or exit states. | One loop-state model must predict a later undisclosed edge in all three panels. A common gap length alone fails. |
| **D. Override/control symbol** | One of the ten interior events is an Alberti-like control symbol that collapses or overrides hidden state; it is discarded in plaintext. | Locate candidate state-change breakpoints using only changes in cross-window partial bijection consistency, not numeric labels. Withhold one panel. | The same event class must predict where another isomorph breaks or reconverges. Per-window breakpoint fitting fails. |
| **E. Index/value pointer record** | Marker, anchor, and endpoint values form addresses rather than prose symbols. | Inventory exact index=value and cross-panel pointer equalities among the frozen landmark fields; compare with controls that reselect all gaps and index conventions. | A pointer chain must predict one destination not used to choose its convention. Nearby-number anecdotes fail. |
| **F. Gate binary-operator diagram** | The later Gate deliberately depicts the now-established interface: two side increments combine into one central total, with an upper control/order component. | Freeze the raw four-part topology only: Molari/Mokke as two inputs, Veska as result, Seula as control. Map the final record by panel type before consulting sprite micro-marks. | The topology must predict an unused marker/position role or one of the unresolved Gate record fields. It is corroboration, not an independent p-value. Unpublished masks remain inadmissible. |
| **G. Cessation/cauldron operation mask** | The confirmed void-day cycle supplies a binary schedule selecting which edge/check operation is active. | Use the exact published schedule only as a selector over the finite K3/check interfaces, never as an 83-number key. | It must select gap, orientation, or row type prospectively and predict a heldout field. `83`/`39` numerology fails. |
| **H. Ten-unit source frame** | The ten singleton interiors are one plaintext unit; the length echoes the ten-symbol `THAT WHICH` isomorph. | First derive a state/control invariant from C/D, then compare the interiors to the already frozen ten-symbol equality class. | It must predict a second source-aligned window and exactly re-encrypt. Length/theme alone fails. |
| **I. Dual-use factoradic byte** | Each marker simultaneously encodes an S3 control edge in its leading digits and a mod-83 check value as a whole. | Build the minimum finite transducer that consumes `(edge,third digit)` and emits the observed record role. Select only on the first two marker rows. | It must predict all three final roles, including which marker carries total versus increment and which supplies `021`. |
| **J. Authored conformance generator** | The bodies are test vectors deliberately planted with loops, prefix probes, and check records rather than encrypted prose. | Extend the maximum-entropy null to preserve copied prefixes and known isomorphs, then ask whether the new anchor record arises without an explicit check constraint. | A generator promotes only if it predicts another unfit statistic; it cannot provide plaintext. |
| **K. In-game operation vocabulary** | Known puzzles teach typed operations—cycle selection, reset, mirror, and binary combination—used to read this record. | Complete the operation catalog by arity/state timing, then compare whole interfaces against A–I. | One confirmed schedule must execute on heldout Eye fields without a panel-specific repair. |
| **L. Version/author archaeology** | A later asset restates the record interface more clearly than the original Eye renderer. | Compare first Gate/Cessation revisions with the final record's arity, direction, and timing, respecting that later decoder hints are chronologically allowed. | A version delta must select an operation or role not inferred from the Eye result itself. |

## Ranking before depth

| Lane | Evidence fit | Falsifiability | New information | Independence | Priority |
|---|---:|---:|---:|---:|---:|
| A. K3 coboundary | 5 | 5 | 5 | 4 | **19** |
| B. row-typed records | 5 | 4 | 5 | 4 | **18** |
| C. synchronizing loop | 5 | 4 | 5 | 3 | **17** |
| F. Gate operator topology | 4 | 4 | 5 | 3 | **16** |
| I. dual-use byte | 5 | 3 | 4 | 3 | **15** |
| D. override symbol | 4 | 4 | 4 | 3 | **15** |
| E. index/value pointer | 3 | 5 | 4 | 3 | **15** |
| J. conformance generator | 4 | 4 | 4 | 3 | **15** |
| K. operation vocabulary | 4 | 3 | 4 | 3 | **14** |
| L. archaeology | 4 | 4 | 4 | 2 | **14** |
| G. cauldron selector | 3 | 3 | 4 | 3 | **13** |
| H. source frame | 3 | 3 | 4 | 2 | **12** |

## First action and stop rules

Start with A, but only as a finite diagram audit. Freeze the incidence
conventions selected by the already established marker edges, self edge, and
component orders. It may not scan arbitrary `3x3` matrices after seeing the
anchors. A useful A result must predict a role or sign beyond the displayed
three difference equations.

Then move to B/C in parallel conceptually: B asks whether other row topologies
have their own equality-selected records; C asks whether the final clean
repeat is an executable state loop. Do not search source text until one
machine invariant survives.

The Gate is no longer dismissed: its two-input/control/output topology now
matches a real Eye interface. Its raw code still does not execute the dossier's
Type4/Type6 cache machine, and missing masks or fresh-value rules remain
missing. The new result upgrades the modest topology lead, not the entire
theory.
