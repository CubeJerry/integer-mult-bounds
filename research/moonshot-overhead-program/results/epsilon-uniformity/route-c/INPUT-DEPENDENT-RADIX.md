# Input-dependent compatible radices with constant padding volume

Status: **proved arithmetic/preparation lemma using an established prime-interval theorem; full uniform tape implementation still open**.

The fixed-radix obstruction in `SOURCE-PADDING-BARRIER.md` does not apply when the radix is chosen from the input width. This note proves a concrete way to obtain such a radix, with integer tests, forbidden-prime avoidance and a charged search. It does not treat a growing radix as a free finite-state alphabet or an already compiled tape routine.

## 1. Source and external theorem

OpenAI tape manuscript pin: `openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`. The relevant source operations are the compatible-radix choice and final binary-range padding in `build/interchange.tex`, `thm:interchange`. The manuscript already invokes a weaker consequence of Baker–Harman–Pintz in `build/integers.tex`, `eq:integer-box`.

R. C. Baker, G. Harman and J. Pintz, *The difference between consecutive primes, II*, Proc. London Math. Soc. (3) **83** (2001), 532–562, Theorem 1, proves the eventual presence of a prime in `[y-y^0.525,y]`. We use only `[y-y^(3/5),y]`. The primary theorem and its effectivity comment were read in the [paper](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/BakerHarmanPintz.pdf). Its absolute threshold is not numerically supplied here; the paper says it could be made effective. This session has not reverified its analytic-number-theory proof.

Let `B_0` be a fixed absolute threshold above which the weaker `3/5` statement holds.

## 2. A narrow interval contains a compatible prime

Let `u,f,W` be positive integers, `f>=4`. Let `Q` be a nonzero integer such that a prime is compatible whenever it does not divide `Q`; the required nonzero rational numerators and denominators may be multiplied into such a `Q`. Let `K>=0` bound the number of distinct prime divisors of `Q`. Define, using integer root extraction,

\[
 B=\lceil2^{u/f}\rceil,\qquad H=\lfloor B/(2f)\rfloor. \tag{R1}
\]

Assume

\[
 B>W,\qquad B\ge4f+4,\qquad B\ge B_0,\qquad
 B^2\ge[16(K+1)f]^5. \tag{R2}
\]

All conditions except the absolute analytic threshold are exact integer tests.

**Lemma R1.** The integer interval `[B,B+H]` contains a prime `b` not dividing `Q`. Any such `b` satisfies

\[
 b>W,\qquad 2^u\le b^f<3\,2^u. \tag{R3}
\]

Thus padding two binary ranges to `b^f` increases their combined volume by less than nine, uniformly in every parameter.

**Proof: prime supply.** Put `S=ceil((2B)^(3/5))+1`. Since `B>=1`, `S<=4B^(3/5)`. Also `H>=B/(4f)`. Condition (R2) implies `B^(2/5)>=16(K+1)f`, and therefore

\[
 (K+1)S\le4(K+1)B^{3/5}\le B/(4f)\le H.
\]

For `j=1,...,K+1`, let `y_j=B+jS`. These endpoints lie in `[B,B+H]`, and `y_j<=2B`. The short-prime intervals `[y_j-y_j^(3/5),y_j]` lie inside `[B,B+H]`. Their lengths are strictly less than `S`, so they are pairwise disjoint. Since their right endpoints exceed the absolute threshold, they supply `K+1` distinct primes. At most `K` divide `Q`, proving existence.

**Proof: volume.** Write `R=2^(u/f)`. We have `R<=B<R+1`. Every permitted `b` satisfies

\[
 b\le B+B/(2f)<R+1+(R+1)/(2f)\le R(1+1/f),
\]

because `B>=4f+4` implies `R>2f+1`. Hence

\[
 2^u\le b^f\le2^u(1+1/f)^f<3\,2^u.
\]

The final inequality follows from the binomial expansion bounded by `sum_(j>=0)1/j!<3`. Squaring proves the two-field volume bound. ∎

## 3. Deterministic search with its costs exposed

The algorithm computes `B,H` exactly, then tests integers in `[B,B+H]` in order. Test primality by division through the integer square root. For a prime candidate, test `gcd(b,Q)=1`, and return the first success. No factorization of `Q` is required. If the finite interval is exhausted, return a failure flag; callers can use a correct fallback. Every successful output is checked independently of the asymptotic prime theorem.

Let `S_Q=max(1,bitlength(abs(Q)))`. Elementary fixed-tape integer arithmetic gives total search time

\[
 O\left([B^{3/2}+(K+1)S_Q]\operatorname{poly}(u+1)\right) \tag{R4}
\]

and `O(S_Q+poly(u+1))` work cells. The polynomial has a fixed degree. The first term counts at most `O(B)` candidates and `O(sqrt(B))` divisions per candidate. Only prime candidates need a compatibility test; before success at most `K` can be rejected. Compute `Q mod b` by a sequential binary remainder scan, then use the Euclidean algorithm on `O(u)`-bit numbers. This costs `S_Q poly(u+1)` per checked prime. Integer root extraction and control are polynomial in `u`, using schoolbook arithmetic; no near-root multiplier is assumed.

Since `f>=4`,

\[
 B\le2^{u/4}+1,\qquad B^{3/2}=O(2^{3u/8}). \tag{R5}
\]

The compatibility term in (R4) must not disappear. A compact bad-prime count does not imply a compact description of the integers whose prime divisors are forbidden.

### A fully computable conservative choice

Take `K=S_Q`, a valid upper bound for the number of distinct prime factors. If (R2) holds with this value, then `S_Q+1<=B^(2/5)/(16f)`. Consequently `(K+1)S_Q=O(B^(4/5))`, and (R4) reduces to

