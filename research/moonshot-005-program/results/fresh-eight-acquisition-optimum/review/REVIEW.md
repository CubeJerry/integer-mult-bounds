# Independent review: fresh-eight line-return gate

**Result:** the exact line-support geometry and the fixed-m price comparison pass independent replay. The temporal one-line conclusion is valid for the stated source-local packet interface. If the interface allows extra copies of individual unchanged D values to branch, they must be priced; a support-overlap argument below extends the price minimum to that case. Transporting precombined or otherwise informative rows to an acquisition chart remains outside this gate.

## Geometry and inherited result

I independently read the pinned native gzip (`2b9495…1883`), reconstructed every hosted D normal and its integer Q9 root, and performed exact rational row reduction. The 511-direction census is 487 forbidden-root ranks 8 and 24 ranks 7. This confirms the already-proved S008 chart theorem; it is not a new result. The predecessor proof and review are pinned at SHA-256 `dae0ad585ad8c2d6a1d128dc32b00025388089fec08d17d9f02accae8e7ed6c4` and `57fc50cabcba8dc8ca5b6fb7aae03a11be6617e8a7807c04c4aa2a98cd05002f`.

For each of those 24 exceptional lines `c`, I computed the actual coefficient row from integer root inner products. Its nonzero source set agrees exactly with the hosted facets containing `c`, namely

\[
S(c)=\{i:\langle r(c),r(n_i)\rangle\ne0\}
    =\{i:c\cdot n_i=0\}.
\]

The minimum of `|S(c)|` is 43, attained uniquely at `c=81`. Among all 276 distinct pairs, the minimum intersection is 15, attained at `(81,98)` and `(81,280)`. The included hosted root `11` is rejected as an eligible line (rank 8), and line 81’s support count is checked directly. Exact counts and all supports/intersections are in `fresh-eight/FRESH-EIGHT-GEOMETRY.json` and `FRESH-EIGHT-PAIR-INTERSECTIONS.json`.

## Why one nonzero birth minimizes price

Under the exact eight-packet, pure-target premise, the target has dimension `8V`, and the eight packets together have at most `8V` observation dimensions. Equality forces every packet to have dimension `V`, all packet row spaces to be independent, and every packet row to lie in the target. Thus a packet born at exceptional line `c` occupies its full one-dimensional shortened Gram code tensor `K^V`; every source block in `S(c)` has a nonzero invertible `V×V` coefficient. Two packets at the same line would be dependent. A packet at a chart of dimension at least two cannot be nonzero by the inherited all-511 line theorem.

In the no-extra-informative-transport interface, two distinct line packets require a common unchanged source `d_i` at incomparable one-dimensional charts, which a single monotone source path cannot visit. This gives at most one nonzero birth. The 43 required paths for line 81 split an 8-rank ascent into ranks 1 and 7, so their extra price over direct rank 8 is

\[
f=1+7^{199/200}-8^{199/200}.
\]

With one line-born packet and seven zero-born packets the return bill is `7·9^t+8^t`. This yields

\[
J_8=7\cdot9^t+8^t+43f
   \in(70.87263179542197,70.87263179542199).
\]

All eight packets born at zero cost `8·9^t`, which is strictly higher. The comparison is exact in the checker, not a floating-point sign test.

### Priced individual-source branching control

The same minimum remains true if the source-local interface permits copies of individual unchanged `d_i` values to branch, provided each additional raw field MOVE is billed and no precombined d-dependent row is transported to a line. For `k≥2` distinct line births, let `S_j` be their supports and `U=∪S_j`. Every `i∈U` must have at least one route that supplies its unchanged value at a selected line and still retains the original value at `F_i`. A primary such route costs at least `1+7^t`, versus the direct `8^t` path, so the excess is at least `f`. Every extra occurrence of the same `d_i` at a different line requires another branch from the common chart intersection 0: distinct lines are incomparable, and the branch has at least one positive-rank MOVE, priced at least 1. Consequently

\[
\text{raw excess}\ge |U|f+\sum_i(q_i-1)
\ge43f+15(k-1),
\]

where `q_i` counts selected line supports containing `i`; the last inequality uses `|U|≥43` and `|S_1∩S_j|≥15` for each `j>1`. The packet return price is `k·8^t+(8-k)·9^t`, so relative to `k=1`, the total lower bound increases by at least

\[
(k-1)\bigl(15-(9^t-8^t)\bigr)>0.
\]

Here `9^t−8^t<1` for `0<t<1`. This extension depends on the raw fields remaining separate until they reach the line. A transported aggregate such as a preformed Gram functional is an informative side packet and is outside this source-local theorem; it cannot be hidden as a free raw copy.

## Complete fixed-m price gate

I recomputed the 467-MOVE profile

`Q_best={1:51, 7:43, 8:358, 9:15}`

from its disjoint roles: 400 raw endpoint paths, with 43 split rank-1/rank-7 paths; 8 forward rank-9 packets; 8 rank-1 entry calls; and 7 rank-9 plus 1 rank-8 return packet. The full caller (`d9ba…6cb7`) and H4 invoice (`b8adae…4248`) are pinned. Applying the fixed-m profile identity gives the limiting signed moment

\[
g_\infty=\frac{(18Q_{best}-18N+18H-T+P)_t}{18}
\in(0.25311068495571478,0.25311068495571479),
\]

and the finite-m addition is `d/(m−1)`, where

\[
d=-\frac{(T-P)_t}{18}
 \in(31.539778367085413,31.539778367085415)>0.
\]

Equivalently, after the 400 direct rank-8 raw paths, eight forward rank-9 packets, and eight rank-1 entry calls are paid, the optimistic remaining return/refinement allowance is below `70.61952111046628`; it is below `J_8` by more than `0.25311068495571478` per native. Every finite multiplicity has the additional positive deficit `d/(m−1)`. The complete exact rational intervals are in the JSON receipt.

The signed-profile calculation uses the fixed-m theorem from `TARGET-005.md` under its complete selected caller; it does not transfer the pure-G or other side-information-free premise to changed current rows. This excludes only the specified fresh-eight interface with its eight forward and eight entry calls. It does not exclude relayed/mixed current rows, a changed target representation, overcomplete packet families, or a redesign before the acquisition cut.

## Reproduction and frozen files

Run:

```sh
python3 check_fresh_eight.py --repo REPOSITORY --output OUTPUT
```

The checker imports no author helper. It uses exact `Fraction` elimination for geometry and integer 200th-root brackets for every strict tariff comparison. `FRESH-EIGHT-MANIFEST.json` hashes this reviewer, the checker/receipts, and the source/proof/invoice dependencies.
