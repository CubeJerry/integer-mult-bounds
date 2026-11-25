# Nonstationary recursion: critical mass, local work and an endpoint contract

Status: **proved analytic transfer and scoped obstruction; conditional interchange theorem; no new multiplication bound**.

This note separates nearly critical recursive call mass from work outside recursive calls. That distinction matters in the November 24 tape construction: interchange has a constant toll for a fixed template, whereas Walsh has a toll at the target power of its active width. Controlling only the homogeneous part of the latter recurrence does not control its endpoint.

## 1. Sources, model and notation

Primary pin: `openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`.

- Tape manuscript, `build/interchange.tex`, `thm:interchange`, `eq:interchange-contraction`, and “Running the recursion”: for fixed template parameters, time per stream symbol obeys
  \[
  T(e)\le C_\alpha+(2m^\gamma+2a)T(\lfloor(e-1)/(m+2a)\rfloor).
  \]
  Main descents reduce stream volume; reserve descents may retain full volume but park only descriptors.
- Tape manuscript, `build/walsh.tex`, `lem:tape-walsh`, “Work and visited space”: after division by bit volume,
  \[
  T(a)\le C_\rho(1+a^\rho)(1+\log(2+k))+(\sigma/W)T(a/A).
  \]
  The outer record parameter `k` remains fixed along this recursion. Address changes are included in the toll.
- Fourier manuscript, `build/kernel.tex`, `eq:kernel-template-saving`: the published family proves `sigma/W < A^theta` for each fixed `theta > 1/2`, without the joint near-critical bounds used below.
- Tape manuscript, `build/uniformity.tex`, `sec:single-machine`: finite descriptions, serialization and the common space cap are necessary expenses. Changing templates cannot be treated as already compiled constant-size machines.

All logarithms here are natural unless a base is shown. `e` is an integer **active address width**, not input bit length or Euler's constant. `V` is bit volume. The multiplication target uses `n` input bits and `L=1+log_2 n`; interchange time `O(V sqrt(e))` is only one enabling component.

Products along recursion paths are established methodology. Harvey, van der Hoeven and Lecerf, *Even faster integer multiplication* (February 11, 2015 preprint), §5, Proposition 5.3, controls a different recurrence family by an infinite product; see <https://www.texmacs.org/joris/mul/mul.pdf>. No novelty is claimed for recurrence unfolding itself. The source-specific contribution here is the integer variable-arity endpoint contract and the different toll obstruction in the Walsh caller.

## 2. Exact accumulated budget

Let `e_0 > ... > e_D >= 1` be a finite width chain. Suppose

\[
 R(e_i)\le t_i+B_iR(e_{i+1}),\qquad R(e_D)\le r_D,
\]

with all quantities nonnegative. Put

\[
 U_i=R(e_i)/\sqrt{e_i},\quad \tau_i=t_i/\sqrt{e_i},\quad
 \mu_i=B_i\sqrt{e_{i+1}/e_i},\quad P_0=1,\quad P_i=\prod_{h<i}\mu_h.
\]

**Proposition C1.**

\[
 U_0\le P_Dr_D/\sqrt{e_D}+\sum_{i<D}P_i\tau_i. \tag{C1}
\]

Equality holds when every recurrence inequality and terminal bound is an equality.

**Proof.** Successively substitute `U_i <= tau_i + mu_i U_(i+1)`. Each toll is multiplied by exactly the preceding factors. Nonnegativity preserves all inequalities. The formula also holds at depth zero. ∎

For a family of equality invoices, suppose `mu_i>=1` and normalized terminal costs lie between fixed positive constants. Uniformly bounded root cost is equivalent to

\[
 \sup_{e_0}P_D<\infty,\qquad \sup_{e_0}\sum_{i<D}\tau_i<\infty. \tag{C2}
\]

The formula is at least the terminal lower constant times `P_D`, and at least the unweighted toll sum. Conversely it is at most `P_D` times the sum of the terminal upper constant and that toll sum. A bounded product is equivalent to a bounded sum of `log(mu_i)`; replacement by `mu_i-1` requires an upper bound on the factors. These are facts about the specified invoice, not lower bounds on a machine whose runtime is merely bounded above by it.

## 3. A variable-arity endpoint theorem

Fix an integer `r>=2` and real `d>=0` with `d/r<1/2`. For sufficiently large integer `e`, define

