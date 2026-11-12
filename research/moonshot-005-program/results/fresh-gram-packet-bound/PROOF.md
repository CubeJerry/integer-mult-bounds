# A source-bound obstruction to fresh Gram-return packet extraction

## Exact claim and scope

**Proved within the stated raw-source packet interface; no new kappa.**
This is a next-step gate for the permanent programme, not a universal
multiplication lower bound. It applies to every positive field volume V and
arbitrary linear mixing of coordinates within each field.

The source has 96 independent hosted reverse values d_j, initially at the
empty chart and required finally at the binary hyperplane F_j=v_j-perp in
F_2^9. Their 96 distinct normal vectors have weight 3 or 7. Let A be the
8-by-96 matrix of the programme's integer E8 columns a(v_j), of squared
length 8. Put W=row(A), over a characteristic-zero field. In the prospective
complete reciprocal offdiagonal construction, the reverse residual is
A^T A/8 and its row space is W.

A fresh raw-source packet is a new full-field message formed at one actual
chart C from unchanged d_j values there, then sent to the full hub by one
new paid MOVE. Stationary copies from actual earlier visits are allowed.
The d_j ascend monotonically to F_j, so C is contained in F_j for every
source used. Arbitrary local linear operations, timing, caches and
input-independent side information are granted. All formation, restoration,
raw subdivision and other non-MOVE costs are free in this lower bound.
The final decoder can use the packets jointly.

**Theorem.** Any such packet family that supplies W tensor F^V has total
MOVE rank at least 48. At t=199/200 its paid moment is therefore at least
48*9^(-1/200)>47.4755522002641 per native. Even the most favorable monotone
raw H4 invoice, after the eight existing forward rank-nine packets, leaves
less than47.0797427433810. The packet completion fails the target before
all remaining ordinary and physical expenses.

The theorem does not apply to packets from changed raw rows, useful common
histories, relayed earlier packets whose source support is no longer local
to C, or already funded informative movements. It does not assert that an
unfinished reciprocal construction already has W as its only residual.

## 1. Every nonzero hosted Gram row uses at least 37 sources

There are 120 projective E8 root rows a(v): 84 weight-three and 36
weight-seven normal vectors. For real w, s=||w||^2, exact sign summation gives

    sum(a.w)^2=120s, sum(a.w)^4=288s^2, sum(a.w)^6=960s^3.

These are polynomial identities. For a direct derivation, double the root
set by adjoining negatives. Its rows are the112 vectors
2(plus/minus e_i plus/minus e_j), i<j, and the128 sign vectors in{+1,-1}^8
with product -1. Degree at most six cannot detect that parity constraint.
Writing S_k=sum_i w_i^k, the two parts contribute, before dividing by two:

| Degree | Two-coordinate rows | Sign rows |
| --- | --- | --- |
|2|112 S_2|128 S_2|
|4|192 S_2^2+256 S_4|384 S_2^2-256 S_4|
|6|3840 S_2 S_4-2048 S_6|1920 S_2^3-3840 S_2 S_4+2048 S_6|

For nonzero w put z_v=(a(v).w)^2/s, so0<=z_v<=8. The polynomial

    p(z)=z(z-6)^2/32

has p(0)=0 and0<=p(z)<=1, because

    1-p(z)=(8-z)(z-2)^2/32.

The moments give sum_v p(z_v)=57. The24 omitted hosted roots contain two
disjoint orthogonal eight-frames, specified by their binary normal vectors:

    B1=[7,25,42,52,76,82,97,127],
    B2=[67,104,137,162,266,289,448,491].

The source checker verifies omission, disjointness and the exact Gram8I.
For either frame sum z_v=8, while

    (10+15z)/32-p(z)=(10-z)(z-1)^2/32>=0.

Its p-sum is at most25/4. The other eight omitted roots contribute at most8.
Thus the hosted p-sum is at least57-2*(25/4)-8=73/2. Each nonzero root
evaluation contributes at most one, so every nonzero row of W has at least
ceil(73/2)=37 nonzero source coordinates.

For complex w, a nonzero real or imaginary part has support contained in
its complex support. For any characteristic-zero field, rational zero
constraints with a nonzero kernel over that field also have a nonzero
rational kernel vector with no larger support. Thus the support bound
holds over that field. A nonzero row of W tensor F^V has at least37 nonzero
source blocks: select a coordinate component giving a nonzero scalar row.
Arbitrary within-field linear mixing does not evade this statement.

## 2. Necessary capacities, including dependent packets

A packet formed at C has MOVE rank r=9-dim(C). Its support normals lie in
the r-dimensional binary subspace C-perp. All normals have odd Hamming
weight, so an r-space has at most2^(r-1) of them: the parity functional is
either zero, giving none, or has a codimension-one kernel. Put

    u(r)=min(2^(r-1),96),  1<=r<=9.

