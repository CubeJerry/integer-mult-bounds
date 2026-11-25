# A quantitative residual exponent for one fixed tape multiplier

Status: **proved written source extraction, independently reviewed by AI
agents**. This uses the pinned published upper-bound construction and the
explicit implementation below. No Weak ETH premise or old five-assumption
interface is used. No complete astronomical template execution, Lean proof
of this refinement, or independent human refereeing is claimed.

## 1. Main theorem

Put

\[
 L(n)=1+\log_2n,\qquad x=\log_2L(n),\qquad
 y=\log_2\log_2(x+16).
\]

**Theorem E.** One deterministic multitape Turing machine, with a fixed
finite alphabet and a fixed number of one-dimensional tapes, computes the
exact full product of two `n`-bit integers in worst-case time

\[
 T(n)=n\sqrt{L(n)}\;
 2^{\,O\!\left(x\left(\frac{\log_2(y+2)}{y}\right)^{1/3}\right)}
 \tag{E}
\]

and visits `O(n)` cells. Inputs and the full `2n`-bit output occupy the
prescribed contiguous binary intervals. Correctness and the common space
bound hold at every positive integer length; the time estimate absorbs
the bounded initial range.

Thus the excess exponent has the explicit bound

\[
 \delta(n)=O\!\left(\left(\frac{\log_2(y+2)}y\right)^{1/3}\right).
\]

A simpler weaker consequence is `H(n)<=2^{O(x/y^(1/4))}` and
`delta(n)=O(y^(-1/4))`. This does not reach constant overhead, polynomial
overhead in `x`, or `2^{O(x^beta)}` for a fixed `beta<1`. It quantifies a
specified implementation of the source scheme, rather than comparing
against the unknown actual residual term of an unspecified implementation.
Absolute constants and the eventual starting length are not numerically
evaluated.

This sharpens the programme's preceding S002 sixth-power extraction at
`96028cba1342c02bdca1f537ae9a80485087bdf3`, with
`H<=2^{O(x/y^(1/6))}`. Both retain separate proofs and review records.
No broader literature-priority claim is made.

## 2. Quantitative finite construction and compiler

