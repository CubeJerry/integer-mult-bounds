# Canonical leaf lines and the binary-alphabet exception

Status: **local geometry component independently accepted by Route C**;
see `route-c-work/REVIEW-FOURIER-LEAF-LINE-CLASSIFICATION.md`.
Concurrent E003 `ROUTING-STATE-WALK-SHARING.md`, read after this derivation,
independently proves the absence of a common odd vector for distinct
canonical states (its W3), the q=2 four-call collapse, and a charged
obstruction. Those overlapping facts retain E003 attribution. The explicit
canonical e/U/r basis here also identifies when DA5's selected phase can
be removed, while retaining zero-level offsets in other internal blocks.
This examines the remaining one-axis leaf maps after DA5. It gives a
canonical basis with no selected-internal shear phase, an exact scoped
obstruction to sharing one geometric odd line when q>=4, and a genuine
q=2 collapse. None changes the complete multiplication envelope.

Use DA1 notation at a fixed destination w: z_i(a) for a!=w_i, sibling
blocks C_i(s), internal spaces U_i(s), and A_w=d_w^perp. The z_i(a)
span A_w: the projection of any label vector onto A_w is the sum of
its one-coordinate neighbor vectors. All claims concern the actual
binary Gram quotient.

## 1. A canonical common odd direction

Define e_i=sum_(a!=w_i) z_i(a). For every generator z_j(b), DA1 gives
<e_i,z_j(b)>=1, independent of i. Nondegeneracy of A_w and spanning by
these generators imply e_i=e_j. Write their common value as e. Since
q-1 is odd, <e,e>=1. Also <e,x>=<x,x> for every x in A_w.

For each level s>=1, choose the same base letter a_i(s) as DA2 and put

    r_i(s)=z_i(a_i(s))+e.

The following is a basis of A_w:

    e; all bases of U_i(s); all r_i(s), for i and s>=1.    (LC1)

To verify this, let E_i be the even-coefficient subspace of the span of
the q-1 orthonormal vectors z_i(a). DA1 shows the E_i are independent
across i and orthogonal to e. Each has dimension q-2. Within E_i the
U_i(s) have total dimension q-1-t. The block parity of r_i(s) is one
on sibling block s and on the singleton block zero, and zero on other
positive-level blocks. Thus the t-1 vectors r_i(s) are independent
modulo the internal spaces and complete E_i. The dimensions add to D-1.

Put u_i=sum_(s>=1) sum_(a in C_i(s)) z_i(a). Each inner sum belongs
to U_i(s), since its block has even cardinality. The singleton neighbor
is therefore

    z_i(a_i(0))=e+u_i.                                  (LC2)

For q>=4, u_i is nonzero: its level-one component is the nonzero sum
of two orthonormal neighbor vectors. The u_i for different coordinates
are independent because they lie in independent E_i. At q=2 they all
vanish, and no internal or r directions remain.

## 2. Exact form of every rectangle's line coset

For a rectangle incident to w, let P be the coordinates with positive
first-difference level s_i>=1. Let Z be its coordinates that are unequal
at level zero; all others are equal. The parity condition is |P|+|Z| odd.
The source span is U_R plus its odd line, and its odd-norm vectors are
precisely the affine coset

    v_R+U_R,
    v_R=e+sum_(i in P)r_i(s_i)+sum_(i in Z)u_i,
    U_R=direct-sum_(i in P)U_i(s_i).                    (LC3)

In the canonical basis LC1, v_R has no component in the selected U_R:
its r terms are outside every internal block and its u terms occur only
at coordinates in Z, disjoint from P. Thus the selected-internal phase
D_alpha in DA5 is the identity for this particular basis. The generic
DA5 phase proof remains necessary for arbitrary fixed bases; the earlier
checker deliberately used such bases and correctly found nonzero phases.
This is a simplification of ordinary maps, not a reduction in Fourier
calls by itself.

For q>=4, the cosets v_R+U_R for distinct incident canonical rectangles
are pairwise disjoint. If their positive-coordinate states differ, their
r-coordinate patterns differ. If the states agree but Z differs, the
offset is a nonzero sum of u_i in zero-state coordinates; it lies outside
their common selected U_R. Neither difference can be removed by an
internal vector. This proves disjointness without selecting a particular
representative from a coset.

Consequently no odd-norm geometric direction belongs to the source spans
of two distinct incident canonical rectangles. A grouping rule that
requires the same such line has only singleton groups. This statement is
intrinsic to these spans. It does not prohibit a common transform after
different shears, other basis circuits, or a more general linear batching
algorithm. Indeed DA5 already realizes all lines through one coordinate
e using different ordinary maps.

## 3. The q=2 exception and its charged obstruction

When q=2, D=2 and A_w is the one-dimensional span of e. Every U_R is
zero and every odd source label has the same vector e. All free
destination endpoint maps can therefore accumulate before the one
e-axis transform. With the source preconditioning retained, the free
bill is at most four axis calls per row: two input auxiliary calls and
two destination auxiliary calls. It is independent of the large literal
incidence lambda=2^(L-1).

This is an additional executor change, so SI's explicit lambda invoice
must not be used as an actual-time lower bound for this special branch.
The case still cannot improve the retained charged route. Partition
binary labels by parity. Free transfers occur only between opposite
parities. If a charged rational matrix C and a free-supported matrix F
satisfy C+F=I, then the same-parity principal submatrix of C on either
parity class is the identity of size N/2. Hence rank_Q C>=N/2. The
charged coefficient m D rank(C)/N is therefore at least m, for every
such choice of correction kernel, not just the particular polynomial P.

This explains the exception without asserting that lambda is inherently
paid by every executor. For q>=4 the disjoint-line result is a narrower
classification, and is not a quantitative lower bound for all remaining
leaf-map batching schemes.

## 4. Exact finite checks

`verify_fourier_leaf_lines.py` checks eight actual Gram quotient families,
140 rectangle line cosets, 588 enumerated coset points and 332 source
labels. It verifies the basis ranks, the vanishing selected-internal phase
in canonical coordinates, and pairwise disjointness for every tested
q>=4. The q=2 cases exhibit the claimed complete collapse. Omitting
level-zero offsets fails 70 rectangle cases. The largest auxiliary
dimension is 29; its finite line cosets are enumerated, not its complete
address array. The receipt is `fourier-leaf-line-verification.json`.
These are finite geometry controls, not a physical runtime benchmark.

Credits: S004's destination internal-space construction; concurrent E003
state-walk span intersections, binary exception and charged obstruction;
the pinned binary Gram quotient; @CubeJerry; substantial ChatGPT assistance.
