# A quantitative residual exponent from smaller full-rate predictors

Status: **complete written proof; independently reviewed by Routes A, B, C
and root**. The algebra, literal finite generator, source interfaces,
physical profiles and final inversion passed the recorded audits. The earlier independently admitted result is preserved
verbatim in [BASELINE-THEOREM.md](BASELINE-THEOREM.md). The stronger theorem
below is not an exact square-root endpoint and makes no practical-runtime,
formal-certification or literature-priority claim.

**Concurrent update.** S002 subsequently established a stronger third-root
envelope at848fbf1d7a5e192aa352d79b4d3e36fa06be21ee using characteristic-two
count formulas. Theorem F below remains the separate all-odd-characteristic
dyadic construction. Its MR hypothesis is not established by the different
fixed-field construction, even though S002 attains the displayed MR rate.
See [README.md](README.md) for the current programme result and review scope.

## 1. Main theorem

For input bit length `n>=1`, put

\[
 L=1+\log_2n,\qquad x=\log_2L,\qquad z=\log_2(x+16).
\]

**Theorem F.** There is one deterministic multitape Turing machine, with
a fixed finite alphabet and fixed number of one-dimensional tapes, which
computes the exact full product of two `n`-bit integers in worst-case time

\[
 \boxed{\quad
 T(n)=n\sqrt L\;
 2^{\,O\!\left(x
       \left(\frac{[\log_2(z+2)]^2}{z}\right)^{1/6}\right)}
 \quad}                                                        \tag{F}
\]

and visits `O(n)` cells. Inputs and the full `2n`-bit output occupy the
prescribed contiguous binary intervals. Correctness and the common visited
space bound hold at every length; the displayed time bound absorbs the
finite initial range. All constants are independent of `n`.

The corresponding excess exponent satisfies

\[
 \delta(n)=O\!\left(
       \frac{[\log_2(z+2)]^{1/3}}{z^{1/6}}\right).
\]

A simpler weaker consequence is `H(n)<=2^{O(x/z^(1/8))}`. The established
envelope remains larger in scale than `2^{O(x^beta)}` for every fixed
`beta<1`. It does not give `H=O(1)` or polynomial overhead in `x`.
Absolute constants and the eventual cutoff have not been numerically
evaluated. No Weak ETH premise or old five-assumption interface is used.

The improvement over the preceding [baseline](BASELINE-THEOREM.md) comes
from a different, explicitly constructed representation of the same integral
predictor. It removes one exponential layer from its sufficient data and
generation budget. This compares two proved analytical envelopes in this
programme, not observed runtimes or an unspecified residual term in the
published theorem. Concurrent S002 results and the matrix-factorization
literature are credited below.

## 2. A smaller predictor with every row occupied

