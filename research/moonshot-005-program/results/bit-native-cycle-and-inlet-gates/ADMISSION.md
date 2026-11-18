# Native endpoint alignment and causal inlet gates

**Admitted S023 checkpoint 1.** A universal algebraic alignment criterion,
a positive one-receiver specialization, and a causal source restriction for
the retained balanced native atlas. No complete BIT supplier or new κ.

The source is the balanced atlas and mixed-coordinate code at programme
parent `8cf982065bccdd62de2856b16635a6ee06dadb0c`. The native source, layout and
balancing factor are pinned in [the proof](author/PROOF.md),
[dependencies](author/DEPENDENCIES.json), and [exact receipt](author/output/RESULT.json).

## Results and scope

1. Arbitrary linear decoding from the retained rank-nine canonical row code
   still forces the canonical contribution to be the native K row. Hence
   proper-path transport must supply O tensor identity. This includes
   arbitrary noncommuting blocks; additional noncanonical ground information
   is outside the interface.
2. For all 6,470 invertible proper blocks, whole donor and receiver gauges
   align every block precisely when 6,249 explicit ordered four-cycle
   equations hold. The 221 tree edges and the ordered equations are stored
   in [SCHEME.json.gz](author/output/SCHEME.json.gz). The maximal common
   aligned row dimension is the common left-fixed-space dimension of the
   tree-normalized blocks. The proof applies over every field and positive
   bank width.
3. Full invertibility and 69 aligned rows alone do not force more aligned
   rows: an exact width-5,760 algebraic counterexample has optimum 69 under
   all endpoint gauges. No physical realization of this counterexample is
   asserted. Conversely, the existing mixed code can be gauged to align
   one entire chosen receiver while retaining 69 common rows everywhere.
   Original restoration and arbitrary-Y normalization remain real costs.
4. If X-to-Y information crosses only after leaving a donor's native line,
   the actual early inlet cut has 2,880–3,600 coordinates, below 5,760. Later
   caches cannot remedy this cut. The finite-alphabet argument also covers
   nonlinear recoding on the specified canonical slice. Real line taps
   restore 6,110 pairs to exactly 5,760 and 360 pairs to 5,940 coordinates.
   Pairwise cut deficits are not independent MOVE bills.

## Review and reproduction

[Independent review](review/REVIEW.md) reconstructs the native root geometry
by reflection, separately checks canonical ranks, and verifies all ordered
cycles with noncommuting matrices over F_101. The author uses distinct
geometry and matrix implementations. Both retain wrong-order and nontrivial
defect controls. These finite checks support the written universal proofs;
they do not replace them.

Run the session [portable replay](../../sessions/2026-11-18-S023/reproduce_cp1.py).
Its validation compares every recorded scientific output, decompressing
gzip artifacts before comparison. Native synchronization, physical interior
coefficients, the strict suppliers, outer caller and all five foundational
assumptions remain open.

Credit @CubeJerry, the native and balanced-atlas authors, S023 worker B's
proof and implementation, and root's independent review; substantial OpenAI
assistance throughout. No external result is silently imported.
