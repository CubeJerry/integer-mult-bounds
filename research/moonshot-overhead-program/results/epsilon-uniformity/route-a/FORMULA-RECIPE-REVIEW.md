# Independent review of the unreduced formula rank obstruction

Status: **review passed**, 2026-11-25. Reviewed file:
[`../route-c/FORMULA-RECIPE-LOWER-BOUND.md`](../route-c/FORMULA-RECIPE-LOWER-BOUND.md).

I checked the published input directly in Hrubes--Yehudayoff,
*Homogeneous formulas and symmetric polynomials*, Theorem 1(i), page 3,
[primary author manuscript](https://users.math.cas.cz/~hrubes/PDFs/SymPoly.pdf).
For `m>=2D`, their lower bound is `m D^{Omega(log D)}` leaves. Their
definition counts scalar and variable leaves and permits arbitrary field
constants. Their multilinearity condition includes the syntactically
multilinear formulas used by the reduction.

The reduction correctly distinguishes degree-one additions, which cost
no factor in the literal rank recurrence, from additions of degree at
least two. After scalar simplification and contraction of maximal linear
subtrees, deleting the `s` latter additions leaves at most `2s+1`
product components. Each component has at most `D` positive-degree
boundary inputs, so expanding the actual linear leaves costs at most
`O(mD(s+1))` leaves. The argument permits arbitrary coefficients for
these linear leaves; it does not charge them to obtain the lower bound.

Taking the top component of a syntactic-degree-`D` formula creates no
addition and preserves disjoint variable supports at products. The
source predictor's top component is indeed `(-1)^u e_D(X)`: the
coefficient `(-1)^u(-2)^D` in indicator variables cancels the top-part
factor `(-1/2)^D` from `b_i=(1-X_i)/2`. Zero components may be deleted.

Combining the formula lower bound with the compression lemma gives
`s>=D^{c' log D}` for a positive absolute `c'` and sufficiently large
`D`. The exact unreduced compilation has
`K=product_v d_v>=2^s`, hence
`K>=2^{2^{Omega(log^2 D)}}`. For the source central window,
`D=Theta(sqrt(m log m))`, the stated matching scale follows.

This conclusion depends on formal equality, syntactic degree `D`,
multilinear intermediates, and the specified unreduced rank recurrence.
It correctly leaves nonmultilinear cancellation, Boolean quotient
reductions, invariant summands, different addition constructions and
arbitrary matrix-root representations open. It is not an optimality
claim for the complete multiplication envelope. No finite example is
used as evidence for the asymptotic lower bound.

This is independent written mathematical review with GPT-6 Astra Pro
assistance, not formal verification or external peer review.
