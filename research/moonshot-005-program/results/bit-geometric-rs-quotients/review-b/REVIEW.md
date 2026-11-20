# Independent verification of the geometric RS rank escape

## Verified statement and limits

The literal geometric node assignments pass independent reconstruction
at all **99 eligible ordinary donors**. Every actual sixteen-plane
source view is a full-rank Reed–Solomon evaluation view. At every one
of the 2,970 prior propagation records, both the saved fifteen receivers
and the complete admissible native receiver family have inverse-fibre
span rank **5**, rather than the rank 15 needed by the single-anchor
propagation obstruction.

The low rank has a structural explanation. A fixed-centre family has
rank 6, and any family whose views contain two specified source nodes
has rank at most 5. These statements hold for every field extension of
GF64 with the same frozen nodes. For the tensor array
`F_R=(1,a_R,...,a_R^15) tensor I_t`, the respective ranks scale by t.
No Hermite-jet rank statement is inferred from tensor repetition.

This is a verified source-information candidate and an escape from the
specified rank obstruction. It is not a construction of a common H word,
an actual early/late source word, downstream D/K/facet operators, a global
return, a complete invoice or an improved multiplication exponent.

## Data and independent methods

The exact node witness is retained in `NODE-WITNESSES.json.gz`. Its
decompressed bytes are the supplied 99-row scratch receipt, with SHA256
`8aeee87046645cb89f1f44768686cb6b93930c4fb2570b18e2318cab047ed9b2`.
The native layout, lattice basis, earlier triangle certificate and
predecessor RS source are independently pinned in `check.py`.

No author code is imported. GF64 arithmetic uses a separately constructed
primitive-element logarithm table. The generator is checked to visit all
63 nonzero elements before returning to one. The real lattice coordinates
are obtained by direct integer formulas and recomposed against the
published basis. No author's rational inverse or Witt-basis constructor
is used.

For each source, six independent literal singular-node labels determine
a binary linear map on its entire 64-vector complement. The reviewer
checks this map on every vector, verifies its quadratic form, and checks
all 28 plane labels. Thus the literal node table is proved to arise from
the required isometry, rather than merely being compared with a second
execution of the author's basis-selection routine.

The finite checks use exact polynomial products, synthetic division,
field elimination and binary rank. The detailed replay retains all native
receiver families and the exact source/fibre bindings.

## The quadratic field model and sparse block polynomial

Use GF64 represented by the irreducible polynomial `x^6+x+1`, and put

\[
q(a)=a^9+a^{18}+a^{36},\qquad
b(v,a)=q(v+a)+q(v)+q(a).
\]

On the base field q is binary valued. Its polar form is nondegenerate
on the six binary coordinates, and its zero set Q has 28 elements.
The exact node polynomial is

\[
S(z)=\prod_{a\in Q}(z+a)=z^{28}+z^{10}+z.
\]

The identity `q(z)=z^8 S(z)` and the 28 distinct base-field roots prove
this factorization directly. Also `S'(z)=1`, so the node polynomial is
separable. The verifier checks the actual product, the polar form and
the complete zero set.

For each nonzero v in GF64, define the sixteen-node block

\[
B_v=\{a\in Q:b(v,a)=q(v)+1\}.
\]

Write

\[
L_v(z)=v z^8+v^2z^{16}+v^4(z^{14}+z^5)
       +v^8z+v^{16}z^2+v^{32}z^4.
\]

The important identities are

\[
b(v,z)=L_v(z)+v^4 z^4 S(z),
\qquad
v^2P_v(z)=L_v(z)+q(v)+1,
\]

where `P_v=product_(a in B_v)(z+a)` is monic of degree sixteen.
The first identity follows by expanding the polar form: its z^32 term
differs from the displayed z^14+z^5 term by `z^4 S(z)`. Thus L_v and
b(v,·) agree on all nodes in Q. The second polynomial has precisely the
sixteen required roots and leading coefficient v^2, so it is exactly
v^2 times the monic block polynomial.

Equivalently, for nonzero base-field v,

\[
P_v(z)=z^{16}+v^2(z^{14}+z^5)+v^{62}z^8+v^{30}z^4
       +v^{14}z^2+v^6z+v^7+v^{16}+v^{34}+v^{61}.
\]

The reviewer verifies this identity coefficient by coefficient for all
63 block polynomials, using their products of actual roots. Every
sixteen-node Vandermonde determinant is nonzero. The full family of
block polynomials has rank 7.

