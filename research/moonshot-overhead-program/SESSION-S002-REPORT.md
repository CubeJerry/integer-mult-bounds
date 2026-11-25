# S002 research-session report

This report accompanies the permanent branch
`research/moonshot-overhead-program` in `CubeJerry/integer-mult-bounds`.
The session ran from **2026-11-25 13:20:23 UTC** to **16:20:45 UTC**: **3 hours
22 seconds (10,822 seconds)**, completing the requested 10,800-second window.
The actual completion timestamp and elapsed duration are recorded in
`STATE.json`. Final publication and its confirmation follow this research
completion record.

## Strongest complete written result

Put \(L(n)=1+\log_2 n\) and \(s(n)=\log_2 L(n)\). The strongest construction
admitted in this session is

\[
 T(n)=O\!\left(n\sqrt{L(n)}\,
 2^{O\left(s(n)\left(\frac{\log_2\log_2 s(n)}{\log_2 s(n)}\right)^{1/3}\right)}
 \right).
\]

The claim is eventual, for **one exact deterministic fixed finite-alphabet
multitape full-product machine**, with **O(n) cells ever visited**. Small inputs
use the stated fallback. Constants and the absolute cutoff are not numerically
evaluated. This is an AI-assisted written mathematical construction accepted
after distinct finite-construction, physical-composition and scheduler reviews;
it is not a fully implemented multiplier, a formal refinement proof, human
refereeing, or a literature-priority certification.

The proof is [fixed-field-extraction-theorem.md](routes/A/fixed-field-extraction-theorem.md),
with the lead admission record in
[lead-review-fixed-field-extraction.md](verification/S002/lead-review-fixed-field-extraction.md).
The construction establishes the programme's previous fixed-field compact
representation premise **IP4**. That premise is no longer assumed. The separate
dyadic, all-odd-characteristic IP statement remains open.

This improves the explicit envelope developed earlier in this programme. It
does not establish a strict comparison against an unspecified published o(1),
an effective practical crossover, or any of the stronger endpoint targets.
In particular, bounded H, poly(s) overhead, and \(2^{O(s^\beta)}\) for a fixed
\(\beta<1\) remain unproved here. No value of kappa_ov is assigned.

## What made the stronger profile possible

1. **Low-degree count formulas in characteristic two.** Carry propagation
   uses `c_next = x*y + (x+y)*c`, so the predecessor carry is copied once.
   A balanced tree computes low count bits by polynomial-size formulas while
   preserving the required syntactic degree. Signed Lucas identities then
   assemble the truncated predictor. Intermediate polynomials need not be
   multilinear. See
   [characteristic-two-count-formula.md](routes/A/characteristic-two-count-formula.md).

2. **A full-rate affine factorization.** The cyclic formula compiler preserves
   `f I` on every independent row, including all cyclic rotations. It does not
   substitute a single-output arithmetic circuit for the full batch operator.
   The graded tensor-product operation is established mathematics and is
   credited to Sheng--Tribone and predecessors; the predictor application and
   finite resource accounting are proved separately. See
   [formula-full-rate-linearization.md](routes/B/formula-full-rate-linearization.md).

3. **A complete physical and scheduling bill.** The accepted profile pays for
   generation, coefficient coordinates, numeric addresses, repair, basis
   conversion, precision, attempted candidates, fallback and cleanup. The
   order-three characteristic-two interchanger and rational Walsh transform
   have separate coefficient semantics, connected by movement of encoded
   records. A uniform visited-cell cap is established before scheduling.
   See [physical-compiler-ledger.md](routes/A/physical-compiler-ledger.md) and
   [review-fixed-field-physical-composition.md](routes/B/review-fixed-field-physical-composition.md).

For the accuracy parameter \(J=j+2\), the search has
\(\log m=O(J^3\log J)\), and the complete finite constructor has budget
\(P_m\le 2^{m^C}\) for an absolute C. The resulting physical profiles satisfy
\(\log D_j,\log L(N_j)\le 2^{C J^3\log J}\). The proof selects a sufficiently small eligible candidate within the sparse
schedule, yielding the displayed bound.
The threshold inversion is part of the proof, not an empirical fit.

## Independent routes and useful negative results

Route A developed source extraction, common-cap scheduling and the physical
compiler, then composed the fixed-field finite constructor. Route B's protected
independent search developed constant-tail rational prediction and reflection
closure before the order-three and full-rate factorization synthesis. Route C
developed count-prediction and representation obstructions, independently
checked the construction, and implemented separate exact verifiers. The lead
audited composition, sources and publication, developed additional rank/sketch
obstructions, and replayed key checks in isolated directories.

