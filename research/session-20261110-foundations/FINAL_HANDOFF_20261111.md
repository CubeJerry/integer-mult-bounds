# Final reviewed handoff — 2026-11-11

Canonical main (refreshed): `e54523517d0f03e58352e647c403a5af3e525a57`. Selected certificate remains conditional `kappa=0.00363005817` from #7000/#7001; all five framework assumptions remain. Newly proposed upstream #7145 claims `0.003643438506419` but is **not** selected in canonical main. No unconditional bound or change to the selected certificate is claimed.

## Verified and independently reviewable

The following five fork branches were rechecked using GitHub compare against exact canonical main. Only files under the corresponding package directory are added. Their complete proposed PR descriptions, evidence, controls, universal arguments and limitations are in each package's `PR-DESCRIPTION.md`.

| Branch | Exact head | Package |
| --- | --- | --- |
| `research/continuous-20261110-dispatcher` | `107ea2e77dcf44d50343eb818b5b14e1f537c8c7` | `contextual-primitive-microcontrol` |
| `research/continuous-20261110-ownership` | `774e7890e9e1379d084e711c53937cc30c8bc434` | `stratified-owned-reserves` |
| `research/continuous-20261110-analytic` | `66adbede4bd4ab603ba3e0a7f6708403905b753c` | `crt-whole-tree-state` |
| `research/continuous-20261110-bit-history` | `96b4d6c7b7dfc0f9facf6effd9277dfb66036cbb` | `fixed-dimension-bit-coefficients` |
| `research/continuous-20261110-crt-control` | `cc35ecedce6f208d5056fab6d17c58555affc73c` | `encoded-balanced-crt-entry` |

Do **not** include `research/continuous-20261110-continuations` as a research PR: a late transitive-vendor audit found the stronger existing `compiled-row-stock-dispatch` theorem. Corrected overlap notes are already committed to that branch.

## Wave-three boundary

The hosted research runtime and its scratch worktrees were unavailable on this continuation. No new independent author/peer replay of the late wave-three packages was possible. The stable recovery patches and exact incomplete obligations are recorded in `INTERRUPTION.md` and `UNVERIFIED/`. The prime-source, row/ROM query, and deferred precision-grid drafts are not verified review candidates.

Next rigorous steps: (1) reconstruct and independently replay the encoded CRT row/ROM query against #5496/#5625, including lease retirement and the full source/ROM tariff; (2) reconstruct and review the encoded fine-prime axis source against the actual #5353 input ABI and root supply; (3) prove a source-specific format/descriptor join for the existing stock dispatcher, including `G_root` and physical tariffs. None is a substitute for full A1–A5 admission.

## PR form URLs

For the five verified branches, a concise Markdown description can be prefilled with GitHub's documented query form
`/compare/main...CubeJerry:<branch>?quick_pull=1&title=<urlencoded>&body=<urlencoded>`.
Standard query encoding and round-trip decoding were checked locally. The authenticated form itself could not be viewed; each package contains the complete long-form description if any prefill is unavailable. No upstream PR was opened. Do not submit this recovery branch.
