# Proposed source-wide elementary-height extraction

Status: **draft mathematical extraction awaiting adversarial review**. The
local finite-template bounds below are being assembled into a complete
fixed-tape certificate. Do not promote the final envelope to the programme's
proved bound until the compiler and threshold sections have been reviewed.

This deliberately weak rate uses the *original* integral predictor and
Clifford construction in both branches. It does not require the changed
real-algebraic predictor. The compact S002 work remains a separate route
towards better constants and stronger rates.

## 1. Source pins and notation

All OpenAI sources are at `3344da59991ed94f9ba711217b29c1d760badfa6`:

- November tape `interchange.tex`, `permutations.tex`, `walsh.tex`,
  `integers.tex`, `uniformity.tex`;
- November Fourier `repair.tex`, `kernel.tex`, `binary.tex`;
- September tape `build/sections/02-streams.tex` and `04-swap.tex`, for
  explicit affine stream operations, triangular factorization, parking and
  radix padding.

The explicit label estimates are also independently extracted in concurrent
S002 `routes/A/interchange-label-growth.md`; use that proof with credit.
S002 `routes/A/parameter-thresholds.md` supplies useful absorption inequalities.
This note addresses the scalar program, radix and compilation expenses left
open by those local estimates.

Define `E_1(t)=2^t`, `E_2(t)=2^(2^t)`, `E_3(t)=2^(2^(2^t))`.
All constants below are absolute; none may depend on the requested exponent
index. Put `theta_j=1/2+1/(j+2)` and choose the intermediate exponent
`rho_j=1/2+1/(2(j+2))`. It is enough to show that complete interpreted
attempts can be chosen with

\[
 \log_2 D_j\le E_2(C(j+2)^3\log_2(j+3)),\qquad
 \log_2(1+\log_2 N_j)\le E_2(C(j+2)^3\log_2(j+3)). \tag{T}
\]

The terminal optimization in Section 5 is conditional on the successful
completion of Sections 2--4; it is not a substitute for them.

## 2. Finite interchange templates have elementary-height descriptions

Write `epsilon=rho-1/2`, `0<epsilon<=1/2`. Choose a prime
`12/epsilon<=p=O(1/epsilon)` using Bertrand's postulate and trial division.
Set `h=2p-1`. For an integer `r>=1`, put

\[
 q=2^r,\quad m=q^{p^2},\quad N=q^{h^2},\quad
 C_r=(1+h^{p-1})^{p+1}.
\]

The source/S002 estimates give

\[
 r_*/N\le C_rq^{-p^2},\quad
 D\le2+hq^h,\quad
 \lambda\le {h\choose p}^{p+1}(q-1)^p r^{p(p-1)}. \tag{I1}
\]

Thus `m r_*/N<=C_r`. A pencil needs at most an absolute constant times
`D(1+lambda)(1+C_r)` smaller calls per input row. The constant is absolute
in this call metric: every general conversion uses at most its number of
coordinate fields minus one exchanges, and endpoint preparation consists
of a bounded number of such conversions. This does not yet bound scans.

Original binary repair takes `O(sqrt(m log m))` pencils. From (I1), the main
call count per row is at most

\[
 \sqrt m\,2^{O(p^2\log(p+1))}
       q^{3p-1}r^{p(p-1)}\sqrt{1+p^2r}+2/m^2. \tag{I2}
\]

Take `gamma=1/2+epsilon/2`. Since
`(epsilon/2)p^2-(3p-1)>=3p`, choosing
`r=C_0 p log_2(p+1)` with a sufficiently large absolute `C_0` makes (I2)
at most `m^gamma`. The `p^2 log r` term and the fixed-prime coefficients
are both absorbed by the available `3pr` margin. Also
`2(D-2)<=2h q^h` and `rho p^2-h>=p^2/3` for `p>=24`, so

\[
 2m^\gamma+2(D-2)\le\tfrac12 m^\rho \tag{I3}
\]

after increasing `C_0`. These bounds are uniform in `p`.

An algorithm need not know the smallest sufficient `C_0`: double `r` and
construct the finite template until the actual rational-power call and
reserve inequalities have the margin (I3). All comparisons are decided by
integer powers. The argument proves that the first successful `r` is at
most `C_1 p log(p+1)` for an absolute `C_1`, even if earlier trials are
retained in the generation budget. Therefore, with

