# Sharp helper-fragmentation threshold at κ = 1/200

**Proved invoice-level relaxation and scoped obstruction. No new κ.**
All source claims below refer to canonical commit
`e54523517d0f03e58352e647c403a5af3e525a57`, selected #7000 with #7001 BIT.
The selected saving is `363005817/100000000000`; the target is `1/200`.
The exact selected invoice is vendored byte-for-byte at `inputs/FULL-RESULT.json`
and authenticated by both SHA256 and Git blob before any calculation.

## 1. Model, complete fixed invoice and theorem

Let T and P be the full caller's productive and paid rank histograms in that
source, and H its native helper histogram. There are 18 native invocations.
H has 1,080 helpers and rank mass 7,650. The full T and P have 23,392 and
117,612 positions, and rank masses 321,364 and 319,844. The surplus is 1,520.
T_root=T−18H is a nonnegative histogram of 3,952 caller targets. The verifier
reads T, P and H directly from the authenticated source, including its
fresh-arbitrary-helper census; all three appear in RESULT.json.

For every ORIGINAL CURRENT helper occurrence of rank r, allow a replacement
by arbitrary positive integer ranks r_1,...,r_k with sum r. The replacement
**debits the old rank-r target** and credits the independent new targets.
Hold T_root and every paid job P fixed. Give every implementation operation,
ordinary expense and interface conversion zero cost. This generous relaxation
is not a physical construction or a provider admission. Its bound applies
only to architectures admitting precisely these unchanged-source partitions.

For 0<C<1 write t=1−C and M_C(T,P)=Σ_r(T_r−P_r)r^t. At C=1/200:

1. If every original helper has at most two descendants, even the optimal
   relaxed invoice has M<0. This persists for every C in [1/200,1).
2. With arbitrary descendant counts, the minimum number of extra targets
   giving M>0 is exactly **22,954**, when occurrences may be changed separately.
3. If all 18 native invocations must use the identical changed native profile,
   the minimum is **1,276 extras per native**, hence 22,968 caller extras.

Positive M is a raw moment condition only. These assertions supply neither
valid helper interfaces nor strict compiler, BIT, precision or outer admission.
The continuum obstruction blocks this fixed-invoice positive-moment route;
it is not a general obstruction to κ=0.005 or to integer multiplication.

## 2. Balanced partition lemma

For 0<t<1 the increments of x^t strictly decrease. If two positive integer
parts satisfy x≥y+2, replacing them by x−1 and y+1 strictly raises their
moment. Iteration proves that an optimal k-part partition of r is balanced.
Writing q=floor(r/k) and s=r−kq, its value is

B_r(k)=(k−s)q^t+s(q+1)^t,  1≤k≤r.

Let φ be the piecewise-linear interpolation of x^t at positive integers.
It is concave. Its perspective kφ(r/k) is concave in positive k over the
relevant domain, and equals B_r(k) at each integer k. Consequently
δ_r(k)=B_r(k+1)−B_r(k) is nonincreasing in k. Every gain is positive because
splitting a positive integer part increases a strictly subadditive power.

## 3. Exact fragment-budget optimization

Each helper supplies a chain of decreasing marginals δ_r(1),...,δ_r(r−1).
Any legal refinement selects a prefix of every chain. For q extra targets,
the q largest available marginals are an upper bound. Break ties with chain
predecessors first; the selected gains then form prefixes and attain that
bound. Thus the greedy value is the sharp optimum, rather than a finite
search over some favorite partitions. This proof applies to all integer
partitions in the stated rank domain and every extra-target budget.

The verifier orders signed marginal profiles using rational intervals for
r^(199/200). Equal signed profiles are exact ties; all unequal comparisons
are separated strictly. It checks predecessor multiplicities in each chosen
allocation. There are 18H_r chains for arbitrary occurrences. For identical
natives there are H_r chains and every gain is multiplied by 18.

The first five descending types are 9:1→2, 8:1→2, 7:1→2, 6:1→2, 9:2→3.
The first four contribute 10,710+1,206+324+756=12,996 caller extras. Of the
10,710 available fifth-type increments, another 9,958 are required.
Exact intervals in RESULT.json prove

- M_opt(22,953)<0; approximately −0.00172465590055555;
- M_opt(22,954)>0; approximately 0.0166778308918005.

Every extra marginal is positive, so these adjacent signs establish the
sharp threshold. The identical-native calculation gives full-caller margins
approximately −0.0569321162776236 at 1,275 extras and +0.274312645984785 at
1,276 extras. Its allocation is explicit:

