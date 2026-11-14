# Prove phase-exact tensor separation and ordinary Gaussian-rank component gates

**proved fixed-family all-width algebraic reduction; concrete group faithful at every width at least6. No new kappa.**

Fixed pairwise projectively distinct unitaries have independent sufficiently high tensor powers; exact phase cocycles retained. Gaussian-rank components are ordinary bimodules. The concrete192-element group is faithful at all widths>=6.

Independent root proof review and separate exact checker are in [REVIEW.md](review-root/REVIEW.md), [check.js](review-root/check.js), and [RESULT.json](review-root/RESULT.json). The full author argument is [PROOF.md](author/PROOF.md). Exact source and transfer pins are in [DEPENDENCIES.json](DEPENDENCIES.json).

Necessary algebraic gates only; arbitrary non-tensor ordinary encodings and growing operator families are outside scope. No caller or physical supplier follows.

This package was reviewed and its pure JavaScript verification actually executed in the cloud runtime. Local Node CLI execution during the executor outage is not claimed. Every native, owned-erasure, compiler, precision/tape and analytic/recovery assumption stays explicit. No change to the selected certificate or complete multiplication exponent is made.

Credit @CubeJerry, the named predecessor/source authors, the S013 construction/bridge/adversarial workers and the root independent review. Substantial OpenAI assistance; no human or formal-kernel audit is asserted.

## Reproduction

From the repository root:

```sh
node research/moonshot-005-program/results/complex-tensor-rank-components/review-root/check.js
```

Expected status: `PASS_ROOT_TENSOR_SEPARATION_REVIEW`. The inputs must match the exact recorded SHA-256 pins. This command is supplied for reproduction; the recorded execution used the same exported functions in cloud JavaScript.
