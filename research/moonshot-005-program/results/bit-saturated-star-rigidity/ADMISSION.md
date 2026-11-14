# Saturated-star rigidity: admitted S011 result

**Proved within the stated algebraic model. No new complete kappa.**

For every characteristic-two field, every positive whole-record width V,
and every fitting on the authenticated 111-port BIT graph, rank exactly 9V
forces vertex-gauge equivalence to the canonical binary fitting. All 6,470
foreign contact blocks are therefore invertible and the residual rank is
108V. Nonsymmetric, noncommuting and initially singular Schur blocks are
included. Higher-rank codes, changed masks and changed interfaces remain open.

The abstract theorem states that a star graph with minimum point degree at
least five has a unique signed gauge orbit at rank (n+1)V over every field.
Summing an elementary rank inequality forces each intrinsic Schur product
to -I. A rank-excess bound and a degree-three counterexample delimit it.

## Dependencies and credit

[The frozen proof](author/PROOF.md) rederives Proposition 10 (LR) of
DreamingOfClouds's open [PR #7114](https://github.com/CrocSwap/integer-mult-bounds/pull/7114),
head `fc90dc68b54d613a0600e5bddd8e4f557a4b4eda`. Its exact
[THEOREM.md](author/PR7114-THEOREM.md) has SHA256
`a2a0b79545a1857aea0bc9ac4beb9f222aa50984c9383053e9163af8e33a4802`.
That source supplies the inequality and rank-floor method, not this equality
classification. Its open status is retained; the argument was read and checked.

The programme's [minimum-rank theorem](../bit-minimum-rank-nine/ADMISSION.md)
and [ordered propagation](../bit-fitting-rigidity/global/PROOF.md) supply the
canonical representation, 35-role seed and 76 extensions. Native SHA256:
`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.
The new saturation argument discharges the former invertible-Schur hypothesis.

## Independent review and reproduction

Worker A supplied a [separate review](review-a/REVIEW.md) and source checker.
The lead independently reviewed kernels and ordered gauges, reconstructed
the binary factors and anchors, and checked noncommuting gauges at V=2,3,4.
Neither checker imports the author implementation. These are research-agent
reviews, not independent human or formal-kernel acceptance.

```bash
python3 -I -B research/moonshot-005-program/results/bit-saturated-star-rigidity/review-root/check.py --native research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz --output /tmp/saturated-star-review.json
```

Expected marker: `PASS_INDEPENDENT_SATURATED_STAR_SOURCE_PREMISES`.
[Root receipt](review-root/RESULT.json) and [A receipt](review-a/RESULT.json)
record finite source premises and controls. The universal claim rests on the
written proof. Missing anchors, altered masks, low degree and incorrect matrix
order are negative controls.

## Programme consequence

Canonical-support arrival gates now apply at rank 9V without an extra block-
invertibility premise. Strictly larger rank means at least 9V+1, **not** 10V
for arbitrary V. No transport, source, supplier or recursive cost follows.
W0 and all five foundations remain open. Prepared for @CubeJerry with
substantial OpenAI assistance and preserved predecessor credit.
Admission baseline: `66caee29c1293a5c3ad9836c6438e9a157a98a82`.
