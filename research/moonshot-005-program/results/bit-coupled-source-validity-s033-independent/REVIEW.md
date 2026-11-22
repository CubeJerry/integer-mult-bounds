# Independent S033 source-validity review

**Accepted in the precise scope below. No fifth receiver or new complete kappa.**

The root reviewer independently implemented GF64 multiplication with polynomial
x^6+x+1 and reverse-pivot elimination. The source-validity constructor, its
geometry helper, and its rank routines are not imported. Geometry is reconstructed
from exact dot products of the pinned root table and literal plane incidence.
The checker reads the S032 source matrices and the proposed coefficient changes
as data, and rebuilds all source views itself.

The fresh exact replay confirms all693 geometric protected views have rank96,
including639 native views. It verifies protected/complement block separation
and literal identity of all complementary coefficients. The three changed
physical early matrices are rebuilt from real row owners and phase frames and
have full rank480. The unchanged eight early bases are reused with source pins.

All2268 ordered propagation pairs at the three changed donors are independently
recomputed from the inverse source views. The maxima are84,60,60, with exactly
the reported histograms. The inherited complementary bounds360,120,120 give
444,180,180, each strictly below450. This is a finite exact certificate and a
uniform field-extension/direct-sum argument, not a sampled rank estimate.

The full paired H-fibre source observations are independently checked at all72
geometric/67 native interfaces. All four t=1 collisions are independently
verified against full480-coordinate source observations, and all four corrupted
collision vectors are rejected. The protected rank is exactly95 in each case.

The reviewer also read the actual source/H/D assembly in interfaces.py and the
whole-fibre proof. The source/H observation identities plus invertible complete
proper restrictions justify whole-fibre equality. The132 proper restrictions,
44 D identity equations and144 D section checks remain author computational
replays with this mathematical/code review; they are not labelled a second
independent matrix reconstruction in this package. The binary compiler receipts
were reviewed for composition and full cost accounting; the author compiler
and symbolic circuit replay were not independently reimplemented here.

The t=26 result is a proved source-specific local construction with exact
finite evidence and stated inherited dependencies. The earlier t=1 point was
only admitted for local interpolation, so its failed full views refine an open
obligation rather than invalidate a previously claimed full-source theorem.
Alternative t=1 extensions are not ruled out.

Reproduce from the repository root:

    python3 -B research/moonshot-005-program/results/bit-coupled-source-validity-s033-independent/check.py --repo . --out /tmp/s033-independent-source

Expected: PASS_INDEPENDENT_T26_SOURCES_PROPAGATION_H. The saved output and log
come from this exact checker. Source hashes bind every literal input and the
independent arithmetic implementation. No global native, erasure, compiler,
precision/tape or analytic recovery assumption is discharged.

@CubeJerry; root review with substantial OpenAI assistance. Independent agent
review is not independent human review or a formal-kernel proof. Apache-2.0.
