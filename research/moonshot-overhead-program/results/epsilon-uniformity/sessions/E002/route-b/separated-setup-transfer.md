# Separate finite preparation from work proportional to the input

Status: **complete conditional fixed-tape transfer; physical premises remain open**.
This E002 Route B construction uses a new input-length-aware machine. It is
not a lower bound on the published weighted-search machine. Its useful
instance is

\[
T(n)=O\!\left(n\sqrt{L(n)}\,
 2^{O(x^{3/4}(\log_2(x+2))^{1/4})}\right),\qquad
x=\log_2 L(n),\quad L(n)=1+\log_2 n,                 \tag{S0}
\]

with uniform `O(n)` visited space. Equation (S0) is conditional on the local
physical contracts below. They have **not** yet all been verified for the
current structured module. The unconditional programme result is unchanged.

Source pins: programme predecessor
`0607d044d1d09489580da0e5828588820e1a6775`; OpenAI `math`
`3344da59991ed94f9ba711217b29c1d760badfa6`. Source sections: the tape
paper's `interchange.tex`, `walsh.tex`, `permutations.tex`, `integers.tex`
and `uniformity.tex`. Predecessors: programme
`routes/A/fixed-field-extraction-theorem.md`,
`routes/A/scheduler-and-chunking.md`, and focused E001
`route-b/preflight-selection.md`.

## 1. The resource distinction

The accepted S002 compiler uses an expanded-data bound `P_m<=2^(m^C)`
for finite preparation, work per input volume, and proportional workspace.
Its candidate prefactor consequently has logarithm `m^{O(1)}`. Changing
only the search schedule cannot remove that expense.

Here preparation and retained data may still be `2^(m^C)`. We instead
require polynomial physical work and workspace per input volume. This is
a falsifiable property of specified tensor-factor, check-map and address
processors. It is stronger than the expanded-template compiler and does
not assume a whole uniformly near-root multiplication algorithm.
Every cost refers to one fixed finite-alphabet multitape processor. Table
lookup, coefficient generation, interpretation and head movement are charged.

## 2. Preparation absorption

**Lemma S1.** If `R>=1`, `G<=2^R`, `1<=v<=R`, `t=log_2 n`, and
`t>=64(R+1)^2`, then

\[
G(1+\log_2 n)^v\le n^{1/2}.                         \tag{S1}
\]

**Proof.** For `t>=1`, `log_2(1+t)<=2 sqrt(t)`. Indeed, with
`u=sqrt(t)>=1`, `2u-log_2(1+u^2)` is positive at 1 and its derivative
is positive: `2u/((1+u^2)ln 2)<=1/ln 2<2`. Hence the logarithm of the
left side is at most `R+2R sqrt(t)<=t/4+t/4=t/2`. ∎

An additive `2^(m^C)L(n)^(m^C)` cost is therefore absorbed by linear time
above a threshold `log_2 n>=m^{C'}`, for a larger fixed exponent and a
fixed constant enlargement. Its generation workspace is bounded by actual
time. Nothing here permits the same cost to be paid once per input record.

## 3. Independently meaningful component premises

Fix the current finite programme family, retaining distinct coefficient
algebras for exact characteristic-two interchange and numerical rational
Walsh. For `J>=4`, let `m=m_J`. Constants below are absolute; increasing a
fixed exponent combines finitely many bounds.

**F: finite identities and call margins.** An explicit terminating
constructor supplies the finite algebraic identities and exact call counts,
with

\[
\log_2 m_J\le C J^3\log_2(J+2),\quad m_J\ge J.       \tag{S2}
\]

At `rho_J=1/2+1/(2J)`, the normalized interchange and Walsh child
coefficients are at most half the corresponding arity raised to `rho_J`.
The finite contraction/spatial children have their original smaller
volumes. Returned finite data, generation and finite checking cost at most
`2^(m^C)`. This premise concerns finite algebra and calls, not tape time.

