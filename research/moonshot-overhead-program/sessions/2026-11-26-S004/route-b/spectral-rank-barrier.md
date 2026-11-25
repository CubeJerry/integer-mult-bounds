# Polynomial prediction, rank repair, and the failure of repair-free rounding

Checkpoint disposition: B1--B3 admitted after C and lead review; B4 separately lead accepted. See `lead/FIRST-WAVE-ADMISSION.md` relative to the session root.

Status: **proved scoped algebraic obstruction; independent review in progress**.
This is not a lower bound on general Fourier algorithms or integer
multiplication. It supplies no new complete multiplication envelope.

The protected Route B question was whether numerical approximation followed
by exact integer rounding could remove spectral repair altogether. It led to
two conclusions. First, a low-degree predictor cannot approximate the required
operator uniformly, even with unlimited row width. Second, allowing arbitrary
row mixing and nonsymmetric predictors does not remove the square-root times
square-root-logarithm degree requirement when the total rank repair is
polynomially rare. The latter statement is stronger in scope than the
programme's earlier *count-symmetric, diagonal* obstruction.

The method is a finite-dimensional polynomial/Hilbert-function argument of
the general kind associated with Razborov and Smolensky. We do not claim
literature priority for that method or for the scalar special case. The
self-contained result needed here is its arbitrary-matrix, multiple-repair
form, with the actual query-degree convention kept visible.

## 1. Model

Fix integers `r>=2`, `m>=1`, and `W>=1`. Let `K` be a field whose
characteristic does not divide `r`, containing all `r`-th roots of unity.
Write `Omega=mu_r^m`, `N=r^m`, and

\[
 A=K[x_1,\ldots,x_m]/(x_1^r-1,\ldots,x_m^r-1),
 \qquad \chi=x_1\cdots x_m.
\]

Every element of `A` has a unique reduced representative with exponents in
`{0,...,r-1}`. Its **support degree** is the largest number of coordinates
having a nonzero exponent in a monomial with nonzero coefficient. It is
subadditive under multiplication: reduction modulo `x_i^r=1` cannot create a
new supported coordinate. A matrix has the maximum support degree of its
entries. Constants, including arbitrary row maps, have degree zero.

This is the relevant degree for the source pencil

\[
 A_0+\sum_{j=1}^m\sum_{a=1}^{r-1} A_{ja}x_j^a.                 \tag{1}
\]

Each such pencil has support degree at most one. In particular, for `r=3`,
both `x_j` and `x_j^2` cost one pencil stage; counting only ordinary total
degree without this conversion would give the wrong stage constant.

Let `P` be an arbitrary `W`-by-`W` matrix over `A`, of support degree at
most `t`. At a spectral tuple `omega in Omega`, the desired transfer is
`chi(omega) I_W`. Define

\[
 \mathcal E(P)=\frac1{NW}\sum_{\omega\in\Omega}
          \operatorname{rank}\bigl(\chi(\omega)I_W-P(\omega)\bigr).
                                                               \tag{2}
\]

There is no diagonal, symmetry, common-eigenvector-in-row-space, or
coordinate-sparse-error hypothesis on `P`. The spectral variables commute,
but the coefficient matrices need not commute with one another. `W` may
depend arbitrarily on `m` and `t`.

## 2. Matrix rank-defect theorem

**Theorem B1.** Put

\[
 T=\left\lfloor\frac{(r-1)m}{r}+\frac{(r-1)t}{2}\right\rfloor.
\]

If `X` has the binomial distribution `Bin(m,(r-1)/r)`, then

\[
 \boxed{\quad \mathcal E(P)\ge \Pr[X>T].\quad}                  \tag{3}
\]

The right side is interpreted as zero when `T>=m`. In particular, some
spectral tuple has normalized rank defect at least this amount.

### Proof

Evaluation on `Omega` identifies `A` with the product of `N` copies of `K`.
Indeed, each polynomial `x_i^r-1` has distinct roots under the stated
characteristic hypothesis, and successive univariate interpolation gives
the isomorphism. Consider the `A`-module

