# Exact common-plane growth budget gate on #7481

This is a scoped source optimization obstruction, not a multiplication lower
bound. It establishes no new complete kappa. All five foundations remain.
Prepared for CubeJerry with substantial OpenAI assistance, Apache-2.0.

Input: exact PR7481 head89eaa9d8cae37c1540de98f2d29a3abaabb96a2b,
WORD compressed SHA256
acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9.
VISITS-7481.json is reconstructed from every one of its76475 instructions.
It contains1517 cocharted contact components and6279 complete MOVE positions.
It includes main,helper and owned visits. All public entrance/exit and all
INIT/CLEAR visits are frozen. ADD/COPY join both operand visits; SCALE is
internal to one visit. Components are maximal under these actual accesses.

Fix any2-dimensional binary subspace W. For any chosen internal component at
chart U, replace all of its visits by chart U+W; leave unchosen components
unchanged. Every scalar contact has both operands in one component, hence
commutes with the common invertible chart change on arbitrary dirty inputs.
No source/target or owned lifetime is retimed. The complete actual entry/exit
quotients, including monomial phases and rank0 ordinary maps, must be paid.
This proof gives them the optimistic cost from dimension differences.
In particular a rank0 quotient can still be a nonidentity monomial with a
global phase. Zero optimistic recursive cost removes only its positive-rank
child; it does not prove that the ordinary map is identity or erase its
physical work. This obstruction grants every such ordinary service free.

For one original nested MOVE U subset V, write
d=dimV-dimU, a=dim(U+W)-dimU, b=dim(V+W)-dimV. Then a>=b.
If b>0, selecting the lower component forces selecting the upper component,
because W has a vector outside V. If b=0, the upper chart is unchanged and
the lower can grow independently. The original orientation remains legal;
zero-rank edges are permitted and receive zero optimistic recursive cost.

Let f(r)=r^t, f(0)=0. When both components can change and b>0, the three allowed
states00,01,11 have costs f(d),f(d+b),f(d+b-a). Therefore the saving equals

    [f(d+b)-f(d+b-a)] x_lower
      + [f(d)-f(d+b)] x_upper,

subject to x_lower<=x_upper. If b=0, the sole lower weight is f(d)-f(d-a).
A frozen lower/upper becomes a fixed0 variable; a forbidden lower selection
is explicitly forced0. Summing all6279 MOVE weights reduces the entire
optimistic invoice exactly to maximum weight closure. The usual source/sink
minimum-cut reduction is used; the integer implementation checks the final
closure constraints and equality of the primal selected weight and
sum_positive_weights minus total_flow on every plane.

All43435 binary planes are enumerated once as pairs v<w<v xor w. The rank
increase is0 when both v,w belong to U,1 when exactly one nonzero plane vector
belongs to U,2 otherwise. Thus the geometry is computed from all actual source
subspaces, not from an assumed orthonormal basis or a sampled flag.

For t=4981/5000, POWER-BOUNDS.json encloses every f(r),0<=r<=9, at denominator
D=10^24. For each2<=r<=9 its candidate integer A is authenticated by
A^5000 <= r^4981 D^5000 < (A+1)^5000. f(0),f(1) are exact. Each closure weight
is replaced by its outward upper integer endpoint. Every real saving of any
selected subset is at most its upper-weight closure objective. Hence an exact
maximum closure on the upper weights is a rigorous upper bound, even though
different weights may share correlated power errors.

PLANES-7481-EXACT.json records the maximum upper bound6/10^24 per native across
all43435 planes. The maximizing upper-bound cut is plane[14,66], components
692 and849; its actual paid histogram delta is empty. The6 units are interval
uncertainty. Consequently no member of this common-plane growth class can
supply a native movement gain exceeding6e-24 at kappa=.0038.

Each canonical auxiliary chart has symplectic mixing block B of rank equal to
its dimension. Rank subadditivity under Clifford multiplication implies the
actual quotient mixing rank is at least the absolute difference of these
dimensions. Thus actual recursive prices cannot beat the optimistic bill used
here. Additional scalar,monomial,ownership,precision or compiler costs cannot
make the excluded budget positive. Degenerate Gram spaces are allowed by the
retained general-GL canonical chart definition; no false orthonormality test is
used in this lower bill.

This extends the earlier public-helper-only common-vector growth scope by
including main and owned companions and common rank2 spans. It retains those
predecessors' credit. It does not exclude different planes at different
components, shrink/grow mixtures, changed scalar contacts, boundary changes,
new productive helpers or earlier joint forward/reverse source mechanisms.

## Exact zero for the entire increasing-concave price cone

The stronger CONE-PLANE-TEST.json now checks the nine integer tariffs
`f_k(r)=min(r,k)`, k=1,...,9, on every one of the43435 planes. All390915 exact
closure optimizations have maximum0. Capacities are exact integers multiplied
by10^24; no root enclosure is needed for these tariff runs. The underlying
program still checks every cut's primal/dual equality and legality.

Let any increasing concave integer-rank tariff f have f(0)=0. Write
`Delta_j=f(j)-f(j-1)`, with Delta_1>=...>=Delta_9>=0. Then for r=0,...,9,

    f(r) = Delta_9 * min(r,9)
           + sum(k=1,...,8) (Delta_k-Delta_(k+1)) * min(r,k).

All coefficients are nonnegative. For any fixed plane and selected component
subset, its saving is the same nonnegative combination of its nine extreme
tariff savings, each at most0 by the exact cuts. Hence the saving is at most0
for every increasing concave tariff. The empty subset attains0. This proves
an exact zero optimum for the entire rank2 common-growth class; it is stronger
than the earlier6e-24 enclosure at t=4981/5000. In particular the class cannot
improve the Gaussian moment at either kappa=.0038 or.004, or any0<kappa<1.
The conclusion concerns the declared frozen boundaries and unchanged scalar
contacts; it grants all ordinary phase,route and lifecycle overhead free.

Open next questions: coordinate different local spans or mixed growth/shrink
with actual legal crossings; preserve a complete scalar endpoint and regenerate
the whole caller invoice before treating any positive relaxed price as a
supplier. The selected result remains unchanged.
