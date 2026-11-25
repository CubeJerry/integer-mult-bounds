# Full-rate affine factorization from a characteristic-two formula

Status: **accepted finite construction and generator after independent A, C and lead review**.
This note supplies a proposed smaller evaluator for the order-three
predictor. Its complete physical consequence is proved in
`../A/formula-extraction-theorem.md` and accepted in
`../../verification/S002/lead-review-formula-extraction.md`.

## 1. Cyclic affine factorizations

Let `K` be a commutative characteristic-two algebra and let the query
variables commute. A cyclic length-d factorization of a scalar polynomial
`f` consists of square affine pencils `A_0,...,A_(d-1)` of common size r
such that **every cyclic rotation** of their ordered product equals
`f I_r`. Products act in temporal order: starting at grade i means
`A_(i+d-1) ... A_i`, with indices modulo d.

An affine scalar leaf has length one and size one. Constants are retained
as length-zero scalars. For a positive required length d, a constant a has
the cyclic factorization `(a,I,...,I)` of size one. Padding any positive
cyclic factorization with identity factors preserves the property. These
conventions handle zero constants and unequal-degree sums without assuming
that any factor is invertible.

Use a formula's **syntactic degree**: constants have degree zero, affine
nonconstant leaves degree one, addition takes the maximum, and multiplication
takes the sum. Cancellation is not used to lower this degree. Prescribed
larger degree budgets can also be used, padding with identities. All budgets
below are at most a fixed D.

## 2. Multiplication costs no extra row factor

If f and g have cyclic factorizations of lengths a,b and sizes r,s, take
the a factors `A_i tensor I_s`, followed by the b factors `I_r tensor B_j`.
This is a length-(a+b), size-rs cyclic factorization of fg. To verify a
rotation starting inside one list, commute the other list past it: the
other list multiplies to its scalar times the identity, and the split list
rejoins in one of its valid cyclic rotations. Factors from the two tensor
coordinates commute. If one input is constant, multiply one factor of the
other list by that scalar. If both are constant, retain their product as a
constant. These operations also work when a scalar polynomial vanishes.

## 3. Addition costs a factor d in the row dimension

Pad the two cyclic factorizations to common length d=max(a,b)>=1. Write
`d=2^v c` with c odd, and suppose K contains a root xi satisfying the
primitive-c cyclotomic polynomial. For c=1 set xi=1.

On the graded module `K^d tensor K^r`, define

\[
 L_A(e_i\otimes x)=e_{i+1\bmod d}\otimes A_i x,
 \qquad Z_A(e_i\otimes x)=\xi^i e_i\otimes x.
\]

Then `L_A^d=f I`, `Z_A L_A=xi L_A Z_A`, and `Z_A^d=I`.
Define `L_B` analogously. On their tensor product put

\[
 X=L_A\otimes I,\qquad Y=Z_A\otimes L_B,\qquad L=X+Y.
\]

Here `YX=xi XY`. The Gaussian-binomial identity gives
`(X+Y)^c=X^c+Y^c`: its mixed coefficients vanish at a primitive c-th root.
This identity holds in `Z[xi]` and after specialization; no division by c
inside K is needed. The two resulting powers commute. Frobenius in
characteristic two now gives

\[
 L^d=(X^c+Y^c)^{2^v}=X^d+Y^d=(f+g)I.             \tag{FL1}
\]

This is the critical characteristic-two step. It does **not** ask for a
primitive even-order root, which would be unavailable in a field of this
characteristic.

Grade the tensor product by the sum of its two cyclic grades modulo d.
Every total-grade space has dimension `d r s`; both X and Y raise total
grade by one. Restricting L between successive total-grade spaces therefore
gives d square affine pencils of size `d r s`. Equation (FL1) gives every
cyclic product, so this is a cyclic length-d factorization of f+g.

## 4. The formula lemma

**Lemma FL.** A commutative arithmetic formula of syntactic degree at most
D>=1, with S addition gates, has a cyclic factorization into D affine
pencils on at most `D^S` independent rows, over an explicit finite extension
of its coefficient algebra containing primitive roots of every odd order
at most D. A smaller final length is padded to D.

**Proof.** Induct using Sections 1--3. A multiplication multiplies row
dimensions. An addition of positive degree d multiplies them by d; a
constant addition does not enlarge them. Hence the final size is the
product of these positive d values, at most `D^S`. The construction retains
the cyclic property even for identically zero intermediate polynomials.
Every product equals the scalar formula value times the **whole identity**.
Thus every row carries an arbitrary independent input. No selected-output
or zero-workspace interpretation is used. QED.

