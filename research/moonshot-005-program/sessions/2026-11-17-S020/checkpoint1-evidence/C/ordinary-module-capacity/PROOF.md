# Regular dimension and augmentation constrain ordinary bank capacity

**Proved algebraic obstruction in the fixed finite root-four ordinary
catalogue. No complete caller, supplier, or new kappa.** This concerns
ordinary split embeddings of free whole banks into ordinary idempotent
ranges. It does not constrain Gaussian-component projection by physical
source rank, and it does not exclude every coupled complex caller.

## 1. Precise ordinary interface

Fix a finite literal catalogue of root-four monomial matrices on a fixed
one-column space. Close it under products and inverses, including the
idempotents and all entries of the proposed input map and retraction. Divide
by the scalar fourth-root centre of this finite group. Call the quotient
`G`. At widths `V` divisible by four, its scalar cocycle is trivial. At all
sufficiently large such widths, the retained tensor-separation theorem makes
the projectively distinct collective lifts linearly independent. The
physical ordinary algebra is thus faithfully isomorphic to `C[G]`.

For completeness, the separation mechanism is elementary. Choose one
unitary representative of each projective group element. For distinct
representatives `u,v`, the normalized trace has modulus
`|tr(u* v)|/d<1`; equality would make them projectively equal. The normalized
Hilbert-Schmidt Gram matrix of their tensor lifts has off-diagonal entries
`(tr(u* v)/d)^V`. Since the catalogue is finite, its off-diagonal row sums are
strictly below one at all sufficiently large widths. The Gram matrix is
then invertible. Restricting to widths divisible by four simultaneously
removes the scalar cocycle and supplies the faithful group-algebra map.

Coefficients may depend on width, but the finite catalogue may not grow with
it. An all-positive-width uniform ordinary construction must in particular
satisfy this subsequence. Small-width coincidences do not supply the
faithful-algebra hypothesis.

Let `P` be an idempotent in `Mat_n(C[G])`. An ordinary split embedding of `r`
free banks in its image consists of actual ordinary matrices

    C in Mat_(n,r)(C[G]), D in Mat_(r,n)(C[G]),
    P C=C,                  D C=I_r.                  (1)

An image of coordinate banks under an ordinary unit has such a pair: use
the corresponding columns of the unit and rows of its actual inverse. We
do not infer (1) merely from physical image dimension or regard its inverse
as a free operation.

Use the regular representation of `C[G]`, of dimension `|G|`, as a faithful
mathematical comparison representation. It is not a changed physical cost
model. Define

    tau(P)=rank_regular(P)/|G|,
    epsilon(sum_g c_g g)=sum_g c_g.

Augmentation is an algebra homomorphism, applied entrywise to bank matrices.

## 2. Dimension-and-augmentation lemma

Every pair (1) satisfies

    r <= tau(P),         r <= rank(epsilon(P)).         (2)

If `r=tau(P)`, then necessarily

    rank(epsilon(P))=r.                                (3)

**Proof.** In the regular representation, `D C=I_r` gives rank `C=r|G|`.
Its image lies in the image of `P`, giving the first inequality. Applying
augmentation to (1) gives the second.

At equality in the regular inequality, the two regular images coincide.
Put `Q=C D`. This idempotent fixes the image of `C`, hence `Q P=P` in the
regular representation and, by faithfulness, in the algebra. Together with
`P Q=Q`, this makes `epsilon(P)` and `epsilon(Q)` have the same image.
But `epsilon(D)epsilon(C)=I_r` makes the latter image have dimension `r`.
This proves (3). We do not assume `P=Q`; their kernels can differ.

Consequently an integer capacity equality is impossible when augmentation
has a different multiplicity. For noninteger `tau(P)`, this argument need
not improve the integer floor `r<=floor(tau(P))`.

## 3. Same-sign involutions

For nonidentity involutions `s_j in G`, put

    p_j^+=(1+s_j)/2,        p_j^-=(1-s_j)/2.

Their regular ranks are `|G|/2`: regular left multiplication by a
nonidentity group element has trace zero. Their augmentations are one and
zero respectively. Different `s_j` need not commute or be conjugate.

A direct sum of `n` plus projectors has `tau(P)=n/2` and augmentation rank
`n`. Every positive free-bank embedding therefore obeys

    2r<n,        or r<=floor((n-1)/2).                 (4)

In particular **two plus sectors cannot contain one ordinary free bank**,
even if their total physical image dimension is greater than a bank. This
excludes the repeated-plus ambient-range escape that passes a physical
rank test; it does not require the ambient range to equal the endpoint.