Zero-rank packets have no nonzero raw Y source and can be discarded.
This is only a support upper bound; it grants unavailable subsets.

For m packets of at most V dimensions whose joint row space B contains
W tensor F^V, necessarily m>=8. All96 columns of A are nonzero, hence

    sum_i u(r_i)>=96.                                      (COVER)

Take any m-7 packet positions J and their joint row space B_J. The seven
omitted packets imply dim(B/B_J)<=7V. The map from W tensor F^V into that
quotient has kernel dimension at least V. Therefore B_J contains a nonzero
row of W tensor F^V, using at least37 source blocks. Ordering the ranks gives

    sum_(i=1)^(m-7) u(r_i)>=37,  r_1<=...<=r_m.              (DISTANCE)

This argument does not assume independent packets and holds for arbitrary
coordinate mixing. Existing Y-dependent hub side information is excluded;
if supplied, its actual row space must be included and the quotient demand
re-derived. A temporal order of linear messages does not itself change the
argument, provided every packet still has the stipulated local raw support.

## 3. Analytic integer rank floor

Assume COVER and DISTANCE but sum r_i<=47. Put q=m-7 and h=r_q.

* h>=6: the qth and seven later ranks already sum to at least8h>=48.
* h=5: the first q ranks have sum at most12. Two rank-five entries leave
  budget two, giving u-sum at most16+16+2=34. At most one rank-five entry
  gives at most16+2*7=30, using u(r)<=2r for r<=4. DISTANCE fails.
* h=4: the first q ranks have sum at most19. Four rank-four entries leave
  budget three and give at most32+4=36. At most three rank-four entries
  give at most8k+(4/3)(19-4k)<=100/3, since u(r)<=4r/3 for r<=3.
* h=3: the first q rank sum is at most26, giving capacity at most104/3<37.
* h=2: the first q rank sum is at most33 and u(r)<=r for r<=2.
* h=1: DISTANCE gives q>=37 and m>=44. The excess rank above one per
  packet is e<=47-m<=3. Concentrating this excess maximizes capacity,
  giving at most m+2^e-1. At m=44,45,46,47 this is51,48,47,47, all<96.

All cases contradict a necessary condition. The numerical relaxation is
attained at rank mass48 by twelve rank-four packets: capacity96 in total
and40 in the five cheapest. This is not an actual packet code. Exhaustive
integer histograms of mass at most47 corroborate the analytic proof; the
finite search is not extrapolated to untested field volumes.

## 4. Complete target invoice

The400 source raw roles all ascend by dimension eight. Concavity gives
sum of segment r^t>=8^t on every monotone path. Grant all400 their direct
rank-eight price. Retain all other exact H4 paid and target terms and charge
the eight forward rank-nine packets:

    T_best=T4,
    P_best=P4+18*(400{rank8}-R_old)+18*8{rank9}.

R_old is the exact1,710-call source raw histogram. The resulting remaining
moment per native is enclosed around47.07974274338085. This grants all
forward offdiagonal, coupled, ordinary, storage, precision and physical
completion duties free and is more favorable than the admitted paired word.

Since r^(199/200)>=r*9^(-1/200) for1<=r<=9, rank mass48 requires a moment
strictly above47.4755522002641. The optimistic margin is already short by
more than0.3958094568832 per native, or7.124570223897 across18 repetitions.
Exact integer200th-power inequalities determine the signs, not floats.

## 5. Exact local geometry and the remaining escape

A further exact certificate resolves individually global packet rows.
For487 of511 nonzero binary directions z, the hosted roots with v_j.z=1
span all eight root dimensions. No nonzero Gram row can be formed at that
line from unchanged raw Y values. The other24 directions are exactly the
omitted root normals: their excluded roots have rank seven and annihilator
line a(z). Distinct omitted roots have distinct annihilator lines. Thus no
chart of dimension at least two can host any nonzero global Gram row.
Eight individually global packets would each need at least rank eight.
The rank48 theorem also covers larger fragmented packet spaces and is the
stronger complete-budget gate.

This closes the fresh raw-source return route. Mixed current rows,
already-paid informative routes, common histories with full restoration,
and changed endpoint/caller interfaces remain legitimate escapes. Feedback
constructions that carry reverse information on funded raw paths are not
excluded. The next concrete task is an actual preterminal mixed-row interface
supplying W while retaining the original Y information at its final facets,
with current observations and every route charged.

Both strict complex/BIT suppliers, the complete physical compiler, and all
five foundations remain. No new complete kappa is claimed.

## Provenance

Prepared for @CubeJerry with substantial OpenAI assistance. The integer E8
representation and frozen native/H4 sources are predecessors. New here are
the omitted-source frame certificate,37-source block bound, all-volume
packet capacity reduction, rank48 completion obstruction and full target
comparison. Source mathematical assumptions are not promoted to theorems
by this package. The original E8 mathematics is not claimed as new.
