# Independent review of the cyclic formula construction

Status: **passes independent Route A audit**. Reviewed
`../route-c/FORMULA-FACTORIZATION-COMPRESSION.md`, Sections 1--6, and its
interface with the source's original count predictor and Hermite repair.
The review is mathematical and AI-assisted, not a formal verification or
execution of the astronomical matrices.

## Formula degree and size

The coefficient identity follows by extracting `T^h` from the product of
the fixed series and elementary symmetric generating function. Coefficients
are integers with polynomial bit lengths. Balanced variable splitting
duplicates each required subformula explicitly and gives
`[C(D+1)]^(ceil(log_2m)+2)` nodes. Every convolution product has the desired
syntactic degree. Omitting `e_0=1` product factors and scaling a single
matrix factor by a scalar coefficient are essential: counting those
constants as extra stages would invalidate the degree claim.

The theorem's `0<=u<v<=m` restriction is compatible with the sufficiently
large source window. The explicitly stated finite fallback handles smaller
source windows extending outside that interval. No small-size conclusion
depends on using an inapplicable formula hypothesis.

## Every cyclic product, not one preferred block

For multiplication, factors from the two tensor families commute. After
any cyclic cut, the subsequence from each family is a cyclic ordering of
its original list. Regrouping gives `fg I` on the whole tensor module.
Inserting identities preserves this property. Multiplying one factor by
a scalar multiplies every cyclic product by that scalar exactly once.

For addition, let `U=delta_A tensor I` and `V=Z tensor delta_B`, with
`Z delta_A=zeta^(-1) delta_A Z`. Then `VU=zeta^(-1)UV`. Mixed Gaussian
coefficients vanish at a primitive complex `d`-th root; because they are
integer polynomials, they vanish in the integral cyclotomic quotient.
Hence `(U+V)^d=(f+g)I` without dividing by `d` or by a root difference.
The total-grade subspaces all have rank `d a b`, and the operator shifts
total grade by one. Each cyclic product of the grade-transition blocks
therefore equals `(f+g)I`. The case `d=1` is direct addition.

One final padding to the source power-of-two `b` is legitimate. Padding
each earlier arithmetic operation to a power of two would change the
degree recurrence; the proof does not do that. The final block-cyclic
matrix has `L^b=P I` on all grades and all rows.

## Ring choice and regular descent

All intermediate lengths are at most `D`, so `M=lcm(1,...,D)` contains
every needed root and `M<=D!`. The formal identity is first proved over
`Z[1/2,zeta_M]`. Its free power basis gives a regular representation over
`Z[1/2]`. Since the target polynomial is dyadic, descent sends its scalar
operator to `P I` on every basis coordinate.

Thus the final coefficient matrices can be reduced directly modulo any
odd prime. No primitive-root property after reduction, semisimplicity,
factorial inversion, or invertibility of an odd divisor of `M` is needed.
The free basis coordinates are full independent inputs, not zero-filled
work registers.

## Finite generation and heights

Rank obeys `K<=max(2,D)^F`; therefore it has the advertised
`E_2(O(log^2 m))` bound. Tensor composition only copies one affine entry
against identities or scalar root phases. It does not multiply arbitrary
affine entries. Redundant `M`-slot root arrays and explicit duplicated
formula nodes consequently have polynomial bit heights in the displayed
finite parameters. Dense intermediate arrays and their sequential scans
remain a fixed polynomial in those parameters.

Cyclotomic coefficients have `O(M)` bits by the unit-root binomial bound.
Exact monic division and companion-matrix powers give polynomial bit
heights and actual polynomial work in `M`. The regular representation
therefore adds no further tower. This checks the potential gap between
an arithmetic construction and an actual finite tape generator.

## Shifts and source compatibility

Sign substitution plus a sign on one factor preserves the same skeleton
and dimension for every shift. Each cyclic product acquires the required
sign once. The `2^m`-block direct sum has each shift equally often, so the
source tail fraction is unchanged. Queries commute with scalar row
matrices; the formal polynomial identity therefore applies to the actual
query operators. The predictor still costs `b` pencils, and Hermite repair
still costs four such predictor applications.

The downstream checks are recorded in `formula-template-transfer.md`:
both source branches, all repair patterns, numerical widths, rational
address values, physical generation/scans, setup clocks, all-length space,
chunking and weighted thresholds. No omitted exponential was found.

Credits: Route C's derivation; the matrix-factorization literature cited
there; the original OpenAI source constructions; @CubeJerry. Independent
review performed with GPT-6 Astra Pro assistance.