A direct sum of any number of minus projectors has augmentation zero, so
it contains no positive free-bank split embedding. Its physical kernel
vectors can nevertheless be nonzero and useful.

For `n_+` plus and `n_-` minus sectors, regular dimension gives
`2r<=n_++n_-`, while augmentation gives `r<=n_+`. If equality holds in the
regular bound, necessarily

    n_+=n_-=r.                                       (5)

This is necessary for arbitrary involutions, and sufficient when plus/minus
sectors can be paired with the same involution, as the control below shows.

## 4. Constructive controls and sharpness

For one involution `s`, let `p=(1+s)/2`, `m=(1-s)/2`. Then

    C=(p,m)^T, D=(p,m), D C=1, diag(p,m) C=C.

They extend to the ordinary involution

    U=[[p,m],[m,p]],          U^-1=U,

which identifies the balanced range with one full bank. The theorem thus
preserves the genuine complementary-sector controlled route.

The strict same-plus bound can be attained. Let `s,t` be commuting
independent involutions, `u=s t`, and

    p_s=(1+s)/2, p_t=(1+t)/2, p_u=(1+u)/2,
    e=(1+s+t+u)/4.

Then `p_s+p_t+p_u=1+2e`, with actual inverse `1-(2/3)e`. Hence

    C=(p_s,p_t,p_u)^T,
    D=(1-(2/3)e) (p_s,p_t,p_u)

satisfy `D C=1` and `diag(p_s,p_t,p_u) C=C`. Three same-plus sectors
can contain one free bank. Literal independent sign passes
`Z_a,Z_b,Z_a Z_b` realize these identities at every width. This supplies
an explicit algebraic inverse, not a claimed profitable Gaussian endpoint
or a complete implementation invoice. It prevents overstating (4) as
impossibility for every number of plus sectors.

## 5. Subgroup-average extension

For nontrivial subgroups `H_j<=G`, set

    e_j=(1/|H_j|) sum_(h in H_j) h.

Their regular ranks are `|G|/|H_j|` and augmentations one. Thus for
`P=diag(e_1,...,e_n)` an ordinary free-bank embedding requires

    r <= sum_j 1/|H_j|,

and equality is impossible when `r>0`: augmentation rank `n` is strictly
larger than that sum. For equal order `h`, necessarily `h r<n`. Three
same cyclic-plus order-three sectors cannot contain one ordinary free bank.
Direct sums of their complements have augmentation zero and cannot contain
any positive free bank.

The subgroup must be nontrivial in the projective quotient actually used.
A scalar fourth-root phase becomes identity at widths divisible by four;
treating it as a nonidentity involution would invalidate the regular-rank
calculation. The independent checker includes an identity-element control.

## 6. Source application boundary

The admitted spectator kernels `(I-SWAP_ad^tensor V)/2` and
`(I-SWAP_ab^tensor V)/2` are genuine nonzero ordinary channels. Their direct
sum nevertheless lacks a free ordinary bank by augmentation. A full column
of an ordinary unit can retain the missing representation types in other
banks, so this does not contradict the admitted kernel construction.

For spectator plus ranges the exact physical rank is `(16^V+8^V)/2`.
Two have physical dimension `16^V+8^V`, greater than one bank. Despite this,
(4) excludes one free ordinary bank within those two plus ranges at
sufficiently large faithful widths divisible by four.

Neither conclusion can be applied to a Gaussian-rank component just because
it comes from a singular source sum: Gaussian-class projection can increase
rank and need not preserve the source's ordinary submodule. A coupled
caller is excluded only after its actual endpoint image is proved to lie
in the relevant ordinary idempotent range. Sources, inverses, independent
endpoint separation, and the whole invoice remain obligations.

## 7. Verification and provenance

The independent checker uses rational group-algebra coefficients, regular
matrices, and augmentation. It verifies both constructive controls and
their inverses, same-sign capacity hypotheses, cyclic-order-three ranks,
and rejection of an identity element labelled nontrivial. The proof above
and the admitted fixed-catalogue tensor-separation interface establish the
universal theorem; finite controls do not substitute for that proof.

Source context is pinned in `MANIFEST.json`: the admitted S019
ordinary-character and spectator-kernel results and tensor-separation
predecessors. This S020 proof was independently reconstructed by Worker C
with substantial OpenAI assistance for @CubeJerry. No uncommitted S019
proof is claimed recovered. All five foundations remain; no complete
kappa improvement is established.
