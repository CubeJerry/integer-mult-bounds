# E002: three-hour uniformity research report

Session start: 2026-11-25 21:19:31 UTC (26 November 08:19:31 Melbourne).
Requested research deadline: 2026-11-26 00:19:31 UTC. The authoritative
completion time and elapsed duration are recorded in `SESSION.json` after
that deadline. This report records completed mathematical work and its limits.

## 1. Strongest admitted unconditional result

Put L=1+log2(n), x=log2(L), and
Phi(y)=(y+1)^(2/3)(log2(y+2))^(1/3). The admitted written construction is

    T(n)=O(n sqrt(L) 2^{O(x^(2/3)(log2(x+2))^(1/3))}),
    cells ever visited=O(n).

It describes one fixed exact deterministic finite-alphabet multitape machine
returning the full product with contiguous input and output. Its invoices
include actual data movement, preparation, arithmetic, finite repair,
precision, decoding and carries. All lengths are covered by a guarded
construction and an exact fallback. No unproved efficiency-family premise
remains in this admitted construction. Absolute constants and the eventual
threshold are not numerically evaluated.

The theorem is `lead/variable-profile-theorem.md`, admitted by
`lead/ADMISSION-V.md`, with `PARAMETERS-V.md` and independent complete
composition reviews from the original A and C workers. Its mathematical
snapshot reviewed before admission has SHA-256
`ccad2873bfa36755382495a24c488d1cdfd622f562fb1c8b3cd7712b6a4b9cb4`;
the status-only amended file has SHA-256
`e3cdaae1f325951365104e275c84663f5e0d290bffcf59482845fe6f5d5611ea`.

This improves the explicit programme envelope present at session start.
An intermediate complete construction gave exponent
x^(3/4)(log2(x+2))^(1/4), retained in `lead/polynomial-profile-theorem.md`.
The final result implies H(n)<=2^{O(x^beta)} for every fixed beta>2/3.
It does not prove the log-free beta=2/3 bound, polynomial overhead in x,
bounded overhead, or the exact n sqrt(log n) endpoint. `kappa_ov` remains
unassigned. Nor does an explicit envelope prove an actual-runtime comparison
against a previously published unspecified o(1), or establish priority.

Concurrent sessions S003 and E003 independently admitted constructions on
the same final scale. Their records and all S004 progress were merged and
preserved. E002 does not claim to have newly audited every concurrent proof.

## 2. Why the variable profile closes

The exact and numerical stages need different arity schedules. Exact
interchange can take polynomial arity in its active bit width. Its retained
geometry selects a power-of-two distance of order
(log m/log log m)^(1/3), giving local loss exp(O(Phi(log m))). The compiler
uses a single explicit common characteristic-two field, a compatible
composite radix, and actual occupied batches. The logarithms of child bit widths contract
geometrically, so the sum of the Phi losses is controlled by its initial
value. Polynomial ordinary work is attenuated by choosing the fixed arity
power sufficiently small.

Space requires more than a time recurrence. The grouped endpoint and query
layouts use their actual incidence/rank volumes, not a generic polynomial
parameter bound for retained data. All low-rank query vectors fit together;
metadata is removed before recursion; explicit main-child and finite-repair contractions, together with bounded
reserve inflation after clearing, permit reused marked tape regions. The proof
therefore bounds the union of visited cells. A late cache audit also ensures
that small spatial children carry local plan chains instead of scanning a
large global plan once for every tiny record.

The numerical Walsh stage takes slower arity: log m is of order Phi(log a),
where a is its active address width. It pays for rational scalar operations with the scalar primitive
and for address changes with the completed exact interchanger. Compatible power-of-two
batches are preserved through recursion; the proof tests the actual spectator
divisibility and avoids multiplying a new padding factor at every level.
After the initial selected-bit gather, active children are contiguous.

The normalized recurrence has a local cost exp(O(Phi(y))), recursive loss
exp(O(y^(1/3)(log y)^(2/3))), and a decrease of order Phi(y) in y.
The potential gap across that decrease dominates the recursive loss with
strict slack. Explicit operation/gain guards give absolute linear working
precision in the required precision parameter. The complete setup is
subexponential in that parameter with a fixed exponent below one; the
smaller Walsh-only setup bound is not substituted for the combined setup.

Finally the actual source integer caller is retained: guarded XOR/position
operations, permutation routing, CRT and the short occupied Fourier calls
are all charged. The proof retains the ordinary O(k log k) short multiplier
where needed, avoiding a circular invocation of the desired bound. Chunk
compression uses exp(O(Phi(x))) chunks and pays for every digit product and
assembly scan. Preparation budgets, quadratic clocks and marked O(n)
regions provide an exact schoolbook fallback before any cap is crossed.

