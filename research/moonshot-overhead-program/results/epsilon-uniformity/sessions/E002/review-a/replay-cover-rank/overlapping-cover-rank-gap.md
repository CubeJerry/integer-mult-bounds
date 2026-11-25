# Low-incidence covers exist, but their exact scalar identity fails by rank

Status: **complete geometric construction and scoped rank obstruction;
independent review requested**. This is not an improved physical pencil or
multiplier. It identifies a substantive distinction between covering all
required off-diagonal pairs and reproducing their exact coefficient matrix.
All logarithms in bounds are binary.

## 1. Retained geometry and target

Use the characteristic-two labels in
`routes/B/characteristic-two-label-geometry.md`: d>=2 a power of two,
h=2d−1, q=2^t, U=[q]^h, V=U^h, N=q^(h²). Let
C=binom(h,d). The matrix P* has diagonal entries one and off-diagonal
support exactly the pairs changing d outer coordinates, with inner Hamming
distance d in each. Its rank satisfies

    rank(P*)/N <= 2^(2d²−2) q^(−d²).                  (CG1)

Write F=P*−I. A source-compatible rectangle has every cross pair in this
far support and has k=0 between every two labels on either one side,
where k counts inner distance-d coordinates. The exact pencil identity
requires F to be a sum of weighted rank-one rectangle matrices. A cover
of its support alone need not satisfy that identity.

The independent noncanonical incidence theorem NC proves that every such
cover has log incidence at least a fixed multiple of d²+dt. We construct
a cover attaining this order, then prove that the constructed sparse family
cannot supply the exact scalar identity in the relevant parameter range.

## 2. Simultaneous separating cuts

Let r>=1. A cut tuple consists of r functions c_i:[q]->{0,1}.
An ordered pair of r-letter words (u,v), unequal in every coordinate,
is separated when c_i(u_i)!=c_i(v_i) for every i. There exist at most

    K=ceil(2^r(2r log2 q+1))                          (CG2)

cut tuples separating every such ordered pair.

Proof: a uniformly random independently chosen cut at every coordinate
separates any one pair with probability 2^(−r). Hence some cut tuple
covers at least this fraction of any current set of uncovered pairs.
Choose such a tuple and repeat. There are at most q^(2r) pairs initially.
After K choices, the number left is at most

    q^(2r)(1−2^(−r))^K <= q^(2r) exp(−K/2^r) < 1,

because log2 q>=ln q and the extra one gives strict slack. It is an
integer, so all pairs are covered. A deterministic algorithm enumerates
all 2^(rq) cut tuples at each step, counts their remaining covered pairs
exactly and takes a maximizer with lexicographic tie-breaking. This is
finite constructive search, with no probabilistic machine or oracle.
For r=0 use one empty cut tuple and K=1.

For each chosen tuple include all 2^r orientations: at coordinate i the
source uses one cut class and the destination uses the other. Omit empty
rectangles. Each fixed source word belongs to at most one orientation
per tuple, hence at most K of these boxes, and similarly on the destination
side. The boxes cover every coordinatewise unequal pair. They generally
overlap, with varying multiplicities.

## 3. Opposite pins and the complete source-compatible cover

This step uses reviewer A's newly proved cross-pinned construction, with
separate provenance. For one inner far pair choose its d unequal positions
S and fix all other letters. Let i1,i2 be the first two positions of S.
Pin the source letter at i1 to a, allowing every destination letter except
a there. Pin the destination letter at i2 to b, allowing every source
letter except b there. Use the preceding simultaneous cuts on the remaining
r=d−2 positions. For every a,b and every oriented cut tuple include the
resulting nonempty box.

Every cross pair differs at all d positions and nowhere else. Each side
has one pinned position, so two words on that side differ at at most d−1
positions. Thus it has the required inner within-side zero condition.
Every far ordered pair is covered: a and b are forced by its source and
destination respectively, and some cut tuple separates its other positions.
No restriction a!=b is needed, because these pins are at different positions.

Each fixed source word has at most

    lambda_in <= C(q−1)K                             (CG3)

incidences: choose S, choose destination pin b unequal to its source letter
at i2, then at most one source orientation per cut tuple. The destination
bound is identical. The total number of inner rectangles is at most

    R_in <= C q^(h−d) q² K 2^r
          = C q^(d+1) K 2^r.                         (CG4)

At the outer level choose d changing positions, fix the others, and take
products of these inner boxes. Every required far pair is covered and
the same-side integer k is zero. Consequently

    lambda <= C^(d+1)(q−1)^d K^d,                    (CG5)
    R/N <= C^(d+1) [K 2^r / q^r]^d.                  (CG6)

