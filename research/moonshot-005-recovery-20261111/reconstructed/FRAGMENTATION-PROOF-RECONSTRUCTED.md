# Fragmentation theorem — reconstructed after disconnect

**Recovery text, not original reviewed bytes. No new κ.** The environment became
unavailable on11 November2026. This document reconstructs the argument from
retained agent context. It has not been compared with the original PROOF.md or
newly replayed against upstream; original review does not certify these bytes.

## Source and optimistic model

Canonical main: e54523517d0f03e58352e647c403a5af3e525a57. Selected #7000 with
#7001 BIT has κ=363005817/100000000000. Fix κ★=1/200 and t=199/200.
RECORDED-RESULTS.json contains the exact recorded target/paid histograms T,P
and native helper histogram H. Source pins are in SOURCE-PINS.json.

There are18 native invocations. H has1,080 helpers and rank mass7,650.
The full selected target/paid counts are23,392/117,612, and rank masses
321,364/319,844, with surplus1,520. T_root=T−18H has3,952 targets.

Grant every ORIGINAL CURRENT helper identity of rank r an arbitrary positive
integer partition r=r_1+...+r_k. Replace its original target by those independent
targets; keep every root target and paid job fixed, and grant all implementation
costs zero. This is a favorable partition relaxation, not a physical supplier.
In particular, the original target is debited; it is not retained additionally.
Write M(T,P)=Σ_r(T_r−P_r)r^t. Positive M alone is not complete assembly.

## Balanced partitions and sharp fragment budget

Strict concavity of f(x)=x^t implies that replacing parts x≥y+2 by x−1,y+1
increases their moment. Thus, for k pieces, every optimal partition is balanced.
Put q=floor(r/k), s=r−kq. Its value is

B_r(k)=(k−s)q^t+s(q+1)^t, 1≤k≤r.

Let φ be the piecewise-linear interpolation of f at positive integers.
Then B_r(k)=kφ(r/k). Concavity of φ and its perspective imply that B_r(k)
is concave in k. Therefore δ_r(k)=B_r(k+1)−B_r(k) is nonincreasing.

Each helper supplies a chain of these decreasing marginal gains. Every legal
partition selects a prefix from each chain. For q total extra targets, the sum
of the q largest available marginals is an upper bound; sorting ties with chain
predecessors first makes that selection feasible, so the bound is sharp.
For arbitrary original occurrences use18H_r chains. For identical-native
deployment use H_r chains and repeat every chosen step18 times.

At t=199/200 the original exact comparisons ordered the first five gain types:
9:1→2, 8:1→2, 7:1→2, 6:1→2, 9:2→3.
The first four use10,710+1,206+324+756=12,996 caller extras.
The fifth type is available10,710 times. Reported rigorous signs were

M_opt(22,953)<0, approximate−0.0017246559005555532;
M_opt(22,954)>0, approximate0.01667783089180048.

Hence22,954 is the sharp threshold in the arbitrary-occurrence relaxation.
For identical natives,1,275 extras have full margin approximately
−0.05693211627762365 and1,276 have0.27431264598478494.
Thus1,276 extras/native are necessary and sufficient for positive raw M in
this relaxation. The first722 native extras split all595 rank9,67 rank8,
18 rank7 and42 rank6 helpers into balanced pairs. Another554 change rank9
partitions4+5 into3+3+3. The other41 rank9 helpers remain4+5. The resulting
native profile is {1:13,2:18,3:1808,4:408,5:109}; caller extras total22,968.

## Binary-descendant ceiling

With at most two descendants per ORIGINAL helper, balanced splitting gives
the pointwise maximum target profile T2 in RECORDED-RESULTS.json.
Its moment atκ★ is approximately−99.61991446331811, strictly negative.

Let F(C)=Σ_r(T2_r−P_r)r^(1−C). To extend the ceiling beyond one tested point,
the original verifier certified F'(C)<0 on[1/200,1) by20 exact interval bounds.
For an interval[a,b], with d_r=T2_r−P_r, a derivative upper bound is

−Σ_{d_r≥0}d_r r^(1−b)log r −Σ_{d_r<0}d_r r^(1−a)log r.

The intervals were[1/200,1/20] and[i/20,(i+1)/20], i=1,...,19.
The largest recorded upper bound was below−2292.640905.

An independent reviewer found a simpler exact proof. Put g_r=d_r log r for
r≥2. Every descending tail S_j=Σ_{r≥r_j}g_r was positive. Each tail sign is an
integer-product comparison:
Π_{r≥r_j,d_r>0}r^(d_r)>Π_{r≥r_j,d_r<0}r^(−d_r).
For u≥0, Abel summation gives
Σ_r g_r r^u=r_min^u S_1+
Σ_{j≥2}(r_j^u−r_{j−1}^u)S_j>0.
Therefore F'(C)<0 for C≤1. Combined with F(1/200)<0, no binary refinement
in this fixed-paid class reaches a positive raw moment for1/200≤C<1.

The failure also persists under direct sums, chronological products of these
already refined full systems and paid-only worsening: nonnegative target and
paid moments respectively add or multiply, preserving target≤paid. This closure
does not permit further refinement after a product, changed original identities,
changed paid profiles or a different caller.

## What remains open

The best at-most-three-descendant relaxation has raw margin approximately
173.658146675509; full rank-one fragmentation gives818.8855295761059.
Thus this is not an unrestricted partition impossibility theorem.
The sharp identical-native profile leaves onlyM/18≈0.0152395914435992 of
additional paid moment per native before other losses; a new rank-one paid
child would already exceed that fixed-profile budget.

No actual554-fold3+3+3 deployment was supplied. Valid cuts still need
prefix/suffix purity, common frames, independent fresh inputs, source versions,
owned lifetimes and restoration. The old completion-tail sufficient test fails
on these small fragments; the separately reviewed target-restriction compiler
specification succeeds arithmetically under its explicitly unbuilt input contract. Positive raw
moment proves neither compiler nor BIT nor outerκ=1/200 admission.

The original arithmetic used integer200th-root enclosures with scale2^128;
log bounds used96-term rational atanh series and geometric tails. Normal and
optimized Python agreed. The run reported96 exact small-partition cases,
seven malformed-input controls and negative controls for keeping the old target
and improperly removing100 paid rank-one jobs. These are historical reports
from context, not original receipt bytes or newly executed checks.

Credit selected shared-wire authors and lineage, Ali Romman, Matarener,
helper-handoff-r18 and Nick Petalas's unit-fee-target-threshold. Concavity,
greedy chain allocation and root enclosures are not claimed as new. Prepared
for @CubeJerry with substantial OpenAI assistance. All five foundational
assumptions remain; κ=0.005 remains open.
