# Parameter ledger for the complete elementary-height bound

Status: **proved analytical bounds for the specified source implementation**.
The construction and compiler proofs are
[`route-a/elementary-tower-extraction.md`](route-a/elementary-tower-extraction.md)
and [`route-a/compiler-invoice.md`](route-a/compiler-invoice.md); the independent
audit is [`route-c/ELEMENTARY-TOWER-REVIEW.md`](route-c/ELEMENTARY-TOWER-REVIEW.md).
The absolute constants below have not been evaluated numerically. This ledger
does not give a practical crossover length or a numeric implementation budget.

Concurrent S002 independently completed an accepted elementary extraction at
commit `96028cba1342c02bdca1f537ae9a80485087bdf3`, with sufficient arity estimate
`log m=O(j^6)` and envelope `H<=2^{O(x/(log log x)^(1/6))}`. The present
extraction sharpens the arity estimate to `O(j^3 log j)` and carries it through
the complete ledger. The proofs have separate provenance; no priority claim
is made.

## 1. Notation and source locations

All logarithms below have base two. Define

\[
 E_1(z)=2^z,\quad E_2(z)=2^{2^z},\quad E_3(z)=2^{2^{2^z}},\qquad
 Z_j=(j+2)^3\log_2(j+3),\quad j\ge1.
\]

Every `O`, fixed polynomial, and constant `C,c` is uniform in `j`. Increasing
an absolute constant does not change the tower height. The bounds describe
specified efficient generators and a specified diagonal ordering. They do
not cover every computable generator or every enumeration of the templates.