The source pin is
[`openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`](https://github.com/openai/math/tree/3344da59991ed94f9ba711217b29c1d760badfa6).
The proof uses the November tape and Fourier manuscripts, and the
September tape paper's elementary stream, rational-map and parking proofs.
Exact section identifiers and the full derivations are in the
[extraction](route-a/elementary-tower-extraction.md) and
[compiler invoice](route-a/compiler-invoice.md).

Define `E_1(t)=2^t`, `E_2(t)=2^(2^t)`, `E_3(t)=2^(2^(2^t))`, and

\[
 \theta_j=\frac12+\frac1{j+2},\quad
 \rho_j=\frac12+\frac1{2(j+2)},\quad
 Z_j=(j+2)^3\log_2(j+3).
\]

Those proofs establish a generated finite data budget `S_j>=2` and
absolute constants `C,c` such that

\[
 S_j\le E_3(CZ_j), \tag{P1}
\]

and the complete interpreted candidate has

\[
 \begin{aligned}
 t_j(u)&\le S_j^c u(1+\log_2u)^{\theta_j}
       &&\text{if }\log_2u\ge S_j^c\text{ and }u\ge U_{\rm abs},\\
 s_j(u)&\le S_j^c(u+1)&&\text{at every positive length},\\
 g_j&\le S_j^c.
 \end{aligned} \tag{P2}
\]

Generation `g_j` is included in the complete run. `U_abs` is the source's
absolute prime-shape cutoff, independent of `j`. Actual checks and
fallbacks mean the machine needs neither this cutoff nor the smallest
analytical constant `c` as advice.

The budget covers **total** description and instruction lengths, row and
role counts, numerical coefficient bit lengths, address-scaling integer
values, radix value, and actual generation time and space. Bit lengths
alone would not pay for the monotone pieces of a rational address scaling.
The principal steps proving (P1)--(P2) are as follows.

1. Interchange uses `p=Theta(j)`, `q=2^r`,
   `r=O(p log(p+1))`, and `m=q^(p²)`. The explicit label estimates give
   `log m=O(j³ log(j+2))` and a relative contraction margin at most one
   half. Binary Fourier routing needs only `log m=O(j² log(j+2))` and
   has margin at most one quarter.
2. The original integral predictor has degree `O(sqrt(m log m))` and at
   most `(m+1)^(O(sqrt(m log m))+1)` multilinear monomials. Its literal
   matrix-root representation and translated rows fit `E_3(O(log m))`.
   Cyclotomic **basis expansion** preserves this height. Listing every
   possible extension-algebra element is unnecessary. Geometric-sum
   inverses and Lagrange products give polynomial-in-row-budget repair
   coefficients and construction cost. Rational address elimination,
   compatible-prime trial division and padding fit the same height.
3. The fixed binary engine serializes aligned roles by scans. Triangular
   maps use successive single-control rotations, keeping an absolute
   number of collapsed counters in each elementary operation. Scaling
   pieces, instruction access, copies, parking and returns all cost
   `poly(S_j)` times logical volume, without changing child volume.
4. Completed normalized children have unit norm. The common-ancestor
   argument bounds logarithmic error gain by
   `poly(S_j) log(2+k)`. Numerical widths `poly(S_j)(1+k)` suffice.
   Short arithmetic scratch is reused additively. Aggregate setup is
   `G(S_j)(1+k)^E(S_j)`, with `G,E<=S_j^c`, and is absorbed into
   `2^(k/4)` above a fixed-power threshold in `S_j`.
5. All layouts are checked before materialization. An aggregate setup
   microstep clock and auxiliary scratch marks trigger cleanup and
   schoolbook on preserved operands if needed. This proves all-length
   space, including short lengths. Finally the exponent gap
   `theta_j-rho_j` absorbs the source's `log^4 k` factor with a
   polynomial-in-`j` coefficient.

These are implementation proofs for a specified finite constructor and
engine. They are not assertions that any effective generator or arbitrary
universal compiler has the same cost.

## 3. Common space and actual weighted search

Write `a_j,c_j<=S_j^c` for the time and space coefficients. Choose a
power-of-two chunk count `2c_j<r_j<=4c_j`. The
[chunk lemma](route-b/linear-chunk-overhead.md) computes all digit products
and carries in

\[
 r_j^2t_j(\lceil n/r_j\rceil)+O(r_jn)
\]

steps. For `n>=max(4c_j,r_jU_j)`, the candidate work fits the common
marked regions. Thus a complete-attempt constant `A_j<=S_j^C` and a
sufficient threshold `N_j` satisfy

\[
 \log_2N_j\le S_j^C+O(\log S_j)+\log_2U_{\rm abs}. \tag{P3}
\]

Explicitly enumerate `(j,k)`, where the chunk count is `2^k`, in
nondecreasing-sum diagonal order. Reserve a schoolbook index. The selected
successful pair has `i_j=O((j+log S_j)^2)`. Round `s` restarts index
`i<=s` with `2^(s-i)` actual physical steps. Generation, copying,
interpretation, clocks, aborts, cleanup and output are charged. The
source schedule costs `O(2^s)` per round and guarantees

\[
 T(n)\le Cn+C2^{i_j}(t+1) \tag{P4}
\]

for a successful attempt of duration `t`. Fixed linear marks fence every
attempt. Schoolbook ensures termination at every length and a final
round `O(log n)`, so schedule storage also fits `O(n)`.

Set `D_j=2^(i_j)A_j`, `d_j=log_2D_j`, and
`b_j=log_2(1+log_2N_j)`. Equations (P1)--(P4) imply

\[
 d_j,b_j\le E_2(CZ_j). \tag{P5}
\]

The sufficient envelope is

\[
 F(x)=\inf_{j:b_j\le x}\left(d_j+\frac{x}{j+2}\right),\qquad
 H_{\rm cert}=1+2^{F(x)}.
\]

The schoolbook term handles an empty feasible set, as specified in
[CERTIFICATE.md](CERTIFICATE.md). This is an upper certificate, not an
equality for actual runtime.

## 4. Inversion with integer choices and eligibility

For sufficiently large attainable `x`, choose for the analysis

\[
 j=\left\lfloor c_0
       \left(\frac{y}{\log_2(y+2)}\right)^{1/3}\right\rfloor
\]

with a sufficiently small fixed `c_0>0`. Then `CZ_j<=y/2` eventually,
so (P5) gives

\[
 d_j,b_j\le2^{\sqrt{\log_2(x+16)}}\le\sqrt x.
\]

Hence `b_j<=x`: the candidate is actually eligible. Integer rounding
keeps `j` at least half its unrounded value eventually. Therefore

\[
 F(x)\le\sqrt x+\frac{x}{j+2}
 =O\!\left(x\left(\frac{\log_2(y+2)}y\right)^{1/3}\right).
\]

This proves (E). Since `(log(y+2)/y)^(1/3)=O(y^(-1/4))`, the weaker
displayed consequence follows. The machine does not receive this choice
of `j` or any charge-free parameter oracle. ∎

## 5. Separate conditional and negative results

The certificate diagnostics prove that growing normalized schedule
constants force `F(x)->infinity`. Under the specified full sum-diagonal
order, `F(x)>=c x^(2/3)`. These limit this certificate formula, without
giving an actual-runtime lower bound.

The [bounded-preflight theorem](route-b/preflight-selection.md) proves a
complete conditional transfer to `H=O(x^a)`, including the endpoint
`a=0`, under its explicit physical plan, threshold and generation
contracts. Those stronger family properties have not been established.
Its constant-absorption lemma shows why prefactors and thresholds must
be controlled jointly: small constants alone are not the decisive issue.

The [characteristic/reserve obstruction](INTERCHANGE-OBSTRUCTION.md) and
[literal p-adic lift obstruction](PADIC-LIFT-OBSTRUCTION.md) rule out
specified direct transfers of the compact count predictor into the
current interchange mechanism. S002's support-preserving lift theorem
has complementary broader support hypotheses. None is an unrestricted
lower bound. The [input-dependent radix lemma](route-c/INPUT-DEPENDENT-RADIX.md)
repairs a scoped padding obstruction; the [variable-arity result](route-c/NONSTATIONARY-RECURSION.md)
gives a conditional endpoint interchange. Neither is used as an unproved
premise in Theorem E.

The binding dependency in (E) is the original finite-characteristic
predictor's matrix-root representation and its scalar/description bill.
A smaller full-rate representation must still preserve the required
individual-query information, shared routing, precision and visited-space
contracts. Improving selection alone does not remove that dependency.

## Review, verification and credits

See [REVIEWS.md](REVIEWS.md) and the independent
[compiler audit](route-c/ELEMENTARY-TOWER-REVIEW.md). Finite exact checkers
support algebra, parameter inequalities and scheduling models. The
universal statement rests on written source and implementation proofs,
not on testing the full astronomical multiplier.

Credits: @CubeJerry; the OpenAI November and September constructions and
their cited predecessors; S002's compact predictor, labels, chunking,
thresholds and independent extraction; and the E001 research/review
agents. Prepared with substantial OpenAI AI assistance.
