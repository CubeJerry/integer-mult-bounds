# Explicit binary kernel parameters after compact prediction

Status: **proved source-specific finite-template estimate**, conditional only on
the algebraic identities of the pinned Fourier construction and the compact
predictor proposition identified below. This is not an integer-multiplication
time bound and not a full fixed-tape compilation.

## Sources and contribution boundary

- OpenAI `math`, commit `3344da59991ed94f9ba711217b29c1d760badfa6`,
  `preprints/The-logarithmic-exponent-of-finite-Fourier-transforms-November-24-2026/build/kernel.tex`:
  the label construction, endpoint Fourier transforms,
  `eq:kernel-pencil-cost`, and `eq:kernel-template-saving`.
- The same source, `build/repair.tex`, `lem:hermite-repair`.
- Concurrent programme checkpoint `bbfd1086b7e629375f9891998e4602270d8801cd`,
  `research/moonshot-overhead-program/routes/A/compact-complex-predictor.md`:
  translated bounded-independence shifts and real-root count prediction.

The compact predictor was discovered in the concurrent S002 session. The
present contribution supplies explicit routing choices, a proved strict
margin, and a quantitative width bound for that predictor inside the published
binary kernel. An initially explored Newton/Clifford factorization in this
session was superseded by S002's real factorization; it is not claimed as a new
advance. No literature-priority claim is made.

Throughout, logarithms with subscript 2 are binary. The letter `M` below denotes
the number of predictor rows, not the source's tensor arity.

## 1. The finite-template theorem

Let `0 < epsilon <= 1/2`, and set

\[
 t=\lceil4/\epsilon\rceil,\qquad
 r=\lceil16t\log_2(16t)\rceil,\qquad z=tr,\qquad
 q=2^r,\qquad m=q^t-1=2^z-1.
\]

Use the binary (`ell=2`) kernel label set of length `L=2t` and alphabet
size `q`. Let `g` be the rank of its Gram matrix over `F_2`, and put

\[
 A=2(m+g-1).
\]

Use S002's shifts with

\[
 r_s=\lceil\log_2(4m^3)\rceil=3z+2,\qquad
 d_s=\lceil\log_2m\rceil=z,\qquad
 M=(2^{d_s})^{2r_s}=2^{6z^2+4z}.
\]

Then the resulting characteristic-zero binary template has

\[
 W=Mq^{2t}=2^{6z^2+6z}
\]

independent input rows, and a finite number `sigma` of one-axis calls satisfying

\[
 2m\le A\le4m,\qquad
 \frac{\sigma}{W}\le\frac14 A^{1/2+\epsilon}.
 \tag{1}
\]

The rows are full independent arrays. No copied or zero work row is counted
among the `W` independent inputs. Normalized calls give the normalized
Walsh transform, with real algebraic pointwise coefficients. The finite
coefficient list is not asserted to be dyadic.

In particular,

\[
 \log_2 A=O(\epsilon^{-2}\log(2/\epsilon)),\qquad
 \log_2 W=O(\epsilon^{-4}\log^2(2/\epsilon)),
 \tag{2}
\]

with absolute implied constants. The estimates include routing labels and
bounded-independence shifts, and require no generalized Clifford enlargement.

### 1.1 Rank and rectangle counts

For `ell=2`, the source matrix is

\[
 \Gamma(v,w)=1-\Delta(v,w)=1-L+\sum_{i=1}^L E_i(v,w)
 \quad\text{over }\mathbb F_2,
\]

where `E_i` tests equality in coordinate `i`. Each `E_i` has rank at most `q`,
and the constant matrix has rank at most one. Therefore

\[
 g\le1+Lq=1+2tq. \tag{3}
\]

The charged rectangle decomposition expands the polynomial of degree `t` in
the source's binomial basis. There are at most

\[
 \sum_{h=0}^t {2t\choose h}q^h\le2^{2t}q^t
\]

charged rectangles. At each fixed source or destination label, a free rectangle
is determined, in every coordinate, by either equality or the first differing
binary bit of the other letter. There are at most `1+r` choices. The total
number of free incidences on either side is consequently at most
`(1+r)^(2t)` per label. Restricting to odd distances only reduces this count.

For one pencil, every free incidence uses at most `2g` one-axis calls at its
endpoint. Summing both sides contributes at most `4g(1+r)^(2t)` calls per
input row. A charged rectangle uses at most `2g` calls at each query, and there
are `m` queries. Dividing by the number `q^(2t)` of labels gives at most
`2g m 2^(2t) q^(-t)`. Since `m<q^t` and `(1+r)^(2t)>=2^(2t)`,

\[
 C_{\rm pencil}\le
 4g(1+r)^{2t}+2g m2^{2t}q^{-t}
 \le6g(1+r)^{2t}. \tag{4}
\]

These are counts of calls, not estimates of non-call tape work. In particular,
the row matrices and address reindexings are still charged separately.

### 1.2 Predictor and repair calls