\[
 Z=1+p^3\log_2(p+1),
\]

we have `log_2 m=O(Z)` and `N<=m^4`.

### 2.1 The literal scalar predictor

Let `d=O(sqrt(m log m))` be the source central-window degree, and let `b_0`
be the least power of two at least `max(2,d)`. In the binary integral
construction, each factor `(1+T)^(b_i)` is `1+b_i T`, where
`b_i=(1-sign_i Q_i)/2`. Expanding and collecting the predictor gives a
multilinear query polynomial of degree at most `d`, with at most

\[
 H\le\sum_{a=0}^{\min(d,m)}{m\choose a}\le(m+1)^{d+1}
\]

monomials. Coefficient numerator/denominator bit lengths are
`O(d log(m+1))`. One can pad every list to the displayed upper bound by
zero terms; this is wasteful but completely explicit.

The matrix-root construction has dimension `b_0^H`. Taking every binary
shift makes the raw row count

\[
 R_0=2^m b_0^H.
\]

Consequently

\[
 \log_2 H=O(\sqrt m\log^{3/2}(m+1))\le E_1(O(Z)),\quad
 R_0\le E_3(O(Z)). \tag{I4}
\]

No efficient linearization hypothesis is being imposed: (I4) prices the
literal tensor-product matrix in the manuscript.

### 2.2 Avoiding an additional alphabet tower

The source cyclotomic extension has power-of-two order at most `2R_0`,
and basis rank at most `R_0`. In odd characteristic it is represented as
`F_p[Y]/(Y^d+1)` with `d<=R_0`. For a root `eta`, every needed inverse
of `1-eta^a` can be written as one half of a geometric sum, because a
suitable power of `eta^a` is `-1`. Thus the Vandermonde inverses, repair
tables and matrix-root coefficients can be generated by polynomially many
operations in arrays of length at most `R_0`, over `F_p`.

Use the basis expansion explicitly authorized by `cor:swap-repair`:
each extension-valued row becomes `d` independent `F_p` rows, and each
scalar multiplication becomes a base-field matrix. Row count and call
count are both multiplied by `d`, preserving (I3). The data alphabet can
therefore remain `F_p`, encoded in `O(log p)` binary bits. There is no
need to list every element or every pair of elements of the extension
as one physical alphabet. Such a literal alphabet lookup would create
an avoidable extra exponential.

There are at most `2^m<=R_0` sign patterns. Even explicitly generating all
their dense spectral tables costs only a fixed polynomial in `R_0,m`:
the extension rank, matrix dimensions, number of polynomial factors and
number of patterns are each bounded by a polynomial in those quantities.
All base-field entries have `O(log p)` bits. This part of the complete
finite description and its generation thus obeys `E_3(O(Z))`.

### 2.3 Address constants and compatible radix

The rational address geometry uses only the `N<=m^4` labels, not the
enlarged scalar row count. It is generated from rational Gram matrices
of polynomial dimension in `m`, with original entries of polynomial
height. Exact elimination, complements and lower-triangular
factorizations require a polynomial number of rational operations.
Even the crude recurrence that doubles bit length at every operation
bounds the resulting heights by `2^(poly(m))`. Hence the absolute
values of all relevant integer numerators and denominators, and their
finite product `B`, are bounded by `E_3(O(Z))`.

Choose a prime radix `b>max(W,B,2)`, where `W` is the expanded batch
width. Bertrand's postulate bounds one such radix by twice this maximum;
trial division finds it in polynomial time in its *value*. This expense
is still `E_3(O(Z))`. It avoids every bad numerator and denominator,
and the source's binary-to-radix padding costs a factor less than `b^2`,
also of the same elementary height.

Thus one computably generated bound `S>=2` of size

\[
 S\le E_3(CZ) \tag{I5}
\]

can cover all finite list lengths, the number of scalar rows and passes,
the radix value, absolute address-scaling integers, numerical coefficient
bit lengths, literal source generation work, and the number of potential
simultaneously live roles. Choosing a larger fixed power of `S` does not
alter the tower height.

## 3. The original binary Fourier template fits the same budget

The binary label estimate in `explicit-binary-kernel.md` also works with
the original predictor: its `4b_0` stages satisfy the same generous
`64 sqrt(m(log_2 m+1))` bound used there. The chosen arity has
`log m=O(epsilon^-2 log(2/epsilon))`, with a uniform strict call margin.
Use all `2^m` shifts and the original matrix-root construction. Section 2.1
then bounds its raw rows and extension rank by
`E_3(O(epsilon^-2 log(2/epsilon)))`.

