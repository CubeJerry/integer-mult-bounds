# Identify the local R10 code and prove its canonical support limitation

**proved all characteristic-two fields and widths; canonical plus one local cubic reservoir has chi222. No new kappa.**

For all characteristic-two fields k and V>=1, a native fitting with row space in C tensor k^V plus Z_D tensor k^V has chi=222. Arbitrary D-supported innovation still has chi>=186. Z_D is the five-dimensional punctured doubled R10 cycle code.

Independent root proof review and separate exact checker are in [REVIEW.md](review-root/REVIEW.md), [check.js](review-root/check.js), and [RESULT.json](review-root/RESULT.json). The full author argument is [PROOF.md](author/PROOF.md). Exact source and transfer pins are in [DEPENDENCIES.json](DEPENDENCIES.json).

No chronological source or global decoder; multiple reservoirs and histories outside the stated containment remain open.

This package was reviewed and its pure JavaScript verification actually executed in the cloud runtime. Local Node CLI execution during the executor outage is not claimed. Every native, owned-erasure, compiler, precision/tape and analytic/recovery assumption stays explicit. No change to the selected certificate or complete multiplication exponent is made.

Credit @CubeJerry, the named predecessor/source authors, the S013 construction/bridge/adversarial workers and the root independent review. Substantial OpenAI assistance; no human or formal-kernel audit is asserted.

## Reproduction

From the repository root:

```sh
node research/moonshot-005-program/results/bit-d5-cubic-local-history/review-root/check.js research/moonshot-005-program/results/bit-proper-flat-cubic-generators/author/RESULT.json research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json
```

Expected status: `PASS_ROOT_D5_LOCAL_HISTORY_REVIEW`. The inputs must match the exact recorded SHA-256 pins. This command is supplied for reproduction; the recorded execution used the same exported functions in cloud JavaScript.
