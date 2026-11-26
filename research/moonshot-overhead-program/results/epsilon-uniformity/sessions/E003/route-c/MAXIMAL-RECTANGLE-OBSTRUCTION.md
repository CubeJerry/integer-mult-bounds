# Maximal rectangles, exact weighted sums and necessary thinning

Status: **proved finite graph restriction; independent review pending**.
The result applies to arbitrary nonlaminar choices and arbitrary exact
weighted sums of supported rectangles. It does not refute S004's JR,
which permits rectangles much smaller than their maximal extensions.

## 1. Model and distinction from earlier restrictions

Let C(q,k) have left and right copies of `[q]^k`, with an edge when the
two words differ in every coordinate. Put N=q^k. A nonempty rectangle
`A x B` is supported if every cross pair is an edge. It is maximal if no
strictly larger supported rectangle contains it. An arbitrary product
rectangle need not be maximal.

Over a field F consider an exact representation

    M = sum_(r=1)^R alpha_r 1_(A_r) 1_(B_r)^T,       alpha_r != 0,       (MR1)

where M is the adjacency matrix and all rectangles are supported. Let
`L_A=max_x #{r:x in A_r}` and `L_B=max_y #{r:y in B_r}`. These count
summands, not absolute coefficient sums. Overlaps and cancellation are
allowed. A partition is the special case with disjoint edges and weights one.

Assume the characteristic of F does not divide q-1. This includes F2
when q is a power of two and also Q. Then J_q-I_q has rank q: its kernel
equation makes every coordinate equal to the coordinate sum, and q-1
times that sum is zero. Tensoring gives `rank(M)=N`, hence `R>=N`.
This is the full-rank fact already used in S004's J2. The new step combines
it with a sharp two-sided size constraint, allowing every summand to have
a different orientation and size.

## 2. All maximal supported rectangles

Let A_i and B_i be the coordinate projections of a supported rectangle.
Support is equivalent to `A_i intersect B_i` being empty for every i.
The product of the A_i and the product of the B_i therefore form a
supported rectangle containing the original one. Maximality forces both
sides to be these products. It also forces their projections to exhaust
the alphabet: an unused letter could be added to one projection while
preserving support. Conversely complementary nonempty projection sets
give a maximal rectangle. Thus the maximal rectangles are exactly

    A=product_i S_i,       B=product_i ([q] minus S_i),                  (MR2)

with `1<=s_i=|S_i|<=q-1`. Consequently

    |A||B| = product_i s_i(q-s_i) >= (q-1)^k,                            (MR3)

because `s(q-s)-(q-1)=(s-1)(q-1-s)>=0`. Equality holds precisely when
every cut is singleton-versus-complement. General JR rectangles may have
correlated sides; it is maximality alone that forces MR2.

## 3. Sharp two-sided obstruction

**Theorem MR.** If every summand of MR1 is maximal, then

    L_A L_B >= (q-1)^k,       max(L_A,L_B)>=(q-1)^(k/2).                  (MR4)

Proof. Put `a_r=|A_r|`, `b_r=|B_r|`, `B0=(q-1)^(k/2)`. By MR3,
full rank and Cauchy--Schwarz,

    N B0 <= R B0 <= sum_r sqrt(a_r b_r)
         <= sqrt[(sum_r a_r)(sum_r b_r)] <= N sqrt(L_A L_B).

Cancel N and square. No positivity, disjointness, common hash layer,
equal sizes or laminar family was used. QED.

The product tradeoff is sharp for every k. Choose r of the coordinates.
For each anchor `a in [q]^k`, let the source side use the complement of
`{a_i}` in those r coordinates and the singleton `{a_i}` elsewhere; let
the destination use the complementary choices. Every edge has a unique
anchor: its destination coordinate in the first r positions and its
source coordinate elsewhere. These N maximal rectangles partition all
edges and have

    L_A=(q-1)^r,                L_B=(q-1)^(k-r).                         (MR5)

For even k, r=k/2 attains the least possible common load, even among
arbitrary weighted maximal-rectangle sums. For odd k this proves the
sharp product tradeoff, without claiming a sharp balanced maximum load.

For C(4,2) the minimum is three, recovering S004's opposing-star control.
For C(8,2) it is seven. For fixed even k and q=2^t it is exponential in t,
so maximal rectangles cannot establish JR. This is separate from the
lead's laminar restriction: the sharp examples here are generally nonlaminar.

