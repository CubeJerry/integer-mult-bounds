# Draft cumulative contribution — research package, not yet submitted

The November 24 fixed-tape multiplier establishes n(1+log n)^(1/2+o(1)) but does not specify a decay rate merely by writing o(1). This programme records quantitative interfaces and representation barriers needed to investigate that remaining overhead.

The package now gives a conservative explicit source extraction for the exact uniform linear-space tape multiplier:

    T(n)=O(n sqrt(L(n)) 2^{O(s(n)/(log2 log2 s(n))^(1/6))}),
    L(n)=1+log2 n, s(n)=log2 L(n).

It bounds actual finite construction, rational/cyclotomic data, physical tape coefficients, numerical precision and validity thresholds, then uses a prefix-weighted restart schedule and O(nr) chunk convolution. This quantifies the published residual o(1); it does not claim a strict improvement over an unspecified o(1), a practical numerical cutoff or the endpoint.

Separate components include growing-arity rational Walsh arithmetic, physical half-angle reflection closure, exact count prediction and characteristic/aliasing obstructions. Their computational scopes are retained. The support-preserving lift proof has also passed independent review; it applies to arbitrary supported unit-diagonal lifts modulo every p^e, e>=2.

## Verification

The lead reviewed the critical source/proof chain and independently replayed route scripts with failure controls. C separately audited the finite generator and addresses; B audited integer assembly. These are AI-assisted mathematical reviews, not human refereeing. Reproduction evidence and exact limits are in VERIFICATION.md. No Lean build or full multiplier validation was performed. Publication to the fork is a research checkpoint; no upstream PR has been opened.

## Consolidated credits

Research coordinated for @CubeJerry with substantial AI assistance from OpenAI ChatGPT and three concurrent research agents. The November 24 Fourier, tape and companion manuscripts and their proofs belong to their credited OpenAI authors. The earlier programme and recovered batch-contraction note retain their provenance. Source lineage includes the shared-wire/helper-split work in #7000/#7001, and the Kartal, Sussman, Davis, Romman, Yao and Liu constructions credited in the manuscripts; this programme does not claim authorship of those constructions. PR #8102 is a prior fixed-kappa specialization, not this programme's result. Exact predecessor references and read scope are recorded in SOURCE-AUDIT.md and EXTERNAL-RESEARCH.md.


Concurrent E001 work retains its own provenance under `results/epsilon-uniformity/`. No priority is claimed over overlapping independent results. This is a fork research checkpoint; no upstream PR has been opened.
