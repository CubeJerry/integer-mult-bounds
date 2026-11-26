# Lead review of the C(4,3) translation-orbit optimum

Disposition: **accept the exact restricted optimum six and the
three-case reduction for the broader product search**. Reviewed proof:
`5162f1ec0a541d336bb8c5406a614885b580ef6ee6c0e35240632cd6a9c14595`.
The lead read the complete proof and verifier and independently replayed
its exact functions. `translation-orbit-replay.json` records all 50 local
subset pairs, 343 difference boxes, 27,216 disjointness checks, 17 budget
patterns, 216 size profiles, and the 96-rectangle sharp witness covering
1,728 edges with source and destination loads six.

For a local supported rectangle A times B in F2^2, its simultaneous
translation orbit covers each edge of its difference footprint once.
This is immediate for a singleton side. Two disjoint two-element sides
are complementary cosets of the same two-element subgroup; their common
stabilizer cancels the two representations of each difference. The orbit
loads are exactly |A|/|H| and |B|/|H|. Replacing a singleton-by-two orbit
with the corresponding coset orbit retains the edge set and lowers loads.
These facts tensor and yield precisely the stated partition of [3]^3
into difference boxes with costs `(3^r,3^(d-r))`.

The budget-five case split is exhaustive. A box with two full projections
must have cost (3,3), leaving only two unit-cost boxes. Its size nine or
18 gives the claimed strict volume deficit. With at most one full
projection per box, there are at most two expensive boxes. Two size-12
boxes cannot be disjoint because every projection has at least two of
the three symbols. The one-expensive and no-expensive cases use the same
intersection fact; their maximum covered volumes are strictly below 27.
The two difference boxes in the witness lift to load six exactly.

For the broader product search, total incidence at load five is at most
640. If every rectangle had edge-to-incidence ratio at most 8/3, total
edges would be at most 640 times 8/3, less than 1,728. The complete six
local-size options give exactly three high-efficiency shapes. Arbitrary
coordinatewise alphabet permutations put one selected rectangle into
the fixed representatives used by the three searches. This reduction
includes all product rectangles in the remaining partition; it does not
require the entire partition to be maximal or translation closed.

All four recorded searches reached their limits without a witness or an
infeasibility certificate. Their failure is inconclusive. The exact
optimum-six theorem instead comes from the finite volume proof and
applies only to unions of whole translation orbits. Averaging cannot
extend it to arbitrary disjoint partitions: that creates a weighted
decomposition and changes the object being bounded. Asymmetric product
partitions and correlated sides remain open at load five, and unbounded
JR remains open. No global multiplication improvement follows here.