These are upper bounds; duplicates and empty rectangles can be removed.
They hold for actual enumerated finite families, not merely expected loads.
Since log C=O(d) and log K=O(d+log(dt+1)),

    log2(1+lambda)=O(d²+dt).                          (CG7)

Together with NC this identifies the correct order of the best **cover**
incidence in this restricted geometry. In particular the canonical
partition's additional d² log t term is not inherent to covering.

## 4. The exact weighted identity cannot use this sparse family

Impose the retained sufficient rank guard

    td² >= 2d²−2+z,  z=log2 m,

with least integer t and d a power of two within a fixed factor of z^(1/3).
Then d=Theta(z^(1/3)), t=Theta(z^(1/3)), and (CG7) becomes
`log(1+lambda)=O(z^(2/3))`. NC's matching lower order applies as well.

But (CG6) has a very different consequence. Taking logarithms and using
r=d−2 gives

    log2(R/N)
      <= (d+1)log2 C + d log2 K + dr −tdr
      <= −td² + O(d²+dt+d log(dt+1))
      <= −z + O(z^(2/3)).                             (CG8)

Thus R/N<=m^(−1) 2^(O((log m)^(2/3))) tends to zero. On the other
hand the elementary rank inequality gives

    rank(F) >= rank(I)−rank(P*) >= N(1−1/m).           (CG9)

Each scalar-weighted rectangle matrix has rank at most one. More generally
one may put any separable row and column weights on one rectangle; its
rank is still at most one. Consequently any sum using the R constructed
rectangles has rank at most R. Equations CG8 and CG9 are incompatible for
all sufficiently large m. No choice of such weights over F2 or any of its
extension fields can turn this family into the required exact identity F.
Extension of the coefficient field does not change the rank of a matrix
whose entries lie in F2.

This is a falsifier for the specific low-incidence covering construction,
not a lower bound on every cover or physical endpoint method. Adding
new independent rectangle directions, changing the scalar identity,
using genuine higher-rank operator terms, or sharing a different
representation is outside this statement. Duplicating the same matrices
or changing their scalar coefficients cannot repair a deficient span.

A simpler local diagnostic is available before the outer construction.
For fixed opposite pins and inactive coordinates, fix also the remaining
free source letter at i2 and destination letter at i1 to allowable values.
The required residual matrix on the r unpinned coordinates is

    (J_q−I_q)^(tensor r).

Over characteristic two with even q, `(I_q+J_q)^2=I_q`, since J_q²=qJ_q=0.
The matrix is invertible and its tensor power has rank q^r. The selected
cut tuples supply at most K2^r rank-one boxes. If K2^r<q^r, they cannot
produce this local exact matrix. This local restriction agrees with the
stronger whole-label rank failure above; it does not assume positive weights.

## 5. Uniform generation and what remains unproved

The greedy cut construction is effective with exact counters and finite
binary lists. In the balanced parameter range, q,r,K and q^(2r) are bounded
by fixed powers of m. Exhaustively enumerating the 2^(rq) possible cut tuples,
including every exact coverage scan and sequential head movement, takes
at most 2^(m^K0) ordinary bit steps for some fixed K0. Its compact retained
cut description has K r q bits, polynomial in m. The outer box description
can be generated from the cuts and finite loops over positions and pins.
No free randomized choice or hidden infinite search is used.

These construction bounds do not promote the cover into a valid pencil.
The exact scalar rank defect persists even if generation and routing were
free. The positive result is an explicit finite cover of optimal-order
incidence within NC's geometric class; the negative result states precisely
why that cover is not an exact weighted decomposition.

This comparison changes the constructive target. NC alone leaves open the
removal of the canonical incidence logarithm, and low-load covering indeed
achieves it. A useful improvement must additionally retain enough independent
rectangle matrices to realize the exact source identity, or replace that
identity by a proved different mechanism. Approximate equality, coverage,
and uniform random expectations do not imply the finite exact cancellation
required for arbitrary occupied data.

The retained exact disjoint cross-pinned partition is a separate positive
component and does satisfy the identity. Its smaller incidence still has
the same optimized asymptotic order as V; it does not use this lossy cover.
No unconditional multiplier improvement, runtime lower bound, formal proof,
full execution or literature-priority claim is made here.

Credits: @CubeJerry; the pinned source and characteristic-two label matrix;
Route A's noncanonical incidence theorem; independent reviewer A's opposite
single-pin partition; the lead's simultaneous-cut cover and rank comparison;
and substantial ChatGPT multi-agent mathematical assistance. Greedy covering
and matrix rank subadditivity are standard tools, not claims of new general
methods.
