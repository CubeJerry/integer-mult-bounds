# Local linearity forces a biclique form for scalar rank-nine fitting matrices

**Status:** proved for the exact scalar source interface below, pending independent review. **No new κ.** This is an algebraic classification and search reduction. It is not a physical packet construction or an all-volume operator theorem.

## 1. The changed architecture and its budget interface

The new proposal permits the fitting matrix itself to change. The old Gram matrix has rank eight; a rank-nine matrix may change the raw side debt as well as the forward decoder. Consequently the earlier fresh-return lower bound cannot simply be attached to this new target.

The complete H4 invoice still provides a useful optimistic envelope: after granting all 400 native raw routes direct rank-eight ascents, every new forward, reverse, restoration and structural expense together must fit within approximately 118.29307104377714 per native word. This envelope retains the fixed source invoice and grants favorable raw routing; it does not certify a construction. A candidate matrix from this theorem must still be realized as a source word and its entire new debt and caller cost recomputed.

The theorem below makes that construction problem smaller: except for at most three active rows, an extra scalar encoder direction can only contribute through a common allowed neighborhood, accompanied by explicitly determined Gram row scalings.

## 2. Source, definitions and precise theorem

Let N be the 104 source binary normals: all weight-three and weight-seven vectors in F2^9, excluding

    7,25,42,52,67,76,82,97,104,127,137,162,266,289,448,491.

The sorted omitted list is recorded in the certificate. It is exactly the inventory already checked against the programme's native source, compressed SHA256

    2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883.

This session regenerated that published inventory after the filesystem became unavailable. It does not claim to have re-read the unavailable gzip bytes.

Associate each normal with its established eight-coordinate E8 root a_i, of squared norm eight. For a weight-three normal containing bit eight, place two in its other two set positions and zero elsewhere. For a weight-three normal without bit eight, place one in its three set positions and minus one elsewhere. For a weight-seven normal missing j<k<8, use 2(e_j-e_k); when k=8, use one in position j and minus one elsewhere.

Let A be the 8 by 104 matrix of these root columns and put

\[
G=A^T A/8,\qquad W=\operatorname{rowspan} A.
\]

The diagonal of G is one. Define the forbidden donors and allowed donors for receiver i by

\[
F_i=\{j:a_i\cdot a_j=0\},\qquad
N_i=\{j:a_i\cdot a_j\ne0\}.
\]

In particular i belongs to N_i. Each source row has |F_i|=55 and |N_i|=49.

Work over a characteristic-zero field. Fix h outside W. Suppose a scalar 104 by 104 matrix K satisfies

\[
K_{ii}=1,\quad K_{ij}=0\ (j\in F_i),\quad
\operatorname{rowspan}K\subseteq W+\langle h\rangle.
\tag{1}
\]

Write its rows uniquely as

\[
K_{i*}=\beta_i^T A+t_i h,
\]

and let I={i:t_i≠0}. The scalar t_i is well-defined after h is fixed, because h is outside W; the roots span eight dimensions, so the beta vector is also unique.

**Theorem.** If the active roots {a_i:i in I} span at least three dimensions, there exists b in the eight-dimensional root space such that

\[
g=h-b^TA,\qquad
\operatorname{supp}g\subseteq N(I):=\bigcap_{i\in I}N_i,
\tag{2}
\]

and the entire fitting matrix has the form

\[
\boxed{K=\operatorname{diag}(1-t\odot g)\,G+t\,g^T.}
\tag{3}
\]

Here g is identified with its coordinate column for the outer product; the i-th row of t g^T is t_i g. Conversely, for any scalar t,g with supp(g) contained in N(supp(t)), formula (3) has diagonal one, all required forbidden zeros, and rank at most nine.

If the active roots span at most two dimensions, there are at most three active rows, and K-G is supported on those rows. A concrete rank-nine example below shows that the common-neighborhood conclusion can fail for this exception.

## 3. Exact source span lemma

For every source row i and distinct pair i,k,

\[
\operatorname{span}\{a_j:j\in F_i\}=a_i^\perp,
\tag{4}
\]

\[
\operatorname{span}\{a_j:j\in F_i\cap F_k\}
=\operatorname{span}(a_i,a_k)^\perp.
\tag{5}
\]