S002 uses `r_s=ceil(log_2(4m^3))` and a window of width

\[
 D\le2\lceil\sqrt{r_sm}\rceil+1.
\]

Its predictor has `D` pencil stages. Binary Hermite repair uses four predictor
applications. Because `r_s<=3z+3`, the number of pencil stages is at most

\[
 4D\le8\sqrt{(3z+3)m}+12\le64\sqrt{m(z+1)}. \tag{5}
\]

The last inequality is deliberately generous and holds for every `m>=1`.
The spectral table uses at most `4s` full conversions, where
`s=floor(M/(2m^3))`. A full conversion, forward or inverse, uses `A` axis
calls. Thus the repair conversions contribute at most `2A/m^3` calls per row.

Combining (3)--(5), using `g<=3tq`, gives

\[
 \frac{\sigma}{W}
 \le1152tq\sqrt{m(z+1)}(1+r)^{2t}+\frac{2A}{m^3}. \tag{6}
\]

### 1.3 Strict slack with integer parameters

Since `t>=8` and `q>=2`,
`1+2tq <= q^t-1=m`; for example the inequality holds at `q=2,t=8`, and
both successive increases in `q` and in `t` preserve it. One may also use
`q^(t-1)>=2^(t-1)>=2t+1` for `t>=8` directly. Equation (3) gives
`2m<=A<=4m`.

Write the first summand of (6) as `P`. As `m>=q^t/2`, `epsilon<=1/2`, and
`t epsilon-1>=3`,

\[
 \frac{P}{A^{1/2+\epsilon}}
 \le2304t\sqrt{z+1}(1+r)^{2t}2^{-3r}.
\]

For `t>=8`, the chosen integer `r` satisfies

\[
 1+r\le(16t)^2,\qquad z+1\le2t(1+r).
\]

The binary logarithm of the prefactor
`2304t sqrt(z+1)(1+r)^(2t)` is at most
`6t log_2(16t)`. Indeed it is at most
`12.5+1.5 log_2 t+(2t+1/2)log_2(1+r)`, and the displayed bounds make this
smaller than `6t log_2(16t)` for `t>=8`.
Meanwhile `3r>=48t log_2(16t)`. Hence

\[
 P/A^{1/2+\epsilon}\le2^{-42t\log_2(16t)}<1/8.
\]

For the second summand, use `A<=4m` and
`1/2+epsilon>=1/2`:

\[
 \frac{2A/m^3}{A^{1/2+\epsilon}}
 \le\frac{4}{m^{5/2}}<1/8,
\]

since our `m` is far larger than 4. This proves (1). All choices are integer
choices and the margin is uniform in `epsilon` on its stated domain.

### 1.4 Width and normalization

Here `z=tr>=3`, so
`2^(3z+1)<4(2^z-1)^3<2^(3z+2)`. Consequently `r_s=3z+2` exactly.
The seed field has size `2^z=m+1`, and the label set has size
`q^(2t)=2^(2z)`. This proves the formula for `W`.

Each row carries an independent input, even if two seeds give the same shift.
Real factorization acts on that row alone through an affine pencil. The
kernel routing is the published identity on the label index, so all `Mq^(2t)`
rows remain independent. Working rows needed for checks, copies, sums and
repair are additional work rows and do not increase the claimed input count.

Normalization uses the same calculation as `build/binary.tex`: the `2g`
axis calls implementing a query kernel provide the common factor
`2^(-gf)`, and two partial transforms at a free rectangle use those same
axes. Full spectral conversions have inverse normalization cancellation.
The scalar count factors and rational check matrices are independent of
the axis width `f`. Therefore all remaining coefficients form a fixed
finite real algebraic set at fixed `epsilon`. S002's root isolation is
effective; this is not an infinite-template machine.

## 2. What this does and does not settle

The estimate replaces the qualitative choices of `L`, `q` and `m` in the
binary kernel by explicit formulas, and makes the full independent-row width
quantitative after the S002 improvement. It also gives a strict quarter-margin
instead of an unspecified eventual strict inequality.

The gate-call recurrence is now quantitatively meaningful. It does not price
all numerical pointwise work, physical address movement, interpretation or
the common-space schedule. The separate repair-table note bounds a major
part of the numerical and generation expenses. Interchange still uses a
finite-characteristic construction to which this count factorization does
not apply. There is no new complete overhead envelope `H(n)` here.

### Open next questions

1. Combine the explicit template with the dynamically generated repair tables
   and prove one uniform bound for the complete pointwise and address caller.
2. Quantify the separate finite-characteristic interchange template, including
   its data alphabet, compatible radix and literal program generation.
3. Decide whether the interchange implementation can use an independent
   architecture whose constants do not dominate (2).

Credits: @CubeJerry; OpenAI's November 24, 2026 Fourier and tape manuscripts and
their cited predecessors; concurrent S002 compact prediction. Quantitative
derivation and checking in this directory used OpenAI GPT-6 Astra Pro.
