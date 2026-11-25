# Lead acceptance of the sharper source-extraction profile

Status: **accepted**, after the separate Route C review and isolated lead replay. This sharpens the analysis of the same fixed machine already accepted in the sixth-power theorem; it adds no conjectural premise.

For L(n)=1+log2 n, s(n)=log2 L(n), and sufficiently large n, the accepted rate is

    T(n)=O(n sqrt(L(n)) 2^{O(s(n) (log2 log2 log2 s(n) / log2 log2 s(n))^(1/3))}),
    visited cells=O(n).

The correct fixed fallback handles the remaining lengths. Absolute constants and the eventual cutoff are not numerically evaluated. This is an AI-assisted proof audit, not a formal kernel build, a full astronomical template execution or human refereeing.

## Independently checked refinement

The source endpoint call lists give the stated absolute per-pencil invoice. Interchange includes the digit-split factor, all four predictor applications, both full-row conversions and the occupied reserve calls. Its bound 1024 b D(1+lambda) leaves ample slack. Fourier's two endpoint sides plus charged rectangles give 5 D_F lambda_F per pencil; four predictor applications and 4d/m^3 repair fit 32 b D_F lambda_F. The pre-padding quarter margin remains explicit.

With x=log2 m, p in [100J,200J] and even L in [100J,202J], I checked the uniform logarithmic inequalities S4--S8 directly against the source kernel/interchange proof. No parameter-dependent O_p term is substituted with growing p. The worst extra log cost is bounded by 3x/p+4p^2 log2(3x)+O(log x). The numerical stopping point x0=2^30 J^3 log2 J pays that cost and all integer guards, including N_I<=m^5, N_F<=m^3, p<=m and prediction degree<=m. Monotonicity of log2(3x)/x extends the bound to all later trials. Dyadic search changes only an absolute factor.

Thus log2 m_j=O(J^3 log J), with the already accepted generator, numeric-address, scalar, physical, precision, space and scheduling costs unchanged. Their combined coefficient and threshold profile has log2 D_j and log2 L(N_j)<=2^(2^(C J^3 log2 J)).

For z=log2 log2 s and Y=(z/(2C log2 z))^(1/3), the largest dyadic J<=Y obeys Y/2<J<=Y. The profile is at most 2^sqrt(log2 s), which is eventually less than s and o(s/Y). The first fact proves actual candidate eligibility; the second bounds the overhead together with the exact exponent penalty s/J. This gives the rate above without uncharged search or an input-dependent machine.

The isolated replay passed 4121 parameter/guard cases, 4121 omitted-constant controls, 170 exact label majorants and 322 sparse-rounding cases. The all-index claim follows from the written inequalities rather than extrapolation from these samples.

## Scope and parallel provenance

The earlier sixth-power theorem remains valid and recorded. This refinement is asymptotically smaller as an advertised envelope. It does not compare the actual runtime with an unknown residual term in the published o(1), establish a benchmark exponent below one in s, or reach poly(s) or constant overhead.

Concurrent E001 commit 0961d2083f80429dde4b6ec5197585f727c7f87b records the same cubic-logarithmic extraction scale with its own compiler and review notes. S002's independent derivation, already written and reviewed before this merge, is retained with separate provenance. Neither is claimed to have priority over the other. Both improve the earlier coarse certificate, not the qualitative mathematical exponent.

Reviewed proof: `routes/A/sharper-parameter-growth.md`; independent audit: `routes/C/REVIEW-SHARPER-PARAMETER-GROWTH.md`; replay: `lead-replay-A-sharper-growth.json`. Credits: source authors, Jerry Chen (@CubeJerry), and AI-assisted independent route work.