\[
 Q=A^W/\operatorname{im}(\chi I_W-P).
\]

Its dimension as a `K`-vector space is

\[
 \dim_K Q=\sum_{\omega\in\Omega}
              \left[W-\operatorname{rank}(\chi(\omega)I_W-P(\omega))\right].
                                                               \tag{4}
\]

In this quotient, `chi v` equals `P v` for every `v`. Multiplication by
`P` preserves the image being quotiented out, because `P` commutes with
`chi I_W-P`. Consequently `chi^h v=P^h v` in `Q` for all nonnegative
integers `h`.

Take a reduced monomial `x^alpha e_j`. For `h=0,...,r-1`, let
`beta_h=alpha-h(1,...,1) mod r`, with reduced coordinates. Then

\[
 x^\alpha e_j=\chi^h x^{\beta_h}e_j
              =P^h x^{\beta_h}e_j\quad\hbox{in }Q.              \tag{5}
\]

Each coordinate of `alpha` equals exactly one of the values of `h`.
Therefore

\[
 \sum_{h=0}^{r-1}|\operatorname{supp}(\beta_h)|=m(r-1),
 \qquad \sum_{h=0}^{r-1}h=r(r-1)/2.
\]

At least one choice of `h` consequently satisfies

\[
 |\operatorname{supp}(\beta_h)|+ht\le T.                         \tag{6}
\]

The representative on the right side of (5) has support degree at most
the left side of (6). Thus `Q` is spanned by the monomial vectors of
support degree at most `T`. There are

\[
 W\sum_{k=0}^{\min(T,m)} {m\choose k}(r-1)^k
       =WN\Pr[X\le T]
\]

such vectors. Combining this dimension upper bound with (4) proves (3).
No independence between row coefficients, diagonalization of `P`, or
inequality over an ordered field was used. QED.

### Binary specialization and a second proof

For `r=2`, in every characteristic other than two,

\[
 \mathcal E(P)\ge
 2^{-m}\sum_{k>\lfloor(m+t)/2\rfloor}{m\choose k}.                \tag{7}
\]

A direct injection proves the same bound. Let
`a=floor((m-t-1)/2)`. Multiplication by `chi` sends a monomial of degree
at most `a` to one of degree at least `m-a`, whereas multiplication by
`P` sends it to degree at most `a+t<m-a`. Hence `chi I-P` is injective
on the `W sum_(k<=a) binom(m,k)`-dimensional low-degree space. Its rank
as an operator on `A^W` is at least this number. Evaluation and binomial
symmetry give (7). This proof also shows why increasing the batch width
does not reduce the normalized obstruction.

### Ordinary total-degree variant

If instead every reduced entry of `P` has ordinary total degree at most
`d`, the same proof replaces support size by `sum_i beta_(h,i)`. Its
average is `m(r-1)/2`. Thus

\[
 \mathcal E(P)\ge
 \Pr\!\left[\sum_{i=1}^m U_i>
                  \left\lfloor\frac{(r-1)(m+d)}2\right\rfloor\right],
                                                               \tag{8}
\]

where the `U_i` are independent and uniform on `{0,...,r-1}`. For the
source's `r`-ary pencil convention, one may safely set `d=(r-1)t`;
the support-degree theorem is stronger for the order-three application.

## 3. Multiple interacting spectral repairs

The earlier count-only note treated one factored correction of a diagonal
predictor. The following formulation includes a finite linear program with
arbitrarily many interacting tables.

**Theorem B2 (total repair width).** Consider a finite linear straight-line
program on `W` arbitrary independent input rows, with any finite number of
workspace rows initialized by query-independent linear maps. Permit:

1. query-independent row maps, copies, accumulation, and deletion;
2. pencil stages of the form (1);
3. spectral-table gates whose departures from a query-independent reference
   gate have rank at most `h_i` at every spectral tuple.

