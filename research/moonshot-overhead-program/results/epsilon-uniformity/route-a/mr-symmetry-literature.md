# Symmetry and module decompositions: a scoped MR literature audit

Status: **documented partial and negative applicability results**,
2026-11-25. No theorem located in this focused search establishes the
stronger MR hypothesis in `single-exponential-root-hypothesis.md`.
This is a search record and several explicit interface checks, not a
claim that no such theorem exists.

## 1. The exact missing representation

For the source integral count predictor `P_m`, with
`D=Theta(sqrt(m log m))` and final power-of-two length `b<2max(2,D)`,
MR requests an affine pencil satisfying

\[
 L(X)^b=P_m(X)I
\]

on every input coordinate, over a uniformly generated finite free
dyadic coefficient algebra. The matrix dimension, algebra rank,
coefficient numerator and denominator bit heights, actual output size,
and generation time must all be bounded by `exp(m^C)` for one constant
`C`. The identity may be formal or valid modulo `X_i^2=1`, provided the
specialization and all-shift repair are proved.

The accepted balanced-formula method gives
`exp(exp(O(log^2 m)))`, a larger sufficient scale. A small determinant,
one designated scalar output, or a representation requiring initially
zero auxiliary coordinates does not supply the full-input identity.
The following checks use that exact distinction.

## 2. A concrete tensor-decomposition lead