The supplied self-contained JavaScript checker proves (4) for all 104 rows and (5) for all 5,356 unordered pairs. It selects independent rows by arithmetic modulo 65,537, then independently computes each selected integer minor by exact BigInt Bareiss elimination. There are 104 nonzero seven-by-seven minors and 5,356 nonzero six-by-six minors. The exact upper bounds follow from orthogonality to one or two independent source roots. No numerical rank tolerance is used.

The actual double-forbidden cardinalities are:

| Pair type | Cardinality | Number of pairs |
|---|---:|---:|
| Nonorthogonal | 30 | 384 |
| Nonorthogonal | 32 | 2,112 |
| Orthogonal | 24 | 240 |
| Orthogonal | 26 | 1,920 |
| Orthogonal | 28 | 672 |
| Orthogonal | 30 | 28 |

Thus the certificate covers every source pair, not a sample. The witness format uses binary normals as immutable identifiers, avoiding an unverified reconstruction of source wire ordering.

Two negative controls retain essential boundaries. A self-pair has forbidden span seven, so the distinct-pair condition in (5) is necessary. Duplicating a selected minor row makes its determinant zero. A separate full-E8 example deletes ten explicitly listed roots from a D6 overlap and leaves a rank-five common-forbidden span; arbitrary deletion cardinality is therefore insufficient to justify (5).

## 4. Affine-line gluing

For an active row define

\[
b_i=-\beta_i/t_i.
\]

The forbidden zero condition gives h_j=b_i·a_j for every j in F_i. On F_i intersect F_k, two active local representatives agree. Equation (5) therefore gives

\[
b_i-b_k\in\operatorname{span}(a_i,a_k).
\tag{6}
\]

Define the affine line L_i=b_i+span(a_i). Distinct source roots are not parallel. Equation (6) says exactly that L_i and L_k intersect.

The following elementary geometric fact supplies the global step.

**Affine-line lemma.** A pairwise-intersecting family of affine lines whose directions span at least three dimensions has a common point.

To prove it, choose three independent directions. The first two lines meet at p. If the third met them at two distinct points, its direction would lie in the plane of the first two directions, contradicting independence. Thus the third line also passes through p. Any further line missing p and intersecting the first two would lie in their affine plane. It could not also meet the third line, which intersects that plane only at p. Hence every line passes through p.

Apply the lemma to get a common b. Then b_i-b is parallel to a_i, so on F_i the vectors b_i and b give the same evaluations. Therefore h-b^T A vanishes on every F_i with i active. This is exactly (2).

## 5. Diagonal restoration and converse

Substitute h=b^T A+g into the i-th row. For an active row, the vector beta_i+t_i b annihilates the forbidden root span. By (4), it is a scalar multiple c_i a_i. An inactive row has t_i=0 and (4) gives the same conclusion. Hence

\[
K_{i*}=c_i a_i^T A+t_i g.
\]

Its diagonal constraint is 8c_i+t_i g_i=1. Replacing c_i gives (3), including the inactive rows, which equal the original Gram rows exactly.

Conversely, assume the stated support condition on t,g. Formula (3) has diagonal (1-t_i g_i)+t_i g_i=1. At a forbidden position (i,j), the Gram entry is zero. If t_i is nonzero, j is outside the common allowed neighborhood and g_j=0; if t_i is zero, the outer-product entry is already zero. Thus all forbidden entries vanish. Finally, the scaled Gram term has rank at most eight and the outer product has rank at most one.

This converse is algebraic. It does not supply collector placement, literal source access, compatible current-row inverses, ownership, precision, restoration, or paid packet routes.

## 6. Quantitative reductions

To justify the small active-set exception, every two distinct source projective roots have absolute normalized inner product zero or one half. Their unoriented angle is therefore at least sixty degrees. In a real two-dimensional plane there can be at most three such projective directions: their cyclic gaps on a semicircle are all at least sixty degrees. The rational root matrix has the same rank over every characteristic-zero extension field. Thus active span at most two implies at most three active rows. Inactive rows equal G by (4), proving the stated support and rank bound for this exception.

Write J=supp(g). Because h is outside W, g is not zero and is outside W. For any j in J, every active i must lie in N_j. Hence a genuine extension with active span at least three has

\[
|I|\le49.
\]