Suppose replacing all table gates by their reference gates leaves an output
matrix of support degree at most `t`. For example, the total number of
pencil stages bounds `t`; more generally one can use the maximum pencil
degree along any input-to-output path. If the original program computes
`chi I_W` exactly, then

\[
 \boxed{\quad \frac{\sum_i h_i}{W}\ge
    \Pr\!\left[\operatorname{Bin}(m,(r-1)/r)>T\right].\quad}       \tag{9}
\]

Here a full table on `h_i` channels can be compared to its identity action;
the difference has rank at most `h_i`. The same bound applies to a linear
correction factoring through `h_i` channels, compared to zero.

### Proof

Embed all rows in one finite state vector, using query-independent
injections and projections for initialization and output. A table acting
on `h_i` channels differs from its reference state transition by a matrix
of rank at most `h_i`. At a fixed spectral tuple, replace the table gates
one at a time. The difference in final input-output matrices at one
replacement is a product `L_i Delta_i R_i` of the changed gate difference
with the preceding and following linear maps. Its rank is at most `h_i`,
regardless of whether those other maps contain remaining tables. The sum
of these telescoping differences therefore has rank at most `sum_i h_i`.

Call the table-free output matrix `P`. The assumed polynomial-path bound
gives its support degree at most `t`. Thus every tuple satisfies
`rank(chi I-P)<=sum_i h_i`. Average and use Theorem B1. QED.

This proof allows all table coefficients to depend arbitrarily on the
spectral tuple. It also allows arbitrary finite workspace and row mixing.
It does not treat a nonlinear, input-dependent control step as a linear
table gate. A coordinate map which does not preserve the common spectral
decomposition is outside this specific model unless its effect is charged
through an appropriate gate in the statement.

### Interpretation of the source's repair

In the source Hermite construction, setting the spectral table output to
zero leaves `g(P)` rather than the initial predictor. Therefore the relevant
degree in (9) is the degree of that entire table-free path. Counting only
the initial predictor degree would omit genuine work. The same rule applies
to the division repair, finite contraction trees, and repeated corrections:
count every surviving predictor application on each path and every table
width used in the telescoping sum.

Theorem B2 is an algebraic rank-width restriction. A gate width by itself
does not specify tape time, full-rate packing, conversion cost, or space.

## 4. Polynomially rare repair requires square-root-log degree

Fix `r>=2` and a positive constant `a`. As `m` tends to infinity, any
sequence of predictors satisfying `mathcal E(P)<=m^(-a)` must have

\[
 t\ge (1-o(1))
      \sqrt{\frac{8a}{r^2(r-1)}\,m\ln m}.                       \tag{10}
\]

The same conclusion holds if a complete linear program has total normalized
table width at most `m^(-a)`, with `t` defined as in Theorem B2. In the
binary case the constant is `sqrt(2a)`; in the source order-three stage
convention it is `2 sqrt(a)/3`.

### Moderate-tail proof

For a fixed `p in (0,1)`, let `X_m~Bin(m,p)`. For fixed positive `c`,

\[
 \Pr[X_m>mp+c\sqrt{m\ln m}+O(1)]
          =m^{-c^2/(2p(1-p))+o(1)}.                              \tag{11}
\]

Here is the quantitative justification needed for (10). A Chernoff bound
obtained from the exact moment generating function gives
`log Pr[X_m>=mp+u] <= -u^2/(2mp(1-p))+O(u^3/m^2+u/m)` on
`u=O(sqrt(m ln m))`. For the lower bound, Stirling's factorial formula
with its bounded logarithmic remainder gives, uniformly on this range,

\[
 \log\Pr[X_m=k]
 =-\frac{(k-mp)^2}{2mp(1-p)}-\frac12\log m
       +O(1+|k-mp|/m+|k-mp|^3/m^2).
\]

Sum `floor(sqrt(m/ln m))` consecutive masses just above the requested
threshold. Their exponents differ by `O(1)`, and their number cancels
the `m^(-1/2)` prefactor up to `(ln m)^(-1/2)`. This proves the matching
logarithmic exponent in (11). The integer rounding affects neither side.

