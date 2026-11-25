# Sharp count-prediction/repair tradeoff in characteristic zero

Status: **proved scoped mathematical obstruction**, with finite exact checks.
This is not a lower bound on integer multiplication, on all Fourier algorithms,
on arbitrary multivariate predictors, or on the tape paper's finite-field swap
implementation. No new complete multiplication overhead bound is claimed.

## 1. Model and exact statement

Fix an integer `m >= 1`. Let `C` have distribution `Bin(m,1/2)`. A count
predictor is a complex polynomial `p` evaluated on the *ordinary integer*
Hamming count. Its exceptional fraction is

\[
 e_m(p)=\Pr[p(C)\ne(-1)^C].
\]

The equality here is exact equality in characteristic zero. Approximate scalar
accuracy is a different question. Write `d = deg(p)`, assigning degree zero to
constant polynomials, including the zero polynomial. For `N >= 0` and integer
`r >= 0`, let

\[
 B_N(r)=2^{-N}\sum_{\text{the }\min(r,N+1)\text{ largest coefficients}}
                         {N\choose k},\qquad B_N(0)=0.
\]

Ties do not affect this number. The largest coefficients occupy a consecutive
central interval.

**Theorem C1 (exact variation bound).** Every such predictor satisfies

\[
 \boxed{\quad e_m(p)\ \ge\ \frac{1-B_{m-1}(d)}2.\quad}                 \tag{C1}
\]

The associated upper bound on *sign agreement* is sharp among degree-at-most-d
real polynomial threshold functions. Sharpness for sign agreement does not
assert sharpness for exact scalar agreement.

The bound includes constant predictors: `p = 1` and `p = -1` both fail with
probability exactly `1/2`, while `p = 0` fails everywhere. When `d >= m`, the
right side is zero, as it must be: degree-m interpolation computes parity
exactly at all `m+1` possible counts.

### Proof

Replace `p` by its real part, obtained by taking real parts of its coefficients.
Every exact match of `p` remains an exact match of this real polynomial. If the
real polynomial is identically zero there are no matches and the claim is
immediate. Otherwise assign a sign `sigma_k` to its value at each integer
`k = 0,...,m`. At zeros choose either neighboring sign so that no unnecessary
sign changes are introduced. The sequence has at most `d` sign changes: each
change between two successive nonzero samples requires a distinct real root
between them, and filling intervening zero samples needs only one change when
the two endpoint signs differ. End intervals can be filled constantly.

Every exact match is a sign match. Let `J` be the set of boundaries `t` with
`sigma_t != sigma_(t+1)`. Then `|J| <= d`. The alternating binomial-prefix
identity is

\[
 A_t:=\sum_{k=0}^{t}(-1)^k{m\choose k}
          =(-1)^t{m-1\choose t}\quad(0\le t<m),\qquad A_m=0.          \tag{C2}
\]

It follows directly by substituting Pascal's identity and telescoping. Summing
by parts gives

\[
 \sum_{k=0}^m\sigma_k(-1)^k{m\choose k}
   =-\sum_{t\in J}(\sigma_{t+1}-\sigma_t)A_t
   \le 2\sum_{t\in J}{m-1\choose t}
   \le 2^m B_{m-1}(d).                                            \tag{C3}
\]

Sign-agreement probability is one half plus one half of the normalized
correlation in (C3), proving (C1).

For sharpness in the threshold problem, choose the `d` heaviest boundaries,
which can be chosen consecutive, and flip the sign at exactly those boundaries.
The increments `sigma_(t+1)-sigma_t` alternate, as do the signs of `A_t`, so an
initial sign makes every contribution in (C3) positive. A real polynomial with
roots at the selected half-integers realizes this sign sequence. For `d >= m`
choose every boundary. This proves the stated sharpness. QED.

### A second exact bound, useful at small degree

If `p` is not a constant equal to `1` or `-1`, the nonzero polynomial `p^2-1`
has at most `2d` distinct roots. Consequently

\[
 e_m(p)\ge1-B_m(2d).
\]

Uniformly over constants and nonconstants,

\[
 e_m(p)\ge\min\{1/2,\,1-B_m(2d)\}.                               \tag{C4}
\]

One can take the larger of the lower bounds (C1) and (C4). The root-count bound
can be stronger at small degree, but (C1) gives the sharp asymptotic constant
for polynomially rare exceptions.

## 2. Arbitrary shift distributions and full-rate rows

