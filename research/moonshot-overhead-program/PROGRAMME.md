# Square-root overhead moonshot

Status: initialized 2026-11-26 (Australia/Melbourne). Historical programme retained intact.

## Objective and model
Study the **exact deterministic fixed finite-alphabet multitape full-product** problem with a uniform O(n) visited-cell cap. Let L=1+log_2 n, s=log_2 L. Seek quantitative bounds T(n)=O(n sqrt(L) H(n)) with H(n)>=1, ultimately H=O(1). Do not count arbitrary fixed-kappa corollaries of the November 24 result as progress. Do not claim an o(1) exponent gives a quantitative rate without uniform constants and thresholds.

## Source pins
- Canonical CrocSwap main: e54523517d0f03e58352e647c403a5af3e525a57 (chosen as the exact current canonical main and shared research base).
- OpenAI math main: 3344da59991ed94f9ba711217b29c1d760badfa6 (new November 24 sources).
- Input prompt CubeJerry/AI_Prompts main moonshot.md blob b5762a4dacb999703e83621301a455fbb12755f7.
- Historical CubeJerry research/moonshot-005-program STATE.json blob 411eb5aba139d47ff3d705cb7da51a4d42660d64 (v22/S033; not imported or modified).
- Upstream PR #8102 proposes the fixed-kappa specialization and confirms the endpoint is open; not a new result of this programme.

## Active distinct routes
A. Extract uniform candidate-generation, precision, chunking and schedule dependence from the tape paper and quantify a valid H.
B. Independent architecture: constant-error-rate prediction plus recursive repair of failures, with a whole-machine cost and information-flow test. Not yet a theorem; must account for finding/locating defects, exact repair, routing and storage.
C. Adversarial: isolate whether polynomial degree lower bounds obstruct the *existing* spectral predictor and distinguish scoped barriers from generic multiplication lower bounds.

## Decisions
The source theorem is n L^(1/2+o(1)); the exact endpoint is not established. Conditional analyses are to be labelled as such. No old five assumptions are inherited. A numerical local certificate never substitutes for an all-size tape theorem.

## S002: first-wave results and decisions

The first wave establishes useful component statements, not a new complete overhead envelope. Route A replaces the exponential index penalty by a prefix-weighted restart schedule and gives a diagonal chunk-convolution wrapper with O(nr) tape work. Its full quantitative interface is in [scheduler-and-chunking.md](routes/A/scheduler-and-chunking.md); candidate constants and thresholds remain explicit unknowns. Compact characteristic-zero prediction and Hermite table bounds are separately documented.

Route B constructs a pairwise-independent shift family of width O(m), a degree O(sqrt(m)) Newton predictor with constant defect, and exact two-predictor discrepancy-division repair. A recovered finite batch-contraction argument has been preserved with provenance and independently replayed. This is a rational/characteristic-zero mechanism; factorial division is not freely available in the source finite-characteristic interchange construction.

Route C proves an exact ordinary-count-polynomial error bound and the sharp asymptotic degree needed for polynomially rare error. For the explicitly defined degree-plus-linear-repair invoice, optimizing the error tolerance alone retains a sqrt(log m) loss. This is a scoped representation obstruction, not a multiplication lower bound.

The next wave tests complete quantitative source compilation and the full physical cost of Route B. A separate characteristic-compatibility obstruction is under review. No substitution of a growing parameter into a fixed-parameter O-constant is admitted. Two distinct constructive routes remain active; the portfolio will be reassessed after this wave.
