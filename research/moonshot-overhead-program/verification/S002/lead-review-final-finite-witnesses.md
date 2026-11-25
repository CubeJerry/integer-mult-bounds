# S002 lead review: final finite witnesses

Review prepared 2026-11-25, following checkpoint
`848fbf1d7a5e192aa352d79b4d3e36fa06be21ee`.

## General-prime count formulas

The lead read A's `prime-characteristic-count-formulas.md`, C's independent
review, and the complete C verifier. The lead accepts PC1--PC8 as finite
formula results, with their stated parameter dependence and on-digit domain.
The identity

\[
 G_p(X,Y)=\sum_{a=1}^{p-1}\binom Xa\binom Y{p-a},\qquad
 H_p(X,Y)=1-(X+Y+1)^{p-1}
\]

gives carry `G_p + H_p c` on digit inputs. The predecessor carry occurs once;
all copies of operand subformulas remain charged. Signed Lucas reduction is
justified using units in the truncated power-series ring, including negative
offsets. No binomial denominator divisible by p is inverted in these digit
formulas.

The lead ran an isolated copy of C's checker in
`prime-count-lead-replay/`; SHA-256 of that script:
`993a224b2ff3d976b7d64226ffc9306099bf2f411bdb5499cbd19aa1625f56ee`.
It passed 5,034 digit/carry cases, 2,517 comparisons of propagation forms,
11,190 balanced-count assignments (including 329 negative offsets), 114
copied formula size/degree budgets, 1,535,617 signed Lucas cases, 1,530 binary
predictors (534 central matches), and 30 negative controls.

PC9's dependence on p is essential. A construction for each fixed prime does
not provide one dyadic integral identity valid uniformly in every odd
characteristic. PC10's growing-prime backup composition is not admitted as a
new complete multiplication theorem here. It is unnecessary for the stronger
accepted fixed-field theorem. No global all-odd-characteristic IP claim follows.

## Formal full-row four-bit witness

The lead read the complete `verify_four_bit_full_rate.py` and replayed an
isolated copy in `four-bit-full-rate-lead-replay/`; SHA-256:
`b811675325af1ed0ac44b3446c06effc2b487461794036b0d7f47ad43524ddb7`.

This checker performs exact sparse polynomial arithmetic over F2, without
Boolean reduction during matrix multiplication. For two two-bit partial sums,
it constructs the carry polynomial `a1*b1 + (a1+b1)*a0*b0` by the actual
cyclic formula compiler. It obtains four affine 8-by-8 factors. Every cyclic
product equals the same formal polynomial times the full identity matrix.
All 256 entries are checked to be affine; all four formal cyclic identities
pass. The 16 Boolean assignments match the fourth count bit. An off-cube F4
negative control distinguishes this nonmultilinear polynomial from the literal
elementary symmetric polynomial.

This is a concrete test of the count-formula/full-rate-compiler interface,
including every independent row. It does not replace the general induction,
prove a global physical implementation, or extend the scoped multilinear
lower bound to the new characteristic-two construction.

## Admission scope

Both finite checks pass and corroborate the corresponding written identities.
Neither changes the current strongest complete overhead envelope. The global
fixed-field construction remains supported by its separate finite, physical,
space, precision, and scheduler reviews. No full multiplier execution, formal
refinement proof, human refereeing, or exhaustive novelty audit was performed.

## Optional power-of-two and structured-shift interfaces

The lead read A's power-two-degree predictor, B's independent review, B's
structured-shift-check refinement and A's independent review in full. The
finite interfaces are accepted at their stated scope. The complete range
0<=h<2^t factors formally into the product of its selected-bit terms. Every
sum gate can be given a power-of-two length, so Frobenius supplies the cyclic
sum without additional roots; the final odd total length is obtained by
concatenation. Bounded irreducible enumeration gives the stated repair field.

For the shift-only construction, actual exceptional sets are entire shift
blocks. Consequently H0 tensor I and its left/right inverses act on all
independent module rows. Pairwise ternary shifts give count variance 2m/3,
and the 5ceil(sqrt m) window gives the stated sub-1/32 defect bound. The
explicit check-row padding restores exactly R/16 inputs in each of the four
paid phases. Only B check nodes are needed; the scalar field degree is
O(log m). The lead checked these identities and rounding inequalities, but
did not independently rerun A's additional finite shift checker.

These refinements retain potentially exponential module width. No succinct
physical tensor executor has been proved here, and the larger window cannot
silently inherit Q's old numerical constant. They do not change the admitted
global theorem, its constants, or its finite-constructor premises.
