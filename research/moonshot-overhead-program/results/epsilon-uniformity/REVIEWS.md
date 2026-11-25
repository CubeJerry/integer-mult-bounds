# Review and verification record

## Root characteristic/reserve obstruction

Root proved the claim; Route C independently re-derived it from the pinned
source. The separate [review](route-c/ROOT-OBSTRUCTION-REVIEW.md) records the
exact scope. `verify_obstruction.py` checks 1,228 eigenvalue/duality identities,
complete spectra of orders 32, 512 and 8,192, 19,998 integer windows and 42,531
alias pairs, with changed-dimension and window controls. CPython 3.12.14 passed.
These are finite checks supporting a written universal proof, not formal
certification of that proof or an implementation replay of the multiplier.

## Route C variable-arity recurrence and padding

Root reviewed NONSTATIONARY-RECURSION.md and SOURCE-PADDING-BARRIER.md directly,
including every proof. The normalized recurrence unfolds with prefix products;
integer-root/ceiling shrinkage separates log-log widths by positive constants;
the excess, rounding and subcritical polynomial toll sums converge under the
stated hypotheses. The conditional interchange result includes a fixed
dispatcher, uniform physical costs, shrinking-volume or descriptor-only
descents, and fixed input/output representation. These are unproved premises
for the published family. The equality-invoice Walsh obstruction is correctly
separated from actual runtime. No implication to a complete root multiplier
is admitted.

For padding, root checked the exact finite-interval dichotomy: either the
radix exponent is constant and the ratio falls by 2^D, or an exponent jump
forces ratio at least b/2. Source b>W>=2^m is specific to its literal all-shift
batch. The first-digit batching factor is a different loss and is correctly
kept separate. The power-selected plateau claim uses literal materialization;
it does not cover different input-dependent radices or compressed layouts.

Root replayed both exact verifiers under CPython 3.12.14. `check_padding.py`
passed 4,160 interval cases and 30 prime-radix witnesses. `check_recurrence.py`
passed 1,970 integer-root cases and 135 recurrence-boundary cases, with
rounding, critical-toll and fixed-excess controls. These tests supplement,
rather than establish, the asymptotic proofs.

All reviewers are AI agents. No independent human review, Lean build or
complete upstream source-kernel replay is claimed. Route A and B results
remain subject to their separate reviews before final admission.

## Input-dependent radix: root review, 25 November 2026 UTC

Root independently checked the narrow prime-interval packing, integer-root
rounding, compatibility-product scan cost, both volume bounds, and the
bitlength selectors in `route-c/INPUT-DEPENDENT-RADIX.md`. The primary
Baker--Harman--Pintz paper's Theorem 1 and effectivity comment were opened
directly. Its unspecified absolute threshold is explicitly retained; finite
experiments do not certify that threshold. No algebraic blocker was found.
The product Q must be supplied and its creation remains charged separately.
This repairs the literal padding obstruction but does not supply the varying
radix address-map compiler or a complete multiplication bound.

An isolated replay exposed an implicit sibling-module import in the finite
checker. The author was asked to fix the import and add checks for the
summable-slack version, which was not covered by the first receipt. Record
the new replay separately after it runs; do not treat this review as an
already successful replay of the revised script.

## Binary-length schedule: root review

Root read `route-b/binary-length-schedule.md` and checked its Kraft sums,
length-first enumeration overhead, actual-step budgets, space fences, sparse
parameter choice and conditional polylog-log transfer. No blocking issue
was found. The method is credited as an application of program-length
universal search; it does not claim the source candidate constants satisfy
the new conditional hypotheses. The separate bounded-preflight proposal
has not yet been admitted.

## Results saved pending full review

`PADIC-LIFT-OBSTRUCTION.md` has a complete written root proof, with independent
review and finite checks pending. Its target is the literal zero/one label
matrix modulo p², not arbitrary lifts or general algorithms.
`route-a/elementary-tower-extraction.md` is a proposed source-wide extraction;
its compiler and threshold audit is an explicit gate. No global envelope
from that draft has yet been added to the proved programme bound.

## Admission after full compiler review — 25 November 2026 UTC

The pending tower gate above has now passed. Root read the complete November
interchange, permutations, Walsh, integers and uniformity proofs and the
September elementary-stream/affine/parking proofs against the detailed
`route-a/compiler-invoice.md`. Route C separately performed the same critical
dependency audit in `route-c/ELEMENTARY-TOWER-REVIEW.md`. Both found a fixed
polynomial in the complete finite budget S, without an extra tower.

The final implementation incorporates the material clarifications from
review: triangular sums are successive single-control rotations with fixed
collapsed counter arity; shape and row-padding checks precede materialization;
the aggregate setup clock counts actual candidate TM microsteps and is not
reset per node; immutable operands support a late fallback; short-multiplier
scratch is bounded by its time and reused additively. Numerical precision
uses the source's computed error majorant. Complete interpreted costs and
all-length visited space are charged before chunking and scheduling.

The admitted result is `THEOREM.md`, with the stronger
`log m=O(j³ log(j+2))` profile. Concurrent S002 separately admitted a coarse
sixth-power profile at `96028cba1342c02bdca1f537ae9a80485087bdf3`; its work is
credited and preserved. Neither extraction is a full template execution or
a claim to improve the unknown actual published residual term.

