# A donor-dependent quotient construction on four actual native sources

## Constructive result

Over `F4=F2[a]/(a^2+a+1)`, there is a literal finite whole-record program
on four two-coordinate source banks and four two-coordinate output banks
which restores every original X at Hub, preserves every arbitrary original
Y baseline, and returns

    Y_i' = Y_i + sum_(j != i) X_j,       i=0,1,2,3.

The source roles are `[0,14,15,30]` and the output roles are
`[33,48,50,1]`, in that order. Output i is perpendicular to precisely the
other three listed donors. These labels are all real native owners.
The six real source-pair A2 planes, in lexicographic pair order, have
indices `[20,17,76,8,957,146]` in the pinned native layout.

The supplied binary word has **32 arbitrary original columns**, 134 ADD,
80 MOVE, 48 INIT and 48 charged dirty CLEAR. Its movement profile is

    24[1] + 24[5] + 32[7].

It uses 26 auxiliary binary records at peak. Every source and output
helper is actually moved, and every original ends at its stated chart.
The word works identically for every positive body width because its
fixed binary lane matrices tensor with the body identity.

This is a complete four-source **foreign-subsum fragment**, not a complete
111-role native supplier. It deliberately pays twelve private field ports
from pair planes to receiver facets. Those ports are additional to the
balanced atlas and cannot be counted as its shared D4 ports. It supplies
an exact positive example of the donor-dependent-kernel escape from the
shared-kernel obstruction. No new kappa or foundational discharge follows.

## The quotient spaces

Choose the four distinct lines represented by

    v_0=(1,0), v_1=(0,1), v_2=(1,1), v_3=(1,a).

Their annihilating linear forms are

    phi_0(x,y)=y,
    phi_1(x,y)=x,
    phi_2(x,y)=x+y,
    phi_3(x,y)=a*x+y.

For every j, phi_j(v_j)=0, while phi_j(v_k) is nonzero for k different
from j. Donor j sends the one-field quotient `phi_k(X_j)` to the plane
H={j,k}. At that same plane donor k sends `phi_j(X_k)`. Thus their kernels
are deliberately different: K_k at the first donor, K_j at the second.
Every pair of quotient forms in a donor's visible two-plane pencil is
independent, so its two-dimensional input is fully distinguished.

At receiver i the three relevant donors form a triangle. For a visible
plane H={j,k}, let l be the fourth label, distinct from i,j,k. Its common
varying source fibre is the line K_l. Indeed fixing donor j's other visible
quotient fixes phi_l(X_j), leaving a coset of K_l; the same is true at k.
This is exactly the required additive gluing, simultaneously at all four
receivers and all six planes.

## Actual plane outputs and decoding

Plane {j,k} sends receiver i the scalar

    t_(i;jk) = phi_k(X_j)/phi_k(v_l)
             + phi_j(X_k)/phi_j(v_l).

All denominators are nonzero. Receiver i adds `v_l t_(i;jk)` into its
two original Y coordinates. For a fixed donor j, its two planes visible
to i contribute

    v_l * phi_k(X_j)/phi_k(v_l)
    + v_k * phi_l(X_j)/phi_l(v_k) = X_j.

To verify the identity, apply phi_k and phi_l: the displayed vectors have
the same two quotient values as X_j, and those forms are independent.
Summing the three planes therefore gives exactly the stated foreign sum.
This proves every input column, not only one test assignment.

Each plane has two different receivers. Its two scalar output rows form
an invertible two-by-two matrix on its two source quotient values, as the
exact certificate checks. The two outputs cannot be replaced by one
unpaid broadcast scalar. In particular this construction does not evade
the shared-port information constraints by silently treating private
receiver messages as a common physical field.

## A literal, fully charged record word

Expand each F4 coordinate in the binary basis (1,a). Scalar multiplication
then is a fixed two-by-two binary matrix; every nonzero matrix entry is
one whole-record ADD. The program uses only INIT, ADD, MOVE and CLEAR.

1. At each genuine source line create three owned field helpers, one for
   each other label, and form the three actual quotient values from X_j.
   Move each helper to its actual A2 plane. These are twelve field moves
   of rank gap one, or 24 binary MOVEs.
2. Move every original X unchanged from its native line to Hub. Move each
   original Y from ground to its genuine receiver facet. Together these
   are sixteen field moves of rank gap seven, or 32 binary MOVEs. Each
   Y remains arbitrary; no zero-Y convention is used in this positive word.
3. At a plane create a field helper for one of its two real outputs, form
   the formula above, move it from the rank-two plane to the rank-seven
   receiver facet, add its decoded two-coordinate contribution to Y, then
   clear it dirty. Repeat for the other receiver and then clear the two
   source quotient helpers dirty at the plane.

Every ADD has co-located operands. Every MOVE is a genuine strict chart
inclusion. Owned moves are upward in the retained paid nested-owned model;
the stricter descending-only submodel would reject this fragment. The
private outputs contribute twelve field moves of rank gap five, or
24 binary MOVEs. Nothing is obtained from a merely rational chart label:
the four source X and four destination Y banks are actual owners.

The GF4 formulas expand to 39 binary source ADDs, 56 plane ADDs and
39 receiver ADDs, totaling 134. There are 24 field helper lifetimes, hence
48 binary INIT and CLEAR. At the largest live point the twelve field
source helpers and one field output helper coexist, giving 26 binary
owned records. All helpers carry nonzero arbitrary-input linear forms at
retirement, so every CLEAR is charged dirty. Original X and Y values are
never erased. Other native inputs are not consumed by this fragment;
extending it by identity does not supply their missing native corrections.

## Why it avoids the parity obstruction

At any receiver the triangle's three donors give an odd left-null vector
of its three pair-plane incidence matrix over characteristic two: each
plane is counted twice. If every plane had one common kernel in actual
input coordinates, its projector would be the same for its two donors.
Summing the three donor resolutions of identity would give `0=I`.

Here the two kernels at {j,k} are K_k and K_j. The plane's two donor
projectors have the same fibre image K_l but different kernels, so their
sum need not vanish. The explicit decoding proves that donor-dependent
quotients really can pass this obstruction. It does not rely on a change
of accounting or a larger alphabet being declared free.

## Verification and remaining native compatibility

Reproduce with

    python3 -B build.py --layout LAYOUT.json.gz --out OUTPUT

The checker validates all 32 original binary columns, every ADD location,
every strict chart inclusion, all final original charts, all helper
lifetimes and the complete invoice. It rejects an omitted receiver ADD
and an omitted source MOVE, and separately verifies all sixteen arbitrary
Y baseline columns. The proof explains the uniform body-width extension.

The next native step must replace these private rank-five deliveries with
compatible maps through the same 45 shared H-to-D ports and the subsequent
D-to-K-to-F routes, while respecting their fixed widths. Independent local
plane decoders are insufficient. Moreover, the same source quotient must
serve every native receiver at once. The companion replicated-scalar
analysis shows why simply repeating this scalar mechanism in identical
stripes cannot meet the existing balanced source contract. Array-coordinate
variation or mixing, or a newly paid geometry, remains necessary.

Credit @CubeJerry, the native and balanced-atlas authors, the source
quotient and shared-kernel proofs, and substantial OpenAI assistance.
Developed by S023 Worker A from programme baseline
`8cf982065bccdd62de2856b16635a6ee06dadb0c`.
