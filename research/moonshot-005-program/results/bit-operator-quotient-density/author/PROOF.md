# A proportional canonical-quotient gap from shared operator directions

**Author theorem; independent review pending. No new supplier or complete kappa.**

This extends the packet-width operator gate to larger quotient dimensions.
The new ingredient is common-vector gluing followed by a subspace-intersection
argument. Historical dimension is not a count of physical packet identities.

## Exact proposition

Let k be any characteristic-two field, V a positive integer, K the pinned
canonical binary fitting on the actual 111 BIT ports, C its nine-dimensional
row code, and C_V=C tensor k^V. Let A have V-by-V blocks with A_ii=I_V and
A_ij=0 whenever K_ij=0. Blocks may be singular and noncommuting. Write

    E=(row(A)+C_V)/C_V, d=dim E,
    ell_i=1[foreign block support(A_i)>36]+1[foreign block support(A_i)>52],
    w_i=2-ell_i, S=sum_i w_i.

The source premises are the reviewed rank-eight single and rank-seven pair
forbidden restrictions, canonical degree census, and seventeen-savings
root-support envelope from bit-one-extra-coset and bit-quotient-direction-savings.
Their old no-Y-feedback physical premise is not used. Quotient injection is
also established by the companion bit-operator-canonical-quotient result.

**Theorem.** If S>17, then d>=V+ceil(V/17). More precisely, if t positive-saving
rows together save more than17, then

    d>=V+ceil(V/(t-1)).                                    (1)

If S>=28 and b rows have ell_i=0, then

    d>=V+ceil(V/(17-min(b,9))).                            (2)

The retained all-route target condition sum ell_i<=194 implies S>=28, so
every source in that theorem's model must meet this quotient gap. If its
historical X-code W supplies row(A), the same bound holds for (W+C_V)/C_V.
If C_V is actually contained in W, then dim W>=10V+ceil(V/17). This is not
a claim that arbitrary rank(A)>10V, nor a sufficient condition for a source.

## 1. Saving rows inject a whole width into the quotient

For each i with w_i>0 set phi_i(u)=u A_i+C_V. If u is in its kernel, the
single forbidden restriction forces u A_ij=K_ij v for one row vector v.
The diagonal gives v=u. A saving row has foreign support at most52, whereas
every canonical degree is at least55. At a deleted canonical block j,
0=u A_ij=u. Thus phi_i is injective and E_i=im(phi_i) has dimension V.

## 2. Common-vector gluing

Let q be nonzero in the intersection of E_i for a set I of saving rows.
Injection supplies a unique nonzero u_i with u_i A_i representing q. Fix
one representative h of q. Each h-u_i A_i lies in C_V and agrees with h on
the forbidden set Z_i. If |I|<=3, the rows save at most6. Otherwise the
distinct binary coefficient normals have rank at least3 over k. The credited
three-normal gluing argument applies entrywise to their V scalar coordinates.
It gives one representative g of q satisfying

    supp(g) is contained in intersection_(i in I) T_i,
    u_i A_ij=K_ij (u_i-g_i)+g_j.                           (3)

Here g_j is a row vector, T_i is the closed canonical support, and the
diagonal fixes u_i-g_i. This is linear gluing; the full images E_i need not
coincide. Since q is nonzero, g is nonzero.

Put D=supp(g), s=|D|, r=real rank of the native root lines in D,
J=I intersect D, j=|J|, and U=I minus D. For i in U, g_i=0 and u_i is
nonzero. If a canonical contact z outside D were a zero BLOCK of A_i,
(3) would force u_i=0. Consequently the original BLOCK row retains at
least a_i-s canonical contacts, not merely its projection u_i A_i. Allow
both savings freely on J. The exact root geometry gives

    r<=s<=N_r, 0<=j<=min(r,s), s<=j+N_(r-j), |U|<=N_(8-r),
    sum_(i in I) w_i <= min(N_(8-r),F(52+s))
                         +min(N_(8-r),F(36+s))+2j.

Here F counts canonical foreign degrees and N=(0,1,3,6,12,20,36,111,111).
The reviewed 569-case envelope and rank-three/orthogonal-four refinements
bound this expression by17. They use only support sets, so apply unchanged
to vector-valued g. Therefore

    sum_(i in I) w_i>17 implies intersection_(i in I) E_i={0}.  (4)

## 3. Dimension and weighted consequences

For t subspaces of dimension V inside dimension d, codimension subadditivity
gives dim intersection E_i>=d-t(d-V)=V-(t-1)(d-V). Combining with (4) proves
(t-1)(d-V)>=V and hence (1). If S>17, select positive-saving rows until their
integer weights first exceed17. Each weight is1 or2, so at most18 rows
suffice. Thus d>=V+ceil(V/17), uniformly in V.

For (2), choose double-saving rows first. If b>=9, nine rows suffice. If
b<=8, choose all b double-saving rows and18-2b single-saving rows. S>=28
ensures enough singles. The chosen size is18-b, giving (2).

Over a finite field of q elements there is also an incidence inequality:

    S*(q^V-1)<=17*(q^d-1).                                (5)

Count nonzero quotient vectors in every E_i with weight w_i. Each E_i has
q^V-1 such vectors; (4)'s stronger pointwise statement bounds each vector's
weighted multiplicity by17. This finite-field corollary does not replace
the all-field dimension argument.

## 4. Limits and meaningful negative controls

The abstract overlap argument alone cannot improve the factor18/17. Over
GF(32) take E=k^18 and, for28 distinct a, the hyperplanes

    E_a={z:sum_(j=0)^17 a^j z_j=0}.

They have V=17. A nonzero z gives a polynomial of degree at most17, so lies
in at most17 of these hyperplanes. Their total unit weight is28 and d=18
attains the bound. Tensoring with k^s gives equality at V=17s,d=18s: one
nonzero component polynomial bounds common membership. This is an abstract
subspace arrangement, NOT a native fitting or a physical source. It refutes
a claim d>=2V based only on the pointwise overlap premise. The checker uses
exact GF(32) arithmetic and a polynomial with17 prescribed roots; the
Vandermonde/root argument establishes all subsets without finite extrapolation.

The credited sharp tensor fitting has S=17 and d=V. Thus S>17 cannot be
weakened to S>=17. Dimensional controls also show positive intersection
below (1), zero intersection at equality, and that pairwise nonzero
intersections do not imply a common nonzero intersection.

## Scope, cost and next obligation

The universal proof is separate from finite controls. Source hashes and
reused evidence are recorded explicitly. Independent review must check the
full-block-to-vector implication in (3), not merely execute a verifier.

No algorithm or movement discount follows. Physical consequences retain the
all-route theorem's complete caller and operation assumptions. Acquisition,
ownership, erasure, precision, compiler, cover and recursion remain open;
both strict suppliers and all five foundations remain. No new kappa.

Next: exploit native support geometry beyond abstract subspace intersections
to construct a useful multi-image code, or strengthen its quotient gap.
Every candidate still needs an actual paid chronology and all endpoints.

Credit @CubeJerry, native/canonical contributors, earlier scalar gluing and
savings authors/reviewers, Worker C's forced-injection extension and independent
overlap observation, and the lead's common-vector/dimension synthesis.
Substantial OpenAI assistance; no human or formal-kernel acceptance claimed.