All OpenAI manuscript references are pinned to
[`3344da59991ed94f9ba711217b29c1d760badfa6`](https://github.com/openai/math/tree/3344da59991ed94f9ba711217b29c1d760badfa6).
The following keys identify their precise locations.

| Key | Pinned manuscript and relevant location |
|---|---|
| `T/interchange` | `preprints/The-logarithmic-exponent-of-integer-multiplication-on-tapes-November-24-2026/build/interchange.tex`; `lem:interchange-labels`, `eq:interchange-stage-cost`, `subsec:swap-spectrum`, `eq:interchange-contraction`, recursion subsection. |
| `T/permutations` | Same tape build, `permutations.tex`; `lem:packed-xor`, `cor:bit-positions`, `lem:controlled-blocks`. |
| `T/walsh` | Same tape build, `walsh.tex`; `lem:tape-walsh`, batch, recursive-call, work/space, precision paragraphs. |
| `T/integers` | Same tape build, `integers.tex`; `eq:integer-box`, `lem:synchronized-short`, coefficient streaming, precision, recovery, time/visited-cell paragraphs. |
| `T/uniformity` | Same tape build, `uniformity.tex`; `sec:single-machine`, template generation, precision certification, common tapes, linear-space scheduling. |
| `F/repair` | `preprints/The-logarithmic-exponent-of-finite-Fourier-transforms-November-24-2026/build/repair.tex`; `lem:count-predict`, `lem:matrix-root`, `lem:hermite-repair`, `cor:swap-repair`. |
| `F/kernel,binary` | Same Fourier build, `kernel.tex` and `binary.tex`; `eq:kernel-pencil-cost`, `eq:kernel-template-saving`, `prop:binary-template`. |
| `Old/streams,swap` | `preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/02-streams.tex` and `04-swap.tex`; elementary/ordered-affine stream lemmas, triangular factorization, radix padding, fixed-tape parking. |

To avoid overloaded symbols, `r_I` is the interchange label parameter,
`R_j` the operand chunk count, `b_rad` the address radix, `b_j` the
certificate threshold, and `D_G` the rational Gram dimension. `D_j` is a
scheduler-weighted time constant. Word precision is `P`; characteristic is `p`.

## 2. Interchange parameters and the improved arity estimate

| Parameter | Choice or bound as a function of `j` | Meaning and provenance |
|---|---|---|
| `theta_j` | `1/2+1/(j+2)` | Final candidate exponent; `T/uniformity`. |
| `rho_j` | `1/2+1/(2(j+2))` | Intermediate exponent; leaves `eta_j=theta_j-rho_j=1/(2(j+2))`. |
| `epsilon_j` | `rho_j-1/2=1/(2(j+2))` | Finite-template saving parameter. |
| `p` | Least prime at least `12/epsilon_j=24(j+2)`; `p=O(j+2)` | Odd characteristic. Trial division and Bertrand's postulate specify an efficient choice. |
| `h` | `2p-1` | Nested label length; `lem:interchange-labels`. |
| `r_I` | First successful doubled integer; `O(p log(p+1))` | Generator checks actual strict call/reserve inequalities by integer powers. |
| `q` | `2^(r_I)` | Binary inner alphabet size. |
| `m_I` | `q^(p^2)`; `log m_I=O(p^3 log(p+1))=O(Z_j)` | Interchange arity; the decisive improved parameter estimate. |
| `N_lab` | `q^(h^2)<=m_I^4` | Number of labels, distinct from numerical records. |
| `C_rank` | `(1+h^(p-1))^(p+1)`; `log C_rank=O(p^2 log(p+1))` | Explicit low-rank coefficient. |
| `r_star` | `r_star/N_lab<=C_rank q^(-p^2)` | Finite-field factor rank; `m_I r_star/N_lab<=C_rank`. |
| `D_G` | `D_G<=2+h q^h` | Rational Gram dimension; reserve parameter `a=D_G-2`. |
| `lambda` | `<=binom(h,p)^(p+1)(q-1)^p r_I^(p(p-1))` | Free-rectangle incidence per label. |

The last three bounds are also independently extracted in S002
`routes/A/interchange-label-growth.md`. The pencil cost is an absolute
constant times `D_G(1+lambda)(1+C_rank)` per row. Original binary repair
uses `O(sqrt(m_I log m_I))` pencils, giving main calls per row at most

\[
 \sqrt{m_I}\,2^{O(p^2\log(p+1))}
 q^{3p-1}r_I^{p(p-1)}\sqrt{1+p^2r_I}+2/m_I^2.
\]

Put `gamma=1/2+epsilon_j/2`. Since
`(epsilon_j/2)p^2-(3p-1)>=3p`, taking `r_I=C p log(p+1)` absorbs this
coefficient into `m_I^gamma`. It also absorbs the reserve, giving

\[
 2m_I^\gamma+2(D_G-2)\le m_I^{\rho_j}/2.
\]

Thus an `O_p(1)` coefficient is not silently treated as uniform. Section 2
of the extraction proves the estimate. Seven exact integer-log controls in
`route-a/verification.json` check representative inequalities without
materializing `m_I`; they are not the universal argument.

## 3. Scalar representations, geometry and the finite budget

The complete theorem retains the original integral predictor and literal
matrix-root construction. It does not require the compact real-root
predictor to specialize in odd characteristic.

| Quantity | Bound | Expense represented |
|---|---|---|
| Window degree `d` | `O(sqrt(m_I log m_I))` | `F/repair`, `lem:count-predict`. |
| Root order `b_0` | Least power of two at least `max(2,d)` | Padding for `lem:matrix-root`. |
| Monomials `H_mon` | `<=sum_(a<=d) binom(m_I,a)<=(m_I+1)^(d+1)<=E_2(O(Z_j))` | Literal collected multilinear predictor; zero padding fixes common size. |
| Predictor coefficient bits | `O(d log(m_I+1))` | Integral truncated series; no factorial invertibility assumption. |
| Raw rows `R_0` | `2^(m_I) b_0^(H_mon)<=E_3(O(Z_j))` | All shifts, with a full block of independent inputs per shift. |
| Cyclotomic basis rank `d_ext` | `<=R_0` | Power-of-two root order at most `2R_0`. |
| Expanded rows and dense scalar lists | `poly(R_0,m_I)<=E_3(O(Z_j))` | Basis expansion, all patterns, Vandermonde checks, repair matrices, entry counts. |
| Characteristic-zero coefficient bits | `poly(R_0,m_I)` | Geometric-sum inverses and polynomially many exact array products. |
| Rational address coefficient bits | Original invoice `2^(poly(m_I))`; reviewed refinement `poly(m_I)` | Direct quotient/complement choices and minor bounds; `route-a/rational-geometry-height.md` and S002's prior rational-address proof. |
| Address numerator/denominator values and their product `B` | Original invoice `E_3(O(Z_j))`; refined `E_2(O(Z_j))` | Values control monotone pieces and forbidden primes. Refined literal determinant generation is also `E_2(O(Z_j))`. |
| Address radix `b_rad` | Prime between `max(W,B,2)` and twice that bound | `W` is expanded batch width. Trial division in the value and padding below `b_rad^2` stay at height three. |
| Complete finite budget `S_j` | `2<=S_j<=E_3(C Z_j)` | Total lists, entries, rows, passes, roles, radix/scaling values, numerical bit lengths, actual generation time/space. |

Each extension-valued row becomes `d_ext` independent `F_p` rows, as
allowed by `cor:swap-repair`. Calls and input rows both multiply by
`d_ext`, preserving the ratio. Binary-coded `F_p` data avoid enumerating
the `p^(d_ext)` extension elements; that unnecessary alphabet table would
create a fourth exponential. Fixed polynomial enlargements of `S_j`
cover total list lengths and scans without changing its height.

The unconditional extraction is already valid with its conservative
address invoice. The separately reviewed refinement proves polynomial
address bit heights and removes address geometry as an independent source
of a third exponential. S002 had established this sharper bound at
`96028cba1342c02bdca1f537ae9a80485087bdf3`; the focused proof and review
corroborate it. The literal scalar width, and hence the complete unconditional
budget and rate, remain unchanged.

### The binary Fourier branch

At the same `epsilon_j`, take

\[
 t=\lceil4/\epsilon_j\rceil=8(j+2),\quad
 r_F=\lceil16t\log_2(16t)\rceil,\quad q_F=2^{r_F},\quad m_F=q_F^t-1.
\]

Then `log(m_F+1)=O((j+2)^2 log(j+3))`, with a quarter-margin finite routing
at exponent `rho_j`. Original all-shift matrix roots give scalar budget
`E_3(O((j+2)^2 log(j+3)))`, within the interchange budget. The source
dyadic normalized even-width construction plus the fixed odd-width
butterfly supplies the numerical template. The compact binary alternative
has better local widths but is not needed here; see
`route-a/explicit-binary-kernel.md` and Section 3 of the extraction.

## 4. From finite data to complete candidate costs

Let `u` be the core input length. At a valid packed shape, `N_rec=2^k`
numerical records satisfy `N_rec k=Theta(u)`, so `k=Theta(log(2+u))`
with absolute constants in the large-input regime. All profiles include
finite generation and physical interpretation.

| Quantity | Bound | Implementation reason |
|---|---|---|
| Total serialized code/list length | `S_j^c` | Binary role indices and a fixed tape engine; no product of logical-head states. |
| Exact movement coefficient | `S_j^c` per logical volume unit | Serialized scans, monotone pieces, parent-charged parking and restores; `Old/streams,swap`, `T/interchange`. |
| Controlled-arithmetic degree | Absolute constant in address width | Triangular sums become single-control rotations. Coordinates contribute an outer `poly(S_j)` loop. |
| Packed-XOR guard | `C_guard ceil(log(2k))`, absolute `C_guard` | Control arithmetic has absolute degree in `k`; its `poly(S_j)` coefficient stays in time. |
| One-level logarithmic gain | `log C_node<=S_j^c` | Actual sum-of-entries bounds, retained registers, copies and merges. |
| Working integer/fractional width `P` | `<=S_j^c(1+k)` | Common-ancestor gain, instruction counts, boundary caps and certified rounding. |
| Reused short-multiplier scratch | `<=S_j^c(1+k)^2` additive | Independent `O(P log P)` multiplier; one active word multiplication. |
| Aggregate non-volume setup | `G_j(1+k)^(E_j)`, `G_j,E_j<=S_j^c` | Descendant count, instructions, shapes, roots, phases, descriptors and padding. |
| Sufficient large-shape condition | `log u>=S_j^c`, plus absolute `u>=U_abs` | `k>=64(E_j+ceil(log G_j)+1)^2` makes setup at most `2^(k/4)`. Prime-box cutoff is independent of `j`. |

The machine is not supplied with the unknown smallest exponent `c` or the
absolute prime-gap cutoff. It computes source shape/coprimality/digit
checks, validates borrowed coordinates and `q'<=2q` row padding before
allocating arrays, and uses an aggregate `u`-microstep setup clock and
`u`-cell auxiliary caps. A microstep is a transition of the fixed tape
engine. Per-record and per-fibre work already charged to volume is outside
that non-volume clock. Failure invokes schoolbook on preserved operands.
All checks pass above the sufficient analytical threshold. At every length,
the union of visited cells is bounded.

Thus integers `a_j,c_j>=1` and a threshold `U_j` can be chosen with

\[
 \begin{aligned}
 t_j(u)&\le a_j u(1+\log_2u)^{\theta_j} &&(u\ge U_j),\\
 \operatorname{space}_j(u)&\le c_j(u+1) &&(u\ge1),\\
 a_j,c_j&\le S_j^c,\qquad
 \log_2 U_j\le S_j^c+\log_2 U_{\rm abs}+O(1).
 \end{aligned}
\]

The unabsorbed time has `(1+log(2+log u))^4` at exponent `rho_j`. The
slack `eta_j` absorbs it at cost `O(eta_j^-4)=O((j+2)^4)`, inside `S_j^c`.
The coefficients and sufficient threshold are analytical witnesses. The
schedule's fences and chunk enumeration do not need their numerical values.

## 5. Chunking, index and certificate parameters

Apply the complete-attempt contract in [`CERTIFICATE.md`](CERTIFICATE.md).
The rowwise carry implementation in
[`route-b/linear-chunk-overhead.md`](route-b/linear-chunk-overhead.md), C2,
gives the explicit transfer below. The extraction's coarser fixed power
of `S_j` gives the same final elementary height.

| Parameter | Formula or sufficient bound | What is charged |
|---|---|---|
| Chunks `R_j` | Least power of two above `2c_j`; `2c_j<R_j<=4c_j` | Common `O(n)` work fence, including generation and code. |
| Chunk exponent `kappa_j` | `log R_j<=2+log c_j=O(log S_j)` | Parameter paired with `j`. |
| Attempt threshold `N_j` | `max(4c_j,R_j U_j)` | Chunk availability, fast applicability and cell cap. |
| Attempt coefficient `A_j` | `<=C a_j c_j<=S_j^c` | Products, copies, erasure, carry accumulation and output. |
| Index `i_j` | `<=2+(j+kappa_j+1)^2` | Explicit nondecreasing-sum diagonal ordering; schoolbook index reserved. |
| Weighted coefficient `D_j` | `2^(i_j) A_j` | Round allowances and common scheduler cost. |
| Logarithmic cost `d_j` | `log D_j=i_j+log A_j=O((j+log S_j)^2)` | Cost coordinate in the certificate. |
| Threshold coordinate `b_j` | `log(1+log N_j)=O(log S_j+1)` | Includes core applicability and space normalization. |

For `n>=N_j`, writing `u=ceil(n/R_j)` gives
`c_j(u+1)<n/2+2c_j<=n`. Wrapper work is `O(R_j^2 u)=O(R_j n)`, so
the prefactor is linear in `c_j`. The candidate workspace is reused; it
is not replicated `R_j^2` times. Tape count and visited-cell multiplier
are independent of `j`.

Because `log S_j<=E_2(CZ_j)`, fixed powers stay at the same height. One
absolute `C` therefore gives

\[
 d_j\le E_2(CZ_j),\qquad b_j\le E_2(CZ_j). \tag{1}
\]

Binary weights or sound preflight reduce the selection contribution to
`d_j`; see `route-b/tower-profile-comparison.md`. They do not change this
height alone, since actual per-volume work and applicability still involve
`log S_j`.

## 6. Optimizing the proved complete profiles

For the final input length put

\[
 L=1+\log_2n,\quad x=\log_2L,\quad y=\log_2\log_2(x+16).
\]

The certificate is `F(x)=inf_(b_j<=x)(d_j+x/(j+2))` and
`H_cert(n)=1+2^(F(x))`. For sufficiently large `x`, choose

\[
 j=\left\lfloor c_0\left(\frac{y}{\log_2(y+2)}\right)^{1/3}\right\rfloor
\]

with sufficiently small fixed `c_0>0`. Then `CZ_j<=y/2` eventually, so
both coordinates in (1) are at most
`2^(sqrt(log_2(x+16)))<=sqrt x`. The chosen candidate is feasible;
thresholds have not been discarded. Thus

\[
 F(x)\le\sqrt x+\frac{x}{j+2}
 =O\!\left(x\left(\frac{\log_2(y+2)}{y}\right)^{1/3}\right),
\]

and

\[
 T(n)\le n\sqrt L\;
 2^{\,O\!\left(x\left(\frac{\log_2(y+2)}{y}\right)^{1/3}\right)},
 \qquad \operatorname{space}(n)=O(n).
\]

A simpler weaker expression is `H_cert<=2^{O(x/(log log x)^(1/4))}`.
The chosen `j` analyzes a fixed schedule, not an uncharged selection
oracle. Small inputs use the direct fallback.

## 7. Binding expenses and requirements for a stronger rate

| Source of growth | Effect in this ledger | Requirement for a substantive improvement |
|---|---|---|
| Interchange incidence versus saving | `r_I=O(p log p)`, `log m_I=O(j^3 log j)` | Stronger label/call estimates, another label family, or another recurrence. The current estimate is sufficient, not a universal lower bound. |
| Literal monomial tensor matrix | `H_mon` is double exponential; `b_0^(H_mon)` makes rows triple exponential | Smaller full-rate pencils in the required odd characteristic, preserving exact repair and call/row ratios. |
| Address constants and radix | Conservative theorem invoice has height three; reviewed address values/generation have height two | The sharper choice removes this independent third-tower expense. The radix still exceeds expanded scalar width `W`, whose current bound has height three. |
| Extension basis representation | Prevents an avoidable fourth exponential | Preserve basis expansion instead of a table over all extension elements. |
| Physical execution and precision | `a_j,c_j<=poly(S_j)`, `log U_j<=poly(S_j)` | Charge actual row scans, field maps, routing, widths, setup and live space; finite-description savings alone do not establish these costs. |
| Weighted enumeration | `i_j=O((j+log S_j)^2)` | Binary weights/preflight improve selection, but core and threshold profiles retain the present height. |

S002's compact real-root predictor and small shift family improve the
characteristic-zero binary branch. They do not directly replace the
odd-characteristic interchange predictor. The scoped obstructions in
`INTERCHANGE-OBSTRUCTION.md`, `PADIC-LIFT-OBSTRUCTION.md`, and
`route-a/count-mod-p-obstruction.md` explain specific failed transfers;
none lower-bounds arbitrary predictors or multiplication.

This theorem is a quantitative mathematical implementation supported by
written source/space/precision proofs and independent AI-assisted review.
Exact finite checks support local identities and controls, not the
asymptotic theorem. The result neither reaches bounded `H` nor lower-bounds
the actual source machine. It uses no Weak ETH assumption, new algebraic-model
premise, Lean certification, practical benchmark, or priority claim.

Credits: @CubeJerry; the pinned OpenAI manuscripts and cited predecessors;
S002's compact predictor, label/threshold invoices and independently accepted
complete extraction; Route B's chunk/schedule analysis; Route C's independent
component/compiler audit. Developed with GPT-6 Astra Pro assistance.
