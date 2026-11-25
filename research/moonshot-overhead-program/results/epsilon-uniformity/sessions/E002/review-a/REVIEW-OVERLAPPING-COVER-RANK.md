# Independent review of the overlapping-cover/rank separation

Reviewer: E002 independent reviewer A. Status: **PASS for the geometric
construction and the stated scalar-rank obstruction**.

Reviewed complete `overlapping-cover-rank-gap.md`, SHA-256
`7229b37ee2e7b5aace2346f89ee97e49d6b99d64e1ab21fd20f7e506f9929b38`.
Read checker SHA-256
`12b6231c5f51ad953a2d430605ae6434bb594eaeb252d86705bb9ebdc3f24f21`
and replayed an isolated exact copy. This review also uses the independently
reviewed NC theorem and the retained characteristic-two geometry. I authored
the cross-pinned partition supplied to Section 3, so this is an independent
review of the lead's greedy-cover/rank composition, not an independent
authorship claim for that supplied pinning component.

## 1. Deterministic simultaneous cuts

Independent random cuts at the r coordinates separate each required pair
with probability 2^(-r). Averaging over all finite cut tuples therefore
supplies a tuple covering that fraction of any remaining pair set. The
number left after K steps is at most
`q^(2r) exp(-K/2^r)`. The specified K has K/2^r>=2r log2 q+1, which is
strictly larger than 2r ln q for q>=2. Thus the remaining integer count is
zero. Lexicographic exhaustive maximization is a finite deterministic
construction; it is not an assumption that random trials happen to work.
The r=0 case is stated and handled separately.

All orientations of one chosen tuple give at most 2^r rectangles. Each
fixed word belongs to at most one source orientation and at most one
destination orientation. Omitting empty rectangles and deduplicating cannot
increase the stated loads. Exact coverage follows from separation, but
nothing in this proof fixes the overlap multiplicities. That distinction
is correctly preserved throughout the theorem.

## 2. Actual geometry and incidence

Opposite pins at two distinct selected coordinates preserve cross distance
d and limit each side's internal distance to at most d-1. The two pin
letters are independent; requiring a!=b would incorrectly omit edges.
Fixed source words have q-1 choices for the destination pin and at most K
orientations across chosen tuples. This gives CG3, while direct enumeration
of common outside letters, the two pins and orientations gives CG4.

The outer product uses d changing positions and fixed inner words elsewhere.
It covers exactly the required support and has k=0 within each side. Its
load and total-rectangle upper bounds are CG5 and CG6. The factor q^(-r)
in CG6 is essential and is correctly present. Since
`log K=O(d+log(dt+1))` and `d log(dt+1)=O(d^2+dt)`, the cover's log
incidence is O(d^2+dt), uniformly including the small parameters. Together
with NC this matches the order of the optimal cover incidence inside its
explicit geometric class. It is not a matching result for exact weighted
decompositions or physical schedules.

## 3. Balanced range and scalar rank

For d within fixed factors of z^(1/3), the least admissible t satisfies
`t d^2=z+O(d^2)` and t=Theta(z^(1/3)). In CG6, r=d-2 leaves leading
term `-td^2`; the remaining positive terms are
O(d^2+dt+d log(dt+1))=O(z^(2/3)). Hence CG8 and R/N tending to zero
follow. This is compatible with cover incidence being large: each of
these few boxes can contain many edges and many endpoints.

The retained matrix F=P*-I has rank at least N-rank(P*), which is at
least N(1-1/m) under the sufficient guard. Every scalar-weighted box,
including separate row and column weights, has rank at most one. A sum
using only R boxes therefore has rank at most R, contradicting the target
rank eventually. The same argument works over every extension of F2,
because the ranks of the original binary matrices do not change.
Reweighting or duplicating a deficient matrix family cannot change this
conclusion. Adding genuinely independent directions or using higher-rank
operator terms is expressly outside the claim.

The local tensor diagnostic is also valid. Fixing both opposite pins and
the two allowed remaining coordinates leaves the coordinatewise-unequal
matrix on the other r coordinates. Every pair in that residual support
has the same unique outer support and pins, so boxes belonging to other
support/pin choices cannot repair this restricted block. Since q is even,
`(I+J)^2=I` over characteristic two. Its r-fold tensor power has rank q^r.
The selected cut family supplies at most K2^r rank-one boxes. Thus the
strict inequality K2^r<q^r is a sufficient local impossibility condition,
without requiring positive weights.

## 4. Finite generation and independent replay

In the balanced range, q,r,K and q^(2r) are bounded by fixed powers of m.
Enumerating 2^(rq) cuts with exact sequential coverage scans is therefore
within 2^(m^K0) for some fixed degree K0. The retained K r q-bit cut list
is polynomial m. Finite loops over supports, pins and outer labels add no
unbounded oracle. This establishes effective cover construction only;
the exact rank failure persists regardless of its generation speed.

At 2026-11-25T23:42:52.319465+00:00, the isolated replay in
`replay-cover-rank/` exited zero with the same theorem/checker hashes.
Seven cases reproduced exact coverage and direct F2 matrix-span tests.
In particular, (q,r)=(4,2) used three cut tuples and twelve nonempty boxes,
covered all 144 required pairs, yet failed to span the rank-sixteen target.
For (8,1), six boxes could not span rank eight. The (4,1) case separately
failed the exact span test even though its four boxes matched the target's
rank in number. Four exact balanced-parameter integer inequalities checked
R/N below the retained rank floor. Complete logs and receipts are retained.

These finite checks support the explicit small constructions and falsifiers.
The written greedy and rank proofs supply the unbounded family. Neither the
review nor the tests prove a tape-runtime lower bound, a stronger multiplier,
formal refinement, full machine execution, or literature priority.

Credits: @CubeJerry; the pinned source and characteristic-two geometry;
Route A's NC argument; the lead's simultaneous-cover/rank theorem;
the cross-pinned supplier; substantial ChatGPT multi-agent assistance.
