# Independent review of native plane asymmetry and the seventeen-term normal form

**Accepted in the stated quotient-source model.** The odd native witnesses
force at least seventeen nonzero plane-projector discrepancies. The rank
inequality and sharp simplex classification are valid for every positive
block width in characteristic two. They neither exclude all donor-dependent
sources nor assign a compatible source on the full native diagram.

## Native applicability

At a tight receiver each participating donor has sixteen independent
quotient coordinates of dimension s on a common 16s-dimensional input
space. The source-quotient proof identifies the same lift image at a shared
plane for any two tight donors there. Projecting onto that image along the
individual quotient kernel is therefore well-defined. The sixteen
projections at one donor sum to identity because they are the inverse
coordinates of the joint quotient isomorphism. No equality of the two
donor kernels has been assumed.

The independent checker forms the native adjacency by integer dot products,
removes exactly those donors whose singleton plane is visible, and solves
all 111 parity systems by ascending-column augmented elimination. This
differs from the author's column-span membership and dual-witness extraction.
There is an odd solution for exactly 87 receivers. The other 24 systems
are inconsistent. Every supplied odd donor set is checked directly, along
with every paired plane and the identity `2*paired=16*donors`. Thus no slack
source pair is smuggled into the tight projector argument.

## Operator inequality

If E and F project onto the same image, their ordered products are
`EF=F` and `FE=E`. In characteristic two their sum N satisfies `N^2=0`.
Its image lies in the common s-dimensional image. Summing all donor
coordinate identities over an odd parity witness gives `sum N=I` because
every visible plane meets that witness in zero or two donors.

For every term N, `I+N` has square I and is invertible. The other terms
must therefore have total rank at least b. This proves
`sum rank N >= b + max rank N` and, because each term has rank at most s,
at least seventeen nonzero terms. The hypotheses are not scalar and do
not require commuting coefficients. They survive every characteristic-two
extension. Different witness inequalities overlap; the proof correctly
does not add them as independent costs.

## Minimum-size classification

If there are exactly seventeen nonzero terms, deleting any one leaves
sixteen rank-at-most-s terms with invertible sum on dimension 16s. Each
of those ranks is s, and their images and row spaces are direct. Varying
the deleted term proves this for all seventeen terms.

Choose full-rank factorizations `N_h=U_h V_h`. The identity sum gives
`UV=I`. From `U_h V_h U_h V_h=0`, injectivity of `U_h` and surjectivity of
`V_h` imply `V_h U_h=0`, without a commutation assumption. Consequently
`P=VU` is a rank-16s idempotent with zero diagonal blocks. Its complementary
idempotent E has rank s and every diagonal block identity. In a full-rank
factorization `E=AB`, each square block relation `A_h B_h=I` makes both
factors invertible and forces `B_h=A_h^{-1}`.

Writing `D=diag(A_h)` gives `D^{-1}ED=J_17 tensor I_s`. Thus the transformed
U has exactly the diagonal block vectors as kernel. Its first sixteen
block columns form a basis, and its last is their sum. The equations
`VU=I+J` then determine the remaining factor uniquely in this basis,
yielding the displayed simplex family. Internal factor-basis changes
cancel in each N_h, leaving simultaneous conjugation on the original bank.
This proves the claimed classification, including noncommuting block maps.

The author's explicit `U_h,V_h` satisfy all diagonal-zero and identity-sum
relations because sixteen is even and seventeen is odd. Choosing a left
inverse W_h of U_h gives two genuine idempotents onto the same image whose
sum is N_h. Tensoring by I_s preserves these identities and the exact ranks.

## Independent controls and boundaries

The reviewer separately constructs the simplex, conjugates it by a sequence
of invertible elementary binary row maps, and then discards the original
factorization. It re-factors every N_h by independent column extraction,
forms the complementary projection, extracts its arbitrary factor bases,
and reconstructs the simultaneous conjugation to the exact standard family.
The recovery succeeds at s=1 and s=2, including a 32-dimensional bank and
seventeen independently recovered 2-dimensional factors. These computations
test the classification's order and basis conventions; its universal
validity comes from the preceding argument.

The result is an obstruction to common plane kernels and an exact abstract
target for a minimum-discrepancy realization. An actual native embedding
must still satisfy all donor coordinate decompositions, source timing,
cross-receiver compatibility and shared outgoing-port constraints. In
particular a separately constructed seventeen-term family is not itself a
completed native code. No new supplier, multiplication exponent, or
foundational discharge follows.

Reproduce with `check.py --layout ... --witnesses ... --proof ... --out ...`.
The result pins the reviewed proof and decompressed native witness data.
Credit @CubeJerry, the retained native and quotient-source authors, root's
operator argument, and S023 worker B's independent review with substantial
OpenAI assistance.
