# Independent review of the sparse ordinary-residual corrector

Reviewed: Route B `deterministic-sparse-residual-repair.md`, S004;
actual source/cost paragraphs read in full. **Verdict: passes the stated
component and physical-cost claim under its explicit sparse-residual
promise.** It supplies no faster candidate construction and is not a
generally sound product verifier.

## Algebra supporting the physical reduction

Lemma R2's composite-modulus logic is correct. If a length ell causes a
collision, ell divides a support difference and hence their product.
Therefore if every ell<=K collided, lcm(1,...,K) would divide that product.
The displayed binomial-coefficient divisibility proves the stated lcm
lower bound, and K=2B_*+4 makes it larger than the product bound. The
argument does not incorrectly infer that a composite modulus failing to
divide one factor must fail to divide their product.

The product modulus needs no coprimality. Each R^ell-1 divides M, so one
residue modulo M supplies all cyclic folds. R's strict height guard
applies to signed E and Theta E even with cancellation. The centered
integer representatives are unique, and balanced base-R extraction
recovers every bounded signed fold coefficient. The sparse candidate
soundness check uses a support bound of 2s for E-E_ell; its height doubles
but still lies within the chosen radix margin. Thus the final modular
check is sufficient under the promise and is correctly not claimed
sufficient without it.

## Charged arithmetic and stream generation

In Barrett reduction, u<M*2^k<2^(2k) and
mu=floor(2^(2k)/M) imply

    u/M-1 < u*mu/2^(2k) <= u/M.

Hence q0 is at most the true quotient and at least one below it; one
subtraction suffices. u, mu, their product, q0 and q0*M have O(k) bits
with fixed absolute factors. Each k-bit input block consequently costs
a fixed number of calls to the fixed short multiplier plus O(k) physical
scans. The claimed (V+k)*L(k)^alpha reduction bound follows with head
returns included, not a unit-cost modular oracle.

The derivative streams are explicitly charged: each i*a_i, i*b_i and
i*c_i fits O(beta) bits and uses one fixed short multiplication at that
size. Since beta<=k, their total V*L(beta)^alpha fits V*L(k)^alpha.
Signed candidate coefficients are separated into positive and negative
parts before modular evaluation, requiring only a fixed number of extra
streams. Record reversal can be done by scanning records backwards and
reversing each bounded record through one reused scratch area; this costs
O(V), so it does not alter the invoice.

The short-data bound k^6 is conservative enough. K,s,log D are O(k);
even candidate validation by K*s*log D grade-school modular products of
O(k)-bit integers is O(k^5). The additional modulus construction, fold
decoding, exact divisions, sorting and counter scans fit k^6. At most one
candidate and one fold pair are stored, with total O(k) bits because
candidate support/height data are dominated by beta*K*(K+1)/2.

## Common visited-cell bound

When k<=V, input, candidate, weighted streams and all short registers use
a constant number of O(V) regions. Reusing marked intervals and clearing
them between lengths bounds the union of visited cells. No K-fold copy
of a long stream is needed. The fixed short multiplier has its own O(k)
space bound and fixed tape count.

When k>V, the direct packed schoolbook fallback is valid: R exceeds every
true coefficient of AB, so its packed product has those coefficients as
its base-R digits. Its time O(V^2) is less than k^6 and its space O(V).
Thus the asymptotic component formula has the asserted common space cap
at every allowed parameter value, not only in the useful sparse regime.

The final corrected coefficients have magnitude bounded by h*2^(2b),
and the original-radix carry has O(beta) bits. Support merging and carry
recovery therefore cost O(V) after the stated short-data sorting work.

## Consequences and scope

For V=Theta(n) and beta=Theta(log n), polylogarithmic s gives k=polylog(n),
so k^6=o(n). For s<=2^{(log n)^tau} with fixed tau<1, k^6=n^{o(1)} and
log k=O((log n)^tau). Choosing the fixed exponent
alpha=(1+tau)/(4tau)>1/2 gives the displayed exponent (1+tau)/4<1/2.
These are fixed-parameter consequences; no growing alpha or uncontrolled
O_tau constant is substituted.

The non-sparse false-promise witness is correctly scoped. A candidate
producer would have to prove the ordinary residual is sparse or supply
an independently sound sparsity certificate. Neither modular agreement
nor the present corrector establishes that missing premise.

This review is mathematical and physical accounting, not a full tape
implementation, formal build, exhaustive prior-art review or human
refereeing. Route C separately reviews the sparse algebra and witnesses.