These are written algorithm/profile proofs. No complete astronomical
template or full multiplier was executed, no new Lean refinement was built,
and the reviews are AI-assisted mathematical reviews, not human refereeing.

## 3. A complete conditional log-free improvement

`lead/rectangle-volume-conditional-transfer.md` and `lead/ADMISSION-RV.md`
prove the implication

    RV-I and RV-W => T(n)=O(n sqrt(L) 2^{O(x^(2/3))}),
                    visited space O(n).

Both hypotheses remain open. RV-I requires an actual exact shared-pencil
executor with recursive volume and visited-space costs controlled by
rectangle count/rank, including low-rank delivery, uniform construction,
full occupancy and explicit individual child/reserve bounds. RV-W requires
the analogous numerical shared-pencil Fourier-call delivery, with polynomial
ordinary work, coefficient heights, array volumes and all source interfaces
preserved. A matrix identity or small rectangle count alone supplies neither.

Under these contracts, exact geometry has logarithmic loss O((log m)^(2/3));
the Fourier construction has logarithmic recursive loss O(sqrt(log m)).
Exact interchange retains polynomial arity; the numerical schedule takes
log m of order y^(2/3), giving the stated log-free exponent. Reviewers required explicit child contraction and visited
regions because neither follows merely from field width or live-data size.
The corrected full conditional theorem passed two independent written reviews.
Its parameter ledger is `PARAMETERS-RV.md`.

## 4. New geometry and endpoint sharing results

The cross-pinned partition fixes a source coordinate and a different
destination coordinate. With C=binom(2d-1,d), its exact regular incidence is

    lambda=C^(d+1)(q-1)^d t^(d(d-2)),
    R/N=C^(d+1) 2^(d(d-2)) (1-1/q)^(d(d-2)).

It saves t^d in incidence and removes the old positive q^d factor from the
normalized rectangle count. It is a genuine disjoint partition preserving
the source Gram conditions. It does not change the optimized leading order
of the unconditional bound, and no new complete physical compiler for it
has been claimed. The independent replay checks 358,296 uniquely partitioned
edges, 21,912 rectangles and the exact count formulas. See
`review-a/CROSS-PINNED-RECTANGLE-PARTITION.md` and its C review.

The lead also constructed a deterministic overlapping cover attaining
logarithmic incidence O(d^2+d log q), the order permitted by the reviewed
noncanonical covering bound. However, at balanced parameters that particular
family has R=o(N), while its intended exact matrix P*-I has rank N-o(N).
Even weighted rank-one rectangles from that family cannot give the required
identity. This is an exact rank obstruction to this tempting cover, not a
general impossibility theorem for all good partitions or multiplication.
See `lead/overlapping-cover-rank-gap.md` and `lead/ADMISSION-CG.md`.
General distinctions between local covers and partitions are prior art;
`COVER-PARTITION-LITERATURE.md` records the primary sources and read scope.

The endpoint-reuse characterization gives a positive compiler criterion.
Partition rectangles into groups with separate oriented endpoint copies.
One reserve-only preparation per endpoint copy, followed by arbitrary
rectangle-specific triangular tails, is possible exactly when the union of
endpoints in each connected group has zero within-side Gram distance and
distance d across sides. Necessity follows from a shared suffix subspace;
sufficiency uses the actual source endpoint construction. Original masks
and weights are retained, so geometric enlargement does not add scalar edges.

For a uniformly described grouping with charged polynomial membership and
ordinary work, let rho be the maximum group incidence per endpoint. Serial accumulation
reduces the shared-pencil recursive-volume invoice to
O(D(1+rho)(1+mr*/N)), with visited regions and temporary reuse explicitly
accounted. A far triangle excludes one universal preparation, and a q^d
grid forces rho>=(q-1)^d within this strategy. No sufficiently better
compatible grouping has yet been constructed. See
`review-c/COMPATIBLE-ENDPOINT-REUSE.md` and the independent lead review.

## 5. Positive batching and its source applicability gate

`batching/WEYL-STAR-BATCHING.md` supplies a physical common-basis executor
for a specified family of phase-modulated translations on complete occupied
query fields. A simultaneous pivot/coset change leaves all parameter data
independent and uses the existing controlled-small-block tape processor.
One basis serves every query term, permitting pointwise row mixing; it can
be retained across a sequence using exactly the same family. The local bill is
V[m^K+sqrt(a+1)E_I(a) polylog(k)] plus separately charged preparation and
declared row buffers. Exact checks include 252 weighted pencils, 38,776
output entries and 252 two-stage reuse cases. No exponential table of all
control settings is assumed.

