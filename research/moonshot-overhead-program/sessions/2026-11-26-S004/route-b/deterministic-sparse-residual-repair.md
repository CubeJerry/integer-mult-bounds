# Deterministic recovery of a sparse ordinary convolution residual

Checkpoint disposition: R1 admitted after A/C/lead review under the explicit sparsity promise. See `lead/FIRST-WAVE-ADMISSION.md` relative to the session root.

Status: **proved component algorithm, pending independent physical review**.
The algorithm uses a promised bound on the number of erroneous ordinary
coefficients. Their positions are unknown. No algorithm producing a fast
candidate with this promise is supplied, so there is no new complete
multiplication overhead bound.

This route changes the repair interface: it corrects ordinary convolution
coefficients by short modular products and sparse interpolation, rather than
converting spectral check rows of a low-degree predictor. The derivative
ratio is established sparse-interpolation mathematics, not a new invention.
The contribution here is an elementary deterministic all-moduli construction,
its packed integer/tape implementation, and an explicit statement of when
its cost lies below the square-root logarithmic multiplication target.

## 1. Input, promise, and quantitative theorem

Let `h>=1`, `b>=1`, and `D=2h`. The inputs are

\[
 A(X)=\sum_{i<h}a_iX^i,\qquad B(X)=\sum_{i<h}b_iX^i,
 \qquad 0\le a_i,b_i<2^b,
\]

and an integer candidate `C(X)` of degree below `D`, with coefficients
`|c_i|<=Cmax`. A known integer `s`, `1<=s<=D`, supplies the promise

\[
 E(X):=A(X)B(X)-C(X)\quad\hbox{has at most }s\hbox{ nonzero terms}.
                                                               \tag{1}
\]

The coefficient positions and values of `E` are unknown. The height bound

\[
 Emax=h2^{2b}+Cmax
\]

is valid without any accuracy assumption on the candidate. Define

\[
 \begin{aligned}
 q&=\lceil\log_2 D\rceil, & B_*&={2s\choose2}q, & K&=2B_*+4,\\
 R&=2^\beta>8D(s+1)(Emax+1),
 & k&=\beta K(K+1)/2.
 \end{aligned}                                                   \tag{2}
\]

Choose the least integer `beta` satisfying the strict inequality. All
parameters can be calculated by integer arithmetic and bit lengths.
Let `V=D beta`; this bounds the bit volume of the packed coefficient
streams up to an absolute constant. Since `s<=D`,

\[
 K=O(s^2\log(D+1)),\quad
 \beta=O(b+\log(D+1)+\log(Cmax+2)),\quad
 k=O(\beta s^4\log^2(D+1)).                                     \tag{3}
\]

**Theorem R1.** Fix any `alpha>1/2` and a fixed exact finite-alphabet
multitape multiplication routine of time `O(u(1+log_2 u)^alpha)` and
visited space `O(u)`. Under promise (1), there is a deterministic fixed
finite-alphabet multitape algorithm that recovers `E` and all exact
coefficients of `AB`, with time

\[
 O_\alpha\!\left(V(1+\log_2(k+1))^\alpha+k^6\right)              \tag{4}
\]

and a single `O(V)` bound on cells ever visited. The constants do not depend
on `h,b,s,Cmax`. The alphabet and number of tapes are fixed. Correct carry
recovery then gives the exact product of the original base-`2^b` integers
in another `O(V)` steps.

The source tape theorem supplies the fixed multiplication routine in this
statement, for each fixed `alpha>1/2`. This use is on much shorter integers.
One may instead insert a classical fixed-tape multiplication bound; the
corrector remains useful in the small-sparsity regime. Formula (4) is a
component bound, not a new multiplier construction.

For `s=0`, the promise already says `C=AB`, so only the output scan is
needed. If a supplied `s` exceeds `D`, replace it by `D`.

## 2. A deterministic collision-free family without prime selection

**Lemma R2.** For every set `S` of at most `2s` distinct integers in
`[0,D)`, some integer `ell`, `1<=ell<=K`, makes the residues of the
elements of `S` pairwise distinct modulo `ell`.