\[
 O(2^{3u/8}\operatorname{poly}(u+1)). \tag{R6}
\]

For the source interchange stream, `V>=2^(2u)`, so this search is `o(V)` and uses `o(V)` cells. The lemma charges access to the supplied compatibility product; creating the rational matrices and that product remains a separate template-generation expense.

Define integer bit lengths `w=bitlength(W)`, `s=bitlength(S_Q)`, `z=bitlength(u)`, and

\[
 t=w+3s+3z+10,\qquad f=\lfloor u/t\rfloor. \tag{R7}
\]

If `u>=4t`, then `f>=4`. Moreover `2^t>=1024(W+1)(S_Q+1)^3(u+1)^3`, so `B>=2^t` implies every algebraic condition in (R2) with `K=S_Q`. The absolute threshold `B>=B_0` also holds for all sufficiently large `u`, uniformly over the other parameters that pass the test. The algorithm need not know `B_0`; it searches the interval and validates a found prime, or reports failure.

For fixed `W,Q`, the test `u>=4t` eventually succeeds because `t=O(log u)` plus a fixed constant. For varying templates it exposes the actual requirement on `log W` and `log S_Q` instead of hiding it in a fixed-template threshold.

## 4. Padding loss can also be made summably small

Constant volume overhead is sufficient for a space bound, but a constant loss repeated at growing recursion depth can spoil an endpoint. The same argument permits a prescribed small loss.

**Lemma R2.** Let an integer `h>=1` specify the reciprocal slack. Retain `B=ceil(2^(u/f))`, `f>=4`, but use

\[
 H_h=\lfloor B/(4fh)\rfloor.
\]

If

\[
 B\ge B_0,\quad B\ge8fh+2,\quad B\ge(W+1)h,\quad
 B^2\ge[32(K+1)fh]^5, \tag{R8}
\]

then `[B,B+H_h]` contains a compatible prime `b`, and

\[
 1\le b^f/2^u\le1+1/h. \tag{R9}
\]

Two-field padding is at most `(1+1/h)^2`. The source's first-digit batch factor is also less than `1+1/h` because `b>=Wh`. Their product is at most `(1+1/h)^3<=1+7/h`.

**Proof.** As before choose `S=ceil((2B)^(3/5))+1<=4B^(3/5)`. Now `H_h>=B/(8fh)`, and (R8) implies `(K+1)S<=H_h`. The same disjoint prime intervals supply a compatible prime. With `R=2^(u/f)`,

\[
 b\le B+B/(4fh)<R+1+(R+1)/(4fh)\le R(1+1/(2fh)),
\]

using `R>B-1>=8fh+1`. The binomial/geometric comparison gives

\[
 (1+1/(2fh))^f
 \le\sum_{j=0}^f(1/(2h))^j
 <\frac{2h}{2h-1}\le1+1/h.
\]

This proves (R9); the remaining statements follow from the exact first-digit factor `W ceil(b/W)/b<1+W/b`. ∎

For the conservative choice `K=S_Q`, the same preparation bound (R6) holds. A computable sufficient selector replaces (R7) by

\[
 t=\operatorname{bitlength}(W)+3\operatorname{bitlength}(S_Q)
   +3\operatorname{bitlength}(u)+3\operatorname{bitlength}(h)+13,
 \qquad f=\lfloor u/t\rfloor, \tag{R10}
\]

again with the check `u>=4t` and the same absolute eventual prime threshold. Indeed `B>=2^t>=8192(W+1)(S_Q+1)^3(u+1)^3(h+1)^3`; squaring verifies (R8), since `32^5=2^25<8192^2`. The other inequalities follow directly. Input-dependent `h` is therefore charged through its description and the applicability test.

For example, a caller using a power-decreasing active width can choose `h` of order `(log log m)^2`. These padding losses then satisfy the summable-excess condition in Theorem C2 of the recurrence note. This only pays for padding; the core call mass and all other local costs still require their own bounds.

## 5. Why this does not finish the endpoint construction

The lemma replaces a nonuniform **volume expansion** by a uniform constant and supplies a sufficiently cheap compatible-prime search, provided the explicit size test is met. This removes the particular obstruction in Theorem P2 of the companion note. It does not establish the remaining source operations uniformly when `b` varies with input width:

- The radix is runtime data. Its digits, counters and arithmetic must be implemented over a fixed physical alphabet with charged scans.
- The finite rational address maps must act modulo `b^f` with a joint cost bound on coefficient heights, increasing pieces, counter work and instruction interpretation.
- Recursive levels need a consistent radix/interface; changing it again inside children may introduce another conversion cost.
- The source's growing scalar extension, live streams and stored descriptions still need one common visited-cell constant.
- Main-call mass, reserve costs and the Walsh routing toll remain independent obligations.

Accordingly, this is a proved preparation lemma and a concrete repair to one scoped obstruction, not a new `O(n sqrt(log n))` or polylog-log-overhead multiplication theorem.

## Open next question and credits

Can the source's ordered affine address maps be executed by one fixed binary tape dispatcher with local cost polynomial in the template description and `log b`, while maintaining the constant padding volume from this lemma? That is the next required bridge.

Prepared for @CubeJerry with substantial OpenAI AI assistance. The input-dependent-radix proposal was supplied by the lead researcher in this session; the integer proof, compatibility accounting and explicit preparation bound were developed on Route C. Credits to the OpenAI tape construction and Baker–Harman–Pintz for the external prime theorem. No full-kernel or human verification is claimed.