This family does not immediately cover the full retained source pencil.
A concrete nonzero q=4,L=2 source rectangle has middle maps exchanging
X_j with Z_b and Z_j with X_b. On complete registers
x_j=(X_j,Z_j), z=(Z_b,X_b), these are star swaps. Their relative permutations
do not commute, excluding a common scalar diagonalization of those terms,
even with arbitrary common input/output bases and nonzero phases. It does
not exclude a basis for one fixed sum, block methods or later cancellation.

An earlier draft incorrectly described a common exchange of spectator query
halves; the initial C review repeated it. Both are explicitly superseded by
the corrected `STAR-SWAP-FALSIFIER.md` and final C review. The full two-half
checker verifies the correction in 768 cases. Theorem V never depended on
this late draft. The corrected source snapshot is
`5db06e11c67fba3e0ed5db2a060bf3616a40f42c5d2281853f58f50f50fd3ceb`.

The subsequent exact SWAP/Weyl expansion is valid, including its inverse
phase and normalization. The unresolved operation is contraction of its
Q^2 parameters while restoring independently occupied rows. Literal broadcast
expands volume by Q^2. Walsh conjugation on existing occupied parameter
fields instead produces explicitly nonzero off-diagonal row blocks. The
note proves scoped phase-pinching and rank obstructions for that literal
lift, including a full-rank defect in its stated regimes. Its three-term
kernel comparison concerns the pure equal-weight SWAP family, not the
complete signed source pencil. Both final reviewers accept these limits.
See `batching/SWAP-WEYL-CONTRACTION-GATE.md`; NI5 and RV-W remain open.

## 6. Certificate statements and verification boundaries

The retained scheduler certificate has F(x)=inf_j(d_j+x/(j+2)). If d_j
tends to infinity, F(x) tends to infinity. Under the specifically defined
full diagonal enumeration, its index penalty gives an Omega(x^(2/3))
certificate floor. These statements concern the written certificate and
that enumeration; they are not lower bounds on actual scheduler runtime,
arbitrary enumerations or multiplication. A fixed-epsilon theorem plus an
effective generator alone does not supply a quantitative overhead rate.

Likewise, the numerical invoice frontier concerns a specified positive-cost
ledger. Upper estimates cannot be relabelled as actual mandatory charges.
Query representative counts, universal-basis obstructions and the new
contraction tests all retain their stated model restrictions. The protected
discovery route continued after these obstructions rather than promoting
them into a general endpoint impossibility claim.

Primary source pins are OpenAI math
`3344da59991ed94f9ba711217b29c1d760badfa6` and canonical programme source
`e54523517d0f03e58352e647c403a5af3e525a57`. Both main refs were refreshed
unchanged at 23:44 UTC. The focused prompt blob
`ce6fe4edbf039aa964a08aaec216a1cc60dbfe2a` and parent prompt blob
`b5762a4dacb999703e83621301a455fbb12755f7` were independently rehashed
unchanged at 23:47:41 UTC. Source coverage and partial-read limitations are
recorded in `SOURCE-AUDIT-E002.md`. Formal statement/instruction files were
read, but no fresh formal build or full transitive formal audit is claimed.

## 7. Saved progress and next obligation

Six remote checkpoints were individually verified before final integration:
`f3ed00d`, `9d5abf1`, `9e84956`, `8af1911`, `a8dd6c2`, `b979d2e`.
The first complete improved theorem was saved at checkpoint three; V at
checkpoint four; the conditional transfer at checkpoint five; late geometry
and positive batching at checkpoint six. The final checkpoint contains this
report, corrected swap bridge, endpoint-reuse review and completion metadata.
Publication uses a lease against the current remote head and preserves
concurrent sessions. No upstream PR or message was sent.

The next substantive task is a genuine physical improvement in shared
endpoint/query delivery or numerical execution. The endpoint characterization
reduces one route to a uniformly describable compatible grouping of low
incidence. The Weyl route needs a cheaper occupied-parameter contraction or
an executor for a fixed star-swap sum. Grouping coordinate-value orbits may
be worth testing, but no fast occupancy-preserving tape gather into that
layout has been supplied. Sorting into it cannot be assumed free. These
are concrete open construction obligations, not efficiency hypotheses
silently included in the admitted unconditional theorem.

Credits: @CubeJerry; the pinned source authors and preceding programme;
all named original and final-phase construction/review agents; substantial
ChatGPT multi-agent mathematical assistance. No literature priority,
practical threshold, formal proof, human refereeing or full execution claimed.