Sheng--Tribone, *Tensor products of d-fold matrix factorizations*,
Theorem 4.4, assumes `Q` is a `Z[omega,1/d]`-algebra, where `omega` is
a primitive `2d`-th root. If both factor lists equal their cyclic
shifts, their tensor product decomposes into the `d` shifts of a
smaller list. Corollary 4.5 substitutes shift-isomorphism under complete
regular-local and residue-field hypotheses. The explicit smaller list
appears in the theorem's proof. [Primary publisher text, Section 4](https://www.cambridge.org/core/journals/nagoya-mathematical-journal/article/tensor-products-of-dfold-matrix-factorizations/526C84981550C9E71BECB481DC4F9B18),
DOI [10.1017/nmj.2025.12](https://doi.org/10.1017/nmj.2025.12).

Here is the relevant algebra directly. Suppose affine pencils `A,B`
commute and satisfy `A^d=fI`, `B^d=gI`. Over the integral cyclotomic
ring, the list

\[
 C_k=A-\omega^{2k+1}B,\qquad 0\le k<d
\]

has every cyclic product equal to `(f+g)I`. Indeed its factors commute,
and the polynomial identity
`product_k(T-omega^(2k+1)U)=T^d+U^d` may be evaluated at `A,B`.
This construction of the smaller list itself divides by no integer.
It is therefore useful to distinguish an explicit new factorization
from the stronger assertion that a given graded tensor module splits
over the coefficient ring; the latter is what the published
direct-sum theorem proves with `1/d` available.

For repeated pencils on separate tensor factors, put
`A=A_f tensor I`, `B=I tensor A_g`. If their dimensions are `a,b`,
this list has grade rank `ab`; the unreduced graded tensor list has
rank `dab`. At `d=2`, it is the familiar pair `A-iB,A+iB`.

### 2.1 The source formula does not preserve the needed property

The formula compiler's product rule concatenates factors. Already the
rank-one factorization `(x,y)` of `xy` is not isomorphic to its cyclic
shift `(y,x)` over the polynomial ring `R[x,y]`, for any integral-domain
coefficient ring `R`. A rank-one isomorphism would give units `u,v`
with `ux=yv`, forcing `x` and `y` to be associates. They are not.
The same argument applies to two nonassociate linear forms on disjoint
variable sets, which occur at products of linear leaves in the
balanced elementary-symmetric formula.

Thus the hypothesis is not an invariant of the current recursive
construction. Symmetry of the output polynomial under variable
permutations does not establish cyclic shift-isomorphism of its
factor list. Nor does it supply a constant, integral change of basis
which would retain affine entries and controlled bit heights.

There is a generic way to impose repeated factors, but its present
cost does not improve the recipe. A length-`d`, grade-rank-`a` cyclic
list becomes one repeated affine root of dimension `da` by block
cyclic assembly. Doing this for both children, followed by the smaller
list above, gives grade rank `d^2 ab`. The unreduced graded sum of the
original lists has rank `dab`. This shows that blindly converting
both children before invoking the decomposition does not save rows.
It does not exclude a specially maintained shift symmetry or a
different common invariant summand.

For a useful global improvement one would need an explicit recursive
class with small shift-compatible representatives, or an efficient
integral summand extraction whose ranks improve after all conversions.
The extracted basis must stay independent of the query variables to
preserve affine pencils, or else a separate affine-degree argument is
needed. Its basis, inverse maps, coefficient heights and actual
generation must satisfy MR's bounds. These are concrete missing
conditions, not a claimed module-theoretic obstruction.

The paper's later decomposition results use polynomials in disjoint
variable sets. The elementary-symmetric convolution terms at a sum
generally reuse the same variable blocks; disjointness of factors
inside each product does not establish that hypothesis for the sum.

The publisher's 2026 corrigendum adds a funding acknowledgement and
does not change the algebraic results. [Corrigendum](https://www.cambridge.org/core/journals/nagoya-mathematical-journal/article/tensor-products-of-dfold-matrix-factorizations-corrigendum/DE782E305264F1CF99F6F8250515281C).

## 3. Other close results and their exact interface gaps

| Primary result inspected | What it supplies | Why it does not presently establish MR |
|---|---|---|
| Branden, *Hyperbolicity cones of elementary symmetric polynomials are spectrahedral*, Theorem 1.2 and equation (1.2), [arXiv:1204.2997](https://arxiv.org/pdf/1204.2997). | A spectrahedral representation of the elementary-symmetric hyperbolicity cone, with an auxiliary polynomial multiplying the defining polynomial in the determinantal formulation. | A cone description and an auxiliary determinantal factor do not give a bounded-length affine cyclic product equal to the exact predictor times an identity. |
| Saunderson--Parrilo, *Polynomial-sized Semidefinite Representations of Derivative Relaxations of Spectrahedral Cones*, [arXiv:1208.1443](https://arxiv.org/pdf/1208.1443). | Polynomial-size semidefinite representations of derivative-relaxation cones, using slices and projections. | A projection of a cone is not a full-coordinate polynomial identity. No conversion with the needed degree, coefficients and generation bounds is supplied by that theorem. |
| Cheng--Huang--Yang, *Generalized Clifford Algebras as Algebras in Suitable Symmetric Linear Gr-Categories*, Section 3, [arXiv:1510.04408](https://arxiv.org/pdf/1510.04408), DOI [10.3842/SIGMA.2016.004](https://doi.org/10.3842/SIGMA.2016.004). | A twisted-group-algebra presentation of the algebra with `e_i^d=q_i` and `e_i e_j=omega e_j e_i`, of dimension `d^m`. | This is a diagonal-form Clifford algebra. Its displayed relations do not identify the algebra for the mixed elementary-symmetric predictor. The name alone cannot justify the desired `d^O(m)` row bound. |
| Chapman--Kuo, *On generalized Clifford algebra of a monic polynomial*, Section 5, [arXiv:1406.1981](https://arxiv.org/pdf/1406.1981), DOI [10.1016/j.laa.2014.12.030](https://doi.org/10.1016/j.laa.2014.12.030). | A correspondence with Ulrich bundles and existence results under the section's algebraically closed characteristic-zero and geometric assumptions. | These statements do not give the uniform rank, coefficient heights, integral model and actual bit generator required here. The predictor's geometric hypotheses would also need checking. |
| Faber--Ingalls--May--Talarico, *Matrix factorizations of the discriminant of S_n*, [primary institutional copy](https://eprints.whiterose.ac.uk/id/eprint/209753/1/Matrix%20factorizations%20of%20the%20discriminant%20of%20Sn.pdf), DOI [10.1016/j.jsc.2024.102310](https://doi.org/10.1016/j.jsc.2024.102310). | Discriminant matrix factorizations built from representation-theoretic decompositions, assuming the characteristic does not divide `n!`. | The polynomial differs from `P_m`, and the stated characteristic condition fails when `n=m` in our regime `p<=m`. An integral alternative would require its own proof; this does not rule one out. |

For the diagonal Clifford example, the limitation can be seen without
any representation classification. The root-of-unity binomial identity
applied to its defining relations gives

\[
 (X_1e_1+\cdots+X_me_m)^d
   =(q_1X_1^d+\cdots+q_mX_m^d)I.
\]

The mixed squarefree coefficients of the desired predictor are absent.
Replacing the list of variables by all its product terms returns to
the large expansion already avoided by the formula construction.
This calculation is an applicability check, not a lower bound for
other Clifford quotients or symmetric representations.

## 4. A sharply stated formula route and its restriction

A uniformly generated, polynomial-size dyadic formula for `P_m` with
syntactic degree at most `D` would imply MR through the accepted cyclic
composition. There would be `m^O(1)` nodes, grade rank at most
`D^(m^O(1))`, cyclotomic order at most `D!`, and affine coefficient
generation of `exp(poly(m))` cost. The one final cyclic assembly and
regular representation preserve that scale. Coefficient bit heights
and denominator exponents must be polynomially bounded at the formula
leaves; otherwise formula size alone is insufficient.

That sufficient route cannot use only smaller **multilinear** formulas
of the same syntactic degree. The precise matching lower bound for
the unreduced recipe is proved in
[`../route-c/FORMULA-RECIPE-LOWER-BOUND.md`](../route-c/FORMULA-RECIPE-LOWER-BOUND.md)
and independently checked in
[`FORMULA-RECIPE-REVIEW.md`](FORMULA-RECIPE-REVIEW.md), using
Hrubes--Yehudayoff's Theorem 1(i). The restriction does not cover
nonmultilinear cancellation, Boolean-quotient identities or smaller
invariant summands.

An interpolation formula of polynomial size can have intermediate
syntactic degree `m` even when its output has degree `D`. Compiling
that expression verbatim produces roughly `m` factors, which changes
the normalized stage cost. Extracting its degree-`D` component is the
nontrivial step; it cannot be treated as an uncharged simplification.
Route B separately audits the Hrubes--Yehudayoff ring-extension and
interpolation results, including their denominator and degree issues.

## 5. Recorded research targets

The focused search leaves three concrete representation questions:

1. Construct a smaller integral module for the **mixed** count
   predictor, with affine generators and a finite free basis whose
   structure constants are generated within `exp(poly(m))` work.
2. Preserve cyclic shift compatibility through symmetric convolution,
   or select useful invariant summands without variable-dependent
   denominators, degree growth or unbounded basis-search costs.
3. Produce a polynomial-size, degree-`D` formula using controlled
   nonmultilinear cancellation or Boolean quotient relations, together
   with the required coefficient and exact identity certificates.

Any successful construction must be applied to both interchange and
the Fourier branch before invoking the conditional global transfer.
All independent input coordinates, shifts, repair patterns, numerical
heights and the common visited-cell cap remain part of that transfer.
None of these targets is claimed solved by this note.

Credits: the cited authors, @CubeJerry, the pinned OpenAI source
constructions, and the concurrent S002 programme. Developed with
GPT-6 Astra Pro assistance. This is not a literature-priority claim.
