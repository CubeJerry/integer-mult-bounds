# Epsilon decay and quantitative uniformity

Focused companion to the square-root overhead programme. See [SESSION.json](SESSION.json)
for source pins, active routes and actual bound status, and [LOG.md](LOG.md) for
the append-only record. This directory is the scope of focused session E001;
concurrent parent session S002 is preserved separately.

See [FINAL-REPORT.md](FINAL-REPORT.md) for the consolidated session findings.

## Current shared-programme result

Concurrent S002 has since established the stronger envelope
`H<=2^{O(x(log_2(z+2)/z)^(1/3))}`, with `x=log_2(1+log_2 n)` and
`z=log_2(x+16)`, using a characteristic-two count-formula construction.
Its [complete theorem](https://github.com/CubeJerry/integer-mult-bounds/blob/848fbf1d7a5e192aa352d79b4d3e36fa06be21ee/research/moonshot-overhead-program/routes/A/fixed-field-extraction-theorem.md)
and its B/C/lead reviews were committed at848fbf1. Root has read the finite
formula, complete extraction and lead review. E001 independently passed
the [finite count audit](route-c/S002-COUNT-FORMULA-REVIEW.md) and
[physical composition audit](route-a/S002-FIXED-FIELD-REVIEW.md). This establishes IP4 and
does not establish our different all-odd-characteristic dyadic MR hypothesis.

The separate fully reviewed E001 result below remains useful as a dyadic
construction and general formula-size transfer. Its bound is weaker than
the new shared-programme result. Both proofs and provenance are preserved.

## Independent dyadic formula theorem

Start with [THEOREM.md](THEOREM.md). Put `L=1+log_2 n`, `x=log_2 L`, and
`z=log_2(x+16)`. A specified fixed exact deterministic multitape machine has

\[
 T(n)=n\sqrt L\;2^{O\left(x\left(\frac{[\log_2(z+2)]^2}{z}\right)^{1/6}\right)},
 \qquad\text{visited cells}=O(n).
\]

Correctness and the common visited-cell bound hold at every length. The
complete formula construction, actual scalar generator and physical
composition passed separate Route A, Route B, Route C and root reviews. Constants and the eventual cutoff
are not numerically evaluated. The square-root endpoint and polynomial
in `x` overhead remain open.

Balanced degree-preserving formulas and integral cyclic factorizations give
a full-rate matrix root of the source predictor with total dimension, bit
output and actual construction budget `2^{2^{O(log^2 m)}}`. This removes one
exponential layer from the preceding sufficient finite-data budget while
preserving query-stage count. Both transform branches, all shifts, repair,
scalar descent, precision, physical movement, fallback, common-space chunking
and scheduling are included.

Concurrent S002 independently established the same stronger envelope at
[58c754b](https://github.com/CubeJerry/integer-mult-bounds/commit/58c754b583815e4fe40d333ec9d71e4c254749ba).
Its proof was read, credited and preserved. The earlier E001 theorem is
preserved verbatim in [BASELINE-THEOREM.md](BASELINE-THEOREM.md), to which
historical review hashes continue to apply. No priority or practical-runtime
claim is made. These are written mathematical proofs and exact finite checks,
not a Lean refinement, human referee report or giant template execution.

## Research files

- [Formula construction](route-c/FORMULA-FACTORIZATION-COMPRESSION.md) and
  [complete transfer](route-a/formula-template-transfer.md): the main new
  algebra, bit generator and complete machine proof.
- [Final synthesis review](route-b/formula-synthesis-review.md): independent
  algebra, generation, source-interface, physical-profile and inversion audit.
- [ROOT-FORMULA-REVIEW.md](ROOT-FORMULA-REVIEW.md),
  [A algebra review](route-a/FORMULA-FACTORIZATION-REVIEW.md), and
  [C transfer review](route-c/FORMULA-TRANSFER-REVIEW.md): separate proof audits.
- [root-formula-replay.json](root-formula-replay.json): 84 predictor cases,
  152 cyclic-product checks and 72 descended matrix-root identities, including
  negative and nonsemisimple controls, independently replayed in isolation.
- [FORMULA-SIZE-TRANSFER.md](FORMULA-SIZE-TRANSFER.md): a general conditional
  formula-size-to-complete-overhead theorem, independently reviewed.
- [Matching recipe lower bound](route-c/FORMULA-RECIPE-LOWER-BOUND.md):
  the literal unreduced multilinear recipe requires `2^{2^{Omega(log^2 m)}}`
  rows for the retained window; arbitrary matrix roots remain open.
- [MR literature audit](route-a/mr-symmetry-literature.md) and
  [LITERATURE-AUDIT.md](LITERATURE-AUDIT.md): primary results, exact applicability
  gaps and provenance.
- [CERTIFICATE.md](CERTIFICATE.md): rigorous diagnostic lemmas and explicit scope
  of the source's weighted-search upper certificate.
- [route-a/elementary-tower-extraction.md](route-a/elementary-tower-extraction.md)
  and [compiler-invoice.md](route-a/compiler-invoice.md): complete quantitative
  construction and physical cost proof underlying the baseline and reused compiler.
- [PARAMETER-LEDGER.md](PARAMETER-LEDGER.md): parameter and threshold ledger.
- [DEPENDENCIES.md](DEPENDENCIES.md): complete path, conditional branches and exact remaining interfaces.
- [route-c/WINDOW-PREDICTOR-DEPTH.md](route-c/WINDOW-PREDICTOR-DEPTH.md): exact window degree/depth and a scoped window-versus-conversion resource obstruction.
- [route-a/single-exponential-root-hypothesis.md](route-a/single-exponential-root-hypothesis.md): a complete stronger conditional transfer from a precise full-rate matrix-root hypothesis; the hypothesis remains open.
- [INTERCHANGE-OBSTRUCTION.md](INTERCHANGE-OBSTRUCTION.md): rational Gram rank
  forces a characteristic/window conflict in the retained tape interchanger.
  This has separate algebraic agent review and exact finite checks.
- [PADIC-LIFT-OBSTRUCTION.md](PADIC-LIFT-OBSTRUCTION.md): literal label transfers
  lose their small-rank advantage modulo p²; complementary to S002's more
  general supported-lift theorem.
- [route-a/README.md](route-a/README.md): additional compact binary-kernel and
  repair-table results, with their local scope and verification.
- [route-b/README.md](route-b/README.md): charged binary scheduling, bounded
  preflight, complete conditional endpoint/poly-`x` transfer, chunking and
  compiler-interface results.
- [route-c/NONSTATIONARY-RECURSION.md](route-c/NONSTATIONARY-RECURSION.md):
  a complete conditional interchange endpoint, and a separate Walsh-toll
  obstruction; neither is a complete multiplication theorem.
- [route-c/SOURCE-PADDING-BARRIER.md](route-c/SOURCE-PADDING-BARRIER.md):
  literal radix padding violates common linear space for a specified natural
  variable-template selector.
- [route-c/INPUT-DEPENDENT-RADIX.md](route-c/INPUT-DEPENDENT-RADIX.md):
  constructive repair of that padding barrier, including compatible-prime
  search, constant or summably small volume loss, and explicit preparation.
- [REVIEWS.md](REVIEWS.md): admitted proofs, actual cross-reviews, finite
  replays and their limits. Exact checker receipts sit beside their scripts.

Exact source revision: OpenAI `math` 3344da59991ed94f9ba711217b29c1d760badfa6.
No upstream PR is opened automatically. Proofs, partial results, scoped negative
results and finite computational checks must keep their distinct labels.

## Open next questions

The current joint coefficient/threshold estimate is explicit but extremely
large. The binding cost is the finite-characteristic predictor's matrix-root
representation and ensuing scalar/description work. A smaller full-rate
representation or different routing mechanism must preserve the individual
query information lost by the ordinary modular count. Preflight removes
search from the execution factor, but the current tower profiles still give
the same envelope scale. Variable-arity endpoint routes also need every
local excess and routing toll controlled, with a uniform physical compiler.

Credits: @CubeJerry, OpenAI manuscripts and cited predecessors, the retained
moonshot programme and concurrent S002 work. Substantial OpenAI GPT-6 Astra Pro
assistance, including three genuinely separate task agents. No human referee or
full Lean-kernel audit is claimed.