### Proof

If `|S|<=1`, use `ell=1`. Otherwise form the positive integer

\[
 \Delta_S=\prod_{u<v,\ u,v\in S}|u-v|<D^{\binom{2s}{2}}
                                      \le 2^{B_*}.
\]

If every `ell<=K` divides `Delta_S`, then
`lcm(1,...,K)` divides it. But

\[
 \operatorname{lcm}(1,\ldots,K)\ge \frac{2^{K-1}}K>2^{B_*}.       \tag{5}
\]

For completeness, every binomial coefficient `binom(K-1,j)` divides this
lcm: for a prime `p`, the factorial valuation formula expresses its
valuation as a sum of zeros and ones over at most `floor(log_p K)`
nonzero terms. This is no larger than the valuation of the lcm. The
largest coefficient is at least the average `2^(K-1)/K`, proving the
first inequality. The second follows from `K=2B_*+4` and
`2^(B_*+3)>2B_*+4`, valid for every `B_*>=0`.

Thus some `ell<=K` does not divide `Delta_S`. Such an `ell` cannot divide
any nonzero difference in `S`, and is collision-free. QED.

This family is deliberately coarse. It avoids a prime-distribution theorem,
randomness, and the need to know the support in advance. The algorithm never
constructs the unknown integer `Delta_S`; it tries the explicitly bounded
family of lengths.

## 3. Cyclic residues and balanced radix decoding

Write `Theta=X d/dX` for the Euler derivative. For every `ell<=K`, let

\[
 M_\ell=R^\ell-1,\qquad M=\prod_{\ell=1}^K M_\ell.               \tag{6}
\]

These integer moduli need not be coprime. The construction uses only the
divisibility `M_ell | M`, never a Chinese remainder reconstruction.

If

\[
 E^{[\ell]}(X)=E(X)\bmod(X^\ell-1)
             =\sum_{j<\ell} u_{\ell,j}X^j,
\]

and similarly `(Theta E)^[ell]=sum_j v_(ell,j) X^j`, then

\[
 |u_{\ell,j}|\le sEmax,
 \qquad |v_{\ell,j}|\le DsEmax<R/8.                             \tag{7}
\]

These inequalities hold even when many error terms collide. Hence

\[
 \left|E^{[\ell]}(R)\right|,
 \left|(\Theta E)^{[\ell]}(R)\right|
 \le DsEmax\frac{R^\ell-1}{R-1}<M_\ell/2.                        \tag{8}
\]

Taking the centered representative of `E(R) mod M_ell` therefore returns
the exact signed integer `E^[ell](R)`, and likewise for the derivative.
Repeatedly take a balanced remainder modulo `R`, in `[-R/2,R/2)`, and
divide the difference by `R`. This recovers all `ell` signed coefficients
exactly, because each true coefficient has absolute value below `R/8`.
No carry can be mistaken for a coefficient. For `ell=1`, the same proof
works with the modulus `R-1`.

The packed derivative values are obtained using the exact product rule

\[
 \Theta E=(\Theta A)B+A(\Theta B)-\Theta C.                      \tag{9}
\]

Thus a fixed number of modular products and long-stream reductions yields
both `E(R) mod M` and `(Theta E)(R) mod M`. Reducing these two short residues
modulo each `M_ell` supplies every pair of folds. This is the point of the
product modulus: the input of volume `V` is scanned only a constant number
of times, rather than once for every `ell`.

## 4. Recovering unknown positions and checking the sparse candidate

For each `ell=1,...,K`, decode `u_(ell,j),v_(ell,j)` as above.

If `u_(ell,j)=0` but `v_(ell,j)!=0`, reject this length. For every nonzero
`u_(ell,j)`, require that

\[
 e_j=v_{\ell,j}/u_{\ell,j}
\]

be an integer in `[0,D)`, satisfy `e_j mod ell=j`, and have
`|u_(ell,j)|<=Emax`. Form

\[
 E_\ell(X)=\sum_{j:\,u_{\ell,j}\ne0}u_{\ell,j}X^{e_j}.           \tag{10}
\]

