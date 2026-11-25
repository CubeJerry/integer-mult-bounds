# Draft cumulative contribution — research package, not yet submitted

The November 24 fixed-tape multiplier establishes n(1+log n)^(1/2+o(1)) but does not specify a decay rate merely by writing o(1). This programme records quantitative interfaces and representation barriers needed to investigate that remaining overhead.

The package now gives a stronger explicit fixed-field extraction for the exact uniform linear-space tape multiplier:

    T(n)=O(n sqrt(L(n)) 2^{O(s(n)(log2 log2 s(n)/log2 s(n))^(1/3))}),
    L(n)=1+log2 n, s(n)=log2 L(n).

A polynomial-size characteristic-two count formula of degree O(sqrt m) is converted into a full-rate sequence of affine matrix factors through the established graded tensor construction. Its actual bounded generator, rational/cyclotomic data, physical tape coefficients, numerical precision and validity thresholds are charged, followed by a prefix-weighted restart schedule and O(nr) chunk convolution. This quantifies the published residual o(1); it does not claim a strict improvement over an unspecified o(1), a practical numerical cutoff or the endpoint.

Separate components include growing-arity rational Walsh arithmetic, physical half-angle reflection closure, exact count prediction and characteristic/aliasing obstructions. Their computational scopes are retained. The support-preserving lift proof has also passed independent review; it applies to arbitrary supported unit-diagonal lifts modulo every p^e, e>=2.

## Verification

The lead reviewed the critical source/proof chain and independently replayed route scripts with failure controls. C separately audited the finite generator and addresses; B audited integer assembly. These are AI-assisted mathematical reviews, not human refereeing. Reproduction evidence and exact limits are in VERIFICATION.md. No Lean build or full multiplier validation was performed. Publication to the fork is a research checkpoint; no upstream PR has been opened.

## Consolidated credits

Research coordinated for @CubeJerry with substantial AI assistance from OpenAI ChatGPT and three concurrent research agents. The November 24 Fourier, tape and companion manuscripts and their proofs belong to their credited OpenAI authors. The earlier programme and recovered batch-contraction note retain their provenance. Source lineage includes the shared-wire/helper-split work in #7000/#7001, and the Kartal, Sussman, Davis, Romman, Yao and Liu constructions credited in the manuscripts; this programme does not claim authorship of those constructions. PR #8102 is a prior fixed-kappa specialization, not this programme's result. Exact predecessor references and read scope are recorded in SOURCE-AUDIT.md and EXTERNAL-RESEARCH.md.


Concurrent E001 work retains its own provenance under `results/epsilon-uniformity/`. No priority is claimed over overlapping independent results. This is a fork research checkpoint; no upstream PR has been opened.

## Focused E001 refinement

The focused epsilon-uniformity work now proves the sharper written source profile log m=O(j³ log j), giving

    T(n)=n sqrt(L) 2^{O(x(log2(y+2)/y)^(1/3))},
    x=log2 L, y=log2 log2(x+16),

on one exact fixed machine with uniform O(n) visited cells. The complete finite-generator and physical-compiler proof has separate root/C AI review. It retains original integral/dyadic templates, specified efficient generation and actual weighted scheduling. The earlier S002 sixth-power extraction remains recorded.

Additional scoped results are a literal p² factor-rank/reserve obstruction, input-dependent compatible-radix preparation, and a complete conditional bounded-preflight transfer. These preserve their distinct premises and do not settle the endpoint. Full astronomical execution, a Lean proof of the refinement, human refereeing, a practical cutoff and a literature-priority audit remain absent. No upstream PR has been opened.

## Fourth-wave formula result

The complete proof is `routes/A/formula-extraction-theorem.md`; construction is `routes/B/formula-full-rate-linearization.md`; the final gate is `verification/S002/lead-review-formula-extraction.md` with a separate C composition review. The new common finite envelope is P_m<=2^{2^{C log²(m+2)}}, giving log-prefactor and log-log-threshold at most 2^{C J^6(log J)^2}. The source permits both varying fixed affine pencils and arbitrary batch width. Exact formula and ramified-ring checkers were independently replayed. The graded tensor sum is credited to its existing literature; no compact-IP assumption enters this result. Earlier focused-session statements above retain their dated provenance.

## Current fixed-field result

`routes/A/characteristic-two-count-formula.md` proves the previously missing IP4 premise by explicit copied carry formulas and a negative-offset binomial identity. `routes/A/fixed-field-extraction-theorem.md` supplies the complete physical composition and eligible sparse schedule. The common finite envelope is P_m<=2^(m^C), and logarithmic prefactors and log-log thresholds are at most 2^(C J^3 log J). The lead and separate B/C global reviews accepted all changed interfaces and constants.

The numerical Walsh template remains rational, with each coefficient prepared once at charged precision; the interchanger is exact in characteristic two. Their coefficient rings are never conflated. The all-odd-characteristic dyadic hypothesis remains open. Exact finite tests and intentional-error controls passed, but no complete multiplier, formal refinement or practical threshold was produced. The constant-overhead endpoint remains open. This cumulative text is a reviewable draft only; no upstream PR has been opened.