## Binding the field blocks to the actual native geometry

The pinned lattice basis identifies the 120 real root lines with all
nonsingular vectors of the eight-dimensional binary plus space. The
review checks all real foreign orthogonality relations against binary
polarity, and all 1120 H triples against their binary vector sums.

Fix a donor vector J and its chosen base plane
`H0={J,U0,J+U0}`. Its perpendicular complement W has dimension six,
minus type, and 28 singular vectors. For a source plane
`H={J,U,J+U}`, put

\[
w_H=U+U_0+b(U_0,U)J.
\]

This vector lies in W and is singular. Replacing U by U+J, or choosing
the other nonanchor representative of H0, does not change it. The 28
source planes give exactly the 28 singular vectors of W, with H0 mapped
to zero. The literal labels are obtained by an independently verified
binary quadratic isometry `phi:W -> GF64` and `a_H=phi(w_H)`.

For a geometric foreign receiver vector R perpendicular to J, write

\[
w_R=R+b(U_0,R)J,\qquad v=\phi(w_R).
\]

Then v is nonzero. If `s=b(U0,R)`, the equation q(R)=1 gives
`s=q(v)+1`. The receiver sees H precisely when

\[
0=b(R,U)=s+b(v,a_H),
\]

which is exactly the block condition defining B_v. The 63 geometric
receivers correspond bijectively to the 63 nonzero field parameters.
The reviewer checks these identities on every actual source plane and
receiver, not just their total counts.

All **6237 geometric source views** at the 99 donors agree with the
sixteen-node field blocks, including all **5767 native views**. Their
evaluation matrices are invertible Vandermonde matrices. A nongeometric
swap of two noncentral node labels is rejected by the isometry/view
checks even though the 28 nodes remain distinct; ordinary MDS rank alone
would not detect that incorrect geometric binding.

## Exact fibre-rank formula

If the view B_v contains centre node c, its one-dimensional inverse
fibre is represented by the coefficient vector of

\[
p_{c,v}(z)=P_v(z)/(z+c).
\]

Since `b(v,c)=q(v)+1` on this family, put

\[
U_{c,v}(z)=\frac{L_v(z)+b(v,c)}{z+c}
          =v^2p_{c,v}(z).
\]

For every base-field v this quotient is defined: on a node c in Q,
`L_v(c)=b(v,c)`. It is binary linear in v. More precisely, it is a sum
of six fixed polynomials with coefficients
`v,v^2,v^4,v^8,v^16,v^32`. The six fixed polynomials have distinct leading
degrees **7,15,13,0,1,3**, respectively, and hence are linearly
independent over GF64 and every extension.

For any parameter family T, its Moore vectors
`(v,v^2,...,v^32)` have field-linear span rank exactly
`dim_F2 span_F2(T)`. To see the nontrivial direction, choose r independent
binary parameters. A singular r-by-r Moore minor would give a nonzero
linearized polynomial of degree at most `2^(r-1)` vanishing on their
entire binary span, which has `2^r` elements. That contradicts the
degree bound for a nonzero polynomial. The other direction follows
because Frobenius powers preserve binary sums.

The independent fixed-polynomial directions and the nonzero rescalings
v^2 therefore give the exact formula

\[
\dim_K\operatorname{span}\{p_{c,v}:v\in T\}
=\dim_{\mathbf F_2}\operatorname{span}_{\mathbf F_2}T
\]

for any fixed-centre receiver subfamily and any field extension
K of GF64.

For a fixed c, the full 36-element receiver set is
`{v:q(v+c)=1}`. Its cardinality exceeds the 32 elements of a binary
hyperplane, so it spans all six dimensions. For distinct c,d, the
20-element common-node family lies in the five-dimensional hyperplane
`b(v,c+d)=0`; its cardinality exceeds 16, so it spans that hyperplane.
All 28 centre counts and all 378 pair counts are checked independently.
Thus the complete fixed-centre and common-two-node ranks are exactly
6 and 5. Every subfamily has the corresponding upper bound.

This rank argument does not rely on which fifteen receivers the old
certificate selected. It prevents saturation to rank 15 in every
propagation of this two-node form, irrespective of that selection.

## Native certificate census and genuine information change