Reject it if it has more than `s` terms. Finally accept it only if

\[
                         E_\ell(R)\equiv E(R)\pmod M.           \tag{11}
\]

At a collision-free length for the true support, each nonzero fold
coefficient is `c`, its derivative coefficient is `e c`, and the ratio is
the true exponent. Such a length exists by Lemma R2, so the correct
candidate is eventually generated.

The acceptance check is sound **under the sparsity promise**. Suppose a
candidate passes (11). The difference `H=E-E_ell` has at most `2s` terms,
degree below `D`, and height at most `2Emax`. If it were nonzero, Lemma R2
would provide a length `a<=K` separating its support. Since `M_a|M`,
`H(R)=0 mod M_a`. Its folded coefficients have absolute value at most
`2sEmax`, so the same centered-radix argument implies that its fold is
identically zero. This contradicts support separation. Hence `H=0`.

This argument handles arbitrary signs, cancellation within a bad fold,
accidentally integral ratios at a collision, and colliding terms whose
coefficient sum is zero. The derivative is used to *generate* a candidate;
the sparse injectivity check establishes its uniqueness.

Once the candidate is recovered, sort its at most `s` exponents, scan the
ordinary candidate coefficient stream, and add corrections at the indicated
positions. The result is exactly `AB`. The final carry pass uses the
original radix `2^b`, not the larger probing radix `R`.

## 5. Charged physical implementation

The following accounting concerns actual fixed-tape bit operations. It does
not assign constant cost to word arithmetic, exponentiation, or a modulus
whose description grows.

### 5.1 Preparing short data

The modulus `M` has fewer than `k` bits by (2) and (6). Its `K` factors,
their product, and all loop bounds are constructible with grade-school
integer arithmetic in `O(k^4)` steps and `O(k)` reused cells. The deliberately
looser `k^6` term will cover all short-data work below. Nested loops use
binary counters whose head movements and resets are included in that bound.

### 5.2 Reducing a long integer modulo M

Take block width `k`, and precompute

\[
                  \mu=\left\lfloor\frac{2^{2k}}M\right\rfloor.
\]

This needs `O(k^2)` steps and `O(k)` cells by exact long division. Given
`0<=u<M 2^k<2^(2k)`, put

\[
 q_0=\left\lfloor\frac{u\mu}{2^{2k}}\right\rfloor.
\]

Then `floor(u/M)-1<=q_0<=floor(u/M)`: replacing `1/M` by
`mu/2^(2k)` introduces an error less than `u/2^(2k)<1`. Consequently
`u-q_0 M` is in `[0,2M)`, and one comparison/subtraction gives `u mod M`.
All numbers in these operations have `O(k)` bits; the reciprocal can have
up to `2k` bits, which remains within that bound.

Process a long stream from its most significant block. If its previous
remainder is `y<M` and its next block is `z<2^k`, use
`u=y 2^k+z`. Two short multiplications and a fixed number of scans suffice
per block. For a stream of `O(V)` bits this costs

\[
              O_\alpha\bigl((V+k)(1+\log(k+1))^\alpha\bigr).      \tag{12}
\]

The `O(k)` allowance for the last incomplete block is absorbed into the
short-data term. Inputs, remainder, reciprocal, product workspace and output
remain on a fixed number of tapes. Rewinding their `O(k)`-bit regions per
block is included in (12); the long input is streamed sequentially.

### 5.3 Forming the weighted coefficient streams

The Euler streams have coefficients `i a_i`, `i b_i`, and `i c_i`.
These are not unit-cost operations. Their magnitudes fit `O(beta)` bits
under (2). Compute every weighted coefficient with the same fixed short
multiplier, at cost `O_alpha(beta(1+log(beta+1))^alpha)` each. Updating and
rewinding the index counter costs `O(beta)` per coefficient and is included.

Thus forming all weighted streams costs

\[
       O_\alpha\bigl(V(1+\log(\beta+1))^\alpha\bigr),             \tag{13}
\]

