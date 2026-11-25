# Draft cumulative contribution — research package, not yet submitted

The November 24 fixed-tape multiplier establishes n(1+log n)^(1/2+o(1)) but does not specify a decay rate merely by writing o(1). This programme records quantitative interfaces and representation barriers needed to investigate that remaining overhead.

The current package contains a prefix-weighted uniform scheduler, an O(nr) chunk-convolution wrapper, exact constant-defect rational prediction and repair, a finite batch-contraction recurrence, and a sharp ordinary-count-polynomial error bound. These results have different computational scopes, stated in the individual notes. **No new complete H(n) bound is claimed.** Uniform template compilation and the full tape caller remain open.

## Verification

The lead reviewed the first-wave proofs and independently replayed the route scripts, including adversarial failure controls. Reproduction evidence and exact limits are in VERIFICATION.md. No Lean build or full multiplier validation was performed. Publication to the fork is a research checkpoint; no upstream PR has been opened.

## Consolidated credits

Research coordinated for @CubeJerry with substantial AI assistance from OpenAI ChatGPT and three concurrent research agents. The November 24 Fourier, tape and companion manuscripts and their proofs belong to their credited OpenAI authors. The earlier programme and recovered batch-contraction note retain their provenance. Source lineage includes the shared-wire/helper-split work in #7000/#7001, and the Kartal, Sussman, Davis, Romman, Yao and Liu constructions credited in the manuscripts; this programme does not claim authorship of those constructions. PR #8102 is a prior fixed-kappa specialization, not this programme's result. Exact predecessor references and read scope are recorded in SOURCE-AUDIT.md and EXTERNAL-RESEARCH.md.
