# Exact total Gaussian-rank conservation in the Pauli-split commuting source

**Proved within the stated source architecture; independent review pending.**
For every fixed number of retained roles and every number of actual split
native calls, arbitrary invertible ordinary matrices from the full translation
algebra cannot produce independent Gaussian endpoints of total rank larger
than twice the number of calls. This closes the entire commuting/Pauli-split
finite synthesis architecture, including mixed orientations and all actual
phase sectors. It does not restrict arbitrary head-permutation transport or
the full ordinary algebra. No new κ.

## 1. Precise model and source dependence

Use the actual source gauges and all-eight-sector lift in
`PAULI-SPLIT-GAUGED-SOURCE.md`. At any fixed Pauli character, the seven normalized
Gaussian direction labels x_v, v∈F₂³\{0}, satisfy

    x_v²=1,       product_v x_v=1.                       (1)

There are no other independent relations: their group is C₂⁶. A source is an
embedded block `N(u,w)=[[x_u,1],[0,x_w]]`, u≠w, or its inverse. Its two labels
are each charged once. Inverse-source availability is authenticated separately
from the physical upper half in `INVERSE-SPLIT-SOURCE-GAUGE.md`; algebraic
inversion is not a free primitive.

Fix any finite R≥2 and m≥0. Let W be a product of m such embedded sources and
arbitrary invertible scalar R×R matrices, including arbitrary scalar endpoint
encoders. Scalars may be arbitrary complex numbers and may vary with the
Pauli sector or width. Suppose on the group (1) the product supplies R
independent Gaussian monomials g_j, up to scalar invertible endpoint matrices:

    W(x)=E diag(g_1(x),...,g_R(x)) F.                    (2)

Each g_j is represented by a subset S_j of the seven labels. Its Gaussian
matrix is `B_j=sum_{v∈S_j} vvᵀ` over F₂; complementary subsets represent the
same normalized group element and the same B_j. Put
`H=sum_j rank_F₂(B_j)`. Rank-zero ordinary endpoints are allowed.

**Theorem.** Every word satisfying (2) obeys `H≤2m`.

The physical all-width assertion is made only in this architecture: ordinary
interstages and endpoint encodings belong to Mat_R(C[T]), where T is the
actual eight-element global translation group. On each Pauli character they
are the scalar matrices above. The retained large-width tensor Gram theorem
makes the finite phase-group algebra faithful at sufficiently large widths;
thus an all-width physical identity implies (2) in every sector. No phase
quotient of a nontrivial sector is silently used.

## 2. A determinantal rank-rounding lemma

**Lemma.** For every complex R×R matrix M, there exists a sign vector
c∈{−1,1}^R such that for every diagonal sign matrix D=diag(d_1,...,d_R),

    number of indices j with c_j≠d_j ≤ rank(M−D).         (3)

**Proof.** The principal-minor expansion gives

    2^(−R) sum_c det(I+diag(c) M)=1.

Every nonconstant sign monomial averages to zero. Choose c for which
`A=I+diag(c)M` is invertible. If x∈ker(M−D), then

    A x=(I+diag(c)D)x.

The vector on the right is supported only on the coordinates where c_j=d_j.
Since A is injective, the kernel has dimension at most the number of those
coordinates. Rank-nullity yields (3). This works for arbitrary complex M;
no positivity, normality, or diagonalizability is required. ∎

## 3. Evaluate the same word outside the Fano relation

Temporarily let all seven x_v be independent signs. The same explicit source
word W is well-defined and invertible at every one of the 128 assignments,
since every source has invertible diagonal signs and every interstage is an
invertible scalar matrix. Equation (2) is required only on the 64 assignments
with product of signs +1.

Choose any assignment η with product -1. For each v, negating x_v gives an
assignment η^v with product +1. Let n_v count how many source factors use v.
A source not using v is unchanged. A source using v has difference of matrix
rank one, and its inverse also does, by

    B⁻¹−C⁻¹=B⁻¹(C−B)C⁻¹.

