# A paid GF(64) source with full original rank in all 6,470 foreign H projections

On the same H words, the following finite source makes the H-to-visible-port
observation injective on the *entire original donor bank* for every one of the
6,470 native foreign pairs, with all other sources fixed. This property is
stronger than formal independent-port rank at a single H. It is weaker than
the equality of inverse fibres for the prescribed common endpoint across
different donors. The ordinary source uses commuting coefficient rows and
is a rank control for the target-directed coupled construction.

## Original source and genuine early map

Use the field, route pins, true owner ordering and H algorithm from
[the H proof](PROOF.md). For each native donor j, sort its 28 actual H planes
by chart ID and assign them distinct field nodes 1 through 28 in this order.
A component of n=9 or 36 ports, k=n/3, contains eight base stripes. Give
each stripe 2k independent polynomials f_c of degree below 16 over GF(64).
The raw coefficients are the original donor input. This gives
8(6+24)16=3,840 field coordinates. Order the original donor coordinates by
component, stripe, channel, power. Within one stripe call the first k channels
A and the last k channels B.

The ordinary source quotient at every plane is the vector of evaluations
f_c(x_H) of all the channels. At ordinary full/partial charts the full H word
in the companion proof recovers this entire quotient from the visible tuples
on the single-donor slice. Which half is early is a true physical source
choice. At a fully early three-donor H put the A evaluations in the first
eight lanes and the B evaluations in the last eight. The designated
large-early donor at a partial H supplies both halves early. On each ordinary
half-early occurrence, supply just A or B early and add the complementary
half onto the genuine late Y line visits.

Exactly 100 donors have no singleton. Their 28 planes comprise four
ordinary all-early and 24 half-early incidences. Within the half-early
incidences ordered by H ID use A at the first 12 and B at the final 12.
Every channel contributes one early evaluation at sixteen distinct nodes.
The 16-by-16 Vandermonde source transform is invertible.

Each of the other eleven donors has exactly one singleton H0, two ordinary
all-early and 25 half-early incidences. Use A early at the first 12 half-early
incidences, and B at the final 13. Write x0 for the singleton node. In its
early stripe put the 2k ordinary evaluations in polynomial degrees 0 through
2k-1 and an additional k values delta f'_c(x0), for c in A, in degrees 2k
through 3k-1. Every B channel gives sixteen distinct-node ordinary early
evaluations. Each A channel gives fifteen distinct-node ordinary early
evaluations and one derivative at the singleton node, scaled by nonzero
delta. The only degree-below-16 polynomial with all these values zero has
fifteen roots, one with multiplicity at least two. It is zero. Thus the true
early map on every original donor bank is invertible.

## Singleton compatibility uses the actual receiver, not an independent extra

At a foreign (i,j), the receiver sees exactly sixteen actual source H planes
through j. If none is the singleton, each H tuple recovers all ordinary
evaluations conditional on donor j, by the H proof. Sixteen-node interpolation
then recovers every polynomial in every stripe. This covers 6,110 pairs.

For any of the remaining 360 pairs, impose zero observations at the fifteen
ordinary H planes. Put

    phi(T) = product over those fifteen a of (T-x_a).
    r_i = phi'(x0)/phi(x0) = sum over a of 1/(x0-x_a).

All the nodes are distinct, including x0. Each polynomial is a scalar
multiple of phi. Consequently the missing singleton scalar derivative is
exactly r_i times the corresponding ordinary value at x0. This equation
holds on the residual kernel, with no independence assumption on the extra
rows.

Let A(Z) and B(Z) have degree below k and have as coefficients the A/B channel
values at x0. The actual polynomial seen by the singleton H Hermite module
on this kernel is

    P(Z) = (1+delta*r_i*Z^(2k)) A(Z) + Z^k B(Z).

Its k distinct port nodes are the actual ones for receiver i in the chosen
spread component. Compute P and P' there. In the power basis on the 2k
coefficients of (A,B) this is a 2k-square matrix. The complete list of
720 minors in source-output/SINGLETON-MINORS.json records the actual node
subsets, r_i, delta and exact rank. Every matrix has rank 2k. The following
scale choices in power-basis integer notation are fixed once for each donor.

