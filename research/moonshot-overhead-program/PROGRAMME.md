# Square-root overhead moonshot

Status: S002 completed at 2026-11-25 16:20:45 UTC after 3 hours 22 seconds; the research programme remains open. Historical programme retained intact. The current strongest accepted rate is the fifth-wave fixed-field extraction linked below; earlier dated sections preserve checkpoint history.

Current handoff: [S002 session report](SESSION-S002-REPORT.md), with the strongest theorem, source pins, independent gates, verification limits and continuation targets in one place.

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

## S002 accepted complete conservative extraction

The finite-constructor, physical-compiler and common-cap assembly gates are accepted. With L(n)=1+log2 n and s(n)=log2 L(n), one fixed exact deterministic finite-alphabet multitape multiplier has

    T(n)=O(n sqrt(L(n)) 2^{O(s(n)/(log2 log2 s(n))^(1/6))}),
    visited cells=O(n).

See the [theorem](routes/A/explicit-extraction-theorem.md) and [lead review](verification/S002/lead-review-explicit-extraction.md). Actual finite generation, rational/cyclotomic data, numeric address magnitudes, interpreted tape costs, precision, thresholds, chunk convolution and unsuccessful attempts are charged. This unconditional quantitative source extraction has unspecified absolute constants and an eventual threshold. It is not a claimed strict improvement over the published unspecified o(1), practical implementation, formal certification or endpoint solution.

The independent route produced a growing-arity rational arithmetic Walsh theorem and a finite half-angle reflection family compatible with physical swap pencils. Their scopes differ: the arithmetic result is not a tape bound, and the reflection component does not yet improve H(n). Characteristic/interchange and count-aliasing obstructions passed independent review. The support-preserving lift obstruction also passed independent review.

After two substantive waves A pursues a sharper search profile; B pivots from its rational-only caller to the physical reflection family and smaller representations; C tests alternatives to count prediction. The exact endpoint and stronger subexponential-in-s benchmarks remain open.

## S002 third wave — sharper extraction and characteristic-two closure

The sharpened search now passes the same complete physical and scheduling gates with log2 m_j=O(J^3 log J), J=j+2. With s=log2 L and y=log2 log2(s+16), it gives

    H(n)<=2^{O(s (log2(y+2)/y)^(1/3))}.

See [sharper proof](routes/A/sharper-parameter-growth.md), [lead acceptance](verification/S002/lead-review-sharper-extraction.md), and [independent C review](routes/C/REVIEW-SHARPER-PARAMETER-GROWTH.md). This independently reaches the same asymptotic scale as concurrent E001 checkpoint 0961d208; both derivations and their provenance are preserved. The earlier sixth-power envelope is superseded as a programme bound, retained as a historical derivation. The current result remains an explicit extraction of the published qualitative bound, with unevaluated absolute constants and no priority or strict published-runtime comparison.

Route B now supplies a complete finite full-rate order-three closure in characteristic two, using new power-of-two-distance labels and a short F4 group identity. Four recursive phases each use 1/16 of the rows; a four-element discrepancy identity reduces repair to two predictor applications. The lead and C have accepted the physical component and independently replayed its finite checker. The generic predictor representation still has a double-exponential profile, so this construction alone does not improve the displayed global envelope.

New scoped barriers distinguish literal formal polynomial compression, two-stage characteristic-two full-rate width, and arbitrary odd-characteristic linear sketches. They do not lower-bound general multiplication. A characteristic-two low-rank error theorem is separately accepted; its missing cheap address-space correction is not assumed by the order-three construction. The IP and IP4 compact-representation bridges remain explicitly conditional, with final review in progress at this checkpoint.

## S002 fourth wave — smaller full-rate formula representation

The fourth-wave complete programme envelope is

    T(n)=O(n sqrt(L(n))
             2^{O(s(n)(log2 log2 s(n))^(1/3)/(log2 s(n))^(1/6))}),
    L(n)=1+log2 n, s(n)=log2 L(n), visited cells=O(n).

See [complete theorem](routes/A/formula-extraction-theorem.md), [finite construction](routes/B/formula-full-rate-linearization.md), [lead gate](verification/S002/lead-review-formula-extraction.md), and [independent final C gate](routes/C/REVIEW-A-FORMULA-EXTRACTION.md). The balanced coefficient formula has syntactic degree O(sqrt(m log m)) and actual tree size 2^{O(log²m)}. A graded tensor factorization turns it into a full-rate affine program. Its actual scalar/address/generator envelope is P_m<=2^{2^{C log²(m+2)}}. The existing complete physical compiler, uniform cap and schedule then give the displayed rate with no compact-IP hypothesis.