Uniform use of all `2^m` shifts is not needed for this obstruction. Let row `i`
have a fixed shift `beta_i` in `{0,1}^m` and a polynomial `p_i` of degree at
most `d`. Assign any nonnegative row weights `w_i` summing to one. At frequency
pattern `k` in `{0,1}^m` its predictor is

\[
 (-1)^{|\beta_i|}p_i(|k\mathbin\oplus\beta_i|),
\]

and its desired multiplier is `(-1)^|k|`. Averaging over *uniform k*, each
shifted count has distribution `Bin(m,1/2)`. Therefore some frequency has
exceptional row weight at least `(1-B_(m-1)(d))/2`. Thus a per-frequency
exception cap `epsilon` requires

\[
 \epsilon\ge\frac{1-B_{m-1}(d)}2.                                \tag{C5}
\]

This allows repeated shifts, nonuniform shift weights, different count
polynomials for different rows, and any finite row multiplicities introduced
by a full-rate linearization. It requires that the tested frequency family
actually contains every sign pattern, or that the asserted cap holds on every
pattern. In the binary query family in `kernel.tex`, every pattern is realized:
take one column, set each distinguished `X_j = 1`, choose `Z_j` to specify the
pattern, and set auxiliary coordinates to zero. For more columns keep the
additional columns zero.

### What pencil degree does and does not establish

A product of `t` matrix pencils affine in the query signs, interspersed with
query-independent row matrices, has matrix entries of total degree at most
`t`. Reduction by `q_j^2 = 1` cannot increase degree. If its final diagonal
entry for row `i` is symmetric in the shifted Boolean variables, then it is
an ordinary count polynomial of degree at most `t`: write its symmetric
multilinear representative in elementary symmetric polynomials, whose values
on bits are `binom(c,h)`, `h <= t`. This last conversion uses characteristic
zero.

Under this *final diagonal shifted-count symmetry* condition, (C5) applies
with `d = t`. Arbitrary row mixing and arbitrary full-rate batch width cannot
remove the obstruction while this condition remains true. We do **not** infer
that every matrix-pencil algorithm has diagonal count-symmetric output.
Breaking that condition is a legitimate route around this theorem.

For a single spectral correction of width `h`, suppose that at a fixed
frequency its transfer has the form

\[
  zI-P(k)=U(k)M(k)V(k),\qquad M(k)\text{ has side }h.               \tag{C6}
\]

If `P(k)` is diagonal, its rank defect equals the number of exceptional rows,
so that number is at most `h`. Combining (C5) with rank gives
`h/W >= (1-B_(m-1)(d))/2` for `W` equally weighted rows. This includes a
factorization of the final Hermite-corrected diagonal predictor and one table;
it does not identify its degree with the degree of the *initial* predictor.
All additional predictor applications must be counted. Multiple table uses
need their own rank budget, rather than silently reusing (C6).

## 3. The sharp polynomially small exception scale

We use natural logarithms in this section. The factor converting `ln m` to
`log_2 m` must be retained when comparing numerical constants.

**Lemma C2 (central binomial moderate tails).** For fixed `c > 0` and
`r_N = floor(c sqrt(N ln N))`,

\[
  1-B_N(r_N)=N^{-c^2/2+o(1)}.                                    \tag{C7}
\]

Here the `o(1)` is as `N -> infinity`, with `c` fixed. It is not a claim
uniform over arbitrarily growing `c`.

### Proof details

The `r_N` heaviest levels have half-width
`a_N = (c/2)sqrt(N ln N) + O(1)` about `N/2`. A Chernoff bound gives upper
tail `2 exp(-2(a_N-O(1))^2/N)`, proving the required upper exponent. For
completeness, this bound follows from
`E exp(t(C-N/2)) = cosh(t/2)^N <= exp(Nt^2/8)` and optimization at `t=4a/N`.

For a matching lower exponent, first take `N=2v`. Its central mass is
`Theta(N^(-1/2))`. Elementary induction suffices: writing
`a_v = binom(2v,v)/4^v`, its ratio to `a_(v-1)` is `1-1/(2v)`, which gives
`1/(2 sqrt(v)) <= a_v <= 1/sqrt(v+1)`. For
`j=O(sqrt(N ln N))`, the adjacent coefficient ratio yields

\[
 \log\frac{\Pr[C=v+j]}{\Pr[C=v]}
 =\sum_{i=1}^j\left[\log\left(1-\frac{i-1}{v}\right)
                  -\log\left(1+\frac i v\right)\right]
 =-\frac{2j^2}{N}+O(j^3/N^2+j/N).                                \tag{C8}
\]

