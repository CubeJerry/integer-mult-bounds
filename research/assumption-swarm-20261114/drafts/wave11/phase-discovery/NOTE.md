# Unverified next-wave candidate: admissible physical narrow pairs

Root derivation, 2026-11-14. Not a frozen result or publication package.
Do not add this to A10's normalized-core claim. Exact canonical base e545;
A9 published085b30f8 supplies the matching minor. Requires source-grid and
novelty review before allocation.

For one dyadic target t and odd prime s<t<2s, put delta=t-s and theta=delta/s.
At a same-cell physical pair (i,i+1), write beta_i=n/s and beta_(i+1)=beta_i+theta.
The exact retained narrow entries give the factor [[1,U],[V,1]], with
U=exp(-a A/s), V=exp(-a B/s),
A=2t-s+2n, B=s-2n, A+B=2t.
Both indices lie strictly inside the same nearest-integer phase cell iff
2delta+1<=A<=2s-1 (A odd). This also bounds B in the same interval.

Fix an even desired minor size r>=2. Choose an integer K in
[r+1, floor((s-1)/r)-1]. Set Abar=2t/(K+1) modulo s, and lift it to the
unique odd A in[1,2s-1]; put B=2t-A. Then B=K A mod s.
The number of candidates is L=floor((s-1)/r)-r-1; their Abar are distinct.
Exactly delta odd lifts violate A>=2delta+1. One further phase may be
excluded to ensure the underlying residue representative i is not s-1.
Thus L>delta+1 guarantees an admissible adjacent physical pair with i<=s-2.
Here n=(A-(2t-s))/2, and i=delta^(-1)n mod s realizes that phase because
beta_i=theta*i-c for the nearest integer c. Actual finite source-grid
coverage of i=0,...,s-1 must be bound from retained definitions, not assumed.

For that pair, (a,b)->a A+b B mod s is injective on0<=a,b<=r: after
multiplication by A^(-1), it becomes a+K b; this lies in[0,r(K+1)] inside
[0,s-1], and K>=r+1 makes the digit representation unique.
For distinct source primes, CRT therefore distinguishes every monomial in
all2g formal variables U_i,V_i whose individual degrees are at most r.
Use the same transcendental base exp(-pi alpha^2/prod s_i) as A10.

For each order, take a size-r A9 trimmed principal minor. Replace each
symmetric binary factor by [[1,U_i],[V_i,1]]. Its determinant polynomial
is nonzero because specialization U_i=V_i=Q_i recovers the nonzero A9
minor. Its individual degrees are<=r. The chosen physical phases and
CRT/transcendence injection make this actual physical minor nonzero.
Thus an existential all-order physical-pair rank floor r may follow,
provided r<=R_(2^g) and L_i>delta_i+1 for each source axis. Inverse ranks
transfer by reversed orders. This does not transfer by similarity.

For fine primes delta/s<=1/p^2 and s exponential in p^(1-epsilon), an even
r<=p^2/4 should satisfy the counting condition eventually. This suggests
r=min(R_N,2 floor(p^2/8)) for groups where r>=2: polynomially growing,
not the full A10 exponential cap. Constants and thresholds need checking.
The scope would be actual same-cell two-point tensor factors at selected
phases, NOT arbitrary phases, rounded matrices, full larger tiles, periodic
aliases, general algorithms or a new kappa. No quantitative singular-value
or Cp-bit robustness follows from this exact nonvanishing argument.

## Stronger all-slope count (unverified candidate)

For2r<s, every difference pair(da,db) in[-r,r]^2 with da!=db defines at most one bad A via(da-db)A=-2t db modulo s. Equal nonzero differences cannot collide. Opposite integer pairs define the same residue; there are4r²+2r such pairs, so at most2r²+r bad residues. At most delta odd lifts fail same-cell admissibility. Thus at least s-1-delta-2r²-r nonzero residues give good actual adjacent phases; A0 already excludes i=s-1. Under p>=3,s>=p⁴,gap<=s/p² and even r<=sqrt(s)/2, this lower bound is at least s/3-1. Set r=min(R_N,2floor(sqrt(s_min)/4)). The source-specific rank cap is now Theta(sqrt(s_min)), rather than polynomial p²; exact matrix and rounded/periodic/capped-schedule exclusions persist. Constructive scan costs O(g*s_max*r²*poly(logs_max)), at most O(g*s_max²*poly(logs_max)).