## 4. Many thin rectangles must carry substantial rank

For unrestricted supported rectangles, extend each `A_r x B_r` to any
maximal `Ahat_r x Bhat_r`, and define the retained geometric density

    eta_r=sqrt[|A_r||B_r|/(|Ahat_r||Bhat_r|)],       0<eta_r<=1.

Every choice of maximal extensions satisfies the following conclusions.
Writing `ell=sqrt(L_A L_B)`, the same inequality gives

    sum_r sqrt(a_r b_r) <= N ell,       sum_r eta_r <= N ell/B0.         (MR6)

In particular, if all densities are at least eta, then

    ell >= eta (q-1)^(k/2).                                           (MR7)

There is a stronger bulk statement. Given B>0, call a summand large if
`sqrt(a_r b_r)>B`. Its count is at most N ell/B by MR6. Its aggregate
matrix therefore has rank at most N ell/B, so the aggregate of all other
summands has rank at least

    N - N ell/B.                                                     (MR8)

This follows from rank subadditivity applied to their exact sum M. It
does not assume that individual summands are linearly independent.
At B=2ell the geometrically small summands carry rank at least N/2 and
thus include at least N/2 nonzero summands.

Likewise, if eta_r>theta then `sqrt(a_r b_r)>theta B0`. The sum of the
remaining rectangles, whose retained densities are at most theta, has
rank at least `N-N ell/(theta B0)`. Choosing theta=2ell/B0 proves:

**Corollary MR-thin.** The rectangles with

    |A_r||B_r|/(|Ahat_r||Bhat_r|) <= 4 L_A L_B/(q-1)^k                 (MR9)

carry, in aggregate, rank at least N/2. In particular at least N/2
nonzero summands obey MR9. A right side at least one makes this a
vacuous density conclusion. It does not require each side separately
to be thin.

Under JR's proposed common load `c^k(t+1)^c`, at least `q^k/2` summands
must therefore retain product density at most

    4 c^(2k)(t+1)^(2c)/(2^t-1)^k.                                    (MR10)

Such thinning is rank-essential in aggregate. Enlarging every candidate
to a maximal biclique, or retaining fixed density on both sides of all
maximal candidates, loses the proposed JR scale. The argument gives no
construction of the required thin, mutually compatible rectangles and
does not prevent them from existing.

## 5. Why the qualifications matter

Cancellation is allowed inside the supported graph. Allowing terms on
nonedges changes the problem: J_q-I_q is the weighted sum of the
all-ones rectangle and q negatively weighted diagonal singletons. It
has per-side load two. Tensoring gives load 2^k for C(q,k), but some
summands are unsupported. At q=8,k=2 the load is four, below the
supported-maximal minimum seven. This identity cannot be substituted
for free rectangles in the source endpoint geometry.

If the field characteristic divides q-1, the one-coordinate matrix has
rank q-1 and its kth power has rank `(q-1)^k`, so the full-rank step
fails. The source cases F2 with q a power of two and Q avoid this issue.

No statement here prices actual tape routing, resolves unrestricted JR
or improves the multiplication overhead. It is a finite structural
restriction with a sharp construction in its restricted family and a
necessary thinning condition outside that family.

## 6. Verification and provenance

`verify_maximal_rectangles.py` checks arbitrary source subsets in small
graphs, finding maximal rectangles by taking common neighborhoods twice,
and compares the result with MR2. It checks opposing-star partitions by
exact edge counts, both loads and rank; tests the density and bulk-rank
statements on nonproduct refinements; and includes negative controls for
exceptional characteristic and unsupported cancellation. The JSON
receipt lists the actual finite cases. Universal claims use the proofs above.

Dependencies: S004 `lead/joint-rectangle-transfer.md`, Sections 1, 2 and 7,
for JR, full rank and the opposing-star control. The maximal-class size
inequality and sharp weighted tradeoff were derived in E003 route C;
the lead supplied the bulk-rank strengthening in Section 4. The lead's
single-laminar-family theorem is a distinct restriction. No literature
priority, formalization or human-refereeing claim is made.

Credits: @CubeJerry; the programme's crown graph formulation; substantial
AI-assisted derivation and verification.
