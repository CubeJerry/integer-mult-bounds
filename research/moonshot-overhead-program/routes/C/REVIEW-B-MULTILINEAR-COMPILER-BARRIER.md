# Independent review of the multilinear compiler barrier

Route C, S002, 2026-11-25. Read the complete current
`../B/multilinear-formula-width-barrier.md` and independently opened the
primary author copy of Pavel Hrubes and Amir Yehudayoff, *Homogeneous
formulas and symmetric polynomials*:
<https://users.math.cas.cz/~hrubes/PDFs/SymPoly.pdf>.

**Gate: PASS, strictly within the stated characteristic-zero, formal
multilinear, degree-controlled and uncompressed canonical-compiler class.**
This is compatible with the new positive count-bit formula. It does not
bound arbitrary matrix representations, arbitrary predictors or formulas
valid only in the order-three spectral quotient.

## 1. Primary theorem and model match

The primary paper defines a multilinear formula by requiring every gate's
polynomial to be multilinear, and defines homogeneous formulas similarly.
Its size is its number of leaves. Theorem 1(i), on page 3 of the author
copy, states that a homogeneous multilinear formula for e_D on m>=2D
variables has at least `m D^(Omega(log D))` leaves. Thus B uses the correct
model and parameter range. The characteristic-zero restriction is safe;
no stronger unrestricted formula lower bound is being imported.

## 2. Top-component pruning

The literal source binary predictor has top homogeneous component

    gamma e_D((-1)^beta_1 q_1,...,(-1)^beta_m q_m),
    gamma=(-1)^(u-sum beta_j).

Indeed its highest indicator term is `gamma (-2)^D e_D(I)`, and the
degree-D term after `I_j=(1-(-1)^beta_j q_j)/2` cancels the factor
`(-2)^D`. Its actual degree is D.

If the root syntactic degree is at most D, it must therefore equal D.
At a product, taking the component of its syntactic degree takes the
corresponding top component of both children. At a sum, children with
smaller syntactic degree contribute nothing to that component. This is
a pruning operation with no duplication or new addition gate. A child
whose actual degree is smaller may give zero, which is simply removed.
Because every original gate polynomial is multilinear, each retained
homogeneous component is multilinear too. After scalar and zero folding,
the result is a homogeneous multilinear formula for e_D up to invertible
variable signs and scalar.

## 3. The number of width-charging sums

After maximal degree-one subformulas are folded into linear leaves and
scalar gates are absorbed, every remaining sum has degree at least two.
Let A be their number and L the number of linear leaves. For a homogeneous
subformula of positive degree d, induction gives `L<=d(A+1)`.

At a product with degrees d1,d2, the two bounds add to at most
`(d1+d2)(A1+A2+1)`. At a sum both children have degree d, so the sum is
at most `d(A1+A2+2)=d(A+1)`. Linear leaves are the base case. Scalar
leaves would invalidate this direct count if retained, which is why the
explicit folding step is necessary and sufficient.

Each linear leaf expands into at most `2m+1` standard variable/scalar
leaves. Applying the published lower bound gives

    (2m+1) D(A+1) >= m D^(Omega(log D)),
    A >= D^(Omega(log D))

after adjusting the absolute exponent for large D. Every one of these
remaining sums came from an original sum of syntactic degree at least
two. In the stated canonical compiler its graded-sum rule multiplies
width by that degree, while product nodes multiply child widths. Hence

    log2(row width) >= A >= D^(Omega(log D)).

At `D=Theta(sqrt(m log m))`, this is
`log2(row width)>=2^(Omega((log m)^2))`. It is an actual limitation of
that specified compilation tree; it is not a lower bound after arbitrary
module compression or a change of polynomial representative.

## 4. Explicit reason the new count formula is outside the class

Take four Boolean input bits x1,x2,x3,x4 and sum adjacent pairs in
characteristic two. Put

    a0=x1+x2, a1=x1*x2,
    b0=x3+x4, b1=x3*x4.

The degree-four carry expression for bit two is

    a1*b1+(a1+b1)*a0*b0.

It contains formal monomials such as `x1^2*x2*x3`, so its intermediate
polynomials are not multilinear. On Boolean inputs, `a1*a0=b1*b0=0`,
and the expression reduces to the correct fourth elementary symmetric
function. Thus its small formula is a different formal polynomial with
the required quotient values and the same syntactic degree bound.

The new characteristic-two predictor uses exactly this permitted
nonmultilinear mechanism. The cyclic factorization theorem applies to
the supplied formula formally, and its operator is then evaluated on the
actual Boolean spectral indicators. The barrier's gatewise multilinearity
and literal-polynomial hypotheses both fail. No inconsistency or remaining
obstruction to the accepted fixed-field positive result follows.

No finite numerical test can establish the imported asymptotic lower
bound. This review checked its primary statement, the exact model match
and the new pruning/count derivation directly. Credits remain with the
cited lower-bound authors, the source predictor, and B for the scoped
compiler consequence; no broader lower-bound novelty is claimed.
