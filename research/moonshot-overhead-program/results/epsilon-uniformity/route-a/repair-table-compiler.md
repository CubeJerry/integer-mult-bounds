# A bounded-height, on-demand compiler for the compact repair table

Status: **proved source-specific enabling result**. Exact coefficient,
generation, storage and algebraic conditioning bounds for binary Hermite
repair; no complete multiplication envelope or physical-query norm bound.

Sources: OpenAI `math` at `3344da59991ed94f9ba711217b29c1d760badfa6`, Fourier
`build/repair.tex`, `lem:hermite-repair`; concurrent S002 checkpoint
`bbfd1086b7e629375f9891998e4602270d8801cd`,
`routes/A/compact-complex-predictor.md`. S002 owns the compact predictor.
This note adds a common denominator, coefficient-height estimate and an
alternative to materializing all frequency tables.

## 1. Exact hypotheses

Let `m>=2`, `M>=2`, `0<=u<v<=m`, and `D=v-u`. There are `M` independent
rows with known binary shifts `beta_i`. Put

\[
 P(c)=(-1)^u\sum_{h=0}^D(-2)^h{c-u\choose h}.
\]

For every sign pattern `k in {0,1}^m`, let

\[
 c_i=|\beta_i\mathbin\oplus k|,\qquad
 p_i=(-1)^{|\beta_i|}P(c_i),\qquad z=(-1)^{|k|}.
\]

Suppose the known set `J=J(k)` contains all `i` with `p_i!=z` and
`j=|J|<=s<=M`. S002 supplies the out-of-window set with
`s=floor(M/(2m^3))`. Use integer-node checks

\[
 H_{a,i}=i^a,\quad 0\le a<s,\quad 1\le i\le M.
\]

## 2. Universal denominator theorem

Set `F_M=(M-1)!` and `Q_M=2F_M^4`. For every pattern and exceptional set,
all entries of the `2s` by `2s` spectral repair table have the form

\[
 a/Q_M,\qquad a\in\mathbb Z. \tag{1}
\]

The same denominator works for every subset. Numerator and denominator bit
lengths are

\[
 O\bigl(M\log_2(M+1)+(D+1)\log_2(4m)\bigr). \tag{2}
\]

An explicit safe numerator bound is

\[
 B_*=4+(6M+2)\lceil\log_2(M+1)\rceil
          +(D+1)\lceil\log_2(4m)\rceil.
\]

### Proof

For `j=0` the table is zero. Otherwise list the exceptional nodes as
`nu_1,...,nu_j`, and let `V_{a,i}=nu_i^a`, `0<=a<j`. Lagrange interpolation
gives

\[
 (V^{-1})_{i,a}=[X^a]
 \frac{\prod_{l\ne i}(X-\nu_l)}{w_i},\qquad
 w_i=\prod_{l\ne i}(\nu_i-\nu_l). \tag{3}
\]

The positive differences below `nu_i` form a subset of `{1,...,M-1}`, and
the absolute differences above it form another subset. Each product divides
`(M-1)!`; thus `w_i` divides `F_M^2`, including its sign.

For binary repair,

\[
 g(y)=(3y-y^3)/2,\quad
 g(y)-z=(y-z)^2D_z(y),\quad D_z(y)=-(y+2z)/2.
\]

Every `P(c_i)` is an integer because generalized binomial coefficients at
integer arguments are integers, including negative arguments. Therefore

\[
 K=V^{-\mathsf T}\operatorname{diag}(D_z(p_i):i\in J)V^{-1} \tag{4}
\]

has denominator dividing `2F_M^4`. Given spectral checks `b=H(PX)`, `c=HX`,
restrict them to the first `j` coordinates by `R_j` and embed an output
`j`-vector into the first `j` of `s` coordinates by `E_j`. The table returns

\[
 a=E_jKR_j(b-zc),\qquad za=zE_jKR_jb-E_jKR_jc. \tag{5}
\]

Its nonzero blocks are `K,-zK,zK,-K`, padded by zero rows and columns.
Formula (5) is exactly the Hermite repair: `V^{-1}` recovers the errors,
the diagonal gives their correction factors, and `V^{-T}` is a right
inverse of the selected transpose checks.

For heights, `|c_i-u|<=m`, `h<=D<=m` give

\[
 |{c_i-u\choose h}|\le(2m)^h,\qquad |p_i|\le(4m)^{D+1}.
\]

The sum of the absolute coefficients of the numerator polynomial in (3)
is at most `(M+1)^(j-1)`. Since `|w_i|>=1`,

\[
 |K_{a,b}|\le j(4m)^{D+1}(M+1)^{2j-2}.
\]

Combining this with `log_2 Q_M<=1+4M log_2(M+1)` proves (2) and `B_*`.
The check entries themselves have at most `M log_2(M+1)` bits.

## 3. On-demand construction

Given `k`, one fixed deterministic finite-tape program constructs (5) in
`poly(M,m)` bit operations and visited cells, with absolute polynomial
degree. It never loops over all `2^m` patterns.

