# Which finite-template quantities affect constants and thresholds?

Status: **proved generic inequalities and source-interface extraction**.
This note does not bound the actual source template sizes. It explains how to
use those bounds once proved, without unnecessarily multiplying fixed setup
expenses into every input bit.

Source pin throughout: `openai/math`
`3344da59991ed94f9ba711217b29c1d760badfa6`; tape manuscript `build/integers.tex`,
`build/walsh.tex`, `build/permutations.tex`, and `build/uniformity.tex`.

## 1. Polylogarithmic losses need not create a huge cutoff

The source controlled-block permutation bound is
`O_rho(V(1+k)^rho(1+log k)^3)+k^{O_rho(1)}`. The integer reduction has
`O(log k)` layers. Its assembled visible loss is therefore a fourth power of
`1+log k`, in addition to candidate-dependent constants and polynomial setup.
The Walsh bound itself has only one such factor. This is a source-specific
inspection, not a claim that all unspecified constants have been bounded.

For an integer `b>=0`, real `0<epsilon<=1`, and real `s>=0`,

\[
(1+s)^b\le 2^\epsilon
\left(\max\{1,b/(e\epsilon\ln2)\}\right)^b2^{\epsilon s}. \tag{P1}
\]

For `b=0` interpret the right-hand constant as at least 1. To prove it set
`x=1+s>=1`; `x^b exp(-epsilon ln(2) x)` attains its unconstrained maximum at
`x=b/(epsilon ln2)` when `b>0`. Multiplication by `2^epsilon` gives (P1),
with a harmless enlargement when the maximizing point lies below 1.
For fixed `b`, its constant is `O_b(epsilon^-b)`.

Thus the visible `log^4 k` loss can be absorbed into an exponent slack
`epsilon` for all lengths by a prefactor `O(epsilon^-4)`. There is no need to
add a cutoff of the form `exp(poly(1/epsilon))` merely for this absorption.
Such a cutoff may still be required by *other* template conditions.

## 2. Polynomial setup and norm growth can be shifted into thresholds

**Lemma P2.** Let `E,H` be nonnegative integers, `q=E+H+1`, and
`k>=64 q^2`. Then

\[
2^H(1+k)^E\le2^{k/4}. \tag{P2}
\]

Indeed `log2(1+k)<=sqrt(k)` for `k>=32` (check at 32, then compare
derivatives). Therefore
`H+E log2(1+k)<=q+q sqrt(k)<=2q sqrt(k)<=k/4`.
This gives an explicit conservative effective threshold; a sharper
`O(q log q)` threshold is unnecessary for the present interface.

Consequences for a *fixed* template:

* A setup charge `G(1+k)^E`, with `G<=2^H`, is at most `2^(k/4)` above this
  threshold. It fits the linear-volume budget of a `2^k`-record stream.
* A polynomial amplification bound `C(1+k)^B` has logarithm at most `k/4`
  above a threshold polynomial in `B+ceil(log2 C)+1`. Its extra guard bits
  can then be included in an absolute multiple of `k`, rather than making
  the record-width coefficient proportional to an enormous `B`.
* A fixed coefficient-encoding allowance of `P_0` bits is at most `k` when
  `k>=P_0`. Keep this threshold distinct from the permanent transition-list
  storage, which contributes additive fixed space `d_j` in A4.

These operations do not remove the dependence. They put it into the valid
input threshold, which must remain in every candidate-selection inequality.
If the fast branch fails a proved preflight inequality, it must use a correct
fallback or abort the attempt; it must not proceed at insufficient precision.

## 3. Counting setup work in the Walsh recursion

Let the fixed Walsh template have arity `A>=3`, batch width `W>=2`, and
`sigma>=2` recursive calls per node. The source splits the active width into
at most `A-1` pieces of every size `2A^j`, `0<=j<=J`. A single piece has
`sum_(ell=0)^j sigma^ell` nodes. Summing over its pieces gives

\[
\text{nodes}\le(A-1)\sum_{j=0}^J\sum_{\ell=0}^j\sigma^\ell
\le4A\sigma^J
\le4A(1+k)^{\log_A\sigma}. \tag{P3}
\]

The second inequality follows by reversing the sums or by two geometric
series: `sigma/(sigma-1)<=2`. Thus if every node's non-volume setup costs
at most `G(1+k)^e`, all setup is bounded by
`4AG(1+k)^(e+ceil(log_A sigma))`. This is an explicit exponent to put into
P2. It is not automatically small: `sigma` may depend severely on the
finite construction.

The row-padding condition is also explicit. The source needs `W^J<=q_rows`,
and for its short selected transforms `q_rows>=2^(k/2)` for large `k`.
Because `W^J<=(1+k)^(log_A W)`, P2 gives a sufficient padding threshold
`k>=64(ceil(log_A W)+1)^2`, in addition to the absolute condition establishing
the short-width bound. Above it, padding adds at most a factor two.

## 4. Precision growth from the finite instruction list

In `uniformity.tex`, one-level instruction gains have product bounded by
`C>=2`, including copies and merges. Depth is
`d<=1+ceil(log_A(1+k))`. Hence

\[
C^{2d+1}\le C^5(1+k)^{2\log_A C}. \tag{P4}
\]

Multiply this by the explicit array-instruction count and coefficient/local
error bounds to obtain a polynomial propagation majorant. P2 can absorb its
polynomial part into `2^(k/4)` after a stated cutoff. The digit and unitary
boundary caps in `integers.tex` already have fixed exponents (`2^(13k)` for
the cited boundary allowance). Therefore this operation can keep the eventual
record precision a fixed multiple of `k`, once its potentially very large
template-dependent cutoff is respected.

This observation does **not** bound the number of simultaneous streams,
serialized passes, or the interpreted instruction cost; those still affect
`c_j` and `a_j`. It also does not cover a changed algebraic coefficient
construction until its local approximation and conditioning bounds are proved.

## 5. The prime-shape threshold is not a new j-dependent growth law

The source sets `l=20 ceil(log2 k)`, `x=2^l`, and searches for
`floor(k/l)` distinct odd primes in `[x(1-k^-2),x]`. Its use of the
Baker–Harman–Pintz short-interval theorem is at these fixed powers, independently
of `j` or `rho`. The eventual prime-shape cutoff is therefore an **absolute
source constant**. The algorithm tests its finite shape conditions and uses
schoolbook below the valid range; this note does not supply a numerical value
for the prime-gap cutoff or independently reprove that theorem.

By contrast, Walsh padding, the setup exponent, finite coefficient heights and
norm gains do depend on the candidate. They cannot be hidden in that absolute
prime-shape constant.

## 6. What an end-to-end extraction still needs

Supply explicit bounds for finite arities, call counts, scan counts,
coefficient heights, program-generation time/space and interpreter cost.
Then apply P1--P4 to obtain explicit `(a_j,c_j,d_j,g_j,U_j)` and substitute
them into A10 in `scheduler-and-chunking.md`. Existence and finite computability
alone do not imply that those profiles are polynomial, exponential or even of
a fixed elementary height. No such source-wide growth claim is made here.

Open next questions: independently check the visible fourth-power loss and
the precise local setup degree; quantify the new candidate's coefficient
preparation; distinguish additive retained code from proportional live streams.

Credits: source OpenAI authors and cited predecessor constructions;
Jerry Chen (@CubeJerry); AI-assisted derivations for this programme. These
generic inequalities are an accounting tool, not a claimed new multiplication
bound.