The error tends to zero on this range. Sum a block of
`floor(sqrt(N/ln N))` levels immediately beyond the central retained interval.
Across this block the exponent in (C8) changes by `O(1)`. Its mass is at least
`(ln N)^(-1/2) exp(-2a_N^2/N+O(1))`, with constants depending on `c`.
This is `N^(-c^2/2+o(1))`. For odd `N`, convolve the adjacent even binomial
distribution with one fair bit. The centering changes by at most one and the
same estimates hold. QED.

**Theorem C3 (optimal exact count degree).** Fix `a > 0`. The least degree of
a characteristic-zero count polynomial with exceptional fraction at most
`m^(-a)` is

\[
 \boxed{\quad(1+o(1))\sqrt{2a\,m\ln m}.\quad}                     \tag{C9}
\]

For the lower bound apply (C1) and (C7). If the degree is at most
`(sqrt(2a)-eta)sqrt(m ln m)` for fixed positive `eta`, its defect is at least
`m^(-(sqrt(2a)-eta)^2/2+o(1))`, larger than `m^(-a)` eventually.

For the upper bound choose a consecutive central window of `D+1` counts with
`D = ceil((sqrt(2a)+eta)sqrt(m ln m))` and interpolate parity exactly there.
Degree is at most `D`, and the omitted binomial mass is
`m^(-(sqrt(2a)+eta)^2/2+o(1))`, below `m^(-a)` eventually. Let `eta` decrease
after taking the asymptotic bounds. This is an existence/interpolation
statement with a constructive degree-D polynomial, not a tape-time estimate.

The theorem covers the source's target exception fraction `O(m^(-3))`:
the required degree has leading scale `sqrt(6m ln m)`. Constant factors in
the exception cap change lower-order terms. The source's particular integer
window is a safe sufficient choice and is not asserted to attain this leading
constant. The conclusion also applies to mixtures of degree-bounded shifted
count predictors with a worst-frequency cap by Section 2.

## 4. A sharp prediction/repair invoice and a pivot criterion

Give degree one unit of abstract cost and give each exceptional row cost
`m^gamma`, normalized by batch size. Define the scalar invoice

\[
 I_{m,\gamma}=\inf_{p\in\mathbb C[x]}
                 \{\deg(p)+m^\gamma e_m(p)\}.                    \tag{C10}
\]

Constants have degree zero. This is a declared cost model. It does not assume
that a correction with this price can be implemented on tapes, or that one
pencil always costs exactly one recursive Fourier call.

**Theorem C4 (repair-price threshold).** For every fixed `gamma > 1/2`,

\[
 \boxed{\quad I_{m,\gamma}
       =(\sqrt{2\gamma-1}+o(1))\sqrt{m\ln m}.\quad}                \tag{C11}
\]

For `0 <= gamma <= 1/2` and `m >= 2`,

\[
                         I_{m,\gamma}=m^\gamma/2.                 \tag{C12}
\]

### Proof

For (C11), choose any fixed `b < sqrt(2gamma-1)`. A predictor of degree at
least `b sqrt(m ln m)` already incurs that much cost. At smaller degree,
(C1), monotonicity of `B`, and (C7) give repair cost at least
`m^(gamma-b^2/2+o(1))`, which dominates `sqrt(m ln m)` because its exponent
is greater than `1/2`. This proves the lower limiting coefficient.

Conversely choose `b > sqrt(2gamma-1)` and use the central interpolation
polynomial of degree `ceil(b sqrt(m ln m))`. Its repair cost is at most
`m^(gamma-b^2/2+o(1)) = o(sqrt(m ln m))`. Its degree supplies the upper
coefficient. Let `b` approach the stated threshold from either side.

For (C12), let `M` be the largest mass of `Bin(m-1,1/2)`.
The elementary central-binomial estimates above imply `M <= sqrt(2/m)`.
Since `B_(m-1)(d) <= dM`, (C1) gives

\[
 d+m^\gamma e_m(p)\ge m^\gamma/2
                  +d(1-m^\gamma M/2)\ge m^\gamma/2.
\]

The last coefficient is positive for `gamma <= 1/2`. A constant predictor
`p=1` attains the bound. QED.

At the full-conversion price `gamma=1`, even this favorable invoice costs
`(1+o(1))sqrt(m ln m)`. Hence merely weakening the requested exception cap
and trading against ordinary linear-price full conversions cannot remove the
logarithmic factor within this representation. A correction price on the
order of `sqrt(m)` would change the invoice qualitatively; so would a
predictor representation outside Section 2. Neither primitive is supplied by
this result. In particular, the cheap constant-predictor invoice in (C12)
does not build a cheap arbitrary-defect correction algorithm.

