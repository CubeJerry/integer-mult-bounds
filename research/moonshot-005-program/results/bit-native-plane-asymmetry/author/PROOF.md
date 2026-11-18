# Odd native witnesses force at least seventeen different plane projectors

**Source-specific algebraic necessity, with a sharp abstract control.** This
does not construct a full source code or claim a new kappa. The result applies
to the separated quotient interfaces forced at the tight first source cuts
of the S022 balanced atlas. It uses the aligned-lift conclusion of the
retained source-quotient argument, as extended to tight balanced donors in
S023. No common maximum-distance-separable dictionary is assumed.

## 1. Interface and finite native witnesses

Let F have characteristic two, let s be a positive integer, and let the
common original-input bank G have dimension b=16s. Fix a native receiver i.
A donor j is tight for i when its sixteen visible A2-plane emissions each
have dimension s and their combined capacity is b. The actual balanced
atlas has s=360 field slots before any internal-width or field-expansion
factor. Exclude a donor whose visible singleton plane has 540 slots; those
are precisely the 360 source--receiver pairs with capacity 5,940.

For every tight donor j and visible plane H, let

    f_(j,H): G -> Q_(j,H)

be its rank-s quotient map. At receiver i its sixteen maps form a direct
coordinate decomposition. Let L_(i,H) be the source fibre obtained by fixing
the other fifteen coordinates. It has dimension s. The saturated shared
H-to-i cut forces the same actual input subspace L_(i,H) for any two tight
donors in H. This is the retained sumset/aligned-lift lemma; there is no
assertion that their quotient kernels are equal.

The unique linear decoder projection

    E_(j,H): G -> L_(i,H) <= G

has kernel ker f_(j,H) and is identity on L_(i,H). At every tight donor,

    sum_(H visible at j) E_(j,H) = I_G.                 (1)

The exact native incidence certificate finds an odd set S of tight donors
for 87 of the 111 receivers, such that every A2 plane in F_i meets S in
zero or two donors. For example receiver 2 has the following 27-element S:

    3,6,7,23,24,27,28,52,53,56,57,66,68,69,71,73,
    75,78,80,97,99,100,102,103,105,108,110.

Every member has sixteen visible planes, all of which meet S in two.
Consequently this witness has 27*16/2=216 paired planes. The statement is
on the pinned finite native incidence table; it is checked directly by
integer root dot products and binary elimination. The script stores an
explicit witness for each of the 87 receivers. The other 24 receivers are
not excluded by this witness test; absence of this certificate is not a
construction of their source codes.

## 2. A square-zero decomposition of identity

For a paired plane H meeting S in {j,k}, put

    N_H = E_(j,H) + E_(k,H).

Both projections have the same image L_(i,H), on which both act as
identity. Thus E_j E_k=E_k and E_k E_j=E_j, and in characteristic two

    N_H^2 = 0,              rank N_H <= s.              (2)

Sum (1) over the odd set S. Each incident H occurs exactly twice, giving

    I_G = sum_(paired H) N_H.                           (3)

Write R=sum_H rank N_H and r=max_H rank N_H. Some term is nonzero.
For every H, I_G+N_H is invertible with inverse I_G+N_H. Equation (3) gives

    b <= rank(sum_(K != H) N_K)
       <= R-rank N_H.

In particular

    R >= b+r.                                           (4)

If only m planes have N_H nonzero, remove one of them. The remaining m-1
terms each have rank at most s. Therefore

    (m-1)s >= b=16s,       m >= 17.                     (5)

So at least seventeen distinct paired planes have different decoder
projections at their two tight donors. Since the image is fixed, two such
projections agree exactly when their kernels agree. Each witness therefore
forces genuine donor-dependent source quotient kernels at at least
seventeen of its paired planes.

