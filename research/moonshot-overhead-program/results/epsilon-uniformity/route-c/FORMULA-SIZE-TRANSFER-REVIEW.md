# Independent review of the general formula-size transfer

Reviewer: Route C, 2026-11-25. Reviewed
`../FORMULA-SIZE-TRANSFER.md`, Lemma G1, profiles G2--G4 and Theorem G2.

**Result: no blocker after two wording/contract repairs.** The finite
constructor must output a valid formula at every source-applicable
parameter; only its complexity bounds may be eventual. Bounded window
exceptions use a specified valid baseline. The endpoint discussion now
refers to the displayed sufficient rate, rather than asserting a lower
bound on the actual envelope from upper profiles. Both changes were
authorized and applied to the reviewed file.

## Generic dyadic coefficient accounting

The formula need not be multilinear for the cyclic algebraic construction.
Its syntactic-degree bound limits every factor length. Affine or variable
leaves start with rank one; products multiply ranks, sums multiply by at
most the current degree, and scalar multiplication changes one factor.
Thus `log K<=F log max(2,D)` remains valid for the stated general formula.

Constant-only subtrees require a denominator-aware bit estimate. For any
such subtree, take the product of the denominators of **all** its leaf
occurrences as a common denominator. Its exponent is at most the sum of
the leaf exponents. Expanding the arithmetic formula, each monomial uses
a subset of leaf occurrences; numerator bits are bounded by the total
leaf numerator bits plus total denominator exponents and `O(F)` for the
number of expanded summands. Formula sharing is forbidden, so no leaf
is reused without being counted. Both numerator bits and denominator
exponents are therefore polynomial in `m+F` under the stated contract.

After scalar-only evaluation, a factor entry is copied, root-shifted,
added or scaled by a scalar coming from a formula subtree. Along any
formula path, the sum of the contributing bit bounds is still a fixed
polynomial in `m+F`. No dense-matrix operation repeatedly squares a
coefficient. Redundant root arrays and cyclotomic regular representation
then have polynomial cost in `D!` and these bit bounds.

## Finite and physical budgets

The factors `D^F`, `D!`, all `2^m` shifts and every fixed polynomial
overhead fit `2^{C(m^C+F log(m+2))}`. The output identity acts on all
independent rows and descends before odd-prime specialization. Hermite
tables use power-of-two root differences with explicit dyadic inverses.
The complete bit, table, row and logarithmic-norm contracts consequently
follow exactly as in the reviewed concrete formula transfer.

Refined address values and generation contribute `2^(m^C)`; trial
division and padding cost only fixed powers of the enlarged budget.
The compiler, auxiliary caps, common-space wrapper and scheduled index
therefore yield G2. The `j` part of the diagonal index is absorbed since
the specified source arity exceeds its exponent index eventually.

For fixed `a>=1,b>=0`, substitution of the formula envelope gives
`d_j,b_j<=2^{O(Z_j^a(log(Z_j+2))^b)}`. Since
`Z_j=Theta(j^3 log j)` as an analysis parameter, the exponent is
`O(j^(3a)(log j)^(a+b))`. The displayed choice of integer `j` makes it
at most `z/2`; both profile coordinates are `O(sqrt x)`, and the
remaining cost is `O(x/j)`. This proves G5 with the stated log powers.

Polynomial-size formulas satisfy the stronger MR **sufficient**
condition. The general transfer does not prove their existence, impose
multilinearity, assert their necessity, or turn the displayed
non-endpoint majorant into a lower bound on a multiplier.