\[
 m(e)=\lfloor e^{1/r}\rfloor,\qquad f(e)=\lceil e/m(e)\rceil. \tag{C3}
\]

Choose a fixed threshold `E` so large that `m(e)>=2`, `f(e)<e`, and the estimates below hold for `e>E`. The integer `r` is part of the fixed program; integer root extraction implements (C3) without a real-number oracle.

The conclusions also hold for `m(e)=floor(e^(1/(2r)))^2`. Then `e^(1/r)/4 <= m(e) <= e^(1/r)` for sufficiently large `e`; replace the factor `3` in the proof by `5` and enlarge `E`. This square-arity variant permits entirely rational finite checks because `sqrt(m)` is an integer. It is used by the accompanying verifier.

For `eta(m)>=0`, suppose

\[
 R(e)\le C m(e)^d+\sqrt{m(e)}(1+\eta(m(e)))R(f(e)),\quad e>E, \tag{C4}
\]

and `R(e)<=C_E` for `1<=e<=E`. Every constant is independent of `e,m`.

**Theorem C2.** If fixed `c,delta>0` satisfy

\[
 \eta(m)\le c/[\log\log m]^{1+\delta} \tag{C5}
\]

for all sufficiently large `m`, then `R(e)=O(sqrt(e))` at every integer width. Enlarge `E` so all nonterminal arities satisfy (C5); small arities need no extra assumption.

**Proof, including rounding.** Let `beta=1/r`, `q=1-beta/2`, and `y_i=log e_i` along `e_(i+1)=f(e_i)`. For large `e`,

\[
 \tfrac12e^\beta\le m(e)\le e^\beta,\qquad
 e^{1-\beta}\le f(e)\le3e^{1-\beta}.
\]

After increasing `E`,

\[
 (1-\beta)y_i\le y_{i+1}\le qy_i. \tag{C6}
\]

Thus the chain terminates, has depth `D=Theta(log log e_0)`, and ends at a width bounded above and below by positive constants. Both depth estimates follow by iterating the corresponding side of (C6).

Put `u_i=log y_i`. Successive values are separated by at least `h_0=-log q>0`. Also

\[
 \log\log m(e_i)\ge u_i+\log(\beta/2)\ge u_i/2>0
\]

after another fixed enlargement of `E`. If a positive decreasing function `g` is integrable on a fixed half-line and the `u_i` have separation at least `h_0`, then

\[
 \sum_i g(u_i)\le g(u_*)+h_0^{-1}\int_{u_*}^{\infty}g(t)\,dt, \tag{C7}
\]

up to one fixed endpoint term, for a fixed lower bound `u_*>0`. Compare each term except the smallest with the integral over the disjoint length-`h_0` interval below it. Apply (C7) to a constant multiple of `t^(-1-delta)` to obtain

\[
 \sum_{i<D}\eta(m(e_i))=O(1). \tag{C8}
\]

Rounding has normalized factor `sqrt(m(e_i)f(e_i)/e_i)`, where

\[
 1\le m(e_i)f(e_i)/e_i<1+m(e_i)/e_i\le1+e_i^{\beta-1}.
\]

The sum of `e_i^(beta-1)=exp(-(1-beta)exp(u_i))` is bounded by (C7). Since `log(1+v)<=v` for `v>=0`, (C8) and this estimate give

\[
 \prod_{i<D}\sqrt{m(e_i)f(e_i)/e_i}\,(1+\eta(m(e_i)))=O(1). \tag{C9}
\]

The normalized toll is at most `C exp(-lambda exp(u_i))`, with `lambda=1/2-beta d>0`, and is summable by (C7). Insert the bounded product, toll sum and terminal bound into (C1). This proves the asserted uniform bound, including bounded widths. ∎

### Quantitative variants

Keeping the upper limit in the integral comparison gives these sufficient bounds with all other constants fixed:

| Hypothesis on excess | Bound for `R(e)/sqrt(e)` |
|---|---|
| `eta(m)=O((log log m)^(-p))`, `p>1` | `O(1)` |
| `eta(m)=O(1/log log m)` | `(log log e)^{O(1)}` |
| `eta(m)=O((log log m)^(-p))`, `0<p<1` | `exp(O((log log e)^(1-p)))` |
| `eta(m)<=c`, fixed `c` | `(log e)^{O(1)}` |

For the last row use `(1+c)^D` and `D=O(log log e)`. The powers are not optimized. The polynomial local toll is summable after normalization in every row. Merely knowing `eta(m)->0` does not ensure the endpoint; the corresponding sum need not converge.