The source is pinned to
[OpenAI math at 3344da59991ed94f9ba711217b29c1d760badfa6](https://github.com/openai/math/tree/3344da59991ed94f9ba711217b29c1d760badfa6).
The November Fourier `repair.tex` predicts the product of `m` commuting
involutions on an integer Hamming window `[u,v]` of width
`D=O(sqrt(m log m))`. Its unshifted integral polynomial is

\[
 P_m(X)=(-1)^u\sum_{h=0}^{D}(-2)^h[T^h](1+T)^{-u}
       \prod_{i=1}^{m}\left(1+\frac{1-X_i}{2}T\right).
                                                               \tag{A1}
\]

The [formula construction](route-c/FORMULA-FACTORIZATION-COMPRESSION.md)
and [complete transfer](route-a/formula-template-transfer.md) prove the
following replacement for the source's monomial tensor matrix:

\[
 L_m(X)^b=P_m(X)I,
 \qquad b=\text{least power of two at least }\max(2,D),           \tag{A2}
\]

where `L_m` is affine in the queries and has dyadic coefficients. Dimension,
total expanded output length, coefficient numerator bit lengths, dyadic
denominator exponents, actual generation steps and generation workspace
are all bounded by

\[
 Q_m=2^{\,2^{\,C[\log_2(m+2)]^2}}                              \tag{A3}
\]

after one absolute enlargement of `C`. The formal identity acts on **every
coordinate**. There is no uncharged encoding into a small initialized
subspace and no loss of input occupancy.

Here are the essential algebraic and quantitative steps.

1. Expand (A1) as `sum_s c_s e_s((1-X)/2)` with integer `c_s` of
   polynomial bit length. Balanced variable splitting and convolution
   produce a division-free formula of size
   `F_m=2^{O(log^2(m+2))}` whose syntactic degree is at most `D`.
   Duplicated subformulas are counted explicitly.
2. Maintain a cyclic matrix factorization of each subformula. Products
   concatenate `B_i tensor I` and `I tensor C_j`, multiplying ranks and
   adding stage lengths. Sums use the standard graded tensor sum after
   padding the shorter list with identities. For common length `d`, its
   rank is `d` times the product of the old ranks. Constants scale one
   factor and add no stage. Every cyclic product has the required scalar
   value.
3. Use the common integral ring `Z[1/2,zeta_M]`,
   `M=lcm(1,...,D)`. Gaussian-binomial cancellation is an integral
   identity, so no odd integer is inverted. The final cyclic factor
   length is `D`, and its rank obeys
   `log_2 K<=F_m log_2 max(2,D)`.
4. Pad once to length `b`, form the cyclic block matrix, and replace
   coefficients by their regular multiplication matrices on the free
   dyadic basis of the cyclotomic ring. The resulting matrix is dyadic
   and still satisfies (A2) on all rows. This also handles internal root
   orders divisible by the eventual odd characteristic.
5. Construct all arrays literally. Factor entries require copies, root
   shifts, additions and scalar scaling; product composition does not
   multiply two arbitrary affine entries. Coefficient bits, the explicit
   cyclotomic polynomial, basis matrices and dense expansion have cost
   polynomial in `m,F_m,D,K,M` and the initial coefficient height.
   This proves actual bit-generation bounds (A3), rather than inferring
   them from an algebraic existence statement.

All translated shifts use the same factor skeleton and row count, with
query sign changes and a sign on one factor. The `2^m` shifts preserve the
source's exceptional-row fraction. Power-of-two Hermite nodes have explicit
unit differences over the dyadic ring and after every odd-prime reduction.
Their tables, all frequency patterns, dense scalar maps and subsequent
basis expansions cost only a fixed power of `Q_m`.

Four applications of the predictor still cost `4b` affine-pencil stages.
The existing exceptional conversion fraction and normalized recursive-call
ratios are unchanged. The replacement applies both to the odd-characteristic
tape interchanger and the characteristic-zero Fourier/Walsh template.
All scalar-basis coordinates remain independent input rows. The original
binary layout accepts arbitrary fixed batch widths, including widths with
odd factors, through its already charged row grouping and padding.

## 3. Complete physical candidate profiles

Define

\[
 \theta_j=\frac12+\frac1{j+2},\quad
 \rho_j=\frac12+\frac1{2(j+2)},\quad
 Z_j=(j+2)^3\log_2(j+3),\qquad j\ge1.
\]

The [source parameter extraction](route-a/elementary-tower-extraction.md)
uses `p=O(j+2)`, `r_I=O(p log(p+1))` and `m_I=2^(r_I p^2)`, giving
`log m_I=O(Z_j)` and a fixed strict contraction margin. The Fourier
arity has the smaller `log m_F=O((j+2)^2 log(j+3))` bound. Equation (A2)
retains the same stage count, so both margins persist.

The [refined rational geometry](route-a/rational-geometry-height.md) has
polynomial-in-`m_I` bit heights and at most `2^{poly(m_I)}` actual generator
cost and address integer values. Its proof uses fixed-depth determinant
formulas, not an uncontrolled chain of unreduced fractions. Scalar rows and
the address radix dominate at the bound (A3). Thus the complete finite
budget can be chosen as

\[
 S_j\le E_2(CZ_j^2),\qquad E_2(t)=2^{2^t}.                     \tag{P1}
\]

It includes total description lengths, role and row counts, numerical
coefficient bit lengths, address-scaling and radix **values**, all finite
generation time and all generation workspace. Every expense is attached
to a specified finite algorithm.

The [physical compiler](route-a/compiler-invoice.md), already independently
audited for the baseline theorem, depends on those quantities through fixed
powers of `S_j`. The [new transfer proof](route-a/formula-template-transfer.md)
checks its applicability to these new matrices. Therefore one fixed binary
engine has complete candidate profiles

\[
 \begin{aligned}
 t_j(u)&\le a_j u(1+\log_2u)^{\theta_j} &&(u\ge U_j),\\
 s_j(u)&\le c_j(u+1) &&(u\ge1),\\
 a_j,c_j,g_j&\le S_j^c,\qquad
 \log_2U_j\le S_j^c+\log_2 U_{\rm abs}+O(1).                    \tag{P2}
 \end{aligned}
\]

Generation `g_j` is included in the complete run. `U_abs` is the source's
absolute prime-shape cutoff, independent of `j`.

The compiler charges sequential row scans, instruction access, scaling
pieces, successive single-control triangular rotations, parking, copies
and head returns. It preserves the actual recursive child volumes. New
matrix dimensions and coefficient heights bound logarithmic instruction
norms by `poly(S_j)`. Completed normalized transforms remain unitary, so
the source common-ancestor argument supplies precision
`poly(S_j)(1+k)`, with reused short-arithmetic scratch. The short multiplier
is an independently known primitive, not the new target multiplier assumed
recursively.

Aggregate non-volume setup is `G(S_j)(1+k)^E(S_j)`, where `G,E<=S_j^c`.
A fixed-power threshold in `S_j` absorbs it into `2^(k/4)`. Actual shape
and padding checks precede materialization; an aggregate setup microstep
clock, auxiliary cell marks and preserved operands support correct fallback
at every length. The machine needs neither the smallest analytical `c`
nor `U_abs` as advice. The gap `theta_j-rho_j` absorbs the remaining
source logarithmic factors with a polynomial-in-`j` constant.

## 4. One common-space machine and joint cost/threshold inversion

Choose a power-of-two chunk count `2c_j<R_j<=4c_j`. The proved
[rowwise chunk wrapper](route-b/linear-chunk-overhead.md) costs

\[
 R_j^2t_j(\lceil n/R_j\rceil)+O(R_jn).
\]

For `n>=N_j=max(4c_j,R_jU_j)`, its candidate workspace satisfies
`c_j(ceil(n/R_j)+1)<n/2+2c_j<=n`. The accumulator and fixed-origin
wrapper regions add `O(n)` visited cells, with a constant independent of
`j`. A complete successful attempt has coefficient
`A_j<=C a_jc_j<=S_j^c` and `log N_j<=S_j^c+O(1)`.

Enumerate `(j,k)`, with chunk count `2^k`, in the specified full
nondecreasing-sum diagonal order and reserve a schoolbook index. The
successful pair has `i_j=O((j+log S_j)^2)`. The source's actual-step
restart schedule gives

\[
 T(n)\le Cn+C2^{i_j}(t+1)                                      \tag{P3}
\]

for a successful attempt of duration `t`. Clocks, initialization, failed
attempts, generation, interpretation, cleanup and output are charged.
Fixed physical marks fence every attempt, and schoolbook guarantees
termination at every length.

Let `D_j=2^(i_j)A_j`, `d_j=log_2 D_j` and
`b_j=log_2(1+log_2 N_j)`. From (P1)–(P3), one absolute `C` gives

\[
 d_j,b_j\le 2^{C Z_j^2}.                                     \tag{P4}
\]

Both coordinates matter. The [certificate](CERTIFICATE.md) is

\[
 F(x)=\inf_{j:b_j\le x}\left(d_j+\frac{x}{j+2}\right),
 \qquad H_{\rm cert}=1+2^{F(x)},                              \tag{P5}
\]

with the explicit schoolbook alternative when the feasible set is empty.
It is a sufficient upper certificate, not a runtime equality.

For sufficiently large attainable `x`, choose for analysis

\[
 j=\left\lfloor c_0
       \left(\frac{z}{[\log_2(z+2)]^2}\right)^{1/6}
       \right\rfloor.                                       \tag{P6}
\]

Here `c_0>0` is a sufficiently small fixed constant. The unrounded value
tends to infinity, so the integer is eventually at least half that value.
Since `log(j+3)=O(log(z+2))`, choosing `c_0` small enough makes
`C Z_j^2<=z/2` eventually. Consequently

\[
 d_j,b_j\le2^{z/2}=\sqrt{x+16}\le2\sqrt x.
\]

Thus `b_j<=x` eventually and the chosen candidate actually applies. From
(P5)–(P6),

\[
 F(x)\le2\sqrt x+\frac{x}{j+2}
 =O\!\left(x\left(\frac{[\log_2(z+2)]^2}{z}\right)^{1/6}\right).
\]

This proves (F). The weaker form follows from
`[log_2(z+2)]^(1/3)=O(z^(1/24))`. The optimizing `j` is not advice
or an uncharged selector; it analyzes the single fixed scheduled machine. ∎

## 5. Stronger targets and scoped obstructions

The [MR theorem](route-a/single-exponential-root-hypothesis.md) remains
**conditional**. A generator with `exp(m^C)` cost and full-rate dimension,
for one fixed `C`, would yield the better profile `S_j<=E_2(CZ_j)` and

\[
 H\le2^{O(x(\log_2(z+2)/z)^{1/3})}.
\]

The present construction proves only `exp(exp(O(log^2 m)))`, so it does
not establish MR. Concurrent S002's more general IP bridge reaches the
same conditional scale. The complete [bounded-preflight transfer](route-b/preflight-selection.md)
to `H=O(x^a)`, including the endpoint `a=0`, has separate stronger family
hypotheses that also remain open.

The [window theorem](route-c/WINDOW-PREDICTOR-DEPTH.md) proves that this
exact predictor cannot use fewer affine-query stages than its window width.
Rebalancing the same all-shift, window-marked full-conversion protocol has
resource optimum `Theta(sqrt(m log m))`. This is compatible with (F): the
new representation reduces rows and preparation, not the source depth.
A runtime lower bound would require additional stage-cost premises.

S002's formal sum-of-products obstruction does not cover the nested cyclic
factorization used here. The [count-residue](INTERCHANGE-OBSTRUCTION.md)
and [literal p-adic transfer](PADIC-LIFT-OBSTRUCTION.md) obstructions rule
out other specified shortcuts; the new dyadic multivariate identity retains
individual-query information and does not lift that transfer matrix.
None of these results lower-bounds arbitrary integer-multiplication machines.

The [matching recipe obstruction](route-c/FORMULA-RECIPE-LOWER-BOUND.md)
further proves that the literal unreduced syntactically multilinear formula
composition already requires `2^{2^{Omega(log²m)}}` rows at this window.
It uses the published homogeneous-formula lower bound and a reduction
counting only degree-at-least-two additions. Nonmultilinear cancellation,
Boolean-quotient methods and smaller invariant summands remain open.
The [general formula-size transfer](FORMULA-SIZE-TRANSFER.md) states the
quantitative improvement that other degree-preserving formula families
would imply, with coefficient and actual generator costs included.

The most direct remaining quantitative target is a smaller degree-preserving
full-rate representation with an actual `exp(poly(m))` constructor. For the
exact endpoint, further progress is needed on local call mass, repair,
physical costs and applicability thresholds; representation size alone
does not settle those issues. See [DEPENDENCIES.md](DEPENDENCIES.md).

## Review, verification and credit

The universal proof is mathematical: an explicit finite constructor,
source-level cost transfer, all-length safety and a single fixed schedule.
Finite exact checks support local identities and failure controls. No
complete astronomical multiplier execution, Lean proof of this refinement,
independent human referee report or practical crossover measurement is
claimed. Review receipts and their precise scopes are in
[REVIEWS.md](REVIEWS.md); the external primary-source audit is
[LITERATURE-AUDIT.md](LITERATURE-AUDIT.md).

Credits: @CubeJerry; the pinned OpenAI November and September constructions
and their predecessors; Sheng–Tribone and Bläser–Eisenbud–Schreyer for the
matrix-factorization methods; the retained moonshot programme and concurrent
S002 parameter, rational-height, conditional-bridge and independent formula
results at58c754b583815e4fe40d333ec9d71e4c254749ba; and the
separate E001 construction and review agents. Developed with substantial
OpenAI GPT-6 Astra Pro assistance. No broad priority claim is made.
