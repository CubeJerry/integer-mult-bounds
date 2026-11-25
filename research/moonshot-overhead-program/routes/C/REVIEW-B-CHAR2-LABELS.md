# Independent review of the characteristic-two label geometry

Reviewer: Route C, 2026-11-25. Status: **pass for the stated shared-pencil
interface**. Reviewed Route B `characteristic-two-label-geometry.md`,
SHA-256 `80d2aa78eea1e83b31df472cec71859eec0483c4c51f58f2a6a35fc17c0a1bc4`.
No complete product/correction algorithm is asserted by this review.

For d=2^r and 0<=c<2d, the coefficients of `(1+T)^c` below degree d
are indexed exactly by subsets of the low r nonzero binary digits of c.
Their sum modulo two is one precisely when that set of digits is empty.
This verifies the degree-(d-1) indicator of c=0 or d, with no collapse
to a polynomial in c modulo two.

There are `C0=sum_(s<d)binom(2d-1,s)=2^(2d-2)` indicator monomials.
Each has matrix rank at most q^(d-1) on the inner word. In an outer
indicator monomial at least d coordinates retain the full inner P0;
the remaining factors have rank at most n0. This gives exactly
`r_*/N<=C0^(d+1)q^(-d^2)` and `Cr=2^(2d^2-2)`.
The factorization over F_2 base-changes to the prescribed data algebra.

The directed rectangles retain the source's essential geometry. Their
first differing coordinate is fixed on each side, so within a side
inner words vary in at most d-1 positions. Across the sides all d
selected positions differ. The outer product construction therefore
has k=0 within either side and k=d across it. The incidence bound
`binom(h,d)^(d+1)(q-1)^d t^(d(d-1))` follows by independent choices
of differing positions and first-differing-bit rectangles.

The rational Gram matrix has orthonormal endpoint pairs and dimension
at most `2+h q^h`. Its endpoint argument uses only k=0,d and is
independent of the scalar characteristic. Its denominator d is harmless
for addresses after choosing a compatible odd radix prime; it is never
inverted in the characteristic-two data algebra. Subtracting rectangle
transfers becomes adding them, with the same exact scalar identity and
the same logical common addresses.

I checked the cited source delivery argument: preparation is shared over
queries; low-rank delivery pays fresh changes only on its intermediate
streams; general rational changes use O(D_route) swaps. This proves the
displayed per-input shared-pencil call invoice. The odd-characteristic
spectral conversion and Hermite repair are not used in that argument.
Their absence remains a real gap for a full product algorithm.

Finally `t<=3+(log2 m)/d^2` is immediate from the explicit Cr. With
`d` within a factor two of `(u/log2(u+2))^(1/3)`, both `u/d` and
`d^2 log2 u` have order `u^(2/3)(log2 u)^(1/3)`. This verifies the
uniform subpower pencil invoice, `log2 N<=4u+O(d^2)`, and
`D_route=m^o(1)`. No growing-parameter constant was silently imported.

This review is proof-based. No dedicated Route B finite verifier existed
at the time of reading, and no claim to have run one is made. The scalar
full-rate evaluator, spatial extraction, recursive correction target and
visited-cell bound remain separate obligations.
