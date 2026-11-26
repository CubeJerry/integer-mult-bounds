# Final integration review for E002

Reviewer: E002 conditional review C. Gate: **PASS for the final report's presentation of the reviewed late components and their exact imported bindings**. No unresolved material correction was found within this audit's scope.

Reviewed complete files:

- `FINAL-REPORT.md`, amended SHA-256 `9756aa369369b2f2e37a8f8900618af744a85a8667963445123fb35e0e7b3829`.
- `lead/LATE-ADMISSIONS.md`, SHA-256 `8c40da9b74c93007741e4679f01d7adfa93bb624e7d8e1471a9deb3897ce8872`.
- `lead/REVIEW-ENDPOINT-REUSE.md`, SHA-256 `a2eb8eeb7f4ee7ad6fd18af390e84b932058df8a0890a1e17ab2bad8a7e3eceb`.

I first read report snapshot `188d7cc8fb4a9dd94d50c65a6a9160fb9cbe03b0270ab399dae3bca8d2cfcc33`. I requested that its reference to reserve contraction be corrected: reserves permit bounded inflation after other arrays are cleared. The accepted amended report now states this accurately. I read the complete amended report, including the additional clarifications about logarithmic width contraction, separate scalar/address costs, distinct exact/numerical arity schedules, and polynomial uniform grouping work.

## 1. Corrected source map and the withdrawn wording

The report and late admission both identify the actual physical cross-swaps `X_j <-> Z_b` and `Z_j <-> X_b`, use the complete composite registers `(X_j,Z_j)` and `(Z_b,X_b)`, and preserve spectator queries. They explicitly disclose that the old draft's spectator-half exchange statement was wrong and that my initial review repeated it. Both old statements are superseded rather than silently reused.

The corrected supplier hash is exactly `5db06e11c67fba3e0ed5db2a060bf3616a40f42c5d2281853f58f50f50fd3ceb`. Its final C review and the replay containing 768 full two-half identities are present byte-for-byte. The noncommutativity claim is about the underlying relative permutations and remains valid with nonzero phases. It is not presented as a physical time lower bound or as an obstruction to every choice of endpoint bases.

The subsequent bridge discussion explicitly distinguishes the pure unsigned equal-weight three-SWAP kernel from the complete signed source pencil. That distinction is essential: the displayed pure-SWAP kernel cannot simply be asserted for arbitrary source phases or weights. The report preserves it and confines phase-pinching, rank mismatch and full-rank defects to their declared literal lifts and parameter regimes. No applicability gate has been silently closed.

## 2. Endpoint-reuse model and physical invoice

The final lead review matches the amended characterization at `a259a8b858bcc10ad0aa7127b7af0b2b35bf1e016d10c52d27cd011d58ee9b5c`.

Separate oriented endpoint copies are created by partitioning rectangles into subfamilies before taking connected components. Thus rho can exceed one and really counts prepared copies. The claim is restricted to reserve-only preparations followed by triangular tails. The suffix-space necessity, source-lemma sufficiency, and the within-side/cross-side Gram conditions are represented correctly.

Geometric enlargement is used only to choose a shared layout; original masks and weights are retained. The report therefore does not replace the intended transfer matrix by the all-ones matrix on a larger superrectangle. Serial low-rank accumulation converts one group sum at a time, clears a reused temporary, and returns symmetrically. The resulting recursive-volume invoice and visited-space interpretation agree with the accepted note.

The amended report now explicitly conditions the compiler invoice on uniformly described grouping and charged polynomial membership/ordinary work. Neither the report nor the late admission claims a new low-incidence compatible grouping, a complete stronger child-volume composition, RV-I, or a new global envelope. The triangle and grid statements remain obstructions inside this preparation model.

## 3. Weyl and partition components

The report accurately states the cross-pinned partition's exact incidence and output-count formulas, its finite replay totals, and the absence of an asymptotic-order improvement or new complete physical compiler.

The Weyl component is identified as a positive local executor with declared row-mixing/space invoices. Its retained-basis result is restricted to a sequence using the same operator family. The report neither distributes a polynomial over rectangle summands nor assumes exponential tables of control settings. Its global source applicability remains open.

The unconditional result is kept separate from the conditional log-free two-thirds implication and these late components. The report correctly says RV-I and RV-W are open and does not claim that rectangle counts or the local batching proof implement them. It also preserves the certificate-versus-runtime distinction, lack of a full multiplier run, lack of a formal refinement, and the limits on priority/practical thresholds.

## 4. Exact imported snapshots

At 2026-11-26T00:11:18.552900+00:00 I compared every one of the 30 files in my frozen handoff manifest with its imported `review-c/` counterpart. All byte hashes matched. I separately checked six accepted supplier bindings: cross-pinned partition, Weyl batching, corrected star-swap note, contraction bridge, corrected bridge checker, and endpoint-reuse characterization. All matched their accepted hashes, with no missing files or mismatches.

The machine-readable receipt is `final-integration-hash-check.json`. This was a byte-identity/receipt audit, not another asymptotic proof or replay. The earlier independently executed component receipts remain the evidence for finite checks.

## 5. Audit limits

This integration review checks faithful reporting and binding of the components I reviewed, plus consistency of their stated scope with the report. It does not independently reprove every concurrent construction, the new overlapping-cover theorem, or the complete unconditional V construction from scratch. Their own admissions and source audits remain authoritative for those subjects.

The report correctly defers actual completion time and elapsed duration to SESSION.json after the requested deadline. This review occurs before that deadline and does not certify final session duration, a future remote publication, or a remote SHA. Those require the lead's actual end-of-session checks.

No main-repository file was changed by this reviewer. Credits: @CubeJerry; the cited component authors and pinned sources; the lead's integration; substantial ChatGPT multi-agent mathematical assistance.
