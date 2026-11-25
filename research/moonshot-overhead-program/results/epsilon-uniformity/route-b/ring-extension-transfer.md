# A bounded-ring interface for ordered affine factorizations

Status: **derived mathematical lemmas; not independently reviewed**.
This optional lead is not used in the admitted formula theorem or S002's
new fixed-field result. No additional multiplication improvement is claimed.

## What the literature lead does and does not supply here

Primary source inspected: Pavel Hrubes and Amir Yehudayoff, *Arithmetic
Complexity in Ring Extensions*, Theory of Computing 7 (2011), 119--129,
Theorem 3.2 and its proof, pp. 122--123:
<https://theoryofcomputing.org/articles/v007a008/v007a008.pdf>,
DOI <https://doi.org/10.4086/toc.2011.v007a008>.

The theorem gives a short formula over a suitable noncommutative extension.
Its displayed proof imposes the coefficients of a product of affine forms
as relations in a free associative algebra. A nearby finite-dimension
remark does not by itself provide the explicit dyadic basis, multiplication
table, coefficient heights and generator needed by this programme.
The following elementary observations isolate that missing interface.

## 1. An explicit finite-free algebra would suffice

Let `B=Z[1/2]`, and let `A` be a unital finite-free central `B`-algebra of
rank `r`, with a specified basis and dyadic multiplication table. Suppose
affine forms `a_1(X),...,a_D(X)` in central variables satisfy

\[
 a_1(X)\cdots a_D(X)=P(X)1_A,
 \qquad 0\ne P\in B[X].
\]

Regular left multiplication produces affine matrices `M_i(X)` over `B`
with product `P I_r`. Over the fraction field of the integral domain
`B[X]`, every `M_i` is invertible: their determinant product is `P^r`.
Conjugating the scalar product by the first factor therefore shows that
every cyclic rotation is also `P I_r`. These are polynomial identities
over `B`, because `B[X]` injects into its fraction field.

Pad the list by identities to the next power of two `b>=max(2,D)`.
The cyclic block matrix has dimension `br`, is affine, and satisfies
`L(X)^b=P(X)I_(br)` on **every** coordinate. No initial workspace state
is imposed. The identities descend modulo every odd prime; they need
not be re-proved by division after that specialization.

Given the basis table and affine coefficients explicitly, all regular
matrices and the block matrix have polynomial construction cost in their
rank, table length, coefficient bit lengths and dyadic denominator
exponents. Hence an `exp(poly(m))` complete table/factor generator of this
type would give the corresponding bounded full-rate matrix-root interface.
This is a sufficient interface, not a construction of such a table.

## 2. The displayed universal quotient need not itself be finite

Already for `P(x)=x^2`, the displayed two-factor construction produces
the algebra with generators `a,b` and relation `ab=1`. Its powers of `b`
are linearly independent: let `b` shift basis vectors `e_i` to `e_(i+1)`
on a countably generated free module, and let `a e_0=0`,
`a e_(i+1)=e_i`. Then `ab=1`, while applying any alleged relation among
the powers of `b` to `e_0` proves every coefficient zero.

A finite quotient exists in this example, by taking `a=b=1`. The point
is only that the displayed universal quotient is not automatically the
bounded finite-free representation required in Section 1. Selecting such
a quotient for the actual predictor and billing its construction remains
a separate obligation in this route.

## 3. A quadratic dimension sanity check

Let `F` be a field of characteristic different from two, and `A` a
finite-dimensional central `F`-algebra. Suppose

\[
 \left(\sum_{i=1}^n a_i x_i\right)
 \left(\sum_{i=1}^n b_i x_i\right)
 =\left(\sum_{i=1}^n x_i^2\right)1_A.
\]

Coefficient comparison gives `a_i b_i=1`. In a finite-dimensional algebra
a right inverse is two-sided, as is seen from the left multiplication
matrices. Put `a=a_1` and `c_i=a^(-1)a_i`, for `i>=2`. The mixed
coefficients give `b_i=-c_i a^(-1)`, and hence

\[
 c_i^2=-1,\qquad c_i c_j=-c_j c_i\quad(i\ne j).
\]

Take `q=2 floor((n-1)/2)` of these generators. For every subset `S` of
them, the ordered product `c_S` is invertible. Conjugation by `c_i`
acts on it by sign `(-1)^(|S|-1_(i in S))`. These `q` conjugations
commute and are involutions. Because `q` is even, the `2^q` resulting
sign characters are distinct: equality of characters forces the symmetric
difference to be either empty or the full set, and the latter cannot
satisfy its required odd parity. Distinct simultaneous sign characters
give linearly independent vectors, by the projectors obtained from
`(1/2)(I plus-or-minus conjugation)`.

Therefore

\[
 \dim_F A\ge2^{2\lfloor(n-1)/2\rfloor}.
\]

This excludes a uniform polynomial-in-`n` dimension estimate for this
**exact two-affine-factor identity**. It does not lower-bound general
short formulas, disprove the ring-extension theorem, or exclude the much
larger `exp(poly(m))` resource target. It explains why a finite-dimension
remark cannot be substituted for a concrete representation invoice.

These proofs are written analytical observations without finite tests or
external independent review. The admitted main construction remains the
separately audited cyclic formula theorem. Credits: the cited ring-extension
paper and matrix-factorization literature; @CubeJerry; GPT-6 Astra Pro
assistance.