which is bounded by the first term in (4), since `beta<=k`.
Unsigned coefficients are padded to `beta` bits and concatenated in reverse
coefficient order, producing exactly the base-`R` evaluation. For signed
candidate/derivative coefficients, split into nonnegative positive and
negative parts, process both streams, and subtract their modular residues.
This adds only a fixed number of scans and streams. The radix inequality
ensures every individual coefficient fits its record.

Equations (9), (12), and (13) now give the two error residues modulo `M`
using a fixed number of long reductions and short modular multiplications.
No evaluation at a general large integer is treated as a free black box.

### 5.4 Decoding and validating short candidates

Process lengths sequentially. A modulus `M_ell` has at most `k` bits.
Grade-school reduction of each saved residue, balanced decoding, and exact
ratio calculations have polynomial `k` cost. A candidate has at most `s`
terms. Evaluate each `R^e mod M` by repeated squaring with `O(log D)`
short modular multiplications, using grade-school arithmetic if necessary
for the coarse bound. Since `K,s,log D<=O(k)`, all candidates together
cost `O(k^6)` steps. Only one candidate, one current fold pair, and a fixed
number of `O(k)`-bit accumulators are live.

Sorting the accepted support and merging it into the output uses
`poly(k)+O(V)` steps. Carry propagation has `O(beta)`-bit carries and costs
`O(V)` by sequential scans. This establishes (4).

### 5.5 A common visited-cell cap

If `k<=V`, the stored input/candidate streams and the reused short-data
areas occupy `O(V+k)=O(V)` cells. A constant number of streams are live;
no `K` separate copies of the long input or all candidate lists are retained.
The chosen fixed short multiplier has its own `O(k)` visited-cell guarantee.
All work areas start at marked origins, are cleared and reused, and their
heads return before reuse. This bounds the union of visited cells.

If `k>V`, bypass the modular construction and multiply the two packed
base-`R` integers by schoolbook multiplication. Since `R` exceeds every
true convolution coefficient, their radix digits recover `AB` directly.
This costs `O(V^2)` time and `O(V)` visited cells, and `V^2<k^6` in this
case. The fallback therefore preserves both (4) and the common space bound
at every length. No parameter-dependent number of tapes is needed.

## 6. Consequences at the multiplication scale

Suppose the input integers have `n` bits and are packed into
`h=Theta(n/log n)` digits with `b=Theta(log n)`. Suppose also that the
integer candidate coefficients have `O(log n)` bits. Then `V=Theta(n)`
whenever `s<=D`, because `beta=Theta(log n)`.

### Polylogarithmically many wrong coefficients

For every fixed `a>=0`, if `s<=(log n)^a`, then `k` is a fixed power of
`log n`, so `k^6=o(n)`. Choosing the fixed source routine with
`alpha=3/4` gives

\[
 T_{\rm repair}(n)
       =O_a\bigl(n(1+\log\log n)^{3/4}\bigr)
       =o(n\sqrt{\log n}),                                    \tag{14}
\]

with uniform `O(n)` visited space for this fixed family. This corrects
unknown positions; their identification does not require another full
length multiplication.

### A wider subpolynomial error regime

Fix `0<tau<1`. If `s<=2^{(log_2 n)^tau}`, then
`log k=O((log n)^tau)` and `k^6=n^{o(1)}`. Choose the fixed
`alpha=(1+tau)/(4tau)>1/2`. Formula (4) gives

\[
 T_{\rm repair}(n)=O_\tau(n(\log n)^{(1+\tau)/4})
                         =o(n\sqrt{\log n}).                    \tag{15}
\]

This is asserted for each fixed `tau`; it does not substitute an
uncontrolled growing parameter into `O_tau`. Small lengths use the
explicit fallback. The constants and eventual crossover are not numerically
evaluated.

Equations (14)–(15) show that such sparse ordinary errors could be corrected
below the target main cost. They do not establish that a candidate with
those guarantees can be computed at that main cost. Assuming such a
candidate as a black box would mostly restate the hard part of the problem,
so this note does not advertise a new conditional overhead theorem.

