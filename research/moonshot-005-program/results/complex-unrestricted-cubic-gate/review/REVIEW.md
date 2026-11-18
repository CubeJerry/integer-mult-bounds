# Independent review of the all-cubic obstruction

**Accepted in its stated fixed finite collective-tail model.** Reviewed
`UNRESTRICTED-CUBIC.md`, SHA256
`cc811adc416ee4344869b2d4674f04243825948221c46f43f68595bebe9fb069`,
and the six exact retained dependencies in `CUBIC-SOURCE-PINS.json`.
The claim excludes three independent Gaussian heads all of rank at least
three for `L C U Q L`; arbitrary ordinary three-bank units and their
ordinary inverses are retained. It is not a one-width matrix-algebra
claim, a complete supplier, or a new kappa.

## Fresh mathematical check

The literal inverse of L has entries a^-1 and -a^-2 in the stated order.
At one letter, their row and column l1 norms are sqrt(2) and 2. Pulling
back any rank-at-least-three endpoint head therefore gives maximum entry
strictly below one. The retained finite-word tensor separation makes
such labels disjoint from the ordinary span at all sufficiently large
faithful widths; width-dependent exterior coefficients do not change the
finite catalogue's independence. Fixed-prefix matrix coefficients commute
with the common tail operations. Ordinary units preserve this span and
its complement because monomial translation preserves nonmonomiality,
and their inverses remain ordinary.

I independently recomputed both flagged rows/columns. The left pullback
forces q21=q22=0 and the right pullback forces c02=c22=0, using separation
of ordinary and one-Gaussian labels. Permuting C's second and third block
rows then gives a genuine block lower triangular matrix with diagonal
blocks B and c12. Since the full finite-width C is invertible, B is
invertible; no inverse of a projected coefficient is assumed.

The last-column formulas for E22 and E02 have the displayed multiplication
order. E22 contains only one- or two-Gaussian labels, so it vanishes
against an endpoint containing only rank-at-least-three labels. Separating
its support classes gives the second row of B times
`(a q02,a q12)^T` equal to zero. In E02 the two inner label families are
disjoint *before* the common exterior a. Left multiplication by an
invertible one-letter A is injective on projective labels, so they remain
disjoint afterward, even when a two-letter inner word reduces in support.
The one-letter inner family has at most four entries after the exterior
and cannot match the endpoint. It therefore vanishes independently and
supplies B's first row equation. This preserves noncommutative order.

Invertibility of B and a forces q02=q12=0. Together with q22=0, Q has a
zero last column, contradicting its unit assumption. The proof does not
require spectator-preserving interstages or commuting ordinary matrices.

## Independent exact controls

`check.py` imports no author implementation and uses no floating point.
It builds the signed four-bit A as an integer-Gaussian numerator over
denominator two, directly from its bit action. It checks unitarity, the
flat supports 1,2,4,8,16 of powers zero through four, sixteen two-sided
inverse-pullback probes, and the essential quadratic control
`A^-2 A^2=I`. The latter is ordinary and rules out extending the first
pullback step to heads merely of rank two.

A separate free noncommutative polynomial interpreter checks the literal
left and right inverses of L and both flagged active-column expressions.
It never commutes c or q blocks through a. Exact hashes bind the reviewed
source and all retained dependencies. These finite/source checks support
the separate algebraic argument; they do not establish tensor faithfulness
on their own or certify the full multiplication framework.

Reproduce with:

    python3 -B check.py --proof AUTHOR-PROOF.md --pins AUTHOR-SOURCE-PINS.json --repo REPOSITORY --out RESULT.json

The remaining profiles (3,2,2), (3,3,1), and (3,3,2) are not excluded:
their lower-rank heads may contain precisely the components forced to
vanish here. Those source constructions and every full supplier/caller
cost remain open.

Independent proof review and controls by S023 Worker A, with substantial
OpenAI assistance. Credit the retained source/separation authors,
@CubeJerry and S023 Worker C's new cubic argument.
