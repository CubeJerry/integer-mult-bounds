# The published interchange Gram form blocks ordinary-count repair in characteristic p

Status: **proved scoped obstruction**. This identifies a concrete incompatibility
between the characteristic-zero compact count evaluators and the *published*
two-level interchange label construction. It does not rule out the source
integral multivariate predictor, a different label family or Gram form, a
different repair program, or a different tape algorithm.

The lead proposed checking the rank of the binary distance-p graph. Route C
proved the exact rank below and strengthened the proposed central-window
collision argument to a bound for every function of the count modulo p.

## 1. The source construction

Pin: `openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`, tape manuscript
`build/interchange.tex`, Section "A family of labels", equation
`eq:interchange-gram`, and the contraction `eq:interchange-contraction`.

The data characteristic is an odd prime `p`. Put `h=2p-1`. The inner label
set is `[q]^h`, with `q >= 2`, and an inner pair is far when its Hamming
distance is p. An outer label has h inner coordinates. Let `k(v,w)` count
the coordinates in which the inner words are far. The rational Gram block
on the two generators at labels v,w is

\[
 G_{vw}=\left(1-\frac{k(v,w)}p\right)I_2+
                         \frac{k(v,w)}p\begin{pmatrix}0&1\\1&0\end{pmatrix}.
                                                               \tag{I1}
\]

The quotient dimension `D_route` is the rank of this rational Gram matrix.
The source reserves `a=D_route-2` fields on each side of its main fields.
Its sufficient recursive contraction for `1/2 < gamma < alpha < 1` is

\[
                         2m^\gamma+2a<m^\alpha.                  \tag{I2}
\]

The `2a` term is a bill of full-volume reserve calls, not an unused dimension
which can be dropped after paying for the main swaps.

## 2. Exact rank on binary labels

**Theorem I1.** For every odd prime p and every q >= 2, the Gram form (I1)
satisfies

\[
 \boxed{D_{\rm route}\ge (2p-1)(2^{2p-1}-1)+2.}                  \tag{I3}
\]

For q=2 equality holds.

### Step 1: all eigenvalues of the inner binary far graph are nonzero

Let `h=2p-1` and let A be the adjacency matrix on `{0,1}^h` joining words
at Hamming distance p. For a Walsh character indexed by a subset of size t,
its eigenvalue is the integer

\[
 K_p(t)=\sum_j(-1)^j{t\choose j}{h-t\choose p-j}.                 \tag{I4}
\]

Double-counting ordered pairs of subsets of sizes t and p, with weight
`(-1)^|intersection|`, gives

\[
 {h\choose t}K_p(t)={h\choose p}K_t(p).
\]

The generating polynomial for the right-hand factor is

\[
 \sum_{t=0}^{h}K_t(p)z^t
       =(1-z)^p(1+z)^{p-1}=(1-z)(1-z^2)^{p-1}.
\]

Consequently

\[
 \boxed{K_p(t)=\frac{{2p-1\choose p}}{{2p-1\choose t}}
       (-1)^{\lceil t/2\rceil}{p-1\choose\lfloor t/2\rfloor}\ne0.}  \tag{I5}
\]

This nonvanishing identity actually holds for every positive integer p.
Thus A has full rational rank `n_0=2^h`. Its constant-vector eigenvalue is
`a_0=binom(h,p)`.

### Step 2: outer tensor structure

Write J for the `n_0`-by-`n_0` all-ones matrix. On h outer coordinates,
the matrix of `k(v,w)` is

\[
 K=\sum_{i=1}^{h}J^{\otimes(i-1)}\otimes A\otimes J^{\otimes(h-i)}.
                                                               \tag{I6}
\]

In the tensor Walsh basis it has the following nonzero eigenspaces:

* the constant vector, with eigenvalue `h a_0 n_0^(h-1)`;
* tensors with exactly one nonconstant inner character, each with eigenvalue
  `n_0^(h-1)` times that character's nonzero eigenvalue of A.

