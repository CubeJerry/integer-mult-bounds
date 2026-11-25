# Variable-arity invoice criteria

Status: **proved scoped recurrence analysis; no tape realization claimed**.
These results test proposed costs, not the existence of an algorithm paying
them. A recurrence upper bound cannot by itself establish an algorithmic
lower bound. Necessity below concerns the declared exact invoice.

## Exact accounting

Let `F_i=c_i+b_i F_(i+1)` be a nonnegative volume-normalized invoice at active
widths `k_i`, with effective arity `A_i=k_i/k_(i+1)`. Put
`h_i=F_i/sqrt(k_i)`, `lambda_i=b_i/sqrt(A_i)`, `tau_i=c_i/sqrt(k_i)` and
`P_i=product_(j<i) lambda_j`. Substitution gives

\[
                 h_0=P_dh_d+\sum_{i<d}P_i\tau_i.                 \tag{V1}
\]

With a terminal cost bounded above and below by positive constants, bounded
overhead is equivalent to both `P_d=O(1)` and `sum P_i tau_i=O(1)`.
Checking only the final product is wrong: losses `K,1/K` have product one
but a unit toll after the first level costs K; all losses one with d unit
tolls cost d. If every loss is at least one, a sufficient bound is
`h_0 <= P_d(h_d+sum tau_i)`.

## Polynomial local work: a sharp power

Use `x=log_2 k`, `u=log_2 A`, and stop at a fixed bounded positive base scale.
Suppose a level has constant normalized loss `lambda>1` and local cost `A^c`
per unit volume. Its normalized toll is `2^(cu-x/2)`. Allow arbitrary positive
real u, a relaxation of integral arity constraints. The minimum exact invoice
has, for fixed c>1/2,

\[
 H(x)=x^{\alpha_*+o(1)},\qquad
 \alpha_*={\ln\lambda\over-\ln(1-1/(2c))}.                       \tag{V2}
\]

Proof: choose `u=beta x`, `0<beta<1/(2c)`. The normalized tolls decay
exponentially in the decreasing x values and have bounded sum. Depth is
`ln x/[-ln(1-beta)]+O(1)`. Let beta approach `1/(2c)` for the upper exponent.
For any invoice R, each toll is at most R, so
`x_(i+1)>=(1-1/(2c))x_i-log_2(R)/c`. The upper bound permits restricting
to near-minimizers with `log R=O(log x)`. Iteration then forces depth at least
`[ln x-O(ln ln x)]/[-ln(1-1/(2c))]`. The terminal contribution `lambda^d`
gives the lower exponent. For `0<c<=1/2`, one step to the base scale has
bounded toll and terminal cost, so the model instead has bounded overhead.

If an independently verified caller has k comparable to `L(n)`, then x is
comparable to `s(n)`. In that caller a power of s strictly below one would
require `lambda<2c/(2c-1)`. For c=1 this is lambda<2; for c=2 it is lambda<4/3.
This is a concrete budget threshold, not a construction satisfying it.

## Quasipolynomial local work: a sharp change of scale

Replace the toll by `2^(c u^q-x/2)` for fixed q>1,c>0, corresponding to local
work `2^(c (log_2 A)^q)`, and keep constant loss lambda>1. The optimal invoice
satisfies

\[
                         \log H(x)=\Theta(x^{1-1/q}).             \tag{V3}
\]

For the upper bound use `u=a x^(1/q)` with `ca^q<1/2`. Tolls sum to a
constant and depth is `O(x^(1-1/q))`, by applying the mean value theorem to
`x^(1-1/q)` until a fixed base range. For the lower bound put `h=log_2 R`.
Every step obeys `u_i<=((x/2+h)/c)^(1/q)`. Therefore
`h >= (log_2 lambda)(x-x_*)/((x/2+h)/c)^(1/q)`. If h>=x the lower bound is
immediate; otherwise the denominator is `O(x^(1/q))`. This tests all adaptive
arity choices, not merely the schedule used for the upper bound.

A large one-time description is not a repeated local charge. V3 applies
only if that repeated charge is actually paid; scanning a large table at
every coordinate is one example. Fast structured checks or shared generation
may change the premise.

## Summable near-critical losses

Along `u=a x^(1/q)`, replace the constant loss by `exp(delta(u))>=1`.
The exact logarithmic loss is `sum_i delta(u_i)`. For q>1 and
`delta(u)=Theta(u^(-beta))`, integral comparison with
`integral x^(-(beta+1)/q) dx` gives a bounded sum when beta>q-1,
`Theta(log x)` at beta=q-1, and `Theta(x^((q-1-beta)/q))` below it.
The local tolls above still have bounded sum. Thus the first case gives an
endpoint invoice, the second a power of x, and the third a stretched
exponential. For q=1 use a fractional log-scale reduction: any positive power
decay in u is summable; constant loss gives `Theta(log x)` total loss;
`delta(u)=Theta(1/log u)` gives `Theta(log log x)` and unbounded overhead.
Merely tending to one is insufficient without a compatible decay rate.

## Physical gates remain open

Actual `b_i` must include padding, recursive repairs and full-volume reserve
calls under one consistent volume contract. Actual `c_i` pays arithmetic,
routing, selectors, coefficient preparation, clearing and movement. A setup
charge `G_i` adds `G_i/V_i` unless a shared execution pays it exactly once.
Every arity must satisfy the real shape and padding thresholds. Rounding
changes effective arity and padding and must be charged.

If depth-first descent parks `s_i V_i` cells and child volume ratio is `r_i`,
its parked-array bill is `V_0 sum_i s_i product_(j<i)r_j`; this must be uniformly
O(V_0). A growing root coefficient already violates that condition. In the
source full-volume reserve descent only descriptors are parked after clearing
streams. Tables, programs, descriptors and precision have additional charges.
These obligations prevent V2 or V3 from being a complete multiplication theorem.

Motivation: the published Fourier, tape Walsh and interchange recurrences at
`openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`. Elementary recurrence
analysis developed with AI assistance for @CubeJerry; no literature-priority
claim. Finite verification and independent review are pending for this note.

Open next question: prove actual uniform local-work and normalized-call
profiles for the polynomial-width route, then test them against V2 before
another local optimization wave.
