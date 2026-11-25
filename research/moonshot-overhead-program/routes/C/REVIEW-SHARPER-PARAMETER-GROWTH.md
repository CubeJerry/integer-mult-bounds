# Independent review of the cubic-logarithmic parameter extraction

Reviewer: Route C, 2026-11-25. Status: **pass** for the refined parameter
and profile implication. This uses the separately reviewed physical
compiler and common-cap assembly; it does not recertify them here.

Reviewed Route A `sharper-parameter-growth.md`, SHA-256
`5d9b6493937bc2aa8feaad3a27a44b16dd2771d1d7ace104311357d4f2d9a3dc`.
I checked the call invoices directly against the pinned Fourier kernel
and tape interchange constructions, then checked every inequality
S1--S17 and independently replayed the verifier.

## 1. Absolute call invoices S1, S3 and S7

For interchange, a conversion acts on at most 2D fields and hence uses
at most 2D-1 pair exchanges by the source lower/permutation/lower
factorization. There are at most 2N lambda endpoint incidences.
Preparation and undo at each incidence cost at most 8RND lambda.
For each of m queries the two rank-r lists have at most 2r(1+lambda)
terms per scalar row, and their conversions cost at most
4mRrD(1+lambda). The stated

    32D(1+lambda)(1+mr/N)

per-input invoice is conservative. R cancels because every internal row
is independent. Pointwise arithmetic and serialized scans add no calls
to this metric; their physical coefficient remains in the finite envelope.

At mr/N<=1, four b-stage predictor applications cost at most
256bD(1+lambda) per input before digit splitting, and at most 512 times
that unit after the factor-two volume loss. More explicitly the latter
is 512bD(1+lambda). Repair adds at most 4/m^2 after splitting and
occupied reserves add 2(D-2). Their sum is below the spare constant in
`1024bD(1+lambda)`. Thus S3 includes the genuine reserve and padding terms.

For Fourier, two endpoint sides at 2D_F calls give at most
4D_F lambda_F per pencil per row. Charged common transforms add at most
`2D_F m 2^L q^(-L/2)`, bounded by `D_F lambda_F` under the selected q.
Thus the 5D_F lambda_F invoice and its four-predictor multiple
20bD_F lambda_F are valid. Repair contributes 4d/m^3, safely covered
by the stated 32bD_F lambda_F when D_F<=m. Scalar descent multiplies
the total calls and independent input count equally. No full-array
copy has been reclassified as a recursive Fourier call.

## 2. Uniform logarithmic bounds

For the source window, b<=8 sqrt(m(x+2)) is valid for x>=3. The
q-rounding bound `t<=x/p^2+log2(2p)+2` follows from the displayed
explicit Cr, with no growing-prime O_p constant.

In S5 the constant part of log2[D(1+lambda)] is bounded by 3p^2:
the binomial term contributes at most (p+1)(2p-1), and the remaining
logarithms of h and factors of two fit the difference. Substitution
of the t bound adds at most 5p^2 because log2(2p)<=p and p>=3.
The resulting `p^2(log2(3x)+8)` is at most `4p^2 log2(3x)` for x>=p.
This verifies both constants in S5 and hence S6.

For Fourier, `D_F<=3L 2^(2x/L)` and x>=L>=16 imply D_F<=m because
`log2(3L)<=L/2` and `L/2+2x/L<=x`. The endpoint incidence bound and
the predictor bound give exactly the additive constant 9 in S8.
The robust pre-padding quarter margin is retained.

## 3. Search stopping point and all guards

At `x0=2^30 J^3 log2 J`, J>=3, the estimate
`log2(3x0)<=32+4log2 J<25log2 J` is valid even at the smallest J.
The constant product `160002*25` is below 2^22, whereas
`x0/(4J)=2^28 J^2 log2 J`. Since log2(3x)/x decreases here, S12 holds
for every x>=x0. Adding 3/100 or 2/100 to 1/4 still leaves a strict
gap below 1/2, proving both contractions with the stated margins.

The label-count bounds follow with the same stopping point. In
particular `4p^2(log2(2p)+2)<=160000J^2(log2 J+11)<=x0` gives N<=m^5,
and `2x+L<=3x` gives q^L<=m^3. The actual source predictor has
`r0=u+2` at m=2^u+1; `2^u>=32(u+2)` for u>=16 gives d_pred<=m.
The prime and dimension guards are therefore paid by the same bound.
Doubling u introduces only an absolute factor, yielding
`log2 m_j=O(J^3 log2 J)`.

## 4. Inverting the profile without losing eligibility

The unchanged constructor/compiler envelope gives
`log2 D_j,log2 L(N_j)<=2^(2^(C1 J^3 log2 J))`. Let
`z=log2 log2 s` and `Y=(z/(2C1 log2 z))^(1/3)`. The dyadic choice
`J=2^floor(log2 Y)` obeys Y/2<J<=Y. Consequently
`C1J^3 log2 J<=z/2`, so the profile is at most
`F(s)=2^sqrt(log2 s)`.

The inequality F(s)<s verifies the actual threshold n>=N_j.
Also `F(s)=o(s/Y)`, while the true candidate exponent penalty is s/J.
Thus the resulting logarithmic overhead has the claimed order

    O(s (log2 log2 log2 s / log2 log2 s)^(1/3)).

This is a sharper bound for the already constructed machine. It is not
a change of algorithm, a comparison to a specified rate in the published
o(1), or an endpoint/poly(s) result.

## 5. Independent replay

The verifier passed and its output is retained as
`sharper-growth-review-replay.json`: 4,121 parameter/guard cases,
4,121 missing-threshold-constant negative controls, 170 exact label
majorants, and 322 sparse-rounding cases. These finite checks supplement
the unbounded inequalities above.

No correction to S1--S17 was required. The refined parameter/profile
implication is approved subject to the already separate source-profile,
physical-compiler and common-cap gates.