Over characteristic zero, represent the cyclotomic ring in its monomial
basis and descend to the dyadic ring as in `kernel.tex` and `binary.tex`.
The inverse of a difference of root-of-unity nodes is a signed monomial
times one half of a geometric sum. Products of at most the row count of
these expressions, and the ensuing dense matrices, have coefficient bit
lengths polynomial in the raw row count and `m`. Their construction costs
a fixed polynomial in those dimensions and lengths. Thus the whole
dyadic list fits (I5); interchange's `epsilon^-3 log(2/epsilon)` scale
dominates this branch.

Normalization is the source's even-width normalized binary construction.
An odd selected width adds the fixed `1/sqrt(2)` butterfly. This weak
extraction needs no changed high-degree algebraic-coefficient premise.

## 4. Compiler and threshold claim requiring independent audit

**Compiler claim.** Let `S` cover the quantities after (I5), Section 3's
binary data, and the successful generators' costs. There is an absolute
integer `c` such that the complete candidate for `theta_j` has a common
finite tape count and alphabet, and

\[
 \begin{aligned}
 T_j(u)&\le S^c u(1+\log_2u)^{\theta_j}
       &&(\log_2u\ge S^c,\ u\ge U_0),\\
 \operatorname{space}_j(u)&\le S^c(u+1)&& (u\ge1),\\
 \operatorname{generation}_j&\le S^c.
 \end{aligned} \tag{C1}
\]

Here `U_0` is the absolute source prime-shape threshold, independent of
`j`; shapes are tested, with schoolbook fallback. The exponent `c` may
be enlarged finitely many times, but must remain absolute.

### 4.1 Finite control and physical streams

Use `uniformity.tex`'s serialization, not a cross-product transition table
for all logical tapes or extension elements. A fixed interpreter scans a
finite list of row indices, coordinate maps and constants. Its loops and
data are binary. A candidate is the fixed engine plus code printing its
finite tables. Printing, scanning and interpreting `poly(S)` bits take
`poly(S)` time per instruction, not an exponential in `S`.

The source instructions admit the following explicit implementations.

- A digit split uses at most `b^2<=S^2` logical streams. Serial extraction
  and merging cost `poly(S)` times the volume. A pointwise map uses at
  most `S` rows and `S`-bit coefficients. After basis expansion, scalar
  data use `F_p`, whose elementary tables are polynomial in `p<=S`.
- September's elementary-stream proof uses ordinary binary arithmetic
  on a fixed number of collapsed lengths, with absolute polynomial
  degree. A list of at most `S` coordinates is an outer loop, not a
  new exponent in the input length.
- An address scaling by an integer `a` uses `|a|` monotone pieces.
  Those absolute values were included in `S`. Inverse scaling reverses
  the split/merge. Controlled offsets have absolute polynomial degree
  in field width and `poly(S)` coefficients; the complete `b^f` fibre
  absorbs that polynomial with a `poly(S)` factor, as in the source.
- General coordinate maps factor into at most their dimension minus
  one exchanges and polynomially many lower-triangular updates. The
  exchanges receive their original volume. Additional scans, parking
  and restoration belong to the parent, preserving call coefficients.
- Full-volume reserve descents retain only descriptors. Main descents
  shrink volume by the source factor below one, so parked arrays sum
  geometrically. End-access stacks avoid scans through ancestors.

The interpreter slowdown is paid once per instruction. Descendants use
the same loop, not recursively nested universal interpreters. The strict
margins in (I3) and the binary template sum the volume recurrences with
absolute geometric constants.

### 4.2 Setup and numerical widths

After a harmless power enlargement of `S`, there are at most `S` calls
per node and depth `O(log(2+k))`, where `k` is the top address width.
Instruction enumeration, descriptors, root/phase preparation and short
shape tests are bounded by

\[
 S^c(1+k)^{S^c}. \tag{C2}
\]

The per-node arithmetic degree is absolute; the large exponent also
covers every descendant and piece. Row-padding exponent `log_A W<=S`
fits the same estimate.