In (3), take `p=(r-1)/r` and displacement `(r-1)t/2`. For
`t=c sqrt(m ln m)`, the logarithmic tail exponent is

\[
 \frac{r^2(r-1)c^2}{8}.
\]

If `c` is smaller than the constant in (10), this tail eventually exceeds
`m^(-a)`. Monotonicity gives the claimed liminf bound. This is a necessary
condition; optimality for arbitrary `r` is not asserted.

### What changes for the existing programme

For binary characteristic-zero count predictors, the older sharp count
theorem already had the leading lower scale `sqrt(2a m ln m)`. The present
matrix theorem preserves that leading lower constant while removing count
symmetry, diagonality, a fixed batch width, a single repair use, and the
characteristic-zero restriction. It does not necessarily reproduce every
older exact finite-`m` constant.

For order-three `F4` predictors, the support-degree form genuinely applies:
`3` is invertible in characteristic two and the three nonzero field elements
are the distinct cube roots of unity. It does not identify `-1` with a
nontrivial binary character, and it does not apply the invalid binary
argument in characteristic two.

In particular, changing only the low-degree predictor to a nonsymmetric or
nondiagonal one cannot make an `m^(-a)` total-rank-repair invoice work with
`o(sqrt(m ln m))` stages. A constant-tail repair has a different budget and
is not ruled out. The programme's existing finite contraction remains a
legitimate way to change that budget.

## 5. Repair-free operator approximation and integer rounding

**Theorem B3 (uniform norm obstruction).** Work over `C` and equip `Omega`
with the uniform measure. If `P` has support degree `t<m`, then

\[
 \frac1N\sum_{\omega\in\Omega}
       \|\chi(\omega)I_W-P(\omega)\|_F^2\ge W,
 \qquad
 \max_{\omega\in\Omega}\|\chi(\omega)I_W-P(\omega)\|_{2\to2}\ge1.
                                                               \tag{12}
\]

### Proof

The characters `x^alpha`, with reduced exponent tuples, are orthonormal
under uniform evaluation on `Omega`. The target character `chi` has
support degree `m`, so it is orthogonal to every matrix entry of `P`.
Each diagonal entry of `chi I-P` has squared norm at least one; each
off-diagonal entry contributes a nonnegative squared norm. This gives the
Frobenius inequality. Since `||M||_F^2<=W||M||_(2->2)^2`, the maximum
operator norm is at least one. QED.

If a family of commuting unitary queries realizes every tuple in `Omega`,
the corresponding physical operator has the same lower norm bound by
unitary spectral conjugation. Small average *exception probability* is
therefore not a small uniform operator approximation. Increasing numerical
precision cannot remove this algebraic error.

There is also an exact physical witness for permutation queries. Let
`G=(Z/rZ)^m` and let `Q_j` translate the `j`-th address by one. For any
input row `a` and address `g`, put a single integer one at `(a,g)` and zero
elsewhere. The target product places that one at `(a,g+(1,...,1))`.
The output of `P(Q)` at that same row/address is zero: its coefficient
would be the `(a,a)` coefficient of the missing support-`m` monomial
`x_1...x_m`. Thus nearest-integer rounding returns zero where the correct
answer is one.

The witness continues to hold for any fixed coordinatewise decoder that
returns zero on zero input. It also covers affine offsets: correctness on
the all-zero input forces the decoder to return zero on the offset, and
the witness produces the same value at the missing target coordinate.
On a product of nontrivial two-element swap orbits this gives the binary
interchange witness directly.

This is not a statement that every approximate multiplication algorithm
must compute this particular intermediate transform. A nonlinear global
decoder, input-dependent branch, alternative representation, or separately
charged exact check can escape this restricted operator model. The theorem
shows that merely deleting exact repair and relying on final rounding is
not such an escape.

**Corollary B4 (dense ordinary-coordinate errors).** In the regular
permutation setting above, let the final decoder act independently at each
output coordinate, with arbitrary fixed scalar decoding functions. For
uniformly independent input bits on all `WN` row/address coordinates, the
expected number of incorrect decoded output coordinates is at least `WN/2`.
Consequently some binary input produces at least `WN/2` incorrect outputs.

