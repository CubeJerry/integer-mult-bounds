# Root review: one local export at a rank-one destination

**Accepted for the exact source-local relaxation stated in the author proof.**
Root reconstructs both actual terminal packet families, then checks all source
pins, all 4,888 individual exclusion duals, 1,712 positive payload witnesses
and every one of the 3,548 projective destination groups. The independent
implementation uses SymPy rational nullspaces: evaluating a receiver normal
on a basis of the source chart identifies its quotient class. This differs
from the author's rational row-remainder algorithm. A separate least-pivot
binary elimination supplies the baseline fitting classification.

## Completeness of the finite geometric reduction

For A=N-perp and B a codimension-one subspace of A, B-perp is a one-dimensional
extension of N. If it contains an eligible receiver normal r_i outside N, it
is exactly span(N,r_i). Thus every useful destination is represented by one
of the checked projective classes; an arbitrary rational destination adds no
unchecked case. Normals already in N give receivers containing A, where any
source-local payload is already local and cannot repair the missing role.

The classification concerns the 33 actual named raw-cache source charts. It
grants all original coordinates local to that chart plus the fixed G15 space
for free. It does not grant arbitrary nonlocal recoding at that chart, or every
possible chart in a changed construction. Both coupled and uncoupled G spaces
are checked separately. A currently fitting or already-completed receiver is
not counted as a new missing role.

## Universal field and width extension

Every negative witness q is binary, supported outside the receiver's local
coordinates and outside the proposed source's available original coordinates,
and annihilates G. Its requested coordinate is one. These are literal matrix
identities after any characteristic-two scalar extension and tensoring with
I_V; the argument is not extrapolation from a finite scalar search.

At the sole exceptional group D4->{2,13}, the same one-field payload could
be decoded with arbitrary V-by-V coefficient matrices M2,M13. The missing-role
dual u13 forces I=M13 Z(u13), hence M13 is invertible. This is a derived square
matrix fact, not an assumption about the decoder. The two other duals have
identical restrictions to the source-local coordinates and annihilate G.
They force M2 S=I and M13 S=0 for the same S, a contradiction. No commutation
or scalar inversion is used. Any independent original-Y noise can be projected
out; genuinely new X information from a changed feedback/source interface is
outside the declared payload space.

All other groups have at most one individually possible missing role. Two
separate local payloads for the exceptional pair satisfy the supplied exact
identities, which Root independently verifies along with their G and local
remainders. This is an algebraic positive control, not chronological acquisition
or an efficient physical decoder. The gate does not exclude interacting exports.

Root's exact execution is recorded in RESULT.json with its certificate hash.
The predecessor's full source MOVE audit and original native gzip authentication
are retained dependencies; this independent check does not misreport either
as freshly rerun. All physical/compiler/erasure/precision/recursive obligations
and all five foundations remain. Credit @CubeJerry, predecessor source authors,
S015 Worker C and Root's separate review; substantial OpenAI assistance.
