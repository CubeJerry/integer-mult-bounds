# The certified quiet-loan family does not deliver new required endpoint coefficients

**Proved source-specific application of the inherited monotone-frame obstruction.**
This is a scope audit of the newly verified quiet helper loans, not a new general
monotonicity theorem or a new multiplication bound. The complete target remains
open.

## 1. Source and inherited geometry

The pinned source is `research/shared-wire-split-composition/data/final.json.gz`,
SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
It has 400 main inputs, 1,710 main MOVEs and 71,261 instructions. Frame labels
refer to the exact binary subspaces in this file, not merely their dimensions.

We reuse the programme's monotone-frame reasoning: ascending routes preserve
initial-frame containment for every input coefficient. Related established
source constraints and exact binary-space arguments are recorded in
`research/p104-monotone-frame-ceiling/PROOF.md`, especially sections 1–2.
The earlier programme source endpoint analysis and
`results/shared-core-temporal/ENDPOINT-REPAIR-PROOF.md` already expose the
endpoint obstruction; neither the 208 off-diagonal terms nor their geometric
origin is presented as new here. The present calculation checks what the new
354-window quiet-loan family changes.

Write the first main copy as x, the second as x+q, and retain arbitrary shared
helper inputs h. Then x,q,h are independent input coordinates. The required
second-minus-first main endpoint is E q, with E obtained by exact homogeneous
replay of the pinned source. There are 208 nonzero off-diagonal entries.

## 2. The class being audited

Use passive main carriers on their literal source main MOVE itineraries, with
arbitrary cochart linear changes of their payloads. Allow every single-MOVE
quiet helper loan of the following certified form. A non-main holder moves
S→T while a main carrier is at S; that main's later prescribed itinerary reaches
T before the helper's next source touch. A signed swap places a coded payload
in the helper and its dirty common payload in the main carrier. At T an inverse
swap restores the common payload before its next source use. The helper may be
read by additional difference-carrier operations during the loan. Such operations
must not contaminate the reference first-copy source or introduce another route
for q-dependence. Compatible loans can be chained and difference carriers can
acquire new codes; this is not restricted to independent raw shears.

An actual quiet loan temporarily places arbitrary dirty common content on a main
route. That is allowed here. We track only coefficients of the independent q
inputs. During the loan these coefficients can cross the helper route and the
passive main route; after restoration they do not leak into the continuing common
source, including its descending owned routes. Read-active loans or other mixed
encodings that do permit such leakage are outside this class.

## 3. Application of the inherited invariant

Every one of the 1,710 main MOVEs is strictly ascending. Any quiet helper loan
has a companion sequence of these routes from S to T. Therefore S is contained
in T, even without separately assuming that the helper MOVE ascends. The exact
census independently checks all 354 loans against the actual binary subspaces.

For an input q_i initially at A_i, maintain this invariant: a nonzero coefficient
of q_i occurs only at charts containing A_i. It holds at entry; cochart scalar
operations preserve it; every q-carrying route in the audited class is ascending.
The quiet swaps do not open a q-dependent descending common route. Thus the
invariant remains valid even with unlimited local memory, arbitrary local coding,
and any physically compatible sequence of these loans.

For exactly 104 of the 208 required off-diagonal coefficients E_(j,i), the final
chart B_j does not contain A_i. All are original X-to-Y coefficients. These
coefficients are impossible in the audited class. A complete E q endpoint cannot
be achieved by adding only these quiet loans to passive main itineraries.

This statement counts 104 missing coefficients, not 104 independent messages,
104 extra fields or 104 paid MOVEs. One nonmonotone coded message might repair
several deficits using side information. No additional cost lower bound is
claimed from this count.

## 4. Stronger optimistic time-graph check

The verifier also grants a substantial relaxation: each chart caches every input
coefficient it has ever received, for free and forever. Each prescribed main MOVE
transports the entire source cache rather than one field. Each quiet-loan start
transports the entire source cache along its helper route. All 354 loans are
granted simultaneously, even when actual loan windows conflict. Scalar work,
storage, common-payload restoration and route capacity are ignored in this
relaxation. Reachability is therefore necessary, never sufficient.

At the full endpoint, exactly 104 of the 208 required off-diagonal coefficients
are reachable in this relaxation both with and without all the quiet loans. No
new required coefficient becomes reachable. The 104 unreachable coefficients
coincide exactly with the geometric obstruction above. This is a source-bound
certificate about the entire finite time graph, not a conjecture extrapolated
from a failed search.

The negative/escape control injects q_0 into the empty chart3 at entry, an operation
outside the ascending class. The formerly forbidden coefficient at output112
then becomes reachable. The control shows why a genuinely nonmonotone route or
another mechanism for q-dependence can escape the obstruction. It is not a free
construction or an uncharged proposed algorithm.

## 5. Verification and next mathematical obligation

Run from a checkout containing the pinned source:

    python research/moonshot-005-program/results/quiet-loan-scope/verify.py --output /tmp/quiet-loan-scope.json

Expected status is `PASS_QUIET_LOAN_MONOTONE_SCOPE`, with 354 quiet windows,
104 geometrically forbidden terms, 104 optimistic temporal failures, and no newly
reachable required term. `RESULT.json` lists every excluded coefficient, exact
source/destination frame, and rational coefficient. The script uses standard
library rational arithmetic and exact binary Gaussian elimination.

The constructive quiet primitive remains valid and may be useful inside a richer
code. To advance the native endpoint, the next mechanism must transport needed
q-dependence outside this monotone route class: for example through a descending
owned route, a read-active helper whose common distortion is later repaired, or
a joint representation that permits such source-channel mixing. Every common
payload, decoder, storage operation and paid transport then needs an explicit
proof and invoice. No new kappa follows from this scope result.

Prepared by Worker A for @CubeJerry, with substantial OpenAI assistance, retaining
all source and predecessor credit. Quiet-loan discovery and the complete literal
seven-ADD instance are due to Workers B and C in this session.
