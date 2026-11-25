# Independent agent review: characteristic/reserve obstruction

Reviewed: `../INTERCHANGE-OBSTRUCTION.md`, working draft read on 2026-11-25 UTC. Source pin: `openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`. Reviewer: independent Route C AI worker; this is not independent human or Lean-kernel review.

## Verdict

The stated Gram-rank, reserve-size and single-count aliasing argument is correct within its declared construction. No blocking mathematical error found. The argument does not apply to the source's multivariate integral predictor, which the draft correctly excludes.

## Checks performed

1. Re-read the exact Gram form, the definition `a=D-2`, the strict contraction, and the complete-sign-pattern statement in pinned `interchange.tex`. Re-read the integral interpolation/window construction in Fourier `repair.tex`.
2. Independently reconstructed the binary principal submatrix: vary only the first outer word over `{0,1}^(2p-1)`. Then `k(v_x,v_y)` is exactly the distance-`p` adjacency entry. The rational sum/difference basis yields blocks proportional to `J` and `J-(2/p)A`; this is a congruence and preserves rank.
3. Independently derived the eigenvalues by summing a character over the radius-`p` sphere. The binomial duality has the direction stated in the draft. The generating polynomial `(1-z)(1-z^2)^(p-1)` has a nonzero coefficient in every degree from `0` to `2p-1`. Hence all distance-`p` eigenvalues are nonzero over the rationals. This is a rational-rank statement, not a rank claim in characteristic `p`.
4. On the constant character, `2^(2p-1)-(2/p) binom(2p-1,p)>0`, so subtracting the rank-one matrix does not introduce a kernel. The principal Gram block has rank `2^(2p-1)+1`, which lower-bounds the whole Gram rank.
5. Dropping the strictly positive main-call term gives `2a<m^alpha<=m`, so `m>4^p-2>p^2` for every odd prime `p>=3`. The source's centered integer window, after intersection with `[0,m]`, has width `min(m,2B)` for even `m` and `min(m,2B+1)` for odd `m`; both exceed `p` under that inequality.
6. For fixed shift `beta`, counts `c,c+p` really occur in the common spectrum and have identical field-valued counts but opposite required signs. A finite field extension cannot distinguish equal prime-field elements. An everywhere-defined scalar rational function also fails for the same reason; no polynomial degree argument is needed.

## Scope qualification

The general extension to any centered window of effective integer width at least `sqrt(m)` is valid. Any named alternative window should retain that explicit condition or point to its actual width formula. No review here certifies the alternative construction's full runtime, precision or tape implementation.

No finite matrix replay or full formal build is claimed by this review. The review is an algebraic re-derivation, separate from the root's numerical checks.
