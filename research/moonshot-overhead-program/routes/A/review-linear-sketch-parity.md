# Independent Route A review of the linear-sketch parity barrier

Result: **PASS within the stated odd-characteristic linear-sketch and
affine-pencil scope**. Reviewed during S002 against:

* `results/linear-sketch-parity/PROOF.md`, SHA-256
  `b8357a0c55af25a383f2e85123ab50e39d0fa4323c8cd8c7f27b5cb706776da9`;
* its checker, SHA-256
  `23388e90afba98eb2a94abf0a2bafe65d20f84d5692b3fb9191c6bc1f25ef8ba`.

## Mathematical review

The signed fiber distribution has Fourier transform
2^{-m} product_j(1-zeta^{<t,a_j>}). Thus each magnitude is the product
of the stated sine magnitudes. Parseval with the unnormalized Fourier
transform contributes p^{-r}; Cauchy-Schwarz contributes p^r, exactly
cancelling. The zero character vanishes for m>=1. For odd p the maximum
sine magnitude is cos(pi/(2p)), giving the factor sqrt(p^r-1), not a
dimension-free bound. Integrating tan z>=z proves the exponential bound
with the stated constant pi^2/8. Rearranging for success >=1-delta yields
r ln p>=pi^2 m/(4p^2)+2ln(1-2delta), with the correct sign.

Boolean XOR replaces columns by their signed versions and adds an affine
constant; parity changes by a fixed sign. This preserves the universal
bound. Averaging over arbitrary nonnegative row weights is valid and yields
a violating frequency if a worst-case guarantee exceeds that average.

A product of D pencils of side R depends on at most DR^2 variable linear
forms, regardless of fixed row maps. Over an e-dimensional extension there
are at most eDR^2 base-field forms. Every output entry is a function of
this sketch. Correctness of a full matrix row on all independent inputs
requires its diagonal entry to equal parity, so the diagonal test gives a
necessary bound even when off-diagonal coefficients cause additional errors.
Mapping any value outside {+1,-1} to either sign cannot decrease the number
of exact agreements, justifying the arbitrary-scalar readout step.

The exact-recovery argument also passes: interpolation on F_p^r has total
degree <=r(p-1); substitution and Boolean multilinear reduction do not
increase it. Parity's unique multilinear polynomial has nonzero degree-m
coefficient (-2)^m. Grouping at most p-1 bits per count attains
r=ceil(m/(p-1)), so that exact linear-sketch bound is sharp.

For a source predictor with D=O(sqrt(m log m)), the scalar contradiction
requires p^2 ln p sqrt(log m)=o(sqrt m), rather than the slightly simpler
condition stated for D=O(sqrt m). The source's exponential m versus p=Theta(J)
range satisfies both by a large margin; this introduces no gap in the
claimed application. Polynomial matrix width remains possible.

## Isolated replay

Copied the checker into `routes/A/linear-sketch-review-replay/` and ran it
there, preserving the lead's original result file. It passed 8,472 exact
ternary Parseval controls; 480 other odd-prime controls and 480 shifts;
1,147 exact-degree cases; 3,666 zero-column cases; 40 matching groupings;
and both characteristic-two and dimension-free negative controls. The
isolated JSON is `linear-sketch-review-replay/verification.json`.

The replay uses exact integer/Fraction arithmetic. Its general-prime bound
uses sin(pi/(2p))>=1/p, a valid rational weakening, rather than floating-point
evaluation of the analytic constant.

This is an independent AI-agent proof review and finite replay, not human
refereeing, a formal kernel proof, a generated tape-multiplier execution,
or a general lower bound for multiplication, all matrix representations,
or arbitrary nonlinear input summaries.
