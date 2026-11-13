# Two-subspace E7 bound and all-monotone arrival obstruction

Proved in the stated interface, with separate independent geometry and
universal proof reviews. No complete supplier or new kappa. All restrictions
below matter. The reviewed draft is preserved verbatim under author/.

## Exact geometric proposition

Complete the pinned BIT source's fourteen weight-four supports to the full
120 real E8 root lines: representatives2e_i and all weight-four sign vectors,
first nonzero coordinate positive. Each has squared norm4. If r is any root
and F=r^perp, then any two proper real subspaces C,D of F satisfy

    |R intersect (C union D)| <= 52.

This counts root lines in the set union, not its linear span. The bound is
sharp. Every actual foreign contact set S_i has55..62 lines in F_i, so no
two proper subspaces of F_i cover S_i.

### Universal reduction and finite certificate

The checker constructs all120 lines from authenticated source supports,
verifies every root reflection on every line and transitivity on all120,
and verifies that all111 actual lines belong to this set. Thus it suffices
to use F={x_0=0}, with63 root lines. A generic orientation gives positives;
the seven indecomposable positives form a basis Delta. Every root has
integral Delta coefficients of one sign, and the Cartan matrix has diagonal2,
off-diagonal0 or-1. All these assertions are checked exactly. The seven
simple reflections permute the finite spanning set, so their group W is finite.

Given any nonzero w in F, choose g in W maximizing (g w,rho), with
(rho,alpha)>0 for every alpha in Delta. A negative pairing (g w,alpha)
would be increased by reflection in alpha, contradicting maximality.
Hence g w is in the closed positive chamber. A positive root orthogonal to
g w uses only simple roots with zero pairing, since all coefficients and
pairings are nonnegative. Some pairing is positive because w is nonzero.
The roots orthogonal to w are therefore contained in a conjugate maximal
parabolic root set obtained by omitting one simple root. Every proper
subspace lies in such a nonzero-normal hyperplane.

Enumerate the seven fundamental-weight normal orbits under W. In integral
simple-coroot pairing coordinates a, reflection j is
a'_i=a_i-a_j*Cartan[j,i]. Breadth-first closure, identifying opposite normals,
is exact and exhaustive. The checker verifies distinct root-zero masks.
For any two orbit types, transitivity lets the first normal be fixed at its
representative, while every second normal is enumerated. This covers all
pairs of proper-subspace root supports through the preceding containment.

| Node | Normal lines | Root lines in a flat | Maximum union with any flat |
|---|---:|---:|---:|
| 0 | 378 | 21 | 46 |
| 1 | 5040 | 10 | 41 |
| 2 | 63 | 30 | 51 |
| 3 | 1008 | 16 | 45 |
| 4 | 288 | 21 | 46 |
| 5 | 2016 | 13 | 42 |
| 6 | 28 | 36 | 52 |

There are8821 maximal-parabolic root sets. Two36-line E6 flats intersecting
in20 lines attain52. The unbounded real-subspace quantifier is discharged by
the chamber proof, not inferred from a finite search. The exact script and
certificate are e7_two_subspace.py and E7-TWO-SUBSPACE.json.

## Precise computational interface

Work over a characteristic-two field with linear value operations and whole-V
records, using the actual111-role geometry. The source circuit may be changed
arbitrarily within these restrictions:

1. There are111 X records starting at their own root lines and ascending to
   Hub. They may mix with cocharted X records and stationary local X caches,
   never with a nonlocal packet or Y information. Every source row at C thus
   uses only x_j with L_j contained in C. Grant unlimited retention of histories actually generated from these
   sources, with every cache initially zero, and grant ordinary operations free. Exact X restoration is not needed for this
   lower bound; requiring it only restricts the interface further.
2. There are111 public Y records ascending from0 to distinct final facets F_i.
   They may mix cocharted public Y records and read packets/caches, while
   restoring arbitrary y coefficients. There are no moving Y-bearing copies.
   Track physical trajectories through whole-record renamings; a swap that
   changes the prescribed X/Y route families is not silently permitted.
3. There are nine persistent whole-V pure-X packet lifetimes descending from
   Hub to0. Grant arbitrary initial linear payloads in x. Each may add actual
   local source-cache functions and apply invertible block units. No global
   payload is discarded by overwrite or CLEAR/re-INIT. Its terminal payload
   is taken immediately before legitimate final clearing. Packet-packet
   mixing is unnecessary and is not included in the present proof.
4. The resulting terminal fitting has canonical foreign support. Admitted
   rank-nine rigidity gives this for all scalar characteristic-two fields and
   all V in the invertible-Schur block stratum. A separately justified fixed
   canonical decoder is another sufficient premise. Arbitrary noncommuting
   singular-Schur block fittings remain outside the conclusion.