The tensor operation is established matrix-factorization mathematics and is credited. The quantified application improves this programme's preceding explicit upper envelope, not a claimed comparison against an unspecified published o(1). A and C independently audited the finite construction; C independently reviewed the complete composition; the lead reread the changed source interfaces and replayed both exact checkers. Constants and the eventual input cutoff remain unevaluated. No full multiplier execution, formal build or human refereeing occurred.

The exact constant-overhead endpoint and stronger 2^{O(s^beta)}, beta<1, benchmarks remain open. IP/IP4 compact-representation targets are stronger than this new quasi-polynomial-exponent construction. A new additive-sketch theorem over F4 also passed independent review; it permits polynomial matrix width and is compatible with the positive result.

## S002 fifth wave — explicit characteristic-two count formulas

The current strongest accepted written envelope is

    T(n)=O(n sqrt(L(n))
             2^{O(s(n)(log2 log2 s(n)/log2 s(n))^(1/3))}),
    L(n)=1+log2 n, s(n)=log2 L(n), visited cells=O(n).

See the [complete theorem](routes/A/fixed-field-extraction-theorem.md), [count-formula construction](routes/A/characteristic-two-count-formula.md), [lead gate](verification/S002/lead-review-fixed-field-extraction.md), and separate [B](routes/B/review-fixed-field-physical-composition.md) and [C](routes/C/REVIEW-A-FIXED-FIELD-EXTRACTION.md) composition reviews.

The new mechanism is a polynomial-size characteristic-two formula for the low bits of an ordinary integer count. Its copied carry expression contains the previous carry once; repeated cumulative sums give polynomial formula size while bit k has syntactic degree at most 2^k. A formal-series coefficient identity handles negative offsets. The resulting degree-O(sqrt(m)) predictor compiles to a whole-row affine factorization with actual data and generation bounded by 2^(m^C). Thus the previously hypothetical IP4 representation is now explicit.

The characteristic-two interchanger and the rational numerical Walsh program retain distinct coefficient algebras. Their complete physical composition, coefficient preparation, all call constants, common cap and eligible sparse schedule passed B, C and lead review. The complete profile is log-prefactor and log-log-threshold at most 2^(C J^3 log J). Exact independent finite tests were replayed by the lead.

This supersedes the fourth-wave upper envelope by a factor (log2 s)^(1/6) in its displayed logarithmic scale. It does not settle the constant-overhead endpoint or any fixed-beta 2^(O(s^beta)) benchmark. The all-odd-characteristic dyadic IP premise remains open. Earlier conditional IP4 sections above describe their checkpoint state and are now superseded by this explicit construction. No full multiplier execution, practical cutoff, formal build, human refereeing or priority claim is made.

## S003 first-wave update

The exact arbitrary-depth asymmetric literal label invoice now has a reviewed lower bound of order J^3 log J in log m. This closes parameter-only improvement within that billed family; it is not a lower bound on multiplication or all routing. A succinct cyclic scalar-factor executor and a conditional packed small-radix batching component are proved and reviewed. The active portfolio now targets explicit compact endpoint maps, on-demand spectral repair and rational Walsh execution. The previous complete fixed-field envelope remains unchanged pending full physical composition. See `sessions/2026-11-26-S003/lead/first-wave-review.md`.

## E002 quantitative breakthrough within the written programme

The current complete explicit envelope is
`H<=2^{O(x^(3/4)(log2(x+2))^(1/4))}` with uniform O(n) visited cells.
It is a written source-specific construction accepted after independent
A/C global reviews and lead audit; no human or formal verification is
implied. The expanded per-volume compiler has been replaced by compact
polynomial-m stream execution. Large finite setup is charged additively
and an actual capped direct selector replaces a certificate infimum.
The endpoint remains open. Current proof/ledger/admission are in
`results/epsilon-uniformity/sessions/E002/`. Variable-arity research is
protected and separately gated; no stronger rate is admitted yet.

## S003 polynomial-profile milestone

S003 independently closes the same polynomial-profile envelope admitted by E002: log H=O(s^(3/4)(log(s+2))^(1/4)). Its explicit dyadic geometry uses radix3 and its proof uses the weighted common-cap scheduler. See sessions/2026-11-26-S003/lead/ADMISSION-PP.md. A separate adaptive route is active but unadmitted.