The negative results are restricted to their stated models. They cover scalar
count aliasing, support-preserving lifts, certain additive/linear sketches,
Chow-type representations, and the canonical uncompressed multilinear formula
compiler. They do not prove a general multiplication lower bound or rule out
the endpoint. The multilinear compiler obstruction explicitly excludes the
new nonmultilinear characteristic-two construction.

A separate concurrent focused session, E001, worked in
`results/epsilon-uniformity/`. Its files, independent source and balanced-formula
extractions, conditional preflight transfer, provenance and state were preserved
when reconciling shared branch updates. Its remaining work and its later
scheduled endpoint are not counted as S002 completion or silently attributed
to S002.

## Verification and its limits

The admission gates are written mathematical audits, with independent reviewers
checking the finite representation and the complete global composition.
The lead read and replayed the characteristic-two count and exact profile
checkers in isolation. Representative final checks include:

| Check | Result and scope |
|---|---|
| B characteristic-two verifier | 5,460 adder cases; 137,214 signed Lucas cases; 120 serialized formulas; 525 size/degree budgets; 45,864 F4 predictor cases; negative controls rejected |
| C independent count verifier | 13,996 count assignments; 178,330 binomial cases; 9,702 predictor cases; copied-size budgets and negative offsets checked |
| A profile verifier | 4,121 exact margin/guard cases and matching threshold negative controls; 290 label majorants; 546 sparse-rounding cases; no floating-point comparisons |
| General-prime count formulas | 1,535,617 signed Lucas cases and additional carry, formula and predictor checks; finite result only, not a new global theorem |
| Four-bit compiler interface | Four formal polynomial matrix identities, all 256 affine entries, all eight independent rows, 16 Boolean points, off-cube negative control |

Scripts, outputs and lead replay records are under `verification/S002/` and the
individual route directories. Earlier exact checks and negative controls are
retained in [VERIFICATION.md](VERIFICATION.md). Finite testing does not establish
an asymptotic theorem by itself. No giant template or end-to-end multiplier was
executed, no Lean build was run, and byte integrity is not represented as source
reading or proof verification.

## Source pins and attribution

The final pre-close source refresh found these pins unchanged:

| Source | Pin |
|---|---|
| Canonical CrocSwap main | `e54523517d0f03e58352e647c403a5af3e525a57` |
| OpenAI math main | `3344da59991ed94f9ba711217b29c1d760badfa6` |
| Requested moonshot prompt blob | `b5762a4dacb999703e83621301a455fbb12755f7` |

Canonical and OpenAI heads and the prompt blob were all rechecked in the
closing audit at 16:18 UTC, after the earlier 15:57--15:58 refresh. Historical programme/bootstrap/
owned-rank/recovery pins are retained in `STATE.json`. The November tape/Fourier
source supplies the core multiplication architecture. The completed source
reading and remaining companion/formal gaps are listed in
[SOURCE-AUDIT.md](SOURCE-AUDIT.md). Primary literature and exact read scope are
listed in [EXTERNAL-RESEARCH.md](EXTERNAL-RESEARCH.md); the novelty search is
incomplete. Weak ETH belongs to the separate lower-bound discussion and is not
an assumption of this upper bound.

## Publication and continuation

Six S002 checkpoints were confirmed before preparing this handoff:

| Checkpoint | Commit |
|---|---|
| 1 | `bbfd1086b7e629375f9891998e4602270d8801cd` |
| 2 | `d0b775ecf26b1f248ffa8839e3890cb452d53919` |
| 3 | `96028cba1342c02bdca1f537ae9a80485087bdf3` |
| 4 | `4689161c5bc6c9e64536034d4fa6af033d26a3e0` |
| 5 | `58c754b583815e4fe40d333ec9d71e4c254749ba` |
| 6 | `848fbf1d7a5e192aa352d79b4d3e36fa06be21ee` |

The closing reconciliation also preserved concurrent E001 head
`d1f3baccdcc547263c0c0cc7241aa0cb1ef12bee`, including all 35 focused files
byte-for-byte and its shared status additions.

The final commit contains this report and the completion record; its identifier
is reported in the chat response and Git history rather than recursively
embedded in its own contents. Updates use an expected-head lease without force.
An intermittent GitHub connector failure delayed checkpoint 6; the API recovered
and the remote ref and commit page were independently confirmed. A stalled
browser upload was discarded without submission. No upstream PR was opened.

The next mathematical target is a smaller complete routing/representation
profile, or a proof that structured modules can be physically executed more
cheaply with all row movements and repair charged. Optional power-of-two-degree
and structured-shift refinements are saved with their review scope; no stronger
global bound follows merely from smaller algebraic descriptions. Separately,
independent human review, a more exhaustive novelty audit, and a formal or
executable refinement would substantially strengthen confidence in the current
construction. `PR-DESCRIPTION.md` remains a draft for that review process.
