# Independent review: varying aligned scalar stripes remain insufficient

## Decision and quantified scope

Accept the varying-stripe gate at its stated scope. For every positive
integer replication r and every finite characteristic-two field F, the
fixed balanced atlas cannot realize the complete native target if each
ordinary source quotient, up to bijective relabeling, has the form

    Z_(j,H,t) = sum_(s=1)^16 c_(j,H,t,s) X_(j,s,t),
    t=1,...,360r,

in one common actual stripe indexing across the source banks. Coefficients
may vary arbitrarily with donor, plane and stripe. The eleven singleton
source encoders are granted their full real 540r capacities. Nonlinear
downstream functions, nonlinear quotient relabelings and arbitrary
same-chart caches do not invalidate the information bound. Extra routes
or raw Hub-to-output information are not granted.

The result does not exclude general source arrays that mix these stripes,
arbitrary source-bank gauges that destroy this aligned-coordinate form,
or newly paid routes. It is not a MOVE tariff or a new complete kappa.

## Mathematical checks

**Independent quotient variables are available locally.** At a receiver
whose source cuts are tight for every donor in H, each donor's sixteen
visible quotient coordinates jointly distinguish its whole source bank.
The stripe hypothesis makes this a direct sum of invertible 16-by-16
matrices. Fixing all other visible plane coordinates leaves the H
coordinates independently free. Outside-facet source inputs can neutralize
the canonical packets because their canonical restriction has rank nine.
They cannot affect the proper routes into that receiver. This justifies
the input variations used in the plane argument on the canonical-zero,
zero-Y slice; it does not assume globally independent overlapping plane
queries.

**The plane target has the asserted direct-sum form.** Tight gluing gives
one common p-dimensional inverse-coordinate lift for the donors of H.
Each donor's inverse decomposes over the same actual stripe coordinates.
Equality of the full lift spaces therefore implies equality of their
one-dimensional lift spaces separately at each stripe. The target row
space is a direct sum of one-dimensional rows rho_(i,H,t) on the actual
donor scalars at stripe t. The nonzero normalizations introduce no extra
dimensions or receiver-specific source information.

**Arbitrary port functions factor through row-space intersections.** The
fifteen visible H-to-D4 ports have total alphabet size |F|^p, exactly the
number of plane-target values. Recovery forces this entire tuple to be a
bijective relabeling of the plane target. Hence each port is a function of
that target. If one port is visible to several joint-tight receivers, its
function is invariant under every corresponding target kernel, and thus
under their sum. The annihilator of that kernel sum is the intersection
of the target row spaces. This is a common-function theorem, not an
assumption of linear port operations.

Aligned direct sums make that intersection split stripe by stripe. A
stripe survives precisely when all receivers seeing the port have the
same projective target line. If a receiver had no incident port whose
neighborhood was monochromatic at that stripe, every one of its ports
would be independent of the stripe while its target varies. Recovery
would fail. Thus the finite self-cover partition condition is necessary.

**Color caps bound information even when later maps mix stripes.** Every
covered port factors through the union of its surviving stripe lines.
At each stripe their span has dimension at most the number of target
colors and at most the number of native donors in H. The finite cap
therefore bounds the entire covered-port tuple by |F|^(alpha_H*p).
Arbitrary later maps or same-chart caches cannot enlarge that alphabet.
Uncovered ports and singleton planes are separately granted their full
physical capacities, so no information is discarded in the upper bound.

**The global cut is valid on the canonical kernel.** On ker(K), the
native output is X because O=I+K in characteristic two. This kernel has
dimension 102*5760r. Every noncanonical route that could alter a receiver
crosses the counted plane boundary. Original X values later restored at
Hub are not an additional unpriced output channel. The resulting bound
538644r < 587520r contradicts injectivity, with deficit 48876r.

## Independent finite computation

The checker reads the pinned layout and balanced factor; it imports no
author search code, no author cap table, and no floating solver. It
recomputes every actual plane/D4/facet incidence, every singleton flag,
all 6110 tight and 360 slack foreign source cuts, and every joint-tight
receiver set. It verifies the true 45-port and 15-visible-port counts,
the actual early-source count 5760, the ordinary source bundle size 360,
the singleton bundle size 540, canonical rank nine, and all 111 outside
canonical rank-nine restrictions.

The finite solver represents each vertex by its allowed-color domain.
For every port it intersects those domains to compute possible monochrome
colors, and removes unsupported colors at each vertex. A singleton domain
with only one supporting port forces that entire port to its color. It
also enforces that every required color appears. It then branches the
most constrained vertex and introduces symmetric unused colors only in
canonical order. Every rule preserves all possible completions. Search
is exhaustive and has no time limit. Successful assignments are checked
again directly against the original neighborhoods.

This differs from the author's bitset-of-color-classes search. Both use
the elementary necessary test that k color classes contain k pairwise
disjoint nonempty ports. An equivalent view is to select a spanning
hyperedge cover and ask whether its connected components admit at least
k nonempty color classes; merging classes preserves feasibility.

The independent result is:

| Native donors in H | Rank cap | Planes |
| ---: | ---: | ---: |
| 2 | 1 | 204 |
| 2 | 2 | 23 |
| 3 | 1 | 630 |
| 3 | 2 | 249 |
| 3 | 3 | 2 |

All 1108 per-plane caps, receiver sets and uncovered-port counts agree
with the final author certificate. Every published successful coloring
is checked directly. There are 420 nontrivial finite-domain searches and
50,871 visited search states. The resulting capacities are 498240 for
covered ordinary ports, 34464 for 1436 uncovered ports, and 5940 for
singletons, totaling 538644 before replication.

## Independent controls and pins

The solver is compared with direct enumeration on all hypergraphs with
at most three vertices and all ordinary graphs on four vertices, for
the relevant two- and three-color conditions (also one color on the
smaller cases). The common-function step is checked on all 1225 pairs
of two-dimensional binary quotient row spaces on F2^4: the equivalence
relation generated by their fibers has exactly the number of classes
predicted by their row-space intersection. All 81 two-stripe combinations
of binary projective lines verify the direct-sum intersection rule.

Output RESULT.json records the exact author proof and compressed decision
certificate hashes, the layout and factor hashes, every independent
decision and successful coloring, and the control counts. The proof
review and exact calculations together justify admission. No statement
about unrestricted array impossibility is admitted.