This proves more than failure of a generic scalar code: a direct common
kernel K_H for all donors at each H is impossible on this balanced source,
at every positive block width and after every characteristic-two field
extension. The same holds after one common global input change of basis.
It does not exclude independent donor changes of basis, arbitrary
donor-dependent kernels, the eleven exceptional singleton encoders, or a
changed source diagram. The seventeen-plane requirements overlap and must
not be added across receivers as independent rank or MOVE costs.

## 3. The seventeen-term case is rigid and algebraically attainable

Suppose (3) has exactly seventeen nonzero terms. On removing any one term,
the other sixteen must sum to an invertible map on a 16s-dimensional bank.
All seventeen terms consequently have rank s, and the images of any sixteen
terms form a direct sum equal to G. Their row spaces have the same property.

There is also a complete normal form. Factor N_h=U_h V_h, with U_h injective
from F^s to G and V_h surjective to F^s. Let U=[U_1 ... U_17] and stack
the V_h in V. Then UV=I_G, while V_h U_h=0 follows from N_h^2=0 and the
full ranks. Thus P=VU is a rank-16s projection on F^(17s) whose diagonal
s-by-s blocks are zero. Its complement E=I-P is a rank-s projection with
every diagonal block I_s. Write E=AB at full rank, with block rows A_h and
columns B_h. Each A_h B_h=I_s, so A_h is invertible and B_h=A_h^-1.

After conjugating the 17 block coordinates by diag(A_h), E becomes
J_17 tensor I_s and P becomes (I_17+J_17) tensor I_s. Here J is the all-ones
matrix. The number seventeen is odd, so J_17^2=J_17 in characteristic two.
The kernel of U in these coordinates consists of equal block vectors.
Any sixteen U_h form a basis; identify the first sixteen with the standard
block basis of G. The last U_17 is their sum. This determines the V_h by
VU=I+J. Hence, up to simultaneous conjugation on G and changes of internal
factor bases, every minimum-size family is the following simplex family.

For s=1 and n=16, write e_1,...,e_n for the standard columns and 1 for the
all-ones column. Define

    U_h=e_h,       V_h=e_h^T+1^T       (1<=h<=16),
    U_17=1,        V_17=1^T.

Then sum_h U_h V_h=I_n, every V_h U_h=0, and all seventeen products have
rank one. Tensoring with I_s gives the claimed sharp block family. Each
square-zero rank-s map can indeed be expressed as the difference of two
rank-s projections onto its image: choose W_h with W_h U_h=I_s and use

    E_h=U_h W_h,      F_h=U_h(W_h+V_h).

Both are projections onto im U_h and E_h+F_h=N_h.

This is a positive algebraic control and a constructive target for a
minimum-asymmetry source interface. It does not assign these seventeen
maps to compatible native planes across all receivers, supply the missing
source quotient spaces, or account for actual new routes. The native
embedding and the rest of the physical source remain open.

## 4. Reproduction, dependencies, and next construction

`check.py` authenticates the S013 root table and S022 layout, independently
identifies tight donors from the singleton-plane incidence, and verifies
all emitted odd witnesses. It tests the rank/square-zero/sum identities
of the simplex family and its projection realization at s=1 and s=2.
A one-plane deletion and a wrong self-dual factor both fail their intended
identities. The all-width statements follow from the written argument
and tensor construction, not from extrapolating these finite checks.

The next constructive test is a genuinely donor-dependent quotient source.
At a minimum-size witness its image subspaces must realize the simplex
normal form above. Source alignment across different receivers, the
weighted early-lane basis criterion, every local shared port, and all
original endpoint/cost contracts must hold simultaneously. This result
does not turn asymmetry into an additional paid-movement tariff.

Credit @CubeJerry, the original native/atlas source authors, the S022
source-quotient and balanced-routing proofs, and S023 workers A and B.
Root developed the odd-witness operator identity and sharp simplex
classification with substantial OpenAI assistance. Independent review is
recorded separately; no human or formal-kernel review is asserted.
