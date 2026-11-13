# A uniform price interval for the conditional eight-packet invoice

This is a proved analytic consequence of the independently checked pinned q8 profile. It is a MOVEMENT inequality, not a covered BIT certificate. The source and every compiler/cover/atom/ordinary/complex obligation remain.

For the same fixed complete caller and hypothetical Q={1:1618}, let

    M_m(k)=(N-H)_(1-k)+m/(36(m-1))*(T2-P2)_(1-k)-1618.

For every real k in [1/200,2503/500000]=[.005,.005006], fixed even m=6 is the first even multiplicity with M_m(k)>0. In fact M_6(k)>1.0413493020838016 and M_6(k)<1.5263753820838017 throughout this interval. Thus one extra unit-rank call still fits; two do not. The limiting margin is between3.5593497111523552 and3.9424107111523554, and the paired moment stays negative, so at most three additional unit calls fit at any finite m.

Proof: for any finite signed profile c and 0<=k<=1,

    |d/dk sum_r c_r r^(1-k)| <= sum_r |c_r| r log r
                                  < (7/10) sum_r |c_r| r ceil(log2 r).

The r=1 summand vanishes. For r>1, r<=2^ceil(log2r), and log2<7/10 because the positive degree-four Taylor partial sum for exp(7/10) already exceeds2. The right side is an explicit rational constant L_c. Integrate over the interval of length3/500000 and apply the exact previously admitted endpoint bounds at k=1/200. No floating point logarithm or sampling is used. The resulting rigorous enclosures are:

| Quantity | Uniform lower | Uniform upper |
|---|---:|---:|
| M_2 | -9.030652334190413 | -8.137765934190412 |
| M_4 | -0.637317637295235 | -0.084314837295234 |
| M_6 | 1.0413493020838016 | 1.5263753820838018 |
| M_infinity | 3.5593497111523552 | 3.9424107111523554 |
| (T2-P2)_(1-k) | -453.240073632340 | -434.886359232339 |

The JSON receipt gives the exact rational bounds; displayed decimals are outward summaries. Negative paired moment makes M_m increase with m toward its limiting value. The m2/m4/m6 signs give the first even m exactly. The limits imply the stated extra-call counts. QED.

This whole interval contains both the hypothetical two-stage price .0050001 and the explicit one-stage-threshold-plus10^-10 price9961475399/1990000000000. The interval's upper endpoint exceeds3112961/621875000 by a positive rational gap. A movement exponent k must not be identified with an admitted covered saving C: the source, all-volume compiler, cover and strictification losses still have to be proved and charged. The interval only shows that the proposed movement profile has genuine room above the bootstrap threshold; it does not supply the missing algorithm or permit any price substitution without its contracts.

This proof uses a uniform derivative bound, independently of worker B's sharper directed log/exp enclosures at two specific prices. It corroborates those target signs by a different argument and gives a continuum statement, not an extrapolation from experiments. Prepared for @CubeJerry with OpenAI assistance; retained source/paired-caller and bootstrap credit remains.