An optional extension permits additional local, upward moving X-only records
born from these local sources. They cannot bring free global data into their
birth charts. All their movements are separately charged. Downward nonlocal
copies and Y-bearing movers remain excluded.

## Terminal normalization

For packet p, solve all subsequent additive/unit updates backward from its
terminal payload Z_p. At a read at C, its payload is a linear function of Z_p
plus later local cache edits at D contained in C. Every such edit has original
support inside D. After arbitrary public-Y mixing the final map is

    Y_final = y + A x + B x,       rank(A) <= 9V,

where all B contributions propagate upward with original support in their
current charts. Hence B has zero diagonal and noncontact blocks. Completion
Y_final=y+x makes A a fitting with diagonal identity and noncontact zeros.
The admitted minimum-rank theorem and hypothesis4 make A a gauge of K.
Thus B_i has a nonzero block at every foreign port in S_i. Initial packet
payloads need not be in the code: this conclusion concerns terminal information.

## Per-facet arrival accounting

Let r_i count local source-record paths visiting exactly F_i. For each such
path let C be its chart immediately before first entry. This is proper, and
the arriving source row is supported inside C. Every source history ever
formed at F_i is a combination of these arrivals. Zero caches or stationary
copies add no new support. Their total support is in the union of r_i proper
subspaces, even when all source operations and timing are redesigned.

Let s_i count packet paths visiting exactly F_i. Each has a first proper
chart D after departure from F_i, because its destination is0. All its later
cache edits below F_i are supported inside D. Future edits while it is still
at F_i use the source arrivals already counted by r_i. Thus normalized local
terms from every read at F_i add at most s_i further proper support subspaces.
Repeated reads or invertible units do not enlarge this support union.

Let C_Y be Y_i's last proper chart before F_i. All normalized local information
already on that public trajectory is supported inside C_Y, including earlier
public-Y mixing and packet reads. No other public-Y trajectory reaches F_i:
its endpoint is a distinct seven-dimensional facet, incomparable with F_i.
At F_i, new local contributions therefore come only from the source arrivals
and packet future-edit terms just counted. Consequently B_i is supported in
at most1+r_i+s_i proper subspaces of F_i.

Since S_i cannot be covered by two proper subspaces, r_i+s_i>=2 for every i.
Summing over111 receivers gives

    sum_i (r_i+s_i) >= 222.

Each ascending X path visits at most one seven-dimensional facet; each
descending packet path also visits at most one. The111 X and nine packet
paths therefore give at most120 such visits. This contradiction excludes the
entire stated monotone source/packet interface, not just the fixed clean-X
history word. It grants arbitrary source coding, chart refinements, initial
packet payloads, public-Y coding and free stationary caches.

## Optional local-copy price corollary

With extra upward-local records, every new independent support subspace at
a facet must trace to a separate MOVE into it from a proper chart. A record
born at F_i uses already arrived data and cannot add a new support subspace.
At least102 additional positive-rank MOVE events are therefore needed beyond
the111 X and nine packet paths. In the whole-V model, each costs at least1
movement-moment unit for0<t<=1.

Grant all original X and Y routes their direct rank-seven minimum and all
nine packets their direct rank-eight minimum. The optimistic base is
222*7^t+9*8^t, equal at t=.995 to1610.2088734840998343... . The complete
fixed-even-m limiting ceiling is1621.750880211152355246... . Only
11.54200672705252... remains, far below102. The limiting deficit exceeds
90.45799327294747; every finite even m is stricter. The separate exact integer-root receipt author/BIT-REVERSAL-BUDGET.json
recomputes this price from the pinned complete caller. It does not price nonmonotone
or Y-bearing copy architectures.

## Limits and controls

Nonmonotone packet turns break future-edit locality. A source receiving
nonlocal packet information breaks source ancestry. Moving Y copies can
bring incomparable local histories to a final facet. Different terminal
fittings require new support analysis. These are genuine escape mechanisms
with their own acquisition, restoration and complete-price obligations.
Whole-V record counting does not automatically apply to fractional-volume
decompositions or a different chart model. No universal multiplication lower
bound is asserted. Both strict suppliers and all five foundations remain.

The52-line bound is sharp: an asserted51 bound is rejected by the explicit
two-E6 witness. A two-line toy plane shows why dimension alone is insufficient:
two proper lines can span a plane. This proof instead uses the actual union
cardinality. Three-subspace coverage is not excluded or claimed impossible.
Independent geometry and universal proof reviews are in review-geometry/
and review-proof/. Root reviewed both arguments and their exact source scopes.