Expand the difference of the full products W(η) and W(η^v). Each of the n_v
changed factors contributes a term of rank one, with all other factors
invertible. Hence

    rank(W(η)−W(η^v))≤n_v.                               (4)

Extend each chosen subset monomial g_j to all independent sign assignments,
and put D₀=diag(g_j(η)). The actual even-sign identity (2) gives

    W(η^v)=E D₀ T_v F,
    T_v=diag((-1)^(1_{v∈S_j}))_j.

Set `M=D₀⁻¹ E⁻¹ W(η) F⁻¹`. Equation (4) becomes

    rank(M−T_v)≤n_v                                      (5)

for all seven directions, simultaneously. Notice that W(η) is only a proof
evaluation of the explicit finite word. It is not a physical source oracle
or an assumption about an unrepresented phase sector.

## 4. One simultaneous rounding gives conservation

Apply the lemma to M and choose one sign vector c that works for every T_v.
For row j with c_j=-1, replace S_j by its complementary subset; for c_j=1,
leave it unchanged. Call the resulting subset S'_j. The full seven-label
relation in (1) ensures that this replacement changes neither g_j nor B_j.
For each direction v, its number of occurrences among the S'_j is exactly
the Hamming distance between c and the diagonal of T_v. Therefore (3) and
(5) give

    number of j with v∈S'_j ≤ n_v.

Finally, matrix-rank subadditivity gives

    H = sum_j rank(B_j)
      ≤ sum_j |S'_j|
      = sum_v number of j with v∈S'_j
      ≤ sum_v n_v
      = 2m.

This proves the theorem for arbitrary source counts, role counts, direction
assignments, orientations, scalar coefficients, and phase sectors.

## 5. Complete fresh-body invoice consequence

Suppose m≥1 actual native calls use m fresh seven-bit bodies and R retained
roles on their common source volume. Each native pays `[1]+[7]+[8]` and every
inactive role pays its rank-seven body transform. Thus at exponent 0<t<1 the
optimistic Gaussian source price is

    P=m + (R−1)m 7^t + m 8^t
     =Rm 7^t + m(1+d),     d=8^t−7^t<1.

The independent endpoints have body rank 7m and head ranks h_j∈{0,1,2,3}, so

    T=sum_j (7m+h_j)^t.

By concavity, `(7m+h)^t≤(7m)^t+h d` for integer h≥0, and
`(7m)^t≤m 7^t`. With H≤2m this yields

    T≤Rm 7^t+2m d,
    P−T≥m(1−d)>0.                                      (6)

The actual spectator factor 2^V and every other common-volume multiplier
remain on both sides. Ordinary, source, compiler, precision, ownership and
recursive expenses can only worsen this already strict deficit. Thus adding
more calls or roles inside this architecture cannot yield a complex supplier
saving. In particular the optimistic four-native target (3,3,3) is impossible,
and the positive arithmetic margin alone was never a construction.

## 6. Architectural implication and scope boundary

The actual split source, exact Fano identity and all-Pauli-sector reduction
remain valid proved components. The scalar/translation-algebra interstage
construction is now closed for every fixed native count, rather than merely
for the first tested four-call word. A useful next caller must introduce a
mathematical mechanism outside this conserved class: genuinely nontrivial
ordinary head transport between retained roles, a changed noncommuting source,
a different body/endpoint interface, or another source of paid Gaussian work.

A head permutation acts on the Gaussian direction labels and is not scalar
in these simultaneous phase coordinates. Such operations therefore break the
hypothesis behind the odd-sign comparison. They are not claimed sufficient;
their actual source compatibility, field costs, uniform implementation,
precision and recursion still have to be established.

Credit @CubeJerry and predecessor source authors. Worker B developed the
actual commuting-direction source, full-sector lift, determinantal rank
rounding, and simultaneous odd-sign conservation argument, with OpenAI
assistance. The earlier seven-direction and four-call completion lemmas are
now corollaries; their history is retained without presenting finite searches
as proofs.