**E: local physical execution.** One fixed processor implements the
specified local grammar: row-linear maps, tensor/module-index rearrangements,
shift-only checks and inverses, spectral selectors, ordered rational address
maps, finite-field coordinates and numerical pointwise arithmetic. Its
*whole one-level list*, excluding self-recursive calls in F, has, at local
bit volume `V` and active field width `a`, actual time at most

\[
m^C V(1+a^{\rho_J})(1+\log_2 L(n))^C
 +2^{m^C}L(n)^{m^C}.                                \tag{S3}
\]

and reusable visited workspace at most

\[
m^C V+2^{m^C}L(n)^C.                                \tag{S4}
\]

Preparation may be shared or repeated at nodes: both cases are allowed.
There are two sequential proof tiers. The exact interchanger has the
stronger ordinary local bound with `1+a^rho_J` replaced by `1`.
Prove that interchanger first. Numerical Walsh then uses it for the
source's column changes and packed XOR operations, charged by the
displayed `a^rho_J` factor. These are local work only relative to the
Walsh recursion; they are not declared free or ordinary linear scans.
Dispatch, tags, sorting, record widths, copying, cleanup and head returns
are included. Extra scans or padding **must not multiply child volumes**;
otherwise they change F's invoice. Numerical record arithmetic uses the
source's fixed short `O(k log k)` multiplier at `k=Theta(L(n))`; an
arithmetic/random-access operation count does not satisfy E.

**N: numerical and shape control.** The numerical branch has local
logarithmic gain, coefficient bit height and logarithmic branch count at
most `m^C`. It admits an absolute `O(k)` working precision for `k>=m^C`.
Preparation is charged in E. Exact shape, compatibility, leading-row and
radix-padding tests succeed for digit lengths

\[
u\ge U_{\rm abs},\qquad\log_2 u\ge m^C.             \tag{S5}
\]

The resulting padded volume is at most polynomial in `m` times the
unpadded volume; E includes this factor and F's child invoice remains
valid. `U_abs` is fixed independently of `J`. Actual tests and exact
fallback are retained; the machine need not know a value of `U_abs`.

**R: reusable stacks and descriptions.** Main descents have the source's
fixed geometric parked-payload contraction. Full-volume reserve descents
park only descriptors. Siblings and successive pieces reuse the same
intervals. There are at most `2^(m^C)` branches per local node, recursion
depth at most `C log_2 L(n)`, and descriptors of at most
`2^(m^C)L(n)^C` bits. This is a bound on visited regions, not only live data.

F has an existing written construction. Numerical parts of N are addressed
in `polynomial-walsh-precision.md`. E, N's shape clause and the exact
application of R to any succinct processor require separate proofs.

## 4. Charged digit candidates

**Lemma S2.** F/E/N/R imply, after increasing an absolute `K`, prepared
digit calls with

\[
\tau_J(u)\le m_J^K u L(u)^{1/2+1/J},\qquad
\operatorname{space}_J(u)\le m_J^K u+d_J(u),           \tag{S6}
\]

and preparation time/space, retained data and total non-volume setup at most

\[
g_J(u),d_J(u)\le2^{m_J^K}L(u)^{m_J^K}.               \tag{S7}
\]

A sufficient applicability threshold is