Original dyadic coefficients have at most `S` bits; a node has at most
`S` instructions and roles. The logarithm of its product norm is
`poly(S)`. The common-ancestor error argument multiplies this by
`O(log(2+k))`; counting faults adds another polynomial term. Digit and
unitary boundary norms have fixed exponents in `k`. Therefore signed
and fractional widths `S^c(1+k)` suffice, including final exact rounding.
This bounds coefficient bit lengths; magnitudes are not enumerated.

The phase routines have absolute polynomial degree in precision and `k`;
the short orders are fixed powers of `k`. The fixed short-integer
multiplier costs `O(P log(2+P))` on `P` bits. Substituting
`P<=S^c(1+k)` adds only `poly(S)` to the volume constant. This primitive
is the independently known multiplier cited by the source, not the new
near-root algorithm being constructed.

For `E,H<=S^c` and `k>=64(E+H+1)^2`,
`2^H(1+k)^E<=2^(k/4)`, using `log_2(1+k)<=sqrt(k)` for `k>=32`.
Enlarging `c` therefore makes `k>=S^c` absorb (C2), finite coefficient
storage and row padding into full-stream volume. Below that preflight
threshold, use schoolbook after generation. Its `poly(S)` retained
generation storage is still within `S^c(u+1)`.

The visible non-setup integer time is
`poly(S)u(1+log u)^rho(1+log(2+log u))^4`: controlled-block permutations
have a third power and the layer count adds one. The slack
`theta_j-rho_j=1/(2(j+2))` absorbs that fourth power with prefactor
`O((j+2)^4)<=poly(S)`. This establishes the form of (C1) if the finite
control audit above is admitted.

### 4.3 Chunking and the weighted certificate

Choose a power of two `r_j` between `4S^c` and `8S^c`. For sufficiently
large `n`, a chunk has `u=ceil(n/r_j)` above the fast threshold and its
complete interpreted run fits the fixed `O(n)` cap. Gathering,
`r_j^2` products, cleanup, shifted additions and output cost another
fixed power of `S` times `n(1+log n)^theta_j`. A sufficient threshold has

\[
 \log_2N_j\le S^{c'}+O(\log S)+\log_2U_0.
\]

In standard diagonal order on `(j,log_2 r_j)`, its index is at most
`O((j+log S)^2)`. The source rounds yield `D_j=2^(i_j)S^(c')`. As
`S<=E_3(C(j+2)^3 log_2(j+3))`, taking logarithms gives (T), with an
enlarged absolute constant. Candidate generation, encoding, interpretation
and operand chunking have all entered either this constant or threshold.

## 5. Envelope if the complete audit admits (C1)

Let `x=log_2(1+log_2 n)` and, for large `x`, put
`y=log_2 log_2(x+16)`. Choose

\[
 j=\left\lfloor c_0\left(\frac{y}{\log_2(y+2)}\right)^{1/3}\right\rfloor
\]

for a sufficiently small fixed `c_0>0`. Then
`C(j+2)^3 log_2(j+3)<=y/2` eventually, so both right sides in (T)
are at most `2^(sqrt(log_2(x+16)))<=sqrt(x)`. The candidate is feasible,
and the certificate satisfies

\[
 \log_2H_{\rm cert}(n)
 =O\!\left(x\left(\frac{\log_2(y+2)}{y}\right)^{1/3}\right). \tag{E}
\]

A simpler weaker form is
`H_cert(n)<=2^(O(x/(log_2 log_2 x)^(1/4)))`. These are subpowers of
`L=1+log_2 n`. The choice of `j` analyzes the weighted schedule; the
machine does not receive a free selection oracle.

## Review gates and scope

The local label counts, literal matrix-root dimensions and finite-basis
representation are explicit source-specific bounds. Admitting the global
claim requires the compiler audit in Section 4: every `poly(S)` factor,
especially role serialization, control words, code generation and the
all-length space fallback, must be checked. If a step requires another
exponential, change the tower height and final rate; do not bury it in an
unspecified fixed-parameter constant.

This would quantify the published mechanism. It does not prove bounded
overhead or a multiplication lower bound, and is not claimed to beat the
actual runtime of the published machine or a later comparable explicit
bound. Exact `O(n sqrt L)` remains open.

Credits: @CubeJerry; the cited OpenAI manuscripts and predecessors;
concurrent S002 label and threshold extraction. This proposed synthesis
was developed with OpenAI GPT-6 Astra Pro assistance.
