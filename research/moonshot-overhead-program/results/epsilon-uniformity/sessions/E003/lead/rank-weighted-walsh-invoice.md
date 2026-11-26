# Exact rank-weighted binary Walsh invoice

Status: **proved geometric and arithmetic statement for a specified new
invoice; physical endpoint-sharing realization is a separate Route A gate**.
This note tests a changed local mechanism rather than simply optimizing
the old positive invoice. It does not establish a faster complete multiplier.

Put q=2^t, t>=1, L>=2, s=floor(L/2), and

    D=2+L(q-2),
    lambda(t)=sum_(j odd) binom(L,j)t^j,
    lambda'(t)=sum_(j odd) j binom(L,j)t^(j-1).

The derivative notation denotes this explicit integer polynomial. Every
odd-distance canonical free rectangle has nonzero weight, as proved in
`binary-walsh-label-invoice-barrier.md`.

## 1. Exact rank of a canonical rectangle side

Let a rectangle side be a product of nonempty proper symbol subsets of
sizes s_1,...,s_L. In the source's nondegenerate Gram quotient, its label
vectors span a subspace of dimension

    r=1+sum_i(s_i-1).                                      (RW1)

To prove this, subtract one fixed label vector from the others. For each
coordinate i, the differences are the independent match-indicator functions
`1_(w_i=a)+1_(w_i=b)` with a,b in that coordinate's symbol subset. Their
space has dimension s_i-1. It contains no nonzero constant function, since
the subset is proper and each function vanishes at an omitted symbol.
Coordinate-function spaces therefore sum directly. The fixed row of Gamma
is outside even the full row-difference space, by the even-q rank proof in
the earlier note. It adds exactly one dimension. Passing from Gram rows
to the nondegenerate quotient preserves this dimension.

For a first-difference block at position h in a t-bit letter, the side
has size 2^(t-h). An equal coordinate has size one. Thus all the subsets
in a canonical rectangle are proper, including q=2, and RW1 applies.
Its two sides have equal size and equal rank r.

At any fixed source or destination label, summing ranks over the incident
odd-distance rectangles gives exactly

    sum_inc (r-1)=(q-1-t)lambda'(t),                        (RW2)

because `sum_(h=1)^t(2^(t-h)-1)=q-1-t`. For j unequal positions, choosing
which position supplies the rank contribution gives
`j t^(j-1)(q-1-t)`, and summing over the odd position sets proves RW2.

## 2. The candidate shared-endpoint invoice

Route A investigates factoring one full auxiliary transform per destination
out of its entire free-rectangle sum. The proposed incidence cost is 2r
source-axis calls and 2(r-1) residual destination-axis calls, plus 2(D-1)
calls once per destination. If the exact phase/coordinate realization is
supplied, RW1--RW2 give the free bill per label

    F=2(D-1)+2lambda+4(q-1-t)lambda'.                       (RW3)

This is an exact count for that proposed axis-call list. It does not count
the physical monomial maps, scalar arithmetic or numerical gains. Those
belong to the separate executor proof. Charged rectangles may retain their
original direct implementation and be added after the free contribution.

For convenience define the positive arithmetic invoice

    J_rank = D+lambda+2(q-1-t)lambda'
             +D m binom(L,s)q^(-ceil(L/2)).                 (RW4)

The last term is the nonzero highest charged coefficient's canonical list.
The full charged list differs by at most an absolute factor two. In RW3,
the free portion equals twice the first three terms of RW4 minus two.

For t>=2 the first three terms improve the old D lambda bill by an
asymptotic factor Theta(t), uniformly in L>=2. More explicitly,

    D lambda/[4(t+1)]
       <= D+lambda+2(q-1-t)lambda'
       <= 10 D lambda/(t+1).                             (RW5)

Indeed q-1-t>=q/4, D<=Lq, and

    (L-1)lambda/(t+1) <= lambda' <= 2L lambda/(t+1).

For even L the derivative-to-value ratio is
`L/(t+1) [1-z^(L-1)]/[1-z^L]`, z=(t-1)/(t+1); the bracket lies between
(L-1)/L and one. For odd L it is
`L/(t+1) [1+z^(L-1)]/[1+z^L]`, between one and two. These prove the
displayed derivative bounds. The lower RW5 follows from L-1>=L/2.
For the upper bound use q/(q-2)<=2, lambda>=(t+1)^(L-1)>=t+1,
and D>=q>=t+1. The estimates deliberately use loose absolute constants.

The factor saving concerns the free part. It is not asserted for a total
invoice dominated by charged rectangles or other physical work.

## 3. The changed invoice still has the square-root logarithmic scale

**Theorem RW.** For all m>=2^16 and all integer L>=2,t>=1,

    log2 J_rank >= (1/4)sqrt(log2 m log2 log2 m).            (RW6)

This is a lower bound on the explicitly defined positive invoice RW4,
not on the actual execution time of any Walsh algorithm.

Write x=log2 m and b=log2 J_rank. If L=2, the charged term alone is
`2mD/q>=2m`, so b>=x. If t=1, D=2. The elementary bound
`binom(L,floor(L/2))>=2^floor(L/2)`, obtained by choosing one element
from each of floor(L/2) disjoint pairs, again makes the charged term
at least m. These cases satisfy RW6.

Otherwise t>=2 and v=L-2>=1. The lower derivative estimate, or directly
`lambda'>=L(t+1)^(L-2)`, gives

    b >= t-1+v log2(t+1).

Since D>=q and `ceil(L/2)-1<=L-2=v`, the charged term also gives

    b >= x-vt.

If b>=x/2, then `x>=4 log2 x` for x>=16 yields a stronger conclusion.
Otherwise vt>x/2 and

    b+1 > t+[x/(2t)]log2(t+1).

The ratio log2(t+1)/t decreases. For t<=sqrt(x), the last inequality
implies `b+1 >= (1/4)sqrt(x)log2 x >= (1/2)sqrt(x log2 x)`.
For t>=sqrt(x), AM-GM instead gives `b+1>=sqrt(x log2 x)`.
Since sqrt(x log2 x)>=8, both bounds imply RW6. This proves the theorem
without a fixed-L, fixed-t or stationary-schedule restriction.

Thus even if the proposed physical sharing is admitted, this specific
rank-weighted invoice retains a logarithmic local loss of order at least
Psi(log m). Its matching upper follows from the older invoice. With the
separately retained positive normalized routing toll, B's coupled theorem
still forces the same Phi global certificate scale. That conclusion
depends on the stated new invoice and toll; the older literal endpoint
lower bound is not reused unchanged after the mechanism changes.

Credits: @CubeJerry; the pinned binary Gram geometry; E003 A's destination
factoring proposal; the lead's exact rank/load calculation and arithmetic
barrier; B's independently reviewed coupled-invoice theorem. The physical
proposal has its own admission status. No actual-time lower bound or new
complete asymptotic result is claimed here.
