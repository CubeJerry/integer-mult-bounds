# Consolidated submission plan — 20 November 2026

This document supersedes the eleven-separate-PR presentation only; it does **not** supersede the eleven reviewed scientific source packages. No upstream PR was opened. Submit at most five grouped PRs using the fully encoded links in [PREFILLED-PRS.md](PREFILLED-PRS.md).

| Proposed PR | Head branch and frozen commit | Preserved reviewed packages | GitHub diff |
| --- | --- | --- | --- |
| Gaussian rounding parity | `research/forward-gaussian-rounding-20261120` / `82553cf6f369459e18d00fb4e6bda808d5f10ce1` | parity-flux | 11 added files |
| Three-axis Gaussian source | `research/gaussian-three-axis-consolidated-20261120` / `f678a6e01df59ad0834a4544617021e5c208c37a` | exact rank, separated fixed-order margin, narrow all-order margin | 74 added files |
| Complete CRT service | `research/crt-literal-complete-consolidated-20261120` / `61257563b9cfd7cb47dad435986f70c76979e1b3` | ordered Word lifecycle, shared arithmetic union, 73-role terminal | 108 added files |
| Rational C-word/compiler | `research/rational-compiler-consolidated-20261120` / `8805d8c5b38d3fc725b37d97f4639df03fad5639` | rational grid, selected complex compiler adapter | 57 added files |
| Selected native reduction | `research/selected-native-consolidated-20261120` / `adf2e0aa6777977a280ce50f8938f4a0f4f19b76` | grade-14 route review, selected four-premise native specialization | 151 added files |

All four grouped branches use the **exact canonical main** `e54523517d0f03e58352e647c403a5af3e525a57` as first parent, with the constituent reviewed source commits as additional parents. Each commit tree was assembled from the original tested *subtree SHA* without editing a source package. GitHub's compare results for all four showed merge-base canonical main, behind_by=0, every changed file added and no deletions; the four commit parent lists and root trees were re-read and verified. This gives an explicit source ancestry as well as identical component content.

Full grouped descriptions are in `research/review-bundles-20261120/{gaussian,crt,rational-compiler,native}/PR_DESCRIPTION.md` on the respective branches; original package-level PR descriptions, proofs and tests remain in their folders. The parity PR retains its original full package description. [PREFILLED-PRS.md](PREFILLED-PRS.md) constructs five full Markdown links with `quick_pull=1` and GitHub's `title`/`body` fields, using one RFC3986 URL encoding pass. Decoding each link recovers the byte-exact committed description. URL lengths: 3809, 5115, 5194, 5463 and 6376 characters, respectively.

**Boundary:** the canonical selected certificate remains conditional at κ=0.00363005817 with five original assumptions. The independently reviewed selected-source specialization removes the need to assume the native instance within its own theorem but retains the other four original contracts. No new complete κ or unconditional integer-multiplication algorithm is asserted. Source-specific analytic margins and fixed local tape integrations do not discharge complete analytic recovery or physical tape/ownership obligations.

Prepared for @CubeJerry with substantial OpenAI assistance. Nothing was submitted upstream; the user reviews the prefilled forms and decides whether to create the PRs.