For an output coordinate `(a,g+(1,...,1))`, the value produced by `P(Q)`
does not depend on the input bit at `(a,g)`, because the corresponding
support-`m` coefficient is zero. Conditional on all other input bits, the
decoded candidate is fixed while the correct output is an independent fair
bit. Its probability of being correct is therefore at most one half.
Linearity of expectation proves the claim; it requires no independence
between different output-error events.

Thus this repair-free route cannot be rescued by an ordinary-coordinate
corrector that assumes a sublinear number of wrong outputs. This conclusion
is specific to the stated translation/permutation model and coordinatewise
decoder; it does not forbid a globally nonlinear candidate constructor.

## 6. Portfolio decision and remaining routes

The proposed repair-free low-degree route fails its first decisive gate.
The failure persists under nonsymmetric matrix coefficients and arbitrary
batch width, and it is witnessed on exact small integer data in the
permutation case. Further tuning of interpolation windows cannot repair
that issue.

Two different mechanisms remain meaningful:

* Change the repair recurrence so that a constant rank fraction can be
  corrected inexpensively, with all physical calls charged. Existing finite
  batch contraction is relevant, but this note does not complete its tape
  execution.
* Replace the common-spectrum polynomial network itself, for example by a
  nonlinear exact residual/certificate mechanism or a representation whose
  charged primitive does not have bounded support degree. Such a proposal
  needs its own end-to-end physical recurrence; it cannot count the escaped
  primitive as a free decoder.

## 7. Sources, provenance, and verification scope

Pinned source: `openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`,
Fourier manuscript `build/repair.tex`, especially `eq:repair-pencil`,
`thm:repair`, and `lem:hermite-repair`. Tape `build/interchange.tex`,
the swap-spectrum subsection, supplies the full binary sign family and
permutation-orbit interpretation. The full source `repair.tex` and
`interchange.tex` were read for this route. The integer rounding paragraphs
of tape `build/integers.tex` were also read; their numerical approximation
is distinct from deleting an algebraically necessary repair.

Programme predecessor: `routes/C/COUNT-PREDICTION-BARRIER.md`; the earlier
note's exact finite count inequality and declared invoice remain valid in
their original scope. The matrix generalization here answers its first
listed open question only at the rare-repair degree scale, not for every
possible nonsymmetric transform architecture.

Prior-art lead: Roman Smolensky, *On Representations by Low-Degree
Polynomials*, FOCS 1993, pp. 130–138,
https://doi.org/10.1109/SFCS.1993.366874. The primary paper's publisher
page was blocked by a browser-verification wall in this session; no claim
of reading that full paper is made. The theorem above is proved directly.
A broader novelty audit and exact comparison against known matrix-valued
versions remain open.

Independent Route C recognized the support-degree strengthening and is
auditing the quotient algebra and finite `F4` cases. Root supplied the
initial requirement to test uniform operator norm and exact integer
rounding. This note was developed for @CubeJerry with substantial ChatGPT
research assistance. It does not claim authorship of the source manuscripts
or classical polynomial method.

No Lean build, full multiplier execution, human refereeing, or general
complexity lower bound is claimed. Finite checks and the independent audit
are recorded in their companion files after completion.

## Open next questions

1. Can constant-fraction spectral repair be physically executed at a
   square-root-scale price without paying equivalent cost in row geometry,
   precision, or routing? The rare-repair theorem explains why this is a
   different and potentially consequential question.
2. Is the `r=3` support-degree rank tail asymptotically sharp, or can a
   stronger matrix-Hilbert argument improve its constant or shape? This
   would sharpen a restricted invoice, not automatically improve runtime.
3. Can a nonlinear deterministic residual certificate exploit an
   approximate product's rigorously bounded error without computing a
   second equally expensive exact product? The certificate, checking,
   correction, and movement costs must all be exposed.