1. Generate the shifts, compute all counts and parities, identify `J`, and
   evaluate the integer `p_i`. Exact binomial recurrences have polynomial
   bit length in `m`; S002's shift generation costs `M poly(m)`.
2. Compute `F_M` once. Form every product polynomial and denominator `w_i`
   in (3) by ordinary coefficient arrays.
3. Form integers
   `B_{i,a}=(F_M^2/w_i)[X^a]prod_{l!=i}(X-nu_l)`; division is exact.
4. The numerator of `K` over `Q_M` is
   `-sum_i (p_i+2z) B_{i,a}B_{i,b}`. Add the signs and zero padding.

All loop lengths and integer lengths are polynomial in `M,m` by the proved
height bound. Even schoolbook bit arithmetic proves the assertion; no
unit-cost rational arithmetic is being assumed. At most `4s^2` numerators
are stored, and one pattern's table can be erased before the next address.

A rational coefficient with numerator/denominator lengths at most `B_*`
can be rounded to `P` fractional bits by binary long division in
`O((P+B_*)B_*)` tape steps and `O(P+B_*)` space. The remainder has
`O(B_*)` bits, and each output bit requires one shift, comparison and
subtraction of that size. All coefficients at one frequency therefore
cost `poly(M,m)(P+1)` steps to prepare.

Applying a dense table uses `poly(M,m)` products and sums on
`O(P+B_*)`-bit words. With the fixed short-integer multiplier already used
in the tape paper, its pointwise cost is

\[
 \operatorname{poly}(M,m)(P+B_*)\log(2+P+B_*).
\]

Serial extraction, accumulation and merging of aligned row entries costs
another polynomial in the row count. Physical alignment and Fourier
conversion are separate charged caller operations. This is an explicit
program for the table encountered at an address, not an uncharged oracle.

## 4. Conditioning of the repair wrapper

Treat each exact query-pencil factor `C_beta-z_h I` as one operation and
each complete spectral conversion as unitary. The following estimate bounds
this wrapper, not the internal amplification of a physical implementation
of one pencil.

The check norm satisfies

\[
 \|H\|_2\le\sqrt{sM}\,M^{s-1}\le M^M.
\]

The spectral table norm is at most `2s` times its largest entry, so its
logarithmic norm is `O(M log(M+1)+D log(2m))`. In S002, the count operator
is self-adjoint with spectrum in `[0,m]`, its real roots lie in that
interval, and the leading scalar has magnitude at most two. Every
partial predictor product has norm at most `2m^D`.

Binary Hermite repair uses four predictor applications and a constant
number of check, lift, table, copy and sum maps. All intermediate and
propagated-fault gains of this abstract wrapper are consequently bounded by

\[
 \exp\!\bigl(O(M\log(M+1)+D\log(2m))\bigr). \tag{6}
\]

A direct dot-product realization of a check or table has the same order of
bound: partial sums are bounded by the absolute row sums, and retained
inputs and completed outputs add only polynomial factors in `M`. It is
unnecessary to multiply the norms of every scalar addition as if each
acted successively on the whole vector.

For `Z` frequency addresses and input norm at most `2^I`, ordinary
telescoping of coefficient perturbations and propagation of the rounding
faults using (6) give output error at most `2^(-p)` with

\[
 p+I+O\bigl(M\log(M+1)+D\log(2m)+\log(2+Z)\bigr)
\]

fractional bits in this wrapper. The constant also covers the polynomial
number of scalar operations and S002's root approximation bound. This
assumes atomic pencils and conversions are delivered at that accuracy.
Their internal precision obligations remain separate.

## 5. Consequence for the compact binary kernel ledger

For `explicit-binary-kernel.md`, `log_2 M=6z^2+4z` and
`z=O(epsilon^-2 log(2/epsilon))`. The following quantities all have bounds

\[
 2^{O(\epsilon^{-4}\log^2(2/\epsilon))}:
\]

- the number of seed rows and routing-label rows;
- the bit lengths and storage for one repair table;
- the bit work to prepare it and its coefficients per precision bit;
- the logarithm of the abstract repair gain in (6).

The number of possible sign patterns is absent because the on-demand
program does not enumerate them. This is a proved local expense bound.
It does not supply complete scheduler constants `A_j,N_j,D_j`:
interchange, physical query routing, root setup, descendants, interpretation
and the common linear-space cap still have to be assembled.

### Open next questions

1. Bound the physical query-pencil implementation and its internal gains.
2. Derive recursion thresholds from explicit arity and width, without a
   fixed-template asymptotic absorption at growing parameters.
3. Consider structured check nodes only after the dominant routing expense
   is known; smaller interpolation constants alone do not close the theorem.

Credits: @CubeJerry; the cited OpenAI manuscripts and S002 compact predictor;
classical Lagrange/Vandermonde interpolation. Derivation and checks used
OpenAI GPT-6 Astra Pro assistance. This is not a multiplication theorem.