For shifted row mixtures, (C1) lower-bounds the worst-frequency defect through
averaging. Thus the lower half of (C11) also applies to that worst-frequency
invoice. Uniformly using all shifts with the central interpolant gives the
matching abstract upper half. This statement pays no tape cost for realizing
the shift family or the correction and is not an end-to-end algorithm.

## 5. Characteristic and model exclusions

* In characteristic two, `-1=1`; the target parity multiplier is constant and
  degree zero succeeds everywhere. The characteristic-zero statements fail.
* The source's Walsh ring inverts two, so this trivial characteristic-two
  counterexample is outside its allowable Walsh specializations.
* In odd characteristic the ordering/sign-variation proof is unavailable.
  No extension of (C1) to that setting is claimed. The simpler root-count
  bound (C4) genuinely fails when integer counts collide in the field: over
  `F_3`, `m=36`, the degree-two polynomial `1+c^2` agrees on binomial mass
  `17309009347/34359738368 > 1/2`, whereas the four heaviest ordinary count
  levels have total mass less than `1/2`.
* The integral source predictor is a polynomial in the query variables. In
  characteristic zero it can be rewritten using the ordinary count, but after
  positive-characteristic specialization its divided-power terms need not be
  functions of that count modulo the characteristic. For example,
  `binom(0,3)=0` and `binom(3,3)=1` have the same input residue in `F_3`.
  One cannot apply this obstruction to the tape paper's odd-characteristic
  swap repair by silently making that conversion.
* A nonsymmetric multivariate predictor, a nondiagonal row transfer, successive
  interacting repair tables, or a different recurrence may evade this scoped
  obstruction. Such a route needs its own complete cost and correctness proof.

## 6. Source and verification record

Primary source: OpenAI, *The logarithmic exponent of finite Fourier transforms*,
November 24, 2026, at `openai/math` commit
`3344da59991ed94f9ba711217b29c1d760badfa6`.

The relevant read chain is `build/repair.tex`, especially
`lem:count-predict`, `lem:matrix-root`, `lem:hermite-repair`, `thm:repair`,
and `cor:swap-repair`; `build/kernel.tex`, especially
`eq:kernel-pencil-cost` and `eq:kernel-template-saving`; and
`build/binary.tex`, `prop:binary-template`. The tape bridge read was
*The logarithmic exponent of integer multiplication on tapes*,
`build/walsh.tex`, `lem:tape-walsh`, at the same commit. Their local bytes were
checked against the pinned Git blobs:

| File | Git blob |
| --- | --- |
| Fourier `repair.tex` | `36bee65ff0264aba1c2204892a88462dc311ceaf` |
| Fourier `kernel.tex` | `beb61a0fc290887a2cf525744eba24639407a4d0` |
| Fourier `binary.tex` | `0fcb688e72b126d29ee949d44bf5990b0813a6be` |
| Tapes `walsh.tex` | `2feee7668300b7250d1d37969393647aecded073` |

Run `python3 -B research/moonshot-overhead-program/routes/C/verify_count_barrier.py`.
The script uses integer and rational arithmetic to check the telescoping
identity, exhaust all small threshold sign patterns, exhaust small exact
interpolants, and demonstrate the finite-characteristic negative controls.
Larger exact-integer binomial optimizations are diagnostic checks on the
declared lower-bound invoice; they do not prove asymptotics. No Lean build or
formal-kernel certification is claimed.

This programme contribution is the scoped extraction and exact quantitative
tradeoff above. The alternating-prefix identity, real root/sign arguments,
and binomial estimates are elementary mathematics; no claim of priority over
all literature is made. The published construction and its authors retain
their attribution. Research and verification were produced with AI assistance
for @CubeJerry.

## Open next questions

1. Can a nonsymmetric, full-rate predictor break this count-degree tradeoff
   without increasing query execution or routing costs? First discriminant:
   give a family and derive its complete per-level invoice.
2. Can exact defect repair be realized at normalized price `O(sqrt(m))` while
   retaining independent inputs, legal tape movement, and uniform linear
   space? The invoice threshold says why this question is consequential, but
   supplies no such primitive.
3. Determine the exact finite-m optimum of scalar *equality* prediction, rather
   than threshold agreement. The asymptotic scale in (C9) is already sharp;
   finite improvements alone do not establish a new multiplication envelope.
