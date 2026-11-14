# Exclude the two-half mixed-head shortcut and retain two exact three-half targets

**proved fixed-tensor ordinary obstruction with arbitrary invertible encodings; both three-half targets remain open. No new kappa.**

Two halves on2+p independent banks with invertible ordinary encodings and no rank-zero endpoint require p<=2 and at least2p rank-one heads. Exact target invoices retain the three-half no-query(2,2,2,1) and one-query(2,2,2,2) alternatives.

Independent root proof review and separate exact checker are in [REVIEW.md](review-root/REVIEW.md), [check.js](review-root/check.js), and [RESULT.json](review-root/RESULT.json). The full author argument is [PROOF.md](author/PROOF.md). Exact source and transfer pins are in [DEPENDENCIES.json](DEPENDENCIES.json).

Both three-half head circuits remain open; endpoint component ranks and favourable arithmetic are not sufficient.

This package was reviewed and its pure JavaScript verification actually executed in the cloud runtime. Local Node CLI execution during the executor outage is not claimed. Every native, owned-erasure, compiler, precision/tape and analytic/recovery assumption stays explicit. No change to the selected certificate or complete multiplication exponent is made.

Credit @CubeJerry, the named predecessor/source authors, the S013 construction/bridge/adversarial workers and the root independent review. Substantial OpenAI assistance; no human or formal-kernel audit is asserted.

## Reproduction

From the repository root:

```sh
node research/moonshot-005-program/results/complex-two-half-component-gate/review-root/check.js
```

Expected status: `PASS_ROOT_TWO_HALF_REVIEW`. The inputs must match the exact recorded SHA-256 pins. This command is supplied for reproduction; the recorded execution used the same exported functions in cloud JavaScript.