The literal p-adic lift proof has also passed two independent reviews, in
`route-b/independent-reviews.md` and `route-c/PADIC-LIFT-REVIEW.md`. Root's
exact checker passed and was independently replayed by B. Root replayed the
revised isolated radix checker successfully: 116 admitted constant-volume
selector cases, five prime witnesses, 55 admitted summable-slack cases,
five slack witnesses and the exhaustion control. The earlier import failure
is resolved and retained above as part of the record.

Root reviewed the full bounded-preflight and rowwise-chunk proofs. The
preflight theorem is admitted as a **conditional** complete transfer; its
stronger family hypotheses are not consequences of the tower extraction.
S002's earlier linear-r diagonal chunk wrapper is explicitly credited.

## Synthesis, window-resource and rational-height reviews — 15:20 UTC

Route B independently audited the complete theorem, finite-budget ledger,
compiler interface, common-space chunking, integer inversion and absence of
circular assumptions. Its `route-b/global-synthesis-review.md` records exact
hashes matching checkpoint0961d2083f80429dde4b6ec5197585f727c7f87b. No
blocking error was found. That review covers the theorem as saved there.

Root independently checked `route-c/WINDOW-PREDICTOR-DEPTH.md`: the parity
subcube and unit-ring condition, integral upper predictor, affine-query
degree induction, clamped window, modal mass, adjacent-binomial ratios,
two outside bands, explicit large cutoff and matching resource upper bound.
Root replayed `check_window_depth.py` under `python3 -I -B`; it passed
10,625 band identities, 5,310 odd-characteristic witnesses, 64 mod-four
negative controls, 2,925 centered-window comparisons and twelve exact source
tail budgets. The floating illustrative optimum is not asymptotic evidence.

Root read `route-a/rational-geometry-height.md` and corroborated Route C's
independent review: quotient principal minors, projection complements,
fixed-depth endpoint construction and minor-controlled triangular factors
give polynomial bit heights and an explicit singly-exponential-in-m
generator. S002's prior proof is credited.

Root also reviewed `route-a/single-exponential-root-hypothesis.md`. The
conditional implication is accepted: actual output and denominator budgets,
shifted roots, Boolean-quotient specialization, finite free scalar algebras,
repair units and full pattern enumeration, both transform branches,
numerical norms, physical compiler, chunking and threshold inversion are
charged. Hypothesis MR itself is not proved. This review does not promote
its conclusion to the unconditional programme bound.

Finally, root read the complete macro-dispatch transfer. Its finite opcode
contracts, additive description scans, explicit stack/head return costs,
shrinking-tree count and charged bill computation are sound as a conditional
compiler lemma. The full source primitive library remains an obligation.

## New formula constructor and full transfer — 16:01 UTC

Route A independently audited C's full cyclic-product invariant, balanced
formula size, degree accounting, integral graded tensor sum and scalar
descent. Route C independently audited A's both-branch transfer, all-shift
repair, finite budget, compiler and joint cost/threshold inversion. Root
separately read both complete arguments and the original source batch-width
interfaces; its six-file receipt is ROOT-FORMULA-REVIEW.md. Arbitrary batch
width is permitted by the source, so cyclotomic regular descent creates no
unaccounted power-of-two width requirement. Route B's additional synthesis
audit is being finalized after a reported preliminary pass.

Root's isolated exact replay is root-formula-replay.json. It verifies
84 predictor cases, 152 cyclic products and 72 full descended matrix roots
with maximum dimension96. The script hash is
67404455b1003f470839c634c780e66e98d0cc9fe0304dbd48be918597fd6475.
The checker includes the wrong-phase control, unequal lengths, all shifted
non-Boolean query cases and a nonsemisimple characteristic-three example.
No inference about asymptotic complexity is based solely on these cases.

Root read C's formula-size-transfer review and A's matching-recipe review.
Root independently verified the latter's compression lemma: contracting
linear subtrees and removing s expensive additions leaves at most2s+1
product components with O(D(s+1)) linear leaves. Expanding those leaves and
applying the published homogeneous multilinear formula lower bound yields
K>=2^{2^{Omega(log²D)}} for the literal unreduced recipe. Top-degree
extraction produces (-1)^u e_D(X) without adding sum nodes. The formal,
syntactic-degree, multilinearity and unreduced-recipe restrictions are
essential and remain explicit.

The earlier Route B synthesis hash for THEOREM.md applies to the exact
preserved BASELINE-THEOREM.md, SHA256
6e814bff4ae85f44cebd5a8fcab74a2c8383b47e0628b486de9add34a56e6097.
No prior review is silently reassigned to the stronger theorem.

## Final additional synthesis gate — 16:05 UTC

Route B's independent formula-synthesis-review.md passes the full new
algebra, actual generator, finite-ring and arbitrary-batch-width source
interfaces, both branches, complete physical profiles and eligible integer
inversion. It records eight exact reviewed hashes. Root read the entire
review. The theorem's review status is now accepted by A, B, C and root.
The later scoped recipe paragraph and concurrent-formula credit were
separately reviewed by root; status/provenance edits are not silently
attributed to earlier exact snapshot hashes. The proof of Theorem F is
unchanged. No additional numerical replay was required.
