# Actual swap-query rank bounds, including characteristic two

Status: **proved bridge; independent B review and exact controls passed**.
This is an actual-rank query-model result, not a general tape-time bound.

## 1. Semisimplicity is unnecessary for regular rank

Over any field K and any integer r>=2, the algebra
K[x_1,...,x_k]/(x_i^r-1) has its r^k reduced monomial basis. Multiplication
by chi=product x_i permutes exponents by simultaneous addition of one
modulo r, even if char(K) divides r. The equivariant plurality rule
therefore still gives r equal cyclic sectors.

A sector-preserving comparison differs from chi I_W by rank at least
(1-1/r)r^k W: the kernel is determined backwards from one sector.
Support-degree-d matrices can cross sectors only on columns whose two
largest symbol counts differ by at most 2d. Rank completion and inverse
differences also work over every field. Thus PA's regular-rank proof
does not need semisimplicity. Its spectral-average interpretation does,
and that interpretation is not used here.

## 2. Actual swap orbits and the model

Field pair j has q_j>=2 values. Its ordinary basis is [q_j]^2, and Q_j
exchanges the two entries. There are q_j singleton fixed vectors and
q_j(q_j-1)/2 disjoint regular two-cycles over every field, including F2.
Across m disjoint pairs, put

    D=product q_j^2, F=product q_j, T=product Q_j.

A tensor stratum with k nontrivial two-cycles is exactly the regular
basis of K[(Z/2Z)^k], with T complementing every exponent. The all-fixed
strata have total dimension F. Binary plurality phases on every k>0
stratum give two equal good sectors of dimension (D-F)/2 and an
exceptional F-dimensional sector. The actual dimension-weighted count is

    K_* = sum_j Bernoulli(theta_j),
    theta_j=(q_j-1)/q_j>=1/2, pi_0=F/D=product 1/q_j.      (NS1)

The network has W independent payload rows. Free maps are constant
K-linear row maps, copies and width changes, acting identically on the
payload coordinate. A direct h-row query is
G=A_0+sum_j A_j Q_j with fixed row coefficient matrices. Its inverse
is allowed only when G is invertible on the actual payload. A port is
an arbitrary K-linear map of actual rank at most hD. Let H sum these
h over actual occurrences, and let Q_d,Q_i sum direct/inverse active
row widths. Reused computed values need not be charged as new ports.
Let E=rank_K(T I_W-P)/(DW).

## 3. Exact inequality and proof

For k>0 define

    tau_d(k)=2^(-k) sum_(j: |k-2j|<=2d) binom(k,j).

Set tau_d(0)=0 and use tau_0(k)=0 for constants. Let eta_d be the
expectation of tau_d(K_*). Then

    E+H/W+eta_1(Q_d+2Q_i)/W >=(1-pi_0)/2.                 (NS2)

Zero the ports and replace each query by its sector part. A one-coordinate
swap changes a binary count difference by at most two, so only the
boundary columns can cross phases. Summing actual stratum dimensions
gives rank loss at most hD eta_1. For an inverse, complete its sector
blocks to invertibility, costing at most twice that loss. Telescope the
actual network; arbitrary ports, even when mixing strata, cost at most
HD. The final sector comparison has distance at least (D-F)W/2 from T.
This proves NS2 without restricting the port network to a single stratum.

A degree-d polynomial matrix predictor in the commuting swaps obeys

    E(P)>=(1-pi_0)/2-eta_d.                               (NS3)

For noncommuting numerator/denominator matrices of support degrees a,b,
either fraction AB^-1 or B^-1 A has lower bound
(1-pi_0)/2-eta_a-2eta_b when B is invertible. Under A=PB or A=BP,
add the normalized actual nullity of B to the left side. This is the
already audited singular-completion argument in the new representation.

## 4. Uniform asymptotics and exact witness

Write mu=sum theta_j>=m/2. Chebyshev gives
Pr[K_*<mu/2]<=4/mu<=8/m. A binomial atom is at most
1/sqrt(k+1), and at most 2d+1 integer levels enter tau_d(k). Therefore,
for d>=1,

    eta_d<=min(1,8/m+2(2d+1)/sqrt(m)).                    (NS4)

Thus sub-square-root support degree or normalized active query volume
forces error plus port width at least 1/2-o(1), uniformly over unequal
q_j and all coefficient fields. The identity predictor attains
(1-pi_0)/2 exactly: T has F fixed vectors and (D-F)/2 two-cycles, and
T-I has rank one on each two-cycle in every characteristic.

## 5. Necessary exclusions

Address-dependent masks, smaller/equal/larger comparisons used as extra
linear gates, arbitrary payload permutations and full interchanges are
not free row maps. A local diagonal mask on a swap orbit need not be a
polynomial in that swap. Including such maps needs a separate invoice
or invariant. Nonlinear/input-dependent suppliers are also outside this
linear model. No efficient physical inverse is supplied.

In F2 a swap has only eigenvalue one and is not diagonalizable. Replacing
it by that eigenvalue would falsely erase its rank-one distance from
the identity. The present proof uses the actual ordinary orbit basis.

The nonsemisimple observation is Route C's; the lead proposed this
explicit actual-swap corollary and scope. It composes the audited
plurality, completion and telescoping proofs, with no priority claim.

The checker `verify_nonsemisimple_swaps.py` passes 12 regular-cycle
rank identities in characteristics dividing the cycle order, 1,461
actual swap boundary-column checks, 14 exact identity baselines, seven
unequal-multiplicity mixtures, four F2 inverse/strata-mixing-port cases
and 1,000 binomial atom bounds. Its negative control exhibits an F2
swap with sole eigenvalue one but actual rank(Q-I)=1. B's independent
proof audit and isolated replay are recorded in
`route-b-work/review-nonsemisimple-physical-swaps.md`.