- all 595 rank-nine helpers first become 4+5;
- all 67 rank-eight, 18 rank-seven and 42 rank-six helpers become 4+4,
  3+4 and 3+3 respectively;
- 554 of the rank-nine helpers are then changed from 4+5 to 3+3+3;
- the original rank-one through rank-five helpers remain intact.

The resulting native histogram is {1:13,2:18,3:1808,4:408,5:109}.
The remaining 41 rank-nine helpers stay 4+5. The full target count is 46,360.
This describes an optimal **partition profile**, not 554 realized ternary cuts.

## 4. Binary-descendant ceiling on a continuum of prices

Balanced two-way refinement maximizes the target moment pointwise for every
0<C<1. Denote its full histogram by T2. At C=1/200 the verified margin is
approximately −99.6199144633181. An endpoint sign alone would not prove a
ceiling for larger C, so we establish monotonicity separately.

Put d_r=T2_r−P_r and g_r=d_r log r for r≥2. Let r_1<...<r_m be the ranks with
nonzero d_r, omitting r=1. For every j define S_j=Σ_{i≥j}g_(r_i).
Each assertion S_j>0 is exactly the integer comparison

Π_{r≥r_j,d_r>0} r^(d_r) > Π_{r≥r_j,d_r<0} r^(−d_r).

The verifier checks all 24 descending tails using integer products, with no
log approximation. For every u≥0, summation by parts gives

Σ_i g_(r_i) r_i^u = r_1^u S_1 + Σ_{j=2}^m (r_j^u−r_(j−1)^u)S_j > 0.

Thus F(C)=Σ_r d_r r^(1−C) has derivative F'(C)<0 for C≤1. Since
F(1/200)<0, F(C)<0 throughout [1/200,1). Any at-most-two refinement is bounded
above by T2 at each such C, proving the claimed continuum obstruction.
The exact-tail argument was proposed independently during this run and is
credited in REVIEW.md. It replaces an earlier derivative interval proof;
the present verifier and evidence are freshly checked after workspace loss.

No closure under a changed source, additional post-product splitting,
modified paid jobs or a different compiler contract is asserted. Purely
algebraically, an inequality of nonnegative target and paid moments is
preserved by sums, products and paid-only increases, but applicability to a
new assembled construction still requires its actual complete invoice.

## 5. Accounting, strictness and the constructive gap

For the same fixed paid profile, balanced at-most-three refinement gives
M≈173.658146675509, and complete rank-one fragmentation gives M≈818.885529576106.
Therefore binary failure does not extend to all partitions. The exact
identical-native threshold profile leaves only

M/18≈0.0152395914435992

of additional paid moment per native. A rank-one paid child costs 1, so even
one per native exceeds that fixed-profile slack. More fragments or paid savings
elsewhere may change the budget; this figure is not an architecture-independent
limit. All moment signs are strict rational interval signs in the receipt.

Even free partitioning does not prove physical independence. Actual cuts must
satisfy source versions, prefix/suffix purity, frame geometry, independent fresh
inputs, copying and restoration, owned lifetimes, recursive tariffs and
precision. The small threshold fragments also invalidate an automatic reuse
of the old strictifier's large target floor. Positive moment must be bridged
to a legal strict compiler and the complete outer inequalities. The standalone fragmentation theorem supplies no such bridge or physical
ternary deployment. A companion arithmetic specification, if included, remains
conditional on unbuilt supplier inputs and does not discharge this construction
gap.

The five inherited assumptions native_all_columns, owned_erasure, compiler,
precision_tape and analytic_recovery are unchanged and undischarged. The
finite arithmetic theorem itself does not assume their truth: it analyzes the
recorded histograms. Any multiplication theorem obtained by reusing this
architecture would still have to establish or explicitly inherit them.

## 6. Exact arithmetic and controls

For r^(199/200), D=2^128 and n=r^199 D^200. Integer Newton iteration finds a
with a^200≤n<(a+1)^200 and verifies both inequalities. Thus [a/D,(a+1)/D]
(or the singleton when exact) encloses the power. Signed interval arithmetic
preserves lower/upper bounds. An unresolved sign causes rejection; floating
point is not used for comparisons or certificates.

The verifier also checks all 96 positive partitions of ranks one through nine
against the balanced optimum, rejects eight malformed histograms and two
source-byte mutations, and demonstrates two false crossings: omitting 100
paid rank-one jobs or retaining the original helper target. Those controls
show why the authenticated full invoice and old-target debit are essential.
Default replay is read-only and compares the entire regenerated RESULT.json;
--write is an explicit receipt-generation option. Normal and optimized Python
both pass; exceptions, not assertions, enforce scientific checks.
