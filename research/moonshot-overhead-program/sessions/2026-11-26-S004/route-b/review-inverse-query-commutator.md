# Independent B review of the inverse-query commutator theorem

Review status: **passes in the stated algebraic model**.
Reviewed draft: `route-c-work/inverse-query-commutator.md`, read in full
during the 2026-11-26 S004 session. This is an independent mathematical
review, not a formal-kernel proof, full tape execution, or human refereeing.

## Boundary and inverse identities

An affine term `x_j^a` changes support weight by at most one even for
`a>1`: a coordinate either enters support, leaves support, or stays in it.
Therefore every nonzero matrix entry of the cut commutator has its source
and destination in levels `k` and `k+1`. Arbitrary coefficient matrices
can mix rows but do not enlarge that supported monomial subspace. Its
dimension is exactly `h(n_k+n_(k+1))`, proving (C1).

The inverse identity is valid without assuming the row coefficient
matrices commute. The finite group algebra splits under the field
hypotheses, so pointwise invertibility is equivalent to invertibility on
the entire monomial module. Multiplication on the two sides by an inverse
preserves rank, proving the equality in (C2). If singularities are allowed,
this equality must not be used; Section 4 prices them separately.

## Full network invoice

The rectangular commutator convention correctly accounts for copies,
initialization, deletion, and changing row counts. Every query-independent
row map commutes with the corresponding cut projections. Rank is
subadditive under the telescoping composition formula, including when
intermediate dimensions vary.

The spectral-table departure has global rank equal to the sum of its
pointwise ranks, because evaluation is an isomorphism. The factor two in
its commutator bound is necessary in general and is retained. Repeated
uses are charged separately. The final error has the same factor-two
bound. The commutator of multiplication by `chi` is a permutation matrix
with precisely `W J_k` nonzero independent columns, including in
characteristic two. These facts prove (C3) with the stated normalization.

This proof gives a lower bound on **active query-row volume**, not just
depth. It continues to hold if an affine inverse is granted as a primitive
without a physical cost model. It does not license that primitive as cheap
on a tape machine.

## Binary and order-three constants

For odd binary `m`, complementation swaps both sides of the central cut,
so `J=2^m`. For even `m`, exactly the central layer stays on the same side.
The boundary mass is `sqrt(8/(pi m))(1+o(1))`, giving the coefficient
`sqrt(pi/8)(1-2 eta)` in (C7).

For the ternary cut, membership means `n_0>=ceil(m/3)` and its translate
means `n_2>=ceil(m/3)`. If `m` is not divisible by three, the three
threshold indicators cannot all be zero or all be one. If `3|m`, the
only all-one case is the completely balanced count tuple; an all-zero
case is still impossible. Exactly two of the three unordered indicator
pairs differ in every remaining case. Exchangeability yields (C8)
exactly. The balanced probability is `O(1/m)` by Stirling, and the two
central masses of `Bin(m,2/3)` sum to
`3/(sqrt(pi m))(1+o(1))`. The displayed constant in (C9) follows.

## Rational matrix fraction

For degree cut `v=floor((m-a-b-1)/2)`, `Bz` has degree at most `v+b`,
so `chi Bz` has no monomials below `m-v-b`. The output `Az` has degree
at most `v+a`, strictly smaller. Hence a vector in the low-degree
kernel of `chi B-A` must also lie in the kernel of `B`.

When `B` is invertible this proves injection and (C10). For
`P=A B^-1`, `(chi I-P) B=chi B-A`; for `P=B^-1 A`,
`B(chi I-P)=chi B-A`. No commutation of `A` and `B` is needed.
For singular denominators, subtracting the entire global nullity of `B`
is a safe bound on the low-degree kernel, and multiplication by `B`
cannot increase the rank of the error. This proves (C11).

A simple negative control explains why the denominator degree is charged:
on the binary two-variable cube, `A=x_1`, `B=x_2` gives
`A/B=x_1x_2` exactly. The numerator has degree one, while the combined
degree is two. Applying the polynomial theorem to the numerator degree
alone would give a false positive lower bound on its exact rank error.

## Scope and relation to B's result

The polynomial-output rank tail is stronger when a small uniform output
degree is known, especially for polynomially rare repair. The commutator
theorem covers a different regime: arbitrary inverse affine gates and
nonuniform active widths, without a low-degree output assumption. It gives
a square-root necessary volume and leaves the endpoint feasible.

No mathematical blocker was found. The proof does not establish that every
physical routing or nonlinear gate is captured by this spectral network.
Any end-to-end use must first prove that representation bridge. Finite
verification remains the separate Route C checker; this review does not
claim to have run it before its completion. The later E003 weighted
two-point transfer is not silently included in this review; its proof will
be audited separately once appended.

Review produced for @CubeJerry with substantial ChatGPT assistance.

## Additional audit: E003 weighted two-point transfer

The appended transfer and rational extension were read on 2026-11-25 at
22:49 UTC and **pass**. E003's original M1--M4 proof was also read in full.

For `c=b-a`, `z=x-b/c`, and `d=-ab/c`, direct evaluation at `x=0,1`
gives `f z=d`, `f=(a+b)+c z`, and `f^-1=z/d`. All denominators are
nonzero under the explicitly stated hypotheses, including for the two
nontrivial elements of `F4`. The signs agree with E003's weights.

For a monomial of phi-degree at least `m-k`, multiplication by `f` removes
every present `z` factor and can introduce factors only on its complement.
The resulting degree is at most `k`, so `fH` is contained in `L`.
Invertibility and equal dimensions give equality. This proves that the
two off-diagonal blocks of the target commutator both have rank `dim L`:
one is onto, and the other is injective because `L` and `H=f^-1 L`
intersect trivially. Their source and destination summands are disjoint,
so their ranks add. The exact binary target rank follows in every allowed
characteristic.

A local function has an affine representation in `(1,z)`. Its multiplication
changes phi-degree by at most one, because `z^2` reduces to a constant plus
a multiple of `z`. Therefore the same query-boundary rank applies, and
inverse gates retain it by the already audited commutator identity.
Uniformly choosing local pairs and then endpoints produces the uniform
full-spectrum measure, so the averaged table/error charges are unchanged.

For the rational extension, multiplication by `f^-1` sends a phi-monomial
of degree at most `v+a` to a combination with degree at least `m-v-a`:
every absent local coordinate becomes a mandatory `z` factor. This is
disjoint from the degree range of `Bz`, proving the same injection modulo
the denominator kernel. The argument works for both `AB^-1` and
`B^-1A` without assuming matrix commutation.

For a larger local alphabet, the numerator and denominator degree bounds
must hold on every two-point restriction (for example, via their charged
affine-query constructions or support degree). They must not be assigned
from an unrelated syntactic expression that hides unrestricted local
functions. With this standard interface reading, no blocker was found.
The stronger F4 constants are correctly credited to the combination with
E003's basis rather than to an unrecorded independent discovery.