## 7. Why this is not a general product certificate

Promise (1) cannot be removed from the soundness argument. With the finite
family of lengths fixed, put

\[
 J(X)=\prod_{\ell=1}^K(X^\ell-1),\qquad F(X)=J(X)^2.              \tag{16}
\]

The nonzero polynomial `F` and its Euler derivative both vanish modulo
every `X^ell-1`. In the packed representation,

\[
 F(R)=M^2\equiv0\pmod M,
 \qquad (\Theta F)(R)=2J(R)(\Theta J)(R)\equiv0\pmod M.           \tag{17}
\]

When `D>K(K+1)`, this is a degree-below-`D` error that fools every value
and derivative probe. Its coefficient height is at most `4^K`, and a
sufficient coefficient bound accommodates it. It has more terms than a
promised small-sparse residual can have, exactly as the uniqueness theorem
requires. A routine supplied with a false sparsity promise could return an
incorrect candidate; this is not a Las Vegas or generally sound product
verifier.

The next construction must prove its residual sparsity, or provide a
separately sound certificate of that property. Finite modular agreement
alone cannot supply it.

## 8. Why repair-free polynomial prediction does not supply the promise

The companion `spectral-rank-barrier.md`, Corollary B4, gives a direct
obstruction. A support-degree-`<m` predictor of a product of coordinate
translations, followed by any coordinatewise decoder, omits the correct
target input variable at each ordinary output coordinate. On independent
binary input bits, each decoded output has error probability at least one
half. Some input therefore has at least half of all ordinary outputs wrong.

Thus deleting spectral repair from that route does not leave a sparse
ordinary residual to which Theorem R1 applies. The positive correction
algorithm and this negative bridge test are compatible: they isolate a
different candidate-construction problem instead of silently reusing an
inapplicable approximation guarantee.

## 9. Sources and provenance

Read primary source: Pascal Giorgi, Bruno Grenet, Armelle Perret du Cray,
Daniel S. Roche, *Fast interpolation and multiplication of unbalanced
polynomials* (February 20, 2024),
https://www-verimag.imag.fr/~grenetb/publis/GGPR24.pdf.
The relevant read chain is Sections 2.2–2.4 (modular reductions, derivative
black boxes, and product differentiation), Section 3 (collisions and
coefficient/exponent recovery), and its related-work account. The derivative
coefficient ratio and modular sparse-interpolation viewpoint belong to this
established literature. That paper's principal algorithms are randomized;
no deterministic fixed-tape theorem is imported from those statements.

Additional primary lead: Qiao-Long Huang, *Sparse Polynomial Interpolation
Based on Derivative*, arXiv:2002.03708, Journal of Symbolic Computation 114
(2023), DOI https://doi.org/10.1016/j.jsc.2022.06.002. Its exact full text
remains a staged read in this session; it is not used as an unexamined
black-box hypothesis.

The short multiplication subroutine is the upper bound in the pinned
OpenAI November 24 tape paper at
`3344da59991ed94f9ba711217b29c1d760badfa6`. Weak ETH is not an assumption
of this corrector. The reciprocal reduction proof is given explicitly;
the general technique is standard Barrett-style modular reduction.

Research for @CubeJerry, with substantial ChatGPT assistance. Root identified
the need to charge derivative-record formation, maintain balanced radix
injectivity, and separate sparse recovery from a general verifier. No claim
of exhaustive literature novelty, formal-kernel verification, or a new
complete multiplication algorithm is made.

## Open next questions

1. Construct a genuinely faster candidate with a proved subpolynomial
   ordinary residual. The companion dense-error obstruction rules out one
   tempting low-degree/rounding shortcut, not every representation.
2. Reduce the coarse `s^4` short-modulus profile while preserving
   determinism, fixed tapes, signed coefficient recovery, and a proof of
   sparse uniqueness. This matters only after a candidate construction
   identifies the required sparsity scale.
3. Find a cheaply checkable structural invariant that certifies residual
   sparsity without already computing the residual densely. A finite list
   of modular equalities by itself cannot do this, as (16)–(17) show.