The independent native audit checks every one of the prior 99 triangles.
It reconstructs the actual source-plane reflection using the binary
transvection at the third root of each shared H plane. This confirms
that the transported anchor plane is the literal reflected leaf plane.
For each record, the full native family seeing H, Q and R equals the
native family seeing the two anchor planes H and R. Receiver 80 is
excluded whenever the original identity-target argument requires it.

All **2970 selected-fifteen spans have exact rank 5**, and all **2970
full admissible native spans have exact rank 5**. The latter families
have between 15 and 20 receivers. The reviewer constructs 6509 distinct
actual inverse fibres directly from their fifteen off-centre evaluation
nodes, checks the complete zero set at each view, and compares them with
the sparse field-block formula.

The review additionally exhausts every fixed centre and every pair of
source nodes at each of the 99 donors, using all native receivers other
than 80. All **2772 native centre families have rank 6**, and all
**37,422 native two-node families have rank 5**. For this larger pair
census the family sizes range from 14 to 20. These ranks follow from
the verified field formula and exact binary parameter spans; the 2970
historical propagation ranks are also checked directly by field
elimination on the actual monic inverse polynomials.

The source information changes are genuine despite both old and new
systems being MDS evaluation tuples. For every anchor the reviewer
recomputes one original fifteen-receiver record with the predecessor
nodes 1 through 28. Its inverse-fibre span has rank 15. The same literal
source planes and receivers have rank 5 under the new geometric labels.
A whole-bank bijection preserves joins of partitions, including their
block cardinalities; bijective quotient labels leave those partitions
unchanged. Consequently these old and new source information systems
cannot be related by such gauges. Equality of all sixteen-observation
source-cut ranks would not have detected this difference.

This explains why the result does not contradict the earlier fixed-node
single-RS-anchor obstruction. It changes the labelled observation
partitions, and it satisfies the exceptional degeneration required by
the general array-anchor theorem. Each of its selected propagation
minors is zero because its underlying rank is 5 rather than 15.

## Field extensions, tensor widths and exclusions

The receiver parameters and source nodes remain in the fixed copy of
GF64. The calculation does not replace that finite geometric set by
arbitrary elements of a larger field. The trace expression is binary
valued on the base field; that assertion is not extended to every
element of an arbitrary coefficient field.

Every displayed matrix and polynomial has coefficients in GF64.
Nonzero minors remain nonzero in every field extension, and zero
minors remain zero. The Moore-polynomial proof also works directly
with coefficients in any such extension. Thus all exact scalar ranks
and rank bounds are preserved. The source view Vandermonde determinants
remain nonzero.

For every positive integer t, take

\[
F_R=(1,a_R,\ldots,a_R^{15})\otimes I_t.
\]

Each off-centre inverse space is the scalar inverse line tensored with
K^t. Sums commute with this tensor product, so fixed-centre ranks are
6t and the certified native pair ranks are 5t, while saturation in the
array-anchor criterion would require 15t. At the abstract bank dimension
3840 this gives quotient width 240, fixed-centre span rank 1440 and
common-two-node span rank 1200, compared with the required 3600.

These are **tensor evaluation arrays**. A Hermite source of polynomial
degree below 16t with t derivatives or jets at each node is a different
array, even though its dimensions agree. Its fibre ranks, physical early
bases and H interfaces require separate proof and verification. This
review performs none of that separate construction work.

Escaping the anchor test is not a sufficiency theorem for global
completion. In particular, this review supplies no alignment of fibres
between different original donor banks at an H cut. All claimed source
information ranks concern the specified source arrays and actual
receiver observations. The five foundational obligations, strict
suppliers, paid downstream word and global return remain unresolved.

## Replay and attribution

From the repository root:

```sh
python -I -B research/moonshot-005-program/results/bit-geometric-rs-quotients/review-b/check.py --repo . --out /tmp/independent-geometric-rs
```

The replay is standard-library Python only. `RESULT.json` contains the
summary and exact source pins; `FIELD-RESULT.json` contains all field
centre/pair checks; `DETAILS.json.gz` contains the literal 99 node tables
and all 2970 selected/full receiver records. Hashes bind the compressed
detail payload and field receipt. A polynomial-coefficient mutation and
a nongeometric node-label permutation are rejected as controls.

Independent OpenAI-assisted verification by Worker B, session S030.
Credit the root's geometric node and field-identity discovery, the native
lattice and binary quadratic-space construction, and the earlier source
and single-anchor certificates. The supplied node witness is preserved
verbatim apart from deterministic gzip compression. No author constructor
or checker was executed as an implementation dependency.
