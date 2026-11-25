# Independent C review of the crown-product laminar obstruction

Disposition: **accepted in the stated ordering/laminar models**.
Read `../lead/crown-product-laminar-obstruction.md` in full and checked
both proofs independently. The cited Welzl-order paper supplies the
research lead, not an unproved step in these elementary statements.

For right words at Hamming distance h, coordinatewise counting gives
`(q-2)^h(q-1)^(k-h)` common neighbors. For distinct words this is at
most `(q-2)(q-1)^(k-1)`, yielding the exact symmetric difference.
The binary-string transition identity includes both endpoint bits.
Each endpoint has degree `(q-1)^k`, so total runs equal

    (q-1)^k + (1/2) sum_j |N(y_j) symmetric_difference N(y_(j+1))|.

The lower bound follows. A reflected q-ary Gray order has Hamming-one
successive pairs, including reversed block boundaries, proving equality
for **total** runs. It does not prove equality for the maximum single
run count or a laminar hierarchy.

Adjoining the full set and singleton leaves and then refining a laminar
family to a binary tree preserves its original clusters. Extra clusters
can only decrease the minimum number covering a neighborhood S. That
minimum equals `|S|` minus the number of internal nodes entirely contained
in S: those full subtrees make precisely the counted leaf merges.
There are N-1 internal nodes, each containing two distinct words. The
common-neighbor bound therefore proves the asserted laminar lower bound.

Overlaps or nonzero scalar weights do not evade the argument when
every rectangle is contained in the graph: every represented edge must
be covered by at least one used cluster. Rectangles using nonedges and
then cancelling them are a different model, correctly excluded.

The boundary q=2 is sound: every neighborhood is a singleton and the
total is N. For q=4,k=2, the universal bound is 54 total incidences and
at least four at some source. It is correctly distinguished from the
general opposing-star partition of maximum load three. The later
finite hierarchy optimization may be stronger; it is not needed for
this universal proof and is not independently certified by this note.

For fixed k>=2, the maximum-load lower bound grows as q^(k-1), exceeding
`c^k(t+1)^c` for q=2^t and each fixed c. One common ordering or one
laminar endpoint family therefore cannot supply JR. Arbitrary nonlaminar
partitions and multiple hierarchies remain outside this result. Supported
parity decompositions are excluded only when they obey this same
one-family restriction. No arbitrary-load tensorization, general
refutation of JR or algorithmic runtime lower bound is inferred.

Credit: the lead's run/tree calculations, the cited graph research
lead, S004's JR and positive control, @CubeJerry, and AI-assisted
independent review. This is written proof review, not formal checking.
