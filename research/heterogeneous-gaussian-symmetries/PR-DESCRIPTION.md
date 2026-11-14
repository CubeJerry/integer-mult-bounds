## Result and why it matters

Classify **every exact simultaneous permutation symmetry** of a normalized
heterogeneous Gaussian tensor on `product_i [n_i]`, with `n_i>=2` and positive
widths. The only symmetries are signed coordinate permutations preserving
both `n_i` and `gamma_i`, with matching signed shifts.

For distinct widths, only zero-shift reflections remain: every symmetry
has order at most two and at least `T/2` vertex cycles. If all shifts are
nonzero, the identity is the only symmetry. The proof also gives the exact
minimum cycle count and the same symmetry group for the inverse.

This closes a specific transfer question left by the
[homogeneous orbit-scale predecessor](https://github.com/CubeJerry/integer-mult-bounds/tree/2ae2fa14eeefe301652f62313b137a97036ab13d/research/gaussian-orbit-certificate-scale):
its long coordinate cycles require interchangeable factors. The retained
fine-prime normalized kernels have distinct widths, so that mechanism
does not supply long orbits on this heterogeneous target.

**No new kappa, foundational assumption discharge or multiplication runtime
lower bound.** The consequence concerns the specified dense global-symmetry
cycle format, not arbitrary displacement rank or other representations.

## Exact source and certificate boundary

At canonical main `e54523517d0f03e58352e647c403a5af3e525a57`, the retained
`GAUGEFREE-INTERIORS.md` defines normalized shifted kernels with broad width
`b0/rho_i` and narrow width `A*rho_i`. `FINE-PRIME-PADDING.md` supplies
distinct odd source primes `s_i`, targets `t_i in {r,r/2}` and `rho_i=t_i/s_i`.

Write `m_i=(r/t_i)s_i`. These are distinct integers below r, including
across the two target-size groups by parity. Thus

`gamma_i^broad=b0*m_i/r`, with gaps at least `b0/r`,

`gamma_i^narrow=A*r/m_i`, with gaps greater than `A/r`.

The earlier format retains exactly `2cT` scalar slots, including prescribed
zeros. Hence `T²<=2cT<=2T²` for every exact symmetry here. Compression,
vanishing/dependent vectors, different successors and implicit application
remain outside this format count.

The target is an **ideal square normalized tile across distinct original
source axes**, with matching row/column index sets and all translations
absorbed into its shifts. Rectangular or differently indexed blocks require
a separate interface; the rounding shift bound must hold after identification.
Its T is the local tile volume, not automatically the full target
volume in the source notes. Gauges, repeated copies, identity spectators,
periodic tails and the complete current selected caller are excluded unless
separately identified and paid.

## Rounding extension

For `|a_i|<=1/2`, every ideal entry is at most one, so entry error eps
changes a pair product by at most `rho=2eps+eps²`. If `gamma_max<2gamma_min`
and

`2rho < min(exp(-2gamma_max)-exp(-4gamma_min), 2exp(-2gamma_max)*delta_gamma)`,

then every exact symmetry of the stored matrix preserves the colored unit
grid edges. Connectivity in the other coordinate directions proves directly
that each coordinate map is identity or reflection. No general graph
automorphism theorem or lower bound on tiny shifts is assumed.

The retained fine-prime gaps are at least `2^-o(p)`, so
`poly(p)2^(-Cp)` entry errors meet this guard eventually. Tiny shifts may
disappear and unequal errors may destroy reflections; the result is
containment and order at most two, not equality with a reflection group.
Transport through omitted source factors still needs its own error contract.

## Reproduction and checks

```sh
python3.12 -I -W error -B research/heterogeneous-gaussian-symmetries/verify.py
python3.12 -I -W error -O -B research/heterogeneous-gaussian-symmetries/verify.py
```

Expected status: `PASS_HETEROGENEOUS_GAUSSIAN_SYMMETRIES`.

The read-only verifier uses exact rational log exponents and rigorous
Taylor enclosures for dyadic rounding. It imports no predecessor executable.
Eleven complete group searches inspect **243,414 vertex permutations**,
covering two-point axes, equal physical sides with unequal grid counts,
axis/diagonal length coincidences, opposite shifts and repeated widths.
Three further complete small-grid searches check the rounding guard.

Controls detect equal-width long cycles, coarse rounding to an identity
matrix, tiny nonzero shifts that gain reflections, bounded nonuniform errors
that destroy them, zero widths, degenerate axes and a failed gap guard.
The three exact source/proof files are retained with byte and Git pins.
Registered normal/optimized results and independent review are packaged.
Finite checks support the written universal proof; they do not replace it.

## Limits and credit

The remaining source obligation is a complete current caller boundary with
these exact normalized factors and an authenticated entrywise error bound.
The remaining representation question is whether implicit, compressed or
different-successor methods avoid this dense format. No all-order rank
or runtime lower bound is established; the selected bound remains conditional.

Prepared for **@CubeJerry** with substantial **OpenAI assistance** in
research, proof, exact verification and independent model-assisted review.
Credit the A4/A5 orbit authors, Chafik Boukhalfa's
CrocSwap/integer-mult-bounds#1786, IdeaOuter and #1758's contributors,
Vlado Vojdanovski's #1673 audits and all authors named in the unchanged
retained sources. The existing fine-prime transfer audit is credited and
not repeated as a new result. No human or proof-kernel certification is claimed.

## Independent review

A separate reviewer checked the universal geometry, signed shifts, cycle optimum, inverse group, colored-edge perturbation bounds and exact fine-prime arithmetic. Its rational-entry checker imports no author executable and covers888,560 full vertex permutations, inverse elimination and eight semantic controls, separately from the author logarithmic-exponent engine. Both modes agree. Source identification is explicitly restricted to matching square normalized grids, with shift bounds checked after any translation. Rectangular or differently indexed blocks and full caller transfer remain open. REVIEW.md and separate receipts record the model-assisted review.

## Publication checks

All four registered commands, seven exact canonical provenance checks, three retained source/proof comparisons, committed bytes/modes, authored whitespace and official export/input integrity passed. The Gaussian note retains its original CRLF bytes. The full-history gate is unavailable in this shallow checkout; no pass is claimed. PUBLICATION-CHECKS.json records the evidence and the reviewed source-scope clarification. No hosted CI, human acceptance or formal-kernel proof is claimed.
