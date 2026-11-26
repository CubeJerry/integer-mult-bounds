# Lead review of maximal rectangles and bulk thinning

Disposition: **accept the universal finite-graph statements MR and MR-thin
within their supported-rectangle and field hypotheses**. The lead read
`../route-c/MAXIMAL-RECTANGLE-OBSTRUCTION.md` in full and checked every
step. The unrestricted JR hypothesis remains open.

Support forces disjoint coordinate projections. Enlarging to their products
preserves support, and maximality then forces complementary nonempty sets
at each coordinate. Conversely these complementary products are maximal.
Thus their side-size product is at least (q-1)^k, with equality exactly
for singleton-versus-complement cuts. This classification does not assume
that arbitrary supported rectangles are products.

The full-rank condition is correctly stated as characteristic not dividing
q-1. The kernel equation for J-I forces a constant vector and then kills
that vector under this condition. It applies to Q and to characteristic
two for power-of-two q. Rank gives at least N summands, even with negative
weights, overlap or cancellation. Cauchy--Schwarz applied to the two total
incidence counts then proves L_A L_B>=(q-1)^k. The anchor partition attains
the product tradeoff for every k and the balanced maximum for even k.
The note correctly avoids claiming the odd-k balanced optimum.

For arbitrary rectangles, every maximal extension has geometric size at
least B0=(q-1)^(k/2). Therefore each retained density eta contributes at
least eta B0 to sqrt(|A||B|). The total of these geometric sizes is at
most N sqrt(L_A L_B). Bounding the number of large summands bounds the
rank of their aggregate; subtracting that aggregate from the full-rank
target gives MR8. At threshold twice the geometric mean of the two loads,
the remaining summands carry rank at least N/2. Applying the same argument
to retained density proves MR9, for every choice of maximal extensions.

This is an aggregate-rank assertion. It does not assert linear independence
of all thin terms or small density on both sides separately. When the
displayed threshold is at least one, its density conclusion is vacuous.
The unsupported cancellation example and exceptional-characteristic case
correctly mark assumptions that cannot be discarded.

This complements the lead's single-hierarchy obstruction: the maximal
class includes nonlaminar rectangles, while a low-load JR partition could
use many strongly trimmed nonmaximal rectangles. Neither theorem excludes
that possibility, charges tape movement, or changes the admitted global H.

Evidence scope: independent written mathematical review. Route C's exact
finite enumerations remain attributed to its receipt; the lead does not
claim to have repeated that checker in this review. No formal or human
refereeing is claimed.