All tensors with at least two nonconstant factors are killed. Hence
`rank(K)=1+h(n_0-1)`.

Changing the two-generator coordinate to its plus and minus combinations
splits the Gram form, up to nonzero scalar factors, into

\[
             J_{n_0^h}\quad\text{and}\quad J_{n_0^h}-(2/p)K.      \tag{I7}
\]

The first block has rank one. The second is nonzero on all `h(n_0-1)`
one-character directions. Its constant eigenvalue is

\[
               n_0^{h-1}\left(n_0-\frac{2h}p{h\choose p}\right).
\]

It is also nonzero. Otherwise `p 2^h=2h binom(h,p)`. Modulo p,
`h=-1` and `binom(2p-1,p)=1`, whereas the left side is zero; this would
give `0=-2` in the odd prime field. The binomial congruence follows by
taking the coefficient of `x^p` in
`(1+x)^(2p-1)=(1+x)^p(1+x)^(p-1)` modulo p.

Thus the total binary rank is exactly `h(n_0-1)+2`. For any q >= 2,
restrict every inner coordinate to two fixed letters. The resulting principal
submatrix is exactly this binary Gram form, and a submatrix cannot have higher
rank than the full matrix. This proves (I3). QED.

## 3. What the rank bound forces on valid source parameters

Combining (I2) and (I3) gives the necessary condition

\[
                2h(2^h-1)<m^\alpha.                             \tag{I8}
\]

In particular `h+log_2 h < alpha log_2 m` and hence

\[
                  p<\frac\alpha2\log_2 m+\frac12.                \tag{I9}
\]

There is also a useful finite implication. Since `alpha<1` and `m>1`,

\[
        m>2a\ge2h(2^h-1)\ge2h^2>p^2.                            \tag{I10}
\]

Thus every parameter choice satisfying the source contraction has `m>p^2`.
The dependence on p hidden in `D_route=O_p(q^(2p-1))` cannot be treated as
uniform when p grows. Already at q=2 its unavoidable size is exponential in p.

The natural refinement using the full child arity `m+2a` does not rescue a
choice with `a >> m`: the full-volume reserve bill `2a` is then asymptotic
to that arity, and cannot be below its alpha-th power for fixed alpha<1.
This is an observation about the source reserve mechanism, not a lower bound
on other ways to perform interchange.

## 4. Every count-residue function has many defects when m >= p^2

The simple collision warning says that if a central count interval contains
both c and c+p, then no function of c modulo p can equal parity on both:
the two target signs differ because p is odd. A stronger statement removes
the requirement of a central interval and the polynomial-degree restriction.

Let `C ~ Bin(m,1/2)`, with `p >= 3` odd. For *any* function of the residue
`C mod p`, taking values in a characteristic-p field or algebra, define exact
agreement with the two distinct values `(-1)^C`. Set

\[
 A_r=\Pr[C\equiv r\pmod{2p}],\qquad
 \Delta=\sum_{r=0}^{p-1}|A_r-A_{r+p}|.
\]

The best possible agreement is exactly `(1+Delta)/2`: for each residue
modulo p one chooses the more likely of its two parity classes. A value other
than `1` or `-1` cannot improve agreement.

**Theorem I2.** Put `a=pi^2 m/(4p^2)`. Then

\[
 \Delta\le\left(\frac{2e^{-a}}{1-e^{-8a}}\right)^{1/2}.           \tag{I11}
\]

In particular, if `m>=p^2`, every count-residue function has exceptional
fraction strictly greater than `1/4`.

### Proof

Let `omega=exp(pi i/p)` and
`phi_j=((1+omega^j)/2)^m`. Fourier inversion modulo `2p` gives

\[
 A_r-A_{r+p}=\frac1p\sum_{\substack{0\le j<2p\\j\ {
m odd}}}
                                      \phi_j\omega^{-jr}.
\]