## 5. An explicit syntactic-degree-D formula for the count predictor

Work over `F4` and treat the two powers of each order-three query as two
formal commuting variables. For a fixed shift beta, let `I_(j,b)` be the
source affine indicator for shifted digit b in `{0,1,2}`. In characteristic
two the local generating function becomes

\[
 (1+T)^{b_j}=1+I_{j,1}T+I_{j,2}T^2.                    \tag{FL2}
\]

This is an identity at every allowed spectral tuple; its right side is
the formal multivariate representation used to construct the predictor.
Pad the list of m factors with constant ones to `m0=2^ceil(log2 m)`.
For a balanced interval I define the coefficient formula

\[
 F_{I,h}=[T^h]\prod_{j\in I}(1+I_{j,1}T+I_{j,2}T^2).
\]

At a leaf the coefficients are 1, `I_(j,1)`, `I_(j,2)`, then zero. At an
internal node use the genuine formula, with copied subexpressions,

\[
 F_{I,h}=\sum_{a=0}^h F_{I_L,a}F_{I_R,h-a}.             \tag{FL3}
\]

Its syntactic query degree is at most h: a coefficient of T-degree one
or two at a leaf has query degree at most its T-degree, and the displayed
degree budgets add under products. This avoids interpolation formulas whose
high-degree cancellations would not control the factor length.

Retain only `h<=D`. If `T_r` bounds the number of nodes in any coefficient
formula after r balanced levels, then
`T_r<=2(D+1)T_(r-1)+2D+1<=4(D+1)T_(r-1)` with `T_0>=1`.
The source multiplication by the fixed series `(1+T)^(-u)`, followed by
the final expression
`omega^(u-sum_j beta_j) sum_(h<=D)(omega-1)^h L_h`, adds only a polynomial
in D number of copies and scalar operations. Retain the displayed scalar
prefactor from the source predictor; it is absorbed into one affine factor
and changes neither the syntactic degree nor the row width. One explicit
loose bound for the
total formula size is

\[
 S_m\le[8(D+1)]^{\lceil\log_2m\rceil+3}.               \tag{FL4}
\]

Its syntactic degree is at most D. Its scalar coefficients lie in `F4`:
the generalized binomial coefficients of `(1+T)^(-u)` are reduced modulo
two. They can be generated by integer arithmetic in time polynomial in
m and D. The tree shape and assigned degree budgets can be chosen
independently of beta, so all shifts receive factors of a common size.
Constant zero subtrees are retained or represented by a zero factor, rather
than invoking an unproved nonvanishing assumption.

For the constant-tail window `D=6 ceil(sqrt m)`, (FL4) gives

\[
 S_m=2^{O((\log(m+2))^2)},\qquad
 r_m\le D^{S_m}=2^{\,2^{O((\log(m+2))^2)}}.             \tag{FL5}
\]

The D pencils on this whole row module multiply to `P_beta I_(r_m)`.
Direct-sum them over all `3^m` shifts and duplicate by 32. The resulting
predictor has `R=32*3^m*r_m` independent rows, still satisfies (FL5), and
takes **D** shared pencil stages. Every pencil is affine in the individual
query powers. This is a full-rate formula construction, not the
single-output branching-program interface.

## 6. Integral version for the original binary source

The same addition proof works over `Z[xi_d]` with a primitive d-th root,
using the integral Gaussian-binomial identity directly. It does not need
Frobenius. Thus Lemma FL has a characteristic-independent cyclotomic
version. Its identities continue to hold under every specialization,
including a prime dividing d. A specialized root is not required to retain
its complex order: the coefficients vanish as polynomial identities in
the cyclotomic quotient.

For the original binary count predictor, the local generating factors are
`1+I_j T`, with affine dyadic indicators `I_j`. The identical coefficient
formula (FL3) has syntactic degree at most h. Its formula size has the
same bound (FL4). The source rare-tail choice
`D=O(sqrt(m log(m+2)))` still gives (FL5), since `log D=O(log m)`.
This version can improve the original source scalar generator directly;
it does not require the characteristic-two gate construction.