**Proposition C2b (sharp summability boundary for the equality invoice).** Suppose (C4) is an equality, normalized terminal costs lie between fixed positive constants, and for a fixed `p>0` the excess is bounded both above and below by positive multiples of `(log log m)^(-p)` at every sufficiently large arity. Then

\[
 \frac{R(e)}{\sqrt e}=
 \begin{cases}
 \Theta(1), & p>1,\\
 (\log\log e)^{\Theta(1)}, & p=1,\\
 \exp(\Theta((\log\log e)^{1-p})), & 0<p<1.
 \end{cases} \tag{C9b}
\]

In the last two lines the positive constants in the exponents need not match. This notation gives two-sided growth classes, not an exact leading constant.

**Proof.** Equation (C6) gives both a positive lower and a finite upper bound on each decrement in `u_i=log log e_i`. Thus, up to fixed constants and endpoint terms,

\[
 \sum_{i<D}u_i^{-p}\asymp1+\int_{u_*}^{u_0}t^{-p}\,dt.
\]

For the lower comparison, cover the integration interval by consecutive gaps of size at most `-log(1-beta)` and use monotonicity. The upper comparison is (C7) with finite upper limit. Also `log log m(e_i)=u_i+O(1)`. The total logarithm of rounding factors is bounded, while `log(1+eta)` is bounded above and below by positive multiples of `eta` after enlarging `E`. This evaluates `log P_D`. The normalized polynomial toll sum is bounded, and `mu_i>=1`, so (C1) for the equality invoice lies between fixed positive multiples of `P_D`. This proves (C9b). ∎

## 4. Complete conditional tape-interchange implication

An analytic recurrence becomes an actual algorithm only under a uniform implementation contract. The following version is adapted to the branching structure in `interchange.tex` rather than assuming a completed endpoint algorithm.

Assume a family of exact **one-level reductions** of binary address interchange. Its input is the complete layout of `thm:interchange`, with active width `e`, arbitrary positive spectator ranges and bit volume `V`. A single fixed dispatcher, given `m>=2`, must provide all of the following whenever `e` is sufficiently large and `m=m(e)` from (C3).

1. The local identity is exact on all records. It reduces to finitely many child interchanges in the same binary representation, of common active width `f(e)`, with arbitrary spectator ranges. Padding is included in child volumes.
2. The child volumes `V_h` obey
   \[
   \sum_hV_h\le V\sqrt m(1+\eta(m)). \tag{C10}
   \]
   This is a local count/volume condition, checkable on a template independently of recursively completed runtime.
3. All nonrecursive work costs at most `C V m^d` actual fixed-tape steps. This includes template generation or regeneration; coefficients, indices and shape tests; program-description access and interpretation; copying, scans, arithmetic, head travel, output, cleanup and control. Constants, physical tape count and alphabet are independent of `m,e,V`.
4. A node uses at most `C V` cells uniformly. On a descent, either `V_h<=lambda V` for fixed `lambda<1` and at most `C V` parent data are parked, or `V_h=V` and all parent arrays and variable-size templates are erased, retaining only `O(log V+(log(e+2))^c)` descriptor bits for fixed `c`. Regeneration after return is included in item 3. Regions and stacks are reused, making these bounds on cells ever visited.
5. For bounded widths a fixed exact routine handles every shape in `O(V)` time and space. The dispatcher and integer-root computation are fixed effective programs; their actual costs are included in item 3.

**Corollary C3 (conditional endpoint for interchange).** Under this contract with `d/r<1/2` and (C5), one fixed deterministic finite-alphabet multitape machine interchanges the two address fields exactly in `O(V sqrt(e))` steps and visits `O(V)` cells, uniformly over widths and spectator ranges.

**Proof.** Recursively use the dispatcher with the exactly selected `m(e)`. Correctness follows by induction on decreasing integer width. Divide the cost recurrence by parent volume. The child bound is uniform over spectator ranges, so summing child costs using (C10) gives (C4). Theorem C2 gives time, with setup, interpretation and cleanup included by item 3.

For space, remove the full-volume descents from a live root-to-leaf path. Across the remaining descents, volumes contract by the fixed factor `lambda`; parked arrays and active local work therefore total at most `C V/(1-lambda)`. Full-volume steps park only descriptors. Path depth is `O(log log(e+2))`. Complete address fields imply `V>=2^(2e)`, so

