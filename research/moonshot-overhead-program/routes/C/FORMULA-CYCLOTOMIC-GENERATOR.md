# Formula evaluation in the original localized cyclotomic template

Status: **accepted finite algebra and generation profile after independent lead
review**. This applies the formula factorization to the original
binary predictor over Z[1/2], including its odd-characteristic tape use.
It supplies a smaller finite-data profile, not a stand-alone tape theorem.

The sum operation is established mathematics: Sheng and Tribone,
*Tensor products of d-fold matrix factorizations*, Nagoya Math. J. 261
(2026), e2, DOI [10.1017/nmj.2025.12](https://doi.org/10.1017/nmj.2025.12),
Definition 3.1 and Proposition 3.2, state it over a commutative algebra
receiving Z[zeta_d]. Their introduction credits several predecessors,
including the generalized Clifford constructions cited in the source.
I independently read the ring hypothesis, definition and proof in the
publisher's full text. The 2026 corrigendum concerns funding attribution.
No novelty claim is made for the tensor sum construction. The contribution
here is its explicit formula-size, specialization and finite-generator
application to this programme.

## 1. Cyclic factors specialize without a primitive root in the residue field

Let A=Z[1/2,eta], where eta is a complex primitive N-th root and every
positive factor length used by the formula divides N. Suppose f,g have
cyclic affine factorizations of common length d and respective widths r,s.
As in Route B's note, put their matrices on cyclic grades and set

    X=L_f tensor I,   Y=Z_f tensor L_g,
    Z_f|grade i=xi^i I,   xi=eta^(N/d).

Then YX=xi XY and `X^d=fI`, `Y^d=gI`. The mixed Gaussian-binomial
coefficients in `(X+Y)^d` are integer polynomials divisible by Phi_d:
over a complex primitive d-th root the product expression has a zero
numerator and nonzero denominators for every interior coefficient.
Consequently

    (X+Y)^d=(f+g)I                                     (FC1)

is an identity over A. Restricting to successive total grades gives
d affine factors of width d*r*s, with every rotation equal to (f+g)I.

After base change to any commutative Z[1/2]-algebra, (FC1) remains exact.
In particular it remains exact in odd characteristic p even when p divides
d. The image of xi need not retain primitive multiplicative order; the
integral polynomial identity is what specializes. No inversion of d or
of an odd prime is used.

Multiplication concatenates the two factor lists after tensoring with
identities. Factors in different tensor coordinates commute, so every
rotation still gives the scalar product on the whole row module. Constants
are folded at degree zero or absorbed into one factor of a positive-length
list. A constant a can be padded as `(a,I,...,I)`, including a=0.
These conventions avoid an extra stage for a scalar coefficient.

Thus a formula of syntactic degree at most D and S addition gates gives
D affine factors of common width at most D^S. This is a full-rate identity,
not one entry of a branching program. Identity padding handles unequal
degrees, and no cancellation or invertibility assumption is needed.

I independently checked Route B's characteristic-two version as well:
using the odd part c of d gives the c-th-power identity, the resulting
powers commute, and Frobenius supplies the remaining power of two. The
localized integral version is preferable for reusing the already audited
original-source physical compiler.

## 2. A syntactic-degree-D binary predictor formula

For each shift beta the source binary indicator is affine,
`I_j=(1-(-1)^beta_j q_j)/2`. The integral predictor can be collected as

    P_beta=sum_(k=0)^D a_k e_k(I_1,...,I_m),
    a_k=(-1)^(u-|beta|) sum_(h=k)^D (-2)^h binom(-u,h-k).

All a_k are integers, with bit lengths polynomial in m when D<=m and
|u|<=m. This is the integral multivariate representation, not a polynomial
in the count reduced modulo p.

Pad the m indicators with zeros to a power of two. For a balanced block,
compute its k-th elementary coefficient by the explicit convolution

    e_k(block)=sum_(a=0)^k e_a(left)e_(k-a)(right).

Subexpressions are copied: this is genuinely a formula. Every coefficient
has syntactic degree at most k, and the final weighted sum at most D.
A coefficient formula at one level has at most D+1 products and D sums.
A loose bound for the total number of formula nodes is

    S_m <= [8(D+1)]^(ceil(log2 m)+3).                     (FC2)

For the original rare-tail D=O(sqrt(m log m)), and also for the constant
tail D=O(sqrt m), this is `2^(O((log(m+2))^2))`. Put r for the resulting
cyclic row width. Then

    log2 r <= S_m log2 D = 2^(O((log(m+2))^2)).           (FC3)

The formula shape and degree budgets can be fixed independently of beta.
Zero scalar values after specialization do not change those budgets.
Thus every shift uses the same width. The all-shift batch has
`B=2^m r` rows before scalar descent; harmless fixed duplication is allowed.
Its logarithm has the same bound as (FC3).

## 3. One finite free extension, selected without circularity

First compute the finite width B from the formula shape. Let tau be the
least power of two at least max(2,B), and choose

    N=lcm(1,2,...,D,tau).

Then `N<=tau D!<=2 max(2,B) D^D`. Adjoin a primitive N-th root eta.
The ring A=Z[1/2,eta] is finite free of rank phi(N), with its usual
power basis. It contains every sum-gate root and the tau-th root
`zeta=eta^(N/tau)` used for B distinct check nodes.

For a quotient rho of two different check nodes, its order is a power of
two. The exact product of `1-rho^v` over the odd residue classes is 2.
Each node difference is therefore a unit in A and in every allowed odd-
characteristic base change, regardless of nonreduced factors elsewhere
in the algebra. This is precisely the source Hermite hypothesis.

The extension is selected from the pre-descent width B. After descent,
the row count is multiplied by phi(N); no second larger set of nodes is
needed. The check map has become a fixed block matrix in basis coordinates.
This avoids a circular extension-size requirement.

## 4. Coefficient heights and an actual cyclotomic constructor

The degree of Phi_N is at most N. Its roots have complex modulus one,
so its coefficient l1 norm is at most 2^N. Multiplication by eta in
the power basis has l1 operator norm at most 2^N. Since eta^N=1,
first reduce an exponent modulo N; every power eta^a then has basis
coefficient bit lengths O(N^2). This bound is deliberately coarse.

The cyclic formula constructor never multiplies two affine coefficient
matrices while assembling a new factor. A product gate tensors existing
factors with identities and concatenates them. A sum gate copies an
existing coefficient, multiplies it by a root power, and adds it to a
different block (or adds the two affine scalars when d=1). Only scalar
formula leaves can multiply coefficient values. Consequently an
unreduced coefficient expression contains at most the formula's leaf
occurrences, with at most S scalar multiplications along any occurrence.
If base coefficient bit height is H0, its dyadic denominator exponent and
the logarithm of its unreduced l1 norm are polynomial in S and H0.
Reducing root exponents modulo N and then in the Phi_N basis adds
O(N^2) bits. All pencil coefficients therefore have bit heights
polynomial in N,S,H0. There is no repeated-squaring chain hidden in this
coefficient bound.

The Hermite inverses have the same concrete control. A node-difference
inverse is one half a product of at most tau/2-1 binomials `1-rho^v`.
A j-node Lagrange entry, j<=B, uses j-1 such inverse products and j-1
numerator factors. Before cyclotomic reduction its numerator l1 norm has
logarithm O(B tau), and its denominator exponent is O(B). Thus its
canonical basis coefficients have bit heights

    O(B tau+N^2)=O(N^2).

The evaluated binary predictor values have O(m^2) bits. A bounded number
of matrix products constructs the left inverse, right inverse and Hermite
table, retaining polynomial-in-N coefficient heights. Multiplication by
each coefficient in the power basis also has polynomial-in-N bit height:
multiply its representative by a basis power, reduce exponent modulo N,
and apply the same O(N^2) bound. Scalar descent is therefore explicit.

There is a finite polynomial-in-N algorithm to construct Phi_N and all
these data. For example enumerate the integers up to N, build cyclotomic
polynomials by monic division of `X^n-1` by the already constructed
proper-divisor polynomials, and use schoolbook arithmetic. Counts, degrees,
intermediate coefficient heights and retained tables are polynomial in N.
This intentionally slow algorithm avoids any irreducible finite-field
polynomial search. For odd-characteristic execution, reduce the completed
dyadic coefficients modulo p and encode the finite free algebra by its
fixed power-basis coordinate blocks.

All 2^m shift/frequency tuples, D factors, dense coefficient matrices and
their descended maps can now be explicitly listed. A formal optional
verification through degree D has at most `(m+D+1)^D` monomials, also
within the envelope below. These are bounded loops, not an output-size
argument for an unspecified constructor.

## 5. A smaller common finite-data envelope

For definiteness take C=100000 in the deliberately loose envelope

    P_star(m)=2^[m^(C(1+log2 m))].                       (FC4)

For example, if l=log2 m>=1 and D<=m, (FC2) gives
`log2 S_m<=(l+4)^2<=25l^2`. Thus `log2 r<=m^(26l)` and, after a
fixed enlargement, `log2 B<=m^(27l)` and `log2 N<=m^(30l)`.
This explicitly places the formula and conductor bounds inside (FC4).

Equations (FC2)--(FC3) bound B, N, the descended row counts, all finite
matrices and coefficient bit heights by fixed powers of P_star. The
previous rational-address bound has numeric magnitudes at most
`2^(m^10000)`; choosing C>=10000 absorbs that bound as well. Label counts
and every endpoint/factor list are unchanged. A compatible radix prime
above the completed numeric unit list and actual batch width can be
found by bounded trial division, again within a fixed power of P_star.

Thus the specified finite constructor, its retained description/workspace,
and the complete finite-data input to the previously audited physical
compiler are all bounded by `P_star(m)^O(1)`. The compiler then gives the
same type of profiles

    a_j,c_j,g_j,d_j <= P_star(m_j)^O(1),
    U_j <= max(U_absolute, 2^[P_star(m_j)^O(1)]).         (FC5)

This substitution changes the evaluator and its finite coefficient list.
It preserves the original source's query algebra, ordinary label geometry,
exact Hermite repair, and recursive child volumes. A predictor now has D
possibly different affine stages rather than repetitions of one root;
the source shared-pencil interface permits arbitrary fixed row matrices
at each stage. Its per-input call invoice can only improve by replacing
the previous b>=D stages with D. The previous conservative parameter
acceptance test may be retained unchanged.

The new descended batch width need not be a power of two. The source
binary proposition already permits incomplete batches with factor at most
`1+W/2^r`; the accepted quarter margin absorbs a factor of two. The tape
Walsh caller explicitly pads its leading range to a multiple of W^J,
then has exact V/W child volumes. Its proof uses arbitrary integer W,
not power-of-two W. The threshold for that padding is already included
in the physical compiler's polynomial-in-finite-data cutoff.

## 6. Global profile inversion through the accepted compiler

Retain the accepted `log2 m_j=O(J^3 log2 J)` parameter bound, J=j+2.
From (FC4),

    log2 P_star(m_j)=2^[O(J^6(log2 J)^2)].

The existing common-cap assembly therefore has

    log2(prefactor_j), log2 L(threshold_j)
       <=2^[C1 J^6(log2 J)^2]                           (FC6)

for an absolute C1. This is a single exponential in that target-index
expression, whereas the monomial-module bound was a double exponential.

Let s=log2 L(n), z=log2 s, and choose a sufficiently small fixed multiple
of `(z/(log2 z)^2)^(1/6)` for a dyadic J. Then the right side of (FC6)
is at most sqrt(s), ensuring both eligibility and a negligible prefactor
relative to s/J. The conditional logarithmic overhead is

    O(s (log2 log2 s)^(1/3)/(log2 s)^(1/6)).             (FC7)

This last statement has passed independent acceptance of the finite-data
substitution and reuses the separate physical/compiler/common-cap gates;
see the lead review and `REVIEW-A-FORMULA-EXTRACTION.md`. It is not a claim of a polynomial-s or constant overhead. The new
factorization also remains exponential in a quasipolynomial of m; it is
not a polynomial-width evaluator.

## 7. Review and verification status

Route C independently checked the product/rotation invariant, total-grade
sum dimension, syntactic degree of the balanced count formula, common
extension, coefficient construction and source padding interface. A
dedicated exact test will include ramified odd-characteristic root images
and power-two node differences in cyclotomic rings with odd conductor
factors. Its finite scope will be stated separately. Lead review has
accepted the new profile (FC4)--(FC7).

The exact checker `verify_formula_cyclotomic.py` passed and saved
`formula-cyclotomic-verification.json`: 120 cyclotomic coefficient-height
checks, 25 integer power-two node inverse products, 75 odd-characteristic
node inverse checks, 522 vanishing Gaussian coefficients (138 with the
characteristic dividing the factor length), and 216 complete rotated
products in 48 ramified degree-three/degree-six sum examples.
The degree-six test uses F3[epsilon]/epsilon^2 and has a nonzero square-zero
partial geometric sum, explicitly excluding a unit-denominator shortcut.
A deliberately noncyclotomic root was rejected. These are finite
corroboration, not a constructed giant formula template.