Let `R=2^m r_m` be the predictor row count before scalar-basis expansion.
Put `M0=lcm(1,...,D)` and choose `2^a>=R` minimally. Work in

\[
 E=\mathbb Z[1/2,Z]/(\Phi_M(Z)),\qquad M=M0\,2^a.       \tag{FL6}
\]

Every needed d divides M, so `Z^(M/d)` supplies the primitive-d
cyclotomic relation. The root `rho=Z^(M0)` supplies `2^a` check nodes.
Its distinct node differences are units by the source's explicit product
identity `Phi_(2^b)(1)=2`. The formula matrices and all repair tables use
this **one common finite free algebra**. Reduction modulo any odd data
prime preserves the identities and the node units, even if that prime
divides M0. No irreducible finite-field polynomial search is required.

The rank of E over `Z[1/2]` is `phi(M)<=M`. Since
`log2 M0<=D log2(D+1)=o(m)`, one has `M0<=2^m<=R` above an effective
absolute cutoff, and hence `M<=2R^2`. The bounded smaller range may be
handled by a direct baseline.

## 7. Actual coefficient and generator bounds

Represent E in the monomial basis modulo `Phi_M`. The integer polynomial
`Phi_M` has degree at most M and coefficient absolute values at most `2^M`:
its complex roots have modulus one, so each coefficient is bounded by the
corresponding binomial sum. Compute it by exact polynomial division from
`X^d-1=prod_(e|d) Phi_e(X)` over divisors of M. Enumerating possible
divisors up to M is allowed; these are finite data and M is already in the
budget. Schoolbook polynomial and integer operations give a fixed
polynomial-in-M construction, including coefficient bit lengths and space.

The formula induction uses copies, Kronecker blocks, root monomials,
addition, grade restriction and scalar constant multiplication. Let B0 be
the maximum original dyadic scalar bit height, polynomial in m for the
count predictor. Before basis reduction, every coefficient has numerator
and denominator bit height `O(S_m(B0+1))`. A root exponent can first be
reduced modulo M because `Z^M=1`. Reducing the resulting polynomial modulo
`Phi_M` adds at most `O(M^2)` to the bit bound by ordinary monic reduction.
Thus every affine matrix coefficient has bit height polynomial in R.
There are at most a fixed polynomial in `S_m,D,m,r_m,M,2^m` listed entries
and intermediate construction operations, all polynomial in R for large m.

For an inverse check-node difference, the source explicit root product
has at most `2^a<=2R` factors and a denominator two. A Lagrange inverse
uses at most R such products. Before basis reduction its coefficient
logarithmic height is `O(R^2)`; reduction adds `O(M^2)`. The remaining
finite Hermite tables use polynomially many matrix entries and arithmetic
operations of bounded depth on these explicit quantities. Their bit
heights, generation time and workspace are polynomial in R. This is an
actual list-and-arithmetic bound, not an inference from output size alone.

Expanding the completed ring-linear template in a basis of E gives dyadic
row matrices. Because the completed target has dyadic base coefficients,
every basis component carries an independent input and receives its own
transform. Both width and recursive calls are multiplied by the extension
rank, preserving their ratio. All expanded scalar-multiplication matrices
have polynomial-in-R dimensions, bit heights and construction cost.

The label matrices have polynomial-m dimensions and rational bit heights.
Their numeric scaling magnitudes and a compatible address prime are bounded
by `2^(m^c)` for a fixed c. Combining them with the formula module gives a
common bound on expanded description, numeric address data, generator
time, generator space, finite alphabets and all coefficient tables:

\[
 P_m\le2^{\,2^{C(\log(m+2))^2}}.                        \tag{FL7}
\]

Here C is absolute. It dominates every fixed polynomial-m address exponent.
This improves the generic monomial-tensor envelope; it does not yet remove
the physical compiler or the common-space-cap requirements.

## 8. Arbitrary batch widths and an optional binary rounding wrapper

The factor dimensions and cyclotomic rank need not be powers of two.
The actual source `binary.tex` and tape `walsh.tex` permit arbitrary W,
with explicit leading-row padding and its threshold. The power-of-two W
of the original scalar constructor is a convenience, not a caller premise.
The quantitative compiler must retain those stated padding costs.

If a different caller requires a power-of-two batch, there is also a
full-rate wrapper. After complete dyadic basis expansion, let B be the
batch of the fast completed normalized Walsh template. Take the least
power of two `W>=m^2 B`. Run `floor(W/B)` full fast batches and use the
direct A-axis normalized fallback on the fewer than B remaining independent
rows. Every row is occupied. The resulting call ratio is at most