\[
U_J\le\max\{U_{\rm abs},2^{m_J^{K'}}\},             \tag{S8}
\]

after a fixed constant enlargement and another absolute exponent `K'`.
All calls and interpretation are physical fixed-tape work.

**Proof.** Omit additive terms first. First solve the interchanger
recurrence, then insert its bound in the numerical Walsh local column
changes in S3. At each tier, dividing by node volume and then by active
width to exponent `rho_J` gives a geometric recurrence of ratio at most
`1/2`, by F. The local coefficient is polynomial in `m`; the allowed
`a^rho_J` toll becomes a bounded local term after this normalization.
There is no mutual or circular recurrence between the two tiers. Source
block assembly adds only a fixed number of factors `1+log L`. The volume
term is thus `m^{O(1)}u L^rho_J(1+log L)^{O(1)}`.

There are at most `(2^(m^C)+1)^(C log_2 L+1)` nodes, bounded by
`2^(m^{C_1})L^{m^{C_1}}`. Multiplying by each node's allowed additive
time/space retains that form. This overcounts repeated setup rather than
assuming free persistence. S1 absorbs the total in `u` once
`log_2 u>=m^{C_2}`. The shape guards can be imposed at the same threshold.

For fixed `b>=0`, maximizing `(1+t)^b 2^{-t/(2J)}` gives

\[
(1+\log_2 L)^b\le C_b J^b L^{1/(2J)}.               \tag{S9}
\]

Since `J<=m`, its coefficient is polynomial in `m`, proving S6's time
bound. Parked payload sums geometrically by R. Overcount all auxiliary
descriptors by all nodes and absorb with S1 as above. Reuse of marked
intervals bounds the union of visited cells. This gives S6--S8. ∎

A list with exponentially many actions *per independent input row* violates
E; such work cannot be renamed preparation. A sort that inflates every
child volume instead changes F and can destroy the geometric margin.

## 5. A bounded input-length-aware machine

**Theorem S3.** F/E/N/R imply (S0) for one fixed exact deterministic
finite-alphabet multitape full-product machine, with uniform `O(n)` visited
space. No universal-search weight multiplies the final digit-execution bill.

### Actual algorithm

1. Preserve the inputs, compute their length `n` with an amortized binary
   counter and mark a fixed number of `O(n)` work regions. Put
   `t=1+floor(log_2 n)` and `q=1+floor(log_2(t+1))`; thus `q=x+O(1)`.
2. Choose the largest dyadic `J=2^h>=4` satisfying `J^4 h<=q`.
   If none exists, use schoolbook. This uses exact integer arithmetic on
   `O(log n)`-bit words, hence fits `O(n)` work above a fixed cutoff.
3. Run F's constructor, obtaining `m`. Set `c=m^K` and let `r` be the
   least power of two at least `8c`; put `u=ceil(n/r)`. Prepare the same
   shape and precision for every `u`-bit chunk product. Give this entire
   selection, construction and preparation an `n/16` actual-step and
   visited-region budget. On timeout, region crossing or failed shape
   test, clean scratch and use schoolbook. The fixed constants may be
   adjusted once for controller overhead.
4. Retain the complete preparation and use the physical rowwise/diagonal
   chunk wrapper for the `r^2` digit products. Cap the candidate work
   regions and use an overall `n^2` actual-step execution budget. On a
   cap violation clean and fall back; accept only a completed exact result.

Low-end binary clocks have amortized constant overhead. Copies, aborted
work, cleanup and head returns are charged. Construction and digit calls
use a common fixed processor, with interpretation included in E.

### Correctness and space at every length

Capped attempts terminate. Every completed plan and arithmetic call is
sound by F and N; the positional wrapper is exact. A failed attempt uses
a fixed total exact schoolbook multiplier. No partial output is returned.
Input, output, wrapper, retained data, active candidate and clocks occupy
a fixed number of marked intervals with total length `O(n)`. Reusing the
same intervals for calls and fallback bounds **all cells ever visited**.
No knowledge of an unknown applicability cutoff is used for correctness.

### Eventual success and runtime

Write `Z=J^3 log_2(J+2)`. Maximality gives
`J^4 h<=q<(2J)^4(h+1)`. For large `q`, `h` is comparable to `log_2(q+2)`;
these inequalities prove

\[
J=\Theta((x/\log_2(x+2))^{1/4}),\quad
Z=O(x^{3/4}(\log_2(x+2))^{1/4})=o(x).              \tag{S10}
\]

Only attainable `x=log_2(1+log_2 n)` is used. Equation S2 gives
`log_2 m=O(Z)`, hence `log_2 r=O(Z)=o(x)`, `r<=n` and
`log_2 u=log_2 n-O(Z)=2^x(1-o(1))`. The preparation bill satisfies

\[
\log_2 g_J(u)\le m^K(1+\log_2 L(u))
               \le2^{O(Z)}(1+x)=2^{o(x)}.          \tag{S11}
\]

Because `log_2 n=2^x-1`, actual preparation eventually takes less than
`n/16` steps and visited cells, including its retained data. Also
`log_2 u>=m^{K'}` eventually, so S8's guards hold. Proportional core
space is `c u<=c(n/r+1)<=n/8+c<=n/4`; adding retained data fits its fixed
region. Thus the actual capped algorithm eventually succeeds.

The positional wrapper costs `O(nr)`, and since `r^2u<=2rn`, `u<=n`,

\[
r^2\tau_J(u)\le C m^K r n L(n)^{1/2+1/J}.          \tag{S12}
\]

All setup is `O(n)` and charged once or already absorbed into the digit
bill. Since `r=O(m^K)`,

\[
\log_2 H(n)\le O(1)+O(\log_2 m)+x/J
 =O(x^{3/4}(\log_2(x+2))^{1/4}).                   \tag{S13}
\]

The resulting runtime is eventually below the `n^2` cap. Shorter lengths
are handled by fallback and absorbed by a fixed asymptotic constant. ∎

### What is new relative to E001 preflight selection

E001 P2 assumes complete physical bills with prefactor `j^a` and a linear
log-log threshold in `j`, and proves polynomial-in-x overhead. Here the
family-level hypotheses are weaker and tied to actual local interfaces:
polynomial per-volume costs in a much larger `m=2^{O(J^3 log J)}` are
allowed. The retained generation may be `2^(m^C)`. Their separation gives
a first fixed-power subexponential-in-x target under explicit physical
contracts, without assuming a polynomial-in-J whole-candidate bill.
This does not establish those contracts or improve the unconditional bound.

## 6. General profile form

The same argument applies to an explicit integer family whose profile is

\[
\log_2 m_J=O(J^p(\log_2(J+2))^r),\quad p>0,\ r\ge0,
\]

and whose remaining contracts have fixed polynomial/exponential exponents
in `m`. A dyadic choice within a fixed factor of
`[x/(log_2(x+2))^r]^{1/(p+1)}` gives

\[
\log_2 H(n)=O(x^{p/(p+1)}(\log_2(x+2))^{r/(p+1)}).   \tag{S14}
\]

For this general version, the family must supply an integer computable
profile inverse or fixed rational comparison exponents realizing that
dyadic scale. No real-number oracle is allowed. The concrete `(p,r)=(3,1)`
algorithm uses only `J^4 h<=q`.

The optimization algebra itself is elementary. The substantive transfer
keeps finite generation, actual physical execution, threshold, padding and
visited space separate throughout the single-machine construction.
For `(3,1)`, S0 implies `H<=2^{O(x^beta)}` for every fixed `beta>3/4`,
for example `beta=4/5`. It does not give the no-log-factor `beta=3/4`,
polynomial-in-x overhead or the exact endpoint.

## 7. Open next questions

1. Prove E for succinct cyclic tensor factors and shift-only checks with
   actual module-index movement and aligned accumulation. Symbolic sparsity
   alone does not give a tape executor.
2. Establish N's small-radix/padding clause after the rational-address
   improvement. Small coefficient bit height does not imply a small padding
   factor.
3. Prove on-demand spectral selection and repair coefficients have polynomial
   bit cost and controlled rational height, including known exceptions.
4. Compose the numerical precision lemma with the final processors and audit
   R after their scratch layouts are fixed.

If any component still needs `2^(m^C)` work or workspace *per volume*, S0
does not follow. This is a failure of the stated transfer premises, not a
lower bound on the source machine or integer multiplication.

Credits: @CubeJerry; the pinned OpenAI manuscripts and cited predecessors;
E001 preflight selection and S002 chunking/profile construction; substantial
ChatGPT multi-agent assistance. Bounded direct selection and fallback are
elementary algorithm design, not a claim to invent universal search.