| Donor j | Singleton H | delta at n=9 | delta at n=36 |
| ---: | ---: | ---: | ---: |
| 49 | 956 | 3 | 2 |
| 97 | 982 | 1 | 1 |
| 53 | 983 | 1 | 2 |
| 77 | 1008 | 7 | 1 |
| 93 | 1009 | 1 | 7 |
| 8 | 1062 | 1 | 2 |
| 82 | 1063 | 3 | 1 |
| 58 | 1064 | 2 | 1 |
| 106 | 1090 | 1 | 1 |
| 31 | 1091 | 1 | 1 |
| 105 | 1118 | 1 | 2 |

This proves trivial kernel of the full foreign observation on all 3,840
independent original coefficients, including all singleton cases. The field
is the same six-bit field and the actual H maps and owners are exactly the
ones already specified. The exact 720-minor statement is finite. Its
application to arbitrary field-valued input follows from the kernel proof.

## Paid source implementation

At the source line, snapshot its independent original X coefficients for
the later line additions. In each channel, implement the genuine 16-by-16
early map by six-bit binary elimination and place its outputs on the
prescribed real early owners by the explicit source permutation. On a
genuine late Y visit, add only the indicated ordinary evaluation from the
stationary snapshot. No operation changes Y's own baseline coefficient.
Clear the snapshots when all late taps finish. The source compiler replays
each distinct early word and inverse on the 96-dimensional binary basis,
checks the literal permutation on all owners, and charges every nonzero
bit of every late coefficient row.

| Source operation | Binary whole-record operations |
| --- | ---: |
| Early evaluation words | 115,084,896 ADD |
| Actual source owner permutations | 7,647,444 ADD |
| True late line additions | 88,184,400 ADD |
| Snapshot copies | 2,557,440 ADD and 2,557,440 INIT |
| Dirty CLEAR | 2,557,440 |
| Forward source ADD | 213,474,180 |
| Pure-X inverse reserve at Hub | 122,732,340 ADD |
| Forward plus reserved pure inverse | 336,206,520 ADD |
| Extra MOVE | 0 |

Each donor peak is at most 23,040 stationary extra owners, with 2,557,440
as the aggregate peak bound. There are 426,240 genuine early owners and
321,000 genuine late line visits at eight-copy scale. Total source and H
forward ADD is 615,610,180, or 1,125,363,352 including both sets of pure
inverse reservations. Source and H together charge 2,732,496 INITs and
the same number of dirty CLEARs. These totals cover just the specified
two stages.

## Verification and endpoint boundary

Run the accompanying rs_source.py with `--repo . --out /tmp/rs-source`.
The input routes, spread, geometry and phases are pinned in RESULT.json.
The payload supplies deterministic source-word hashes and every singleton
minor. Setting the 36-port scale to one at donor 8, H1062 yields rank 22
instead of 24 at receiver 3. Replacing the derivative scale by zero makes
a true 16-row early source channel have rank 15.

The original low-excess matrix specifies one *shared* delivered sum across
the donors. Individual 3,840-dimensional injectivity leaves the inverse
maps for different donors unconstrained. For example, donor 0, 61 and 62 at
H263 have ordinary RS scalar evaluation coefficients on the common channel
basis, even though physical phases or H later mix those channels. The
S027/S028 commuting-source and fully-early divisibility gates still constrain
attempts to use this source for the identity blocks on that chart. The
one-fixed-vector Clifford orbit bound has a different hypothesis: here the
evaluation node can change with H. The intended role is a paid GF64 input
witness for rank-transport modules, independent of the selection of a
target-compatible coupled source. A joint phase-respecting D/K/F word for
the specified low return, both strict suppliers, whole recursion and all
five foundations remain separate. No new κ.

Credit @CubeJerry and the original native, source, finite-field and
phase-module contributors. This finite evaluation/derivative source,
singleton kernel certificate and binary price were developed with
substantial OpenAI assistance.
