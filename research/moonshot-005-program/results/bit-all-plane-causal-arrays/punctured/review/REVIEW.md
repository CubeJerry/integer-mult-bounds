# Independent review of the 227 two-donor causal array interfaces

## Decision

Accept the positive local theorem for all 227 actual two-native-donor
A2 planes. The explicit F128 coefficients give every actual receiver
an invertible projection onto each donor's complete 360-dimensional
quotient. The early/late map is causal and invertible on all public
inputs, including arbitrary independent Y baselines. Its stationary
early cache, ordinary additions and physical holder permutations are
charged. No additional movement is introduced at H.

This acceptance is local. It does not assert compatible quotient inputs
from the same original source bank at different planes, a completed
D-to-K-to-F code, singleton handling, global restoration/preload maps,
or a complete supplier price. The author's scope statements are sound.

## Direct independent verification of the original transfer matrices

The independent checker reconstructs all actual H-D4-facet incidences
from the pinned integer root table. It checks all 227 source-pair sets,
45-port lists, native receiver sets and thirty-row receiver selections.
It verifies that each local coefficient file has the full 90-by-90
matrix over the stipulated field and that every claimed receiver/donor
condition is represented.

A separately written C++ verifier uses carryless polynomial product and
long reduction modulo z^7+z+1. It constructs the original 60-by-60 matrix

    [ A[S,45j..45j+44]                 0 ]
    [ C[S,45j..45j+44]  B[S,15j..15j+14] ]

for every actual receiver and donor. It performs direct Gaussian
elimination on all 15,098 such matrices. Every matrix has rank sixty.
This check does not reuse the author's kernel bases or rely on its
reduced 15-by-15 determinants. The direct full determinants are retained
in DIRECT-DETERMINANTS.json. Setting C to zero in a control gives rank
45, as predicted by the causal information deficit.

## Algebraic existence argument

The reduction to L C N is valid. The early block has rank thirty, its
right kernel N has dimension fifteen, and the late-source block has
rank fifteen with a fifteen-dimensional left annihilator L. A full
kernel vector must have early part Nq; a compatible late part exists
exactly when L C Nq vanishes. The late block has trivial right kernel,
so full invertibility is equivalent to invertibility of L C N.

For each fixed receiver/donor pair, the map from C's relevant block to
L C N is onto the fifteen-by-fifteen matrices, using one-sided inverses
of L and N. Its determinant polynomial is therefore nonzero. One entry
of C changes this reduced matrix by a rank-one matrix, so that variable
has degree at most one in each determinant. It belongs to only one
donor block and occurs in at most thirty-six receiver conditions.
The product polynomial is nonzero with individual degree at most
thirty-six. The finite-grid lemma over F128 consequently gives a common
nonzero assignment. This existence argument is independent of how the
explicit candidate enumeration found the retained matrices.

The reviewed explicit matrices have the stated trial distribution and
all their actual direct projections pass. They are finite witnesses,
so no probabilistic or numerical qualification is needed for them.

## Physical holders, cache and causality

The real early flag has six holders from each donor at every D4 exit.
One per donor is assigned to each of six stripes, giving ninety early
inputs per stripe. The real late flag has two source-visited holders
from each donor and eight direct-ground Y holders. The review explicitly
assigns source holder s to stripe s+2*((j+p) mod 3), using the local
port ordinal p. It fills each stripe to two holders at each port using
the actual eight direct-ground holders. Every genuine holder occurs
exactly once. Each late stripe has fifteen source additions from each
donor and sixty pure-Y holders; every one of the ninety late fields
has an arbitrary independent original Y baseline.

Physical contents are permuted at H into the stated input-column order.
The early permutation is performed **before** copying the early
coordinates into the stationary cache. Thus C reads the intended
coordinate order after the early public holders have left H. The
late permutation is performed before B. Output records keep their
real port destinations; only contents are changed by co-located ADDs.
No MOVE or imaginary source holder is hidden in these permutations.

The independent replay applies the literal V90 word and the crosswave
ADDs to all 1260 original binary columns for each of the six physical
stripe layouts. It obtains the exact triangular public map, including
the arbitrary late baseline. All 630 cache owners per stripe remain
dirty and can be retired after the late additions. Omitting a cache
copy or the crosswave stage changes the output and is detected.

## Ordinary invoice

The V90 word has 167,325 ADDs on 630 binary records and is independently
replayed on every input column. The review recomputes the binary weight
of every retained C coefficient and agrees with the author's crosswave
ADD counts. Each H needs 3780 stationary binary cache INIT, copy ADD and
dirty CLEAR operations, and no additional MOVE. Across all 227 planes
the INIT and dirty CLEAR counts are each 858,060.

The review materializes the actual input permutations. The early
permutation has eighty field swaps and is used six times. The late
permutations have swap counts [84,84,81,81,85,85]. Each field swap costs
twenty-one binary ADDs. Their exact per-H cost is therefore 20,580 ADDs,
less than the author's conservative 22,428 bound. The exact local totals
with these physical permutations are:

    3,210,516..3,232,878 ADD per H,
    731,524,866 ADD over all 227 H.

The author's conservative total 731,944,362 remains valid. Source
encoding, other chart maps, all global restoration and ground preload,
body work and recursive accounting remain separate costs.

## Common field and pins

The companion full-three-donor V45 word is independently replayed over
F128 on all 315 original binary columns. This is a new realization in
the common field, not an embedding of the earlier F64 field into F128.
The Vandermonde proof still applies to all distinct-node receiver sets.
Its literal word has 42,522 ADDs.

RESULT.json pins the author proof, coefficient file, author result,
layout, and direct full-determinant certificate. PHYSICAL-PERMUTATIONS.json
contains the exact physical input orders and every ADD of their swap
prefixes. The checker imports no author algebra or search implementation.
No global quotient compatibility or complete kappa claim is admitted.
