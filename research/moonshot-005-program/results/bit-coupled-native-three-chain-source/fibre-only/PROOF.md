# Connected inverse-fibre alignment with different quotient kernels

## Positive statement

There is a paid source on the seven original donors

\[
\{0,25,45,47,61,62,100\}
\]

that preserves the canonical common inverse fibres at H263, H642 and H135,
while the three donors' off-centre point quotients do **not** have equal
kernels at two of the point interfaces. This is a concrete distinction
between common receiver inverse fibres and equal individual quotient
kernels. It removes the latter premise from the construction at the stated
interfaces; it does not yet close a fourth centre.

For each k=3,12 component, the literal source passes all 441 geometric
foreign cuts, including all 408 native cuts; all 108 geometric and 101
native common centre/receiver fibres; and all seven actual early bases.
The source has bank width 3840 over GF64, with the original 16 spinor
lanes. No source value or shared donor is cloned.

The separate [closing-centre proposition](CLOSING.md) proves an obstruction
only while the 101 specified native fibres remain fixed. It is not an
obstruction to moving those fibres in a new joint construction.

## 1. A hybrid starting word

Use the same three centres, actual field, original owners, point incidence
and Vandermonde H words as in the preceding connected-chain package. Start
again from 34 point-quotient classes; this is a new coefficient word, not
an affine perturbation of the preceding package's frozen seed.

At H263 and H135 use the general two-row point relations from the preceding
construction. At middle H642 retain the older rank-one ramp relation:
each radical point contributes one selected quotient row to the two port
differences. This is the middle coordinate group of width k/3 in the
point quotient. All contrast and coefficient tags use base seed zero.

The simultaneous constraint matrix still has rank 18k on 34k quotient
coordinates, hence an original kernel domain of dimension 16k. Its source
cuts and the common inverse-fibre properties pass in both components.

For every geometric centre/receiver pair let K_(H,i) be the complete
k-dimensional common kernel of its 15 off-centre quotient matrices.
For an actual flag (j,Q), put

\[
E_{j,Q}=
\left(\sum_{\substack{H\text{ designated},\ j\in H\\
i\text{ sees }H,Q,\ Q\ne H}}K_{H,i}\right)^\perp.
\tag{1}
\]

Every row of a new source quotient at (j,Q) may be chosen in E_(j,Q)
without changing its vanishing on the old common fibres. Central controls
are left unchanged in the positive construction.

Among noncentral flags, exactly four have dimension(E_(j,Q)) greater than
k:

| Actual donor | Source plane Q | Dimension for k=3 | Dimension for k=12 |
| ---: | ---: | ---: | ---: |
| 0 | 116 | 6 | 20 |
| 62 | 643 | 6 | 20 |
| 25 | 394 | 6 | 20 |
| 47 | 652 | 6 | 20 |

Every other noncentral flag constrained by the selected fibres has
dimension k. These are exact GF64 ranks, not estimates from parameter
counts. The dimensions and all flags are recorded in the positive receipt.

The first two flags are the outer donors' copies of point 130 at H263;
the last two are the outer donors' copies of point 238 at H135. The
corresponding shared-donor controls at H642 are retained.

## 2. Independent quotient changes

For each flexible flag, take the canonical row basis E from (1). Replace
its old k-row quotient by A E, where A is the deterministic k-by-dim(E)
coefficient matrix with tag

```text
fibre-only/{k}/{seed}/{donor}/{plane}
```

The frozen perturbation seed is 3 at k=3 and 15 at k=12. All other source
quotients and all central controls remain equal to the hybrid word.

Each replacement has rank k. Stacking the old and new quotient gives rank
6 at k=3 and rank 20 at k=12, so their kernels really differ in the original
input coordinate space. This is not an invertible change of basis on a
fixed plane output. In full-bank coordinates the old and new quotient row
spaces together have dimension

\[
16(6+20)=416,
\]

where each quotient individually has dimension 16(3+12)=240.

The source still has full rank on every 16-plane foreign cut. For a
selected centre H and receiver i, every new off-centre row annihilates
the old K_(H,i), by (1). The off-centre matrix has 15k rows. Adding its
central quotient gives a full 16k source cut, so the off-centre rank is
15k and its kernel is exactly the old K_(H,i). Central controls and the
Vandermonde H map did not change, so the entire common readout and its
injectivity on this fibre are retained for all three donors.

The verifier performs this argument on the actual matrices. It does not
use literal point-table equality after the perturbation. In particular,
the old shared quotient at H263's point 130 still appears as donor 61's
H642 control, while the new donor 0 and donor 62 quotients have different
kernels. The same happens at H135's point 238.

## 3. Physical word and full source price

The same exact owner compiler is applied to all 14 component source
matrices. Each 32k-by-32k early basis is invertible at early seed zero.
Every late parity is computed on the original X fields before departure,
stored in its own paid cache, delivered to the actual Y owner, and
dirty-cleared. Both pure source directions and all original-owner swaps
are charged.

| Scope | Forward ADD | Pure inverse ADD | Total ADD | INIT | Dirty CLEAR |
| --- | ---: | ---: | ---: | ---: | ---: |
| Seven changed sources | 150,251,520 | 119,492,888 | 269,744,408 | 120,960 | 120,960 |
| Full 111-donor source with 104 pinned background words | 350,263,656 | 234,480,224 | 584,743,880 | 2,517,120 | 2,517,120 |

The seven source-owner permutations cost 477,216 ADDs, already included.
There is no extra source MOVE. The background invoice replaces, rather
than duplicates, the seven corresponding predecessor charges.

This is a complete source invoice, not a complete H/D/K/facet and return
invoice. No complete endpoint, whole-return rank, S028 two-star extension,
or new multiplication exponent is claimed.

## Replay

From the repository root:

```sh
python -B research/moonshot-005-program/results/bit-coupled-native-three-chain-source/fibre-only/check.py --repo . --out /tmp/fibre-only-check
python -B research/moonshot-005-program/results/bit-coupled-native-three-chain-source/fibre-only/compile.py --repo . --out /tmp/fibre-only-price
python -B research/moonshot-005-program/results/bit-coupled-native-three-chain-source/fibre-only/check_closing.py --repo . --out /tmp/fibre-only-closing
```

The compiler's `--emit-words` option retains all packed reductions and
original-holder dictionaries. The optional exact rank accelerator changes
no source coefficient. An arbitrary coefficient flip outside the permitted
annihilator is a negative control and is rejected.

## Open next question

Move some of the existing 101 native inverse fibres while closing H44,
H116, H394, H643 or H652. The accompanying exact obstruction shows that
preserving all those fibres cannot complete any of these five closures,
even though genuine donor-dependent quotient changes are now available.
Any candidate must recheck all original source cuts, the three old centre
interfaces, the new centre, physical early bases, and the complete source
invoice on the same word.

## Attribution

This package builds on the preceding connected-chain construction and
the retained source, native geometry, GF64 and original-owner compiler
packages named there. No predecessor file was modified. Their functions
are imported from the pinned repository paths. Substantial OpenAI
assistance, session S030; Apache-2.0.
