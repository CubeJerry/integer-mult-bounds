# Wave-three preliminary independent arithmetic audit — 2026-11-11

**Status:** INCOMPLETE / NOT PR-READY. This is a fresh, independently designed arithmetic and source-contract review of three interrupted wave-three investigations. It is **not** an execution of the original author implementation, independent verification of a complete source-specific construction, assumption discharge, or a new conditional exponent.

**Base:** canonical main `e54523517d0f03e58352e647c403a5af3e525a57`. Selected conditional `kappa=0.00363005817`, five assumptions unchanged. No main/certificate/PR has been modified. The two earlier patches in `UNVERIFIED/` remain UNVERIFIED.

## 1. Encoded CRT row query

Independently reconstruct the physical row-selector combinatorics (from the `#5496` compiled formula, not the new source's helper):
- For declared full width `h=ell`, timeline is `1^(2ell-1)`.
- For short width `h=ell-1`, timeline is `1^(ell-1) 00 1^(ell-2)`.
- Exactly `2h-1` rows are active. A short axis has only the two middle idle rows.
- For an active row `j`, the number of preceding active rows equals its local index `lambda=j` below the gap and `lambda=j-2` above the gap for short axes (full axes: `lambda=j`). Therefore the selected coordinate bit index is `min(lambda, 2h-2-lambda)`, and the final global row is active.

A fresh deterministic Python arithmetic check covered 32,760 (`ell, h, j`) cases (ell=3..128), of which 32,508 were active and 252 idle, and 252 end-row-active cases. All passed. This establishes the **static selector identity**, not correct implementation of `row_control.py`.

**Unverified:** actual `Bank` lease retirement and pending VALUE/STEP marker across multiple active rows; `ROM` header/row query; proof that the real source/borrowed tape heads are preserved; complete ROM occurrence and backing bills; compiled control instruction bound, and candidate source/novelty checks against #5496/#5519/#5625. The author patch is `UNVERIFIED/crt-row-query-wave3.patch`; the separate `research/continuous-20261110-crt-rows` fork branch contains pinned inputs only.

## 2. Encoded fine-prime axis source

For `n=2^(ell-1)` (half) or `2^ell` (full), independently derive the integer search range
```
L=n-ceil(n/(2p^2)); U=n-ceil(n/(4p^2));
candidate integers L+1,...,U
```
which exactly represents the strict-left/weak-right rational band
`n-n/(2p^2) < candidate <= n-n/(4p^2)`.

A fresh independent trial-division reference checked 216 `(p,ell)` pairs (`p=2..19, ell=3..14`), 9,432 exact rational/integer interval endpoint comparisons, and 173 feasible quota combinations (counting dyadic `d` up to `p` and the implicit final full axis). All passed. `p=2,ell=8` gives first half/full primes 113 and 227. `p=4,ell=11`, prefix flags `(1,1,0)`, gives emitted moduli `(1987,1993,997,1997)`. The suggested last coordinate 2000 exceeds the final modulus 1997, so that particular fixture tests an invalid-right coordinate while the left group (1986,1992) remains valid.

**Unverified:** execution of the encoded `frontend.py` against actual #5353/#5219/#5053 source objects, correct owned-port allocation and cleanup in all controls, 74-role and history bounds, prime abundance at large parameters, uniform physical time and `#5353` acceptance. The author patch is `UNVERIFIED/prime-axis-source-wave3.patch`.

## 3. Deferred odd-grid splice

The original local-only draft is **not present** as a recoverable GitHub patch. An independent, *narrow* embedding lemma is valid:

Let completed phases select disjoint `A_j`, with cumulative `r_j` in `[0,g]`. If their completed scalar representation is `x_j=m_j 2^-(p+r_j)` with integer `m_j` and `|x_j| < 2^(h+r_j)`, then
```
M_j = 2^(g-r_j) m_j
x_j = M_j 2^-(p+g)
|M_j| < 2^(p+h+g+r_j) <= 2^(p+h+2g).
```
Therefore the **completed endpoints** embed exactly into common `F*=p+g` and signed `W*=p+h+2g+3` bits (with margin). This is an algebraic proof embedding, **not** a free physical runtime rescaling. A fresh check covered 32,000 deterministic disjoint phase schedules and 121,866 completed-phase embeddings; all passed.

The separate narrow eager-policy lower bound
`(ceil(u/64)+ceil(u/128))V >= 3uV/128`
holds by `ceil(x)>=x` and was checked for `u=1..100,000`. It applies to that *specific eager reservation policy*, not to every deferred or sublinear implementation.

**Unverified:** commutation of actual `scale1125` odd divisions and LAMBDA steps across a changing phase format; exact signed temporary `W*+26` without cumulative rounding; pre-existing proof overlap; actual root `G_root` and descriptors, stock, inverse/exposure and all physical tariffs. These require a reconstructed source-specific proof using #6115/#6901/#6970, not merely the endpoint embedding above.

## Independent test status and reproducibility

The original detached runtime and third draft are unavailable here. The independent checker was executed in an isolated local Python environment on 2026-11-11 and reported `PASS_SCOPED_INDEPENDENT_ARITHMETIC_ONLY`. This file records the exact deterministic test domains and counts, **not** a committed full source replay. The standalone checker and JSON report were produced as separate conversation artifacts. No source-level publication preflight or CI was run for these three investigations.

**Verdict: all three remain NOT CLEARED for research PR.** The two recovered source implementations need real end-to-end test execution and peer proof review, and the third needs its lost source draft reconstructed. These scoped identities are consistent with the proposed constructions but cannot be used as evidence of A1–A5 admission or a changed selected bound.

Prepared for @CubeJerry with OpenAI assistance; Apache-2.0. Keep predecessor/source attribution from the pinned research packages.