As functions of `r=0,...,p-1`, these p odd-frequency characters are orthogonal
(a common unimodular factor times the ordinary p-point character basis).
Parseval followed by Cauchy--Schwarz therefore gives

\[
 \Delta^2\le\sum_{j\ {
m odd}}|\phi_j|^2
          =\sum_{j\ {
m odd}}|\cos(\pi j/(2p))|^{2m}.
\]

The central term `j=p` is zero. Pair the other terms around it. The inequality
`cos x <= exp(-x^2/2)` for `0<=x<pi/2` follows by differentiating
`log cos x + x^2/2`. Hence

\[
 \Delta^2\le2\sum_{l\ge0}e^{-a(2l+1)^2}
       \le\frac{2e^{-a}}{1-e^{-8a}},
\]

using `(2l+1)^2 >= 1+8l`. This proves (I11).

If `m>=p^2`, then `a>=pi^2/4>9/4`. We have `e^(9/4)>9` by the first six
terms of its positive power series, and `e^18>9`. Thus
`8e^(-9/4)<8/9<1-e^(-18)`, implying the bound in (I11) is strictly less
than `1/2`. Agreement is therefore less than `3/4`, and the exceptional
fraction is greater than `1/4`. QED.

The argument applies to a mixture of shifts and different count-residue
functions on different rows. Average over all Boolean sign patterns k;
`|k XOR beta|` is binomial for every fixed beta. Therefore some frequency
has weighted exceptional fraction greater than `1/4` whenever `m>=p^2`.
The interchange source explicitly realizes all `2^m` sign patterns by choosing
sum or difference coordinates independently on a two-point orbit of each swap.

## 5. Combined obstruction and its limits

**Corollary I3.** With the published Gram form (I1) and any parameters satisfying
the published sublinear contraction (I2), no diagonal shifted predictor whose
row value is a function only of the ordinary count modulo p can have a
per-frequency exceptional fraction at most `1/4`.

Proof: (I10) puts every such parameter choice in the range of Theorem I2,
and the shift-averaging argument produces a violating frequency. QED.

This rules out directly importing either a rare-tail characteristic-zero
count polynomial or the new constant-tail `1/16` count predictor into that
finite-characteristic architecture. Merely choosing `p>D_count` to make the
Newton divisions legal cannot work: it changes the Gram dimension and
violates the source's reserve budget before producing the claimed contraction.

There is no contradiction with the source theorem. Its integral multivariate
predictor retains divided-power information which is not determined by the
ordinary count modulo p. For example `binom(c,p) mod p` distinguishes c=0
from c=p although those counts have the same residue. The source's generic
linearization can preserve that information. A genuinely different compact
finite-characteristic evaluator, a different rational Gram form or labels,
or a repair method tolerating the resulting larger defect is outside this
obstruction and remains a valid research direction.

## 6. Verification, provenance, and next question

Run `python3 -B research/moonshot-overhead-program/routes/C/verify_interchange_obstruction.py`.
The verifier checks the exact Krawtchouk identity and all its nonzero factors,
the constant-eigenvalue congruence, small exact matrix spectra, exact optimum
count-residue agreement, and the finite implications of the contraction.
It never materializes the enormous outer label matrix. Tests complement the
proof; no full tape implementation or formal-kernel verification is claimed.

Attribution: OpenAI's November 24 tape manuscript and its cited label/routing
predecessors supply the construction. The binary restriction/rank question
was proposed by the lead; Route C derived the full eigenvalue proof and the
finite count-residue obstruction. These are AI-assisted programme results
for @CubeJerry. General Krawtchouk diagonalization and finite-cycle Fourier
analysis are standard mathematics; literature novelty beyond this application
has not been established.

**Open next question.** Can one compactly evaluate the required divided-power
predictor over the fixed odd-characteristic data algebra, at full rate, while
preserving the source's rational layout identities and bounded reserve cost?
This is a more precise bridge obligation than "increase the characteristic"
or "reduce the rational coefficients modulo p".