In particular, fifty or more active source rows are impossible for a genuine single scalar extension satisfying (1).

The change from the Gram matrix obeys

\[
K-G=t g^T-\operatorname{diag}(t\odot g)G,
\]

so

\[
\operatorname{rank}(K-G)
\le \min\bigl(|I|,\ 1+|I\cap J|\bigr).
\tag{7}
\]

If I and J are disjoint, this is a rank-one change. The overlap I intersect J is a clique in the source nonorthogonality graph: every two of its vertices are mutually allowed. Equation (7) gives a rigorous bound on how much this fitting matrix itself can change a linear residual rank. It is not a price for a source implementation or a theorem about an unassembled reverse interface.

These statements reduce the scalar search to allowed bicliques (I,J), scalar weights (t,g), and the explicit diagonal restoration in (3). The three-row exception must be searched separately.

## 7. A sharp three-active-row exception

The actual native normals 13,505,11 have roots

\[
a=(1,-1,1,1,-1,-1,-1,-1),\quad
b=(0,2,-2,0,0,0,0,0),\quad
c=(1,1,-1,1,-1,-1,-1,-1).
\]

They satisfy c=a+b and a·b=-4. Define h on the source donors by

\[
h_j=\begin{cases}a\cdot a_j,&c\cdot a_j=0,\\0,&c\cdot a_j\ne0.\end{cases}
\]

Its restrictions on F_a and F_b are zero; on F_c it equals a·a_j. The three compatible local affine lines are

\[
L_a=\operatorname{span}(a),\quad
L_b=\operatorname{span}(b),\quad
L_c=a+\operatorname{span}(c).
\]

They meet pairwise but have no common point. Indeed, the first two meet only at zero, which is not on the third. No global b can remove these three local restrictions.

A genuine fitting matrix realizes the example. Leave every inactive row equal to G. On the active rows set

\[
K_{a*}=G_{a*}+h,\quad
K_{b*}=G_{b*}+h,\quad
K_{c*}=(-a+5c/8)^T A+h.
\]

All diagonal entries are one and every forbidden entry is zero. The extra coefficient is one on all three active rows. The checker verifies every one of the 10,816 entries. A nine-by-nine minor of 8K, using row and column normals

    11,13,14,19,21,26,35,69,131,

has determinant 8,388,608. Since the displayed factorization has rank at most nine, K has rank exactly nine. The inactive roots still span eight dimensions.

This is a valid scalar fitting-matrix construction and a counterexample to dropping the active-span hypothesis. It remains unpriced and has no literal source-word admission.

## 8. Why this is not an operator or all-volume classification

The proof divides by each nonzero scalar t_i to recover a full local restriction of h. For a block decoder, a nonzero but singular operator T_i does not permit that inference: it constrains only T_i h. A tensor product of a scalar fitting matrix with the identity gives an algebraic all-volume example, but the present theorem does not classify arbitrary operator-valued rank-nine-field factorizations.

A future extension would need invertibility hypotheses, a decomposition that prices singular blocks and their information, or a new gluing theorem for those partial restrictions. No such step is silently assumed here.

## 9. Reproduction, classification and next action

Run the self-contained source verifier with a current JavaScript runtime:

    node verify-source.mjs

It outputs the regenerated source inventory, all exact minor witnesses, the overlap census, and negative controls. Run the separate rank-two checker to reproduce the displayed exceptional matrix and its nonzero nine-by-nine minor.

The source-span lemma and scalar gluing theorem are proved statements under the precisely retained finite source interface. The counterexample is an explicit scalar rank-nine fitting matrix. The source-word realization, complete modified debt, all-volume operator case, and the multiplication target remain unresolved.

The next concrete attempt is to choose an allowed biclique and weights that reduce an actual current residual, then construct and replay its diagonal row scaling and outer-product packet together with all original endpoint duties. The active overlap in (7), not the mere algebraic rank nine, controls its optimistic rank effect.

Credit: @CubeJerry programme; source E8 construction and prior verified inventory retain their original provenance. The parent orchestrator proposed the single-extension fitting-matrix interface and overlap gluing test. The global-code worker supplied the exact overlap certificate, affine-line gluing proof, converse, quantitative reductions and sharp scalar exception. AI-assisted mathematical research and verification.
