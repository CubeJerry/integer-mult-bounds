# The native quadratic reservoir has one-dimensional local intersections

**Author theorem, independent review pending. No new kappa.**

This package connects the actual 111-port BIT source to a binary quadric,
the Schur square of a code, and an exterior-square quotient. It proves an
all-width obstruction for a specific, natural reservoir of scalar modes.
The obstruction also supplies explicit common-flat modes for constructive
chronological work. It does not construct a physical source or prove a
multiplication bound.

## 1. Definitions and the main theorem

Let k be any field of characteristic two and V any positive integer. Let
K be the native 111-by-111 binary fitting and let C be its nine-dimensional
row code, extended to k. Let J_i be the own index i together with the
indices of the real roots orthogonal to root i. Thus K_i is the indicator
of J_i. Define the Schur-square reservoir

    Q2 = span_k{c star d : c,d in C},

where star denotes coordinatewise multiplication. The binary identity
c star c=c shows that C is contained in Q2. All uses of Q2 below mean the
linear span of products; they do not ask the computational model to
multiply two unknown data-dependent values.

Let A be a fitting in V-by-V blocks: A_ii=I_V and A_ij=0 for j outside
J_i. Say that A is Q2-valued if each scalar coordinate of each block row,
viewed as a length111 vector, belongs to Q2. Its canonical quotient is

    E = (row(A)+C tensor k^V)/(C tensor k^V)
      <= (Q2/C) tensor k^V.

A pure tensor is a nonzero vector h tensor v. The condition used below is
that E contains no pure tensor over k. Requiring this after algebraic
closure, as in the companion matrix-pencil theorem, is stronger and also
suffices. Say that receiver i deletes a canonical contact if A_ij=0 for
some j in J_i minus {i}.

**Theorem 1.** If A is Q2-valued, E contains no pure tensor, and
dim_k E<2V, then at most one receiver deletes a canonical contact.
Consequently its capped proper-cover charge is at least220.

The charge convention is unchanged: chi_i=0 if the foreign whole-block
support lies in one proper real subspace of the rank7 receiver facet,
chi_i=1 if two suffice but one does not, and chi_i=2 otherwise. The
canonical source has chi_i=2 at every receiver. Thus chi=sum_i chi_i.

**Corollary 2, using the companion Kronecker theorem.** No Q2-valued
width2 fitting can have both dim E<=3 and chi<=194. Indeed that companion
theorem forces any such fitting to have a geometrically completely
entangled quotient of one of the three pure left-chain types. Theorem1
then gives chi>=220, a contradiction.

The proof of Theorem1 only requires the exact finite local-intersection
lemma in section2. The exterior interpretation in section3 is proved
separately; it is explanatory mathematics, not an additional unverified
premise hidden in Theorem1.

## 2. Exact native local spaces and the tensor argument

Write

    Llit_i = Q2 intersect k^{J_i},
    L_i = (Llit_i+C)/C <= Q2/C.

**Lemma 3 (finite native proposition).** For the pinned native source:

1. dim C=9 and dim Q2=36.
2. Llit_i = K_i star C and dim Llit_i=8 for all111 receivers.
3. C intersect k^{J_i}=k K_i, so dim L_i=7.
4. For every distinct pair i,j,

       L_i intersect L_j = k [K_i star K_j],

   and the displayed quotient class is nonzero.