\[
 O\bigl(\log\log(e+2)[\log V+(\log(e+2))^c]\bigr)=O(V).
\]

Sequential siblings reuse work and stack regions. No growing tape count or implicit alphabet expansion is used. ∎

This is a complete conditional theorem **for interchange**, and remains partial progress toward multiplication. The hypotheses are stronger than the published fixed-template contracts: joint recursive-volume bounds, polynomial local setup, common binary interfaces and uniform workspace. The source does not prove them for a growing template parameter.

## 5. A distinct Walsh obstruction

An endpoint interchange supplier does not remove every toll in the Walsh recursion. The published invoice charges address changes at each node in addition to recursive transforms. Isolate that issue through the favorable equality invoice

\[
 Q(e)=c\sqrt e+\sqrt{m(e)}Q(f(e)),\qquad e>E, \tag{C11}
\]

with positive bounded terminal costs and the same integer `m,f`. This omits the source's logarithmic factor and all growing template constants, deliberately granting a favorable idealization to the toll alone.

**Proposition C4.** The invoice (C11) satisfies

\[
 Q(e)=\Theta(\sqrt e\,\log\log e).
\]

**Proof.** Every normalized toll equals `c`. Every normalized multiplicative factor is at least one because `mf>=e`. Their product is bounded by the rounding estimate in (C9). Formula (C1) places `Q(e)/sqrt(e)` between a positive constant times path depth and a constant times depth plus one. By (C6), depth is `Theta(log log e)`. ∎

For fixed arity `m>=2` and exactly divisible widths `e=m^D`, the same normalized toll gives `Theta(sqrt(e) log e)`. Changing scale can reduce the extra factor, but bounded homogeneous excess alone cannot eliminate it.

The same obstruction holds for any nonnegative equality invoice with normalized factors at least one and normalized toll bounded below at every visited level. To reach the endpoint through such a recurrence, one must make the normalized toll summable, create a uniform contraction of normalized recursive mass, fuse operations so repeated routing is not separately charged, or use a bounded-depth mechanism with its large-arity setup charged. This is an obstruction to the specified invoice and proof strategy, not an unconditional lower bound on a Walsh algorithm or multiplication.

## 6. What the source does and does not supply

The source interchange family has the right local-toll *form*: fixed-template linear work plus recursive volume. Its `C_alpha`, radix, alphabet and serialization constants depend on the template, and its displayed sufficient coefficient is `2m^gamma+2a`, with `gamma>1/2`. Relative to `sqrt(m)`, that invoice contains `2m^(gamma-1/2)`, rather than a certified summably vanishing excess. This diagnoses a sufficient invoice, not the minimum achievable call count.

The source shrinkage is `floor((e-1)/(m+2a))`, not (C3). A proposed family must prove compatible parameters and interfaces before applying Corollary C3. No substitution `alpha=alpha(e)` into `O_alpha` occurs here.

For Walsh, even compatible near-critical child-volume estimates would leave a target-power local toll in the present proof. Proposition C4 identifies the additional scale-dependent routing or fusion obligation. The integer reduction also needs controlled permutations, coefficient streaming, precision and multiple layers; interchange alone discharges none of those obligations automatically.

## 7. Open next questions

1. **Near-critical local mass.** Construct a uniform binary reduction satisfying (C10), including reserve calls and padding. Measure total child bit volume divided by `V sqrt(m)`, not only a fixed-exponent saving.
2. **Polynomial local work and common space.** Can one streaming dispatcher execute the family in `V poly(m)` actual steps and `O(V)` visited cells, including regeneration across full-volume descents? Fixed-table existence does not settle this.
3. **Walsh routing toll.** Can address changes be fused across levels, or their normalized total made summable? A better child-call ratio alone leaves Proposition C4's obstruction.
4. **Alternative shrink law.** More aggressive shrinkage reduces toll-bearing depth, but setup and description costs must remain in the same complete budget. This is an architecture change, not free infinite arity.

## Credits and limits

Prepared for @CubeJerry with substantial OpenAI AI assistance. Credits to the November 24 OpenAI tape/Fourier manuscripts for recurrences and layouts, and Harvey–van der Hoeven–Lecerf for recurrence-product methodology. No old five-assumption construction is invoked. No Lean kernel proof, independent human review, or new end-to-end multiplication theorem is claimed.