\[
 \sigma_{\rm fast}/B+A/m^2,\qquad W<2m^2B.              \tag{FL8}
\]

Here `A=O(m)` at the chosen parameters, so the added ratio is `O(1/m)`
and can be included in the strict contraction test. This wrapper preserves
(FL7), but is optional for the source compiler. Replicating an odd-factor
module to exactly a power of two without residual handling would be wrong.

## 9. Consequence of the separately proved physical compiler

This section states the composition through the accepted finite construction
and quantitative physical compiler. The complete theorem and independent
gates are linked in the status paragraph above.
The uniform source label estimates permit exponent slack `Theta(1/J)`
with a fixed margin at `log2 m=O(J^3 log(J+2))`, as detailed in
`reflection-template-growth.md`. The original rare-tail predictor suffices.
Equation (FL7) gives

\[
 \log_2 P_{m_J}\le2^{O(J^6(\log(J+2))^2)}.              \tag{FL9}
\]

If the bounded-template compiler supplies time/space/generation coefficients
`<=P^C` and threshold `U<=2^(P^C)`, the common-cap schedule has

\[
 \log_2(\text{candidate prefactor}_J),\quad
 \log_2 L(N_J)\le2^{O(J^6(\log(J+2))^2)}.              \tag{FL10}
\]

For `s=log2 L(n)`, choose a dyadic inverse slack J within a fixed factor of
`c (log(s+2))^(1/6)/(log log(s+4))^(1/3)`, with c sufficiently small.
The right side of (FL10) is then `s^a` for a fixed `a<1`, while exponent
slack contributes `O(s/J)` and dominates the log-prefactor and schedule.
The resulting target is

\[
 H(n)\le2^{O\left(
 s\,{(\log\log(s+4))^{1/3}\over(\log(s+2))^{1/6}}
                         \right)}.                    \tag{FL11}
\]

Unlike IP4, the representation premise here is the explicit construction
in this note. The complete bound has passed independent verification of the construction,
actual generation bill, physical compiler and common-cap composition;
see the separate A theorem and lead/C final reviews.

## 10. Prior art and attribution

The graded sum operation is the established tensor product of d-fold
matrix factorizations. See Richie Sheng and Tim Tribone, *Tensor products
of d-fold matrix factorizations*, DOI `10.1017/nmj.2025.12`, Definition 3.1
and Proposition 3.2 (online 2025; Nagoya Mathematical Journal 261, 2026).
Their construction requires a ring map from the integral cyclotomic ring,
so specializations dividing d are included. No invention of that tensor
operation is claimed here.

The programme contribution is the explicit formula-size/full-rate
application to the source predictors, its all-row and arbitrary-rotation
accounting, and the effective common algebra and generator bounds. Route C
independently identified the integral version while reviewing the
characteristic-two derivation; Routes A and C and the session lead
independently checked the cyclic tensor argument. Final gate status is
recorded separately, not inferred from this note.

Credits: the cited matrix-factorization literature and its predecessors;
the OpenAI source predictor, routing and tape proofs; Jerry Chen
(@CubeJerry); AI-assisted derivation and verification during this session.

## 11. Exact finite verification

`verify_formula_linearization.py` constructs the grade-restricted matrices
over `F_p[z]/(z^4-z^2+1)` and checks their full formal-polynomial matrix
identities, rather than evaluating at sampled query values. It checked all
196 cyclic products in its cases with `d=2,3,4,6` and `p=2,3,5,7`.
This includes nonreduced specializations at primes dividing the conductor,
zero children, unequal degree budgets, constants and products of
noncommuting cyclic modules. Every resulting matrix entry remained affine.
Deliberately wrong root twists, wrong total grades and replacement of the
cyclic invariant by a single product identity were all rejected. A further
264 cases checked the copied-formula node recurrence and degree budgets.
The result is recorded in `formula-linearization-verification.json`.

These finite checks corroborate the construction and distinguish its key
invariants. They do not establish the asymptotic data bounds or execute the
physical tape compiler. Route C's separate ramified-ring checker and
generator proof are in `../C/FORMULA-CYCLOTOMIC-GENERATOR.md` and its linked
verification artifacts; the final independent gate is recorded by the lead.