The native input is
`research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz`,
SHA256
`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.
The source has finitely many fixed rational roots, not an asymptotic
parameter. The included exact binary-elimination certificate constructs
C and Q2, computes every shortening Llit_i, verifies all111 local
identities and all6105 pair intersections, and records the source pin.
The rank calculations prove the stated finite proposition; they are not
a statistical or bounded-size approximation to a varying-size claim.

These binary identities hold over every characteristic-two extension
field. Ranks of fixed binary matrices are unchanged by extension, and
extension preserves kernels, images and intersections of these finite
linear spaces. This applies to arbitrary, including transcendental,
extensions. No finite-field extrapolation is used.

**Lemma 4 (local quotient injection).** If receiver i deletes a canonical
contact, the V-dimensional output row space of A_i injects into E.

Proof. Suppose a row combination u A_i lies in C tensor k^V. Its scalar
coordinates are supported in J_i, so native local rigidity gives
u A_i=K_i tensor b for some value vector b. At a deleted canonical
contact j, K_ij=1 and A_ij=0, hence b=0. At the own block, A_ii=I_V then
gives u=0. This proves injection. The image E_i has dimension V and is
contained in L_i tensor k^V. This is the same canonical local-kernel
argument already admitted by the programme, stated here in full. QED.

**Proof of Theorem1.** If two distinct receivers i,j delete contacts,
Lemma4 supplies two V-dimensional subspaces E_i,E_j of E. Since
dim E<2V, their intersection is nonzero. On the other hand,

    E_i intersect E_j
       <= (L_i tensor k^V) intersect (L_j tensor k^V)
        = (L_i intersect L_j) tensor k^V
        = k[K_i star K_j] tensor k^V.

Every nonzero vector in the last space is a pure tensor. This contradicts
the hypothesis on E. At least110 receivers therefore retain the complete
canonical foreign support. Their charge is2 each and the remaining
charge is nonnegative. Hence chi>=220. QED.

The identity commuting tensor product with intersection follows, for
example, by expanding against a fixed basis of k^V: membership in
U tensor k^V means every scalar coefficient belongs to U.

## 3. A binary quadric and the exterior-square explanation

This section derives the local-pair structure in a coordinate-free way
once the exact native identification and local dimensions are known.

### 3.1 Recovering the finite quadric directly from the source

Let B=K+11^T over F2. The included certificate verifies rank B=8,
alternation and symmetry. Select native indices

    F = (0,1,2,4,8,14,30,59).

The principal B-submatrix G is nonsingular. Its rows, with the first
coordinate as the low bit, are

    224, 208, 176, 112, 238, 221, 187, 119.

For every source index j define x_j in F2^8 by

    G x_j = (B_fj : f in F).

All111 points are distinct, and the certificate checks
B_ij=x_i^T G x_j for every pair. Define

    q(x) = sum_a x_a + sum_{a<b} G_ab x_a x_b.

Its polar form is G. Every native x_j has q(x_j)=1; the full set q=1 in
F2^8 has120 points. Thus the native model is a puncturing by nine points
of the nonsingular plus-type binary quadric's anisotropic set. This
identification is derived and checked directly from the authenticated
source. It does not rely on identifying an externally labelled E8
configuration by visual similarity.

The affine functions 1,x_1,...,x_8 evaluate to C. The37 square-free
monomials of degree at most2 evaluate to Q2 and have rank36. Their sole
linear relation is q+1. These assertions are all checked independently
of the pair-intersection certificate.

### 3.2 Passing from quadratics to exterior algebra

Let W be the eight-dimensional space of linear forms, over k. The
quadratic part of a square-free polynomial identifies, in characteristic
two, with Lambda^2 W: the coefficient of x_a x_b goes to x_a wedge x_b.
Modulo affine functions, the identity x_a^2=x_a on the binary point set
removes squares, so this identification applies to evaluation classes.
Let

    omega = sum_{a<b} G_ab x_a wedge x_b.

The rank36 statement and the unique relation q+1 give the isomorphism

    Q2/C = Lambda^2 W / k omega.

The alternating matrix of omega is G and has rank8. Here rank is the
rank of that alternating matrix, not the dimension of its one-dimensional
linear span.

Put a_i(x)=x_i^T G x. Since K_i evaluates the affine function1+a_i,
the local identity Llit_i=K_i star C implies

    L_i = image(a_i wedge W) in Lambda^2 W/k omega.

Distinct native x_i give distinct nonzero binary a_i; hence any two
remain linearly independent over every characteristic-two extension.
The product K_i star K_j has quadratic class a_i wedge a_j.

**Lemma 5 (exterior intersection).** Let W be a finite-dimensional vector
space over a field, omega in Lambda^2 W have alternating rank greater
than4, and a,b be independent. Then the images of a wedge W and
b wedge W in Lambda^2 W/k omega intersect exactly in k[a wedge b].

Proof. If a wedge u and b wedge v have equal quotient classes, then

    a wedge u - b wedge v = lambda omega.

The alternating rank on the left is at most4, since the image of its
alternating linear map is contained in span(a,u,b,v). If lambda is
nonzero the right side has rank greater than4, impossible. Hence
lambda=0. In the ordinary exterior square,
(a wedge W) intersect (b wedge W)=k(a wedge b), as is seen by extending
a,b to a basis. Conversely a wedge b belongs to both spaces and cannot
be a multiple of omega, whose rank exceeds2. QED.

Applying Lemma5 to the rank8 native form recovers Lemma3(4). This shows
why the source-pair certificate has the same answer for all6105 pairs:
it is the quotient of a Grassmannian incidence identity by one high-rank
alternating form.

## 4. Actual common-flat representatives and acquisition implications

The quotient line has the literal representative q_ij=K_i star K_j.
Its own i and j coordinates both equal K_ij. Define

    m_ij = q_ij + K_ij(e_i+e_j).

Then m_ij is supported on exactly the common foreign neighbours of i,j.
All of its source roots lie in the rank6 real flat F_i intersect F_j.
For every native pair they span that entire flat. The certificate gives
an exact lower bound6 using a nonzero minor modulo101 and an exact
upper bound6 from orthogonality to the two independent real roots.

For the3235 orthogonal pairs, the support cardinality ranges from23 to30.
For the2870 nonorthogonal pairs, it ranges from29 to36. The exact
histogram is in RESULT.json. Thus these modes always have a genuine
proper common chart, but their complete support cannot be acquired in a
smaller-rank chart.

For nonorthogonal i,j, m_ij=q_ij. For orthogonal i,j, the two own terms
must be restored when q_ij is required. Removing them need not preserve
the canonical quotient class: e_i+e_j is generally not canonical. Any
physical construction must account for where these terms reside, how
they are read or recoded, the complete chart-to-chart route, every dirty
record, and cleanup. A proper-flat aggregate alone is not a source word.

Theorem1 concerns the quotient of the assembled fitting. It does not
bound the number of chronological states of a packet or prohibit
interleaving higher-dimensional histories of quadratic modes. In
particular it does not convert the scalar dimension36 into a physical
packet lower bound. The constructive multi-packet chronology work may
use the modes m_ij while leaving the d<2V hypothesis.

## 5. Boundary controls and exact scope

### 5.1 The pure-tensor exclusion is necessary

Take the orthogonal native pair i=0,j=1. In the scalar fitting replace
rows i,j by q_ij and leave all others canonical. The own entries remain1
and the forbidden entries remain0. Both changed rows delete contacts.
Their canonical quotient has dimension1 and is generated by [q_ij].
Tensoring by I_V gives quotient dimension V<2V but has pure tensors.

At each changed receiver, the foreign support is the rank6 common flat
support together with the other root. Its rank is7, so it is not in one
proper receiver subspace. The displayed two-piece cover gives chi_i=1.
The whole fitting therefore has chi=220. This is a native algebraic
positive control, not a physically implemented source.

### 5.2 Rank greater than4 in Lemma5 is essential

In W=k^4 let omega=e1 wedge e2+e3 wedge e4, of rank4. For a=e1,b=e3,
the two local images intersect in the two-dimensional span of

    p=[e1 wedge e3],
    q=[e1 wedge e2]=[e3 wedge e4].

Let r=[e1 wedge e4] and s=[e2 wedge e3]. These four quotient vectors are
independent. The space

    E=span{(r,p),(p,q),(q,s)}

is a pure C3 chain: it has dimension3 and no pure tensor over any field
extension. Its first two generators belong to the a-local tensor space;
its last two to the b-local tensor space. These two local planes share
the non-pure vector(p,q). Thus the mechanism of Theorem1 cannot be
extended to a rank4 form by dropping the rank hypothesis. This example
is an abstract local-geometry control, not a native fitting.

For completeness, a nonzero combination of a pure shifted chain has
linearly independent value slices: their first and last nonzero scalar
coordinates occur at different endpoints. The argument works over every
extension, not merely the binary field used to replay coordinates.

### 5.3 What is and is not proved

The all-width theorem is a proved implication of the exact authenticated
finite local geometry, with independent review pending. The companion
Kronecker theorem is an explicit additional dependency of Corollary2.
There is no general lower bound for arbitrary scalar reservoirs, larger
canonical quotients, recoded source interfaces, or chronological packet
histories. No full recursive supplier, uniform complex companion,
precision theorem, ownership theorem, or multiplication bound is supplied.
The five foundational assumptions remain unchanged.

## 6. Provenance, research connection, and reproduction

The canonical local-kernel theorem is in programme
`results/bit-operator-canonical-quotient/author/PROOF.md`, sections1--2.
The real-facet/canonical-charge source facts are retained in
`results/bit-monotone-arrival-gate/PROOF.md`. Their exact SHA256 hashes
are recorded in RESULT.json. The companion package is the present
session's Kronecker-quotient proof; its final integration path must be
recorded with Corollary2 before admission.

The mathematical exploration was motivated by the coding/geometry
dictionary in Hugues Randriambololona, [On products and powers of linear
codes under componentwise multiplication](https://arxiv.org/abs/1312.0022),
and [The quadratic hull of a code and the geometric view on multiplication
algorithms](https://arxiv.org/abs/1912.06627), especially the latter's
quadratic-identity viewpoint. Those papers provide context and
terminology; neither proves this native local-intersection result or
the physical-cost bridge sought by the programme. The finite-quadric and
exterior arguments above are self-contained.

Reproduce the exact author certificate with:

```sh
python author/check.py --repo /path/to/integer-mult-bounds --output author/RESULT.json
```

Expected status: `PASS_AUTHOR_QUADRATIC_EXTERIOR_CONTROLS`, dimension36,
111 local spaces of literal dimension8,6105 pair intersections of
quotient dimension1, and both boundary controls. Source pin mismatch,
any local-rank mismatch, or any wrong pair dimension fails closed.

This package is AI-assisted research for @CubeJerry's persistent
programme and preserves credit for all cited predecessor arguments.
