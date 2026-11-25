# Independent check of the repeated-root decomposition lead

Reviewer: Route C, 2026-11-25. Scope: Section 2 of
`../route-a/mr-symmetry-literature.md`, together with the primary
Sheng--Tribone text, Theorem 4.4, Corollary 4.5 and their displayed
factorization. **No blocker found.** This does not review every other
paper in that note's literature table.

For commuting affine matrices `A,B` with `A^d=fI`, `B^d=gI`, a primitive
`2d`-th root `omega` gives

\[
 \prod_{k=0}^{d-1}(A-\omega^{2k+1}B)=A^d+B^d=(f+g)I.
\]

This is the integral polynomial identity for `T^d+U^d`. The factors
commute, so every cyclic product is correct. Constructing the list
does not invert `d`. The stronger published direct-sum isomorphism
uses `1/d`; the note correctly separates these facts. The corollary's
complete regular-local and residue-field conditions are additional
hypotheses, not automatic properties of a dyadic polynomial ring.

The shift-isomorphism counterexample is sound. Over an integral-domain
coefficient ring, polynomial-ring units are constant units. A graded
rank-one isomorphism between `(x,y)` and `(y,x)` forces `u x=y v` for
units `u,v`; setting `x=0` rules this out. A variable permutation is
not a linear isomorphism over the fixed coefficient ring.

Converting arbitrary length-`d` lists of grade ranks `a,b` into repeated
block roots produces dimensions `da,db`. The smaller repeated-root
list then has grade rank `d^2 ab`, compared with `dab` for the direct
unreduced graded sum. The generic conversion therefore loses a factor
`d`. This leaves special shift-compatible representatives and useful
invariant summands open.

## A finite-free localization check

An odd divisor cannot become a unit just by adjoining a finite free
algebra over the dyadics. Let `A=Z[1/2]` and let `R` be a unital free
`A`-algebra of positive finite rank `t`. If an odd prime `q` were a
unit in `R`, multiplication by `q` would be an invertible `A`-linear
map. Its matrix is `q I_t`; its determinant `q^t` would then be a
unit in `A`, a contradiction.

Thus the module-splitting theorem's `1/d` hypothesis cannot simply be
absorbed into finite free dyadic descent when `d` has an odd factor.
This does **not** obstruct the explicit integral list above, the
accepted Gaussian identity, a special integral summand, or a different
construction avoiding that inversion. It identifies only the failed
localization shortcut.

Primary reference: Richie Sheng and Tim Tribone, *Tensor products of
d-fold matrix factorizations*, DOI
<https://doi.org/10.1017/nmj.2025.12>, Section 4.
