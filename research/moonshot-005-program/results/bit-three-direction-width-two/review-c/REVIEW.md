# Independent review of the width-two, three-direction envelope theorem

**Accepted as an all-field algebraic lower bound under its explicit native
rigidity/scalar205 dependencies. No physical source or new kappa.**

Reviewed author proof SHA256:
`2a35dcb0a8b804b3c30d3759533070d903699c0b1dbb237618586511ce9d2bb5`.
I checked the proof directly and wrote a separate pencil/Jordan checker.
No author verifier is imported. Native scalar205 is inherited rather than
claimed as reproved by these finite algebra tests.

## Universal proof audit

The prior subwidth/full-line and two-direction results reduce the remaining
case to a three-dimensional quotient in a three-dimensional scalar envelope,
with no whole scalar tensor line even after extension. This last exclusion
is justified: full-line membership is the kernel of a linear map, so its
dimension is preserved under scalar extension.

The square pencil is injective as a two-component map, and its two images
span the scalar envelope. Thus it has no common right or left kernel.
If its normal rank were at most one, both coefficient matrices would have
rank at most one, contradicting the three-dimensional sum of images. In
the singular case its adjugate is therefore nonzero of rank one. Primitive
polynomial right/left kernel vectors factor the adjugate with a polynomial
scalar factor: Bezout combinations justify the polynomial assertion.
Neither kernel vector is constant. The degree bound on the adjugate forces
both to be linear, and comparing the three polynomial coefficients creates
the two vectors spanning a whole scalar tensor line. Primitivity excludes
dependent constant/linear coefficients, and absence of a common kernel
ensures their shared scalar direction is nonzero. This contradiction is
complete; no unproved matrix-pencil classification is used in this step.

A regular pencil admits an invertible value projection after extension.
The value-basis change must act by simultaneous similarity on fitting
blocks, as the proof explicitly states; this preserves both identity
diagonal and zero blocks. The quotient can then be identified with a graph
and its scalar basis changed to put the graph map into Jordan form.

At a deleting receiver, canonical rigidity makes the quotient map injective,
so the two selector rows have rank two. The matrix-annihilator argument
correctly forces identity into the span of the three scalar coefficient
matrices. The functional criterion is exact: c annihilates ker Phi precisely
when it is the restriction of a matrix functional, and c dot a is its value
on identity. Dividing that functional's entire receiver row gives a local
scalar fitting in the single global direction specified by c. This avoids
an unjustified assumption that each original scalar direction was separately
local. Independence of the choice of identity preimage follows from the
kernel-annihilation condition.

All Jordan cases check. For a length-three block, ker Phi is zero or the
final coordinate eigenline, and identity forces the first two preimage
coordinates not to vanish together. For a length-two block with repeated
eigenvalue, the first coordinate alone works. For two distinct eigenvalues
with one length-two block, the kernel is zero or one of the two stated
coordinate eigenlines. The two generic directions work in the zero-kernel
case; the fixed first-coordinate direction plus the appropriate generic
one work in each eigenline case. The nonvanishing arguments follow from
the impossibility that identity is a multiple of a rank-one matrix.

The semisimple cases use either a scalar contraction of rank at most one
or three rank-one coefficient matrices with distinct value lines. Their
active independence follows from the rank argument given. At least two
global scalar directions then dominate each saving row.

The use of independent transcendentals is legitimate: choose the identity
preimages over the preexisting data field, then extend. Nonzero linear
polynomials cannot vanish. Each of the resulting scalar directions is fixed
across receivers, while row functionals and normalizations may vary. The
weighted two-of-three count gives2S<=51, and integrality gives ell>=197.
Two-unit savings are counted with their actual weight. None of these
algebraic scalar reductions is asserted to be a physical algorithm.

## Independent finite controls

The checker examines all262144 ordered pairs of binary3-by3 matrices. It
filters by the exact injective-stack and full-envelope ranks and computes
the determinant polynomial, not only its values at binary parameters.
All7056 admissible singular pencils contain a whole scalar tensor line.
Explicit controls show why both rank hypotheses are needed: dropping the
full-envelope condition or dropping injectivity gives a singular example
without a whole scalar tensor line.

A further control has determinant t+t^2. Its first, second and summed
binary value projections are all singular, but an F4 projection is
invertible. Thus the graph reduction really may require field extension;
binary point sampling would wrongly classify this pencil as singular.

All rank-two2-by3 selectors are enumerated over F2 and F4. Thirty Jordan
parameter cases contain19614 selectors whose coefficient span contains
identity. For each, exact elimination constructs an identity preimage and
the entire coefficient kernel, checks the eigenline condition, and checks
the promised number of fixed scalar dominators. Transcendental coefficient
vectors are represented by their formal linear polynomial coefficients;
the checker does not substitute a few finite values for t or s. When the
identity preimage is nonunique, every finite-field preimage is checked for
the same domination result. Repeated-eigenvalue scalar contractions are
also checked directly.

The proposed four-direction chain is tested on all nonzero quotient vectors
over F2 and F4, each of which has tensor rank two. The proof's first/last
nonzero-coordinate argument supplies the all-extension statement. This
control shows only that the next abstract representation is outside the
proved envelope-three theorem, not that a native fitting exists there.

## Reproduction and limits

```bash
python3 -I -B check.py --proof ../author/PROOF.md --output RESULT.json
python3 -I -O -B check.py --proof ../author/PROOF.md --output optimized/RESULT.json
```

Expected status is PASS_INDEPENDENT_THREE_DIRECTION_WIDTH_TWO_ALGEBRA,
with262144 binary pencils,7056 admissible singular cases,30 Jordan cases
and19614 identity-span selector rows. Normal and optimized mathematical
receipts agree. The proof hash is enforced and checks use exceptions.

The finite enumerations are controls for the proof, not the justification
of arbitrary-field quantifiers. The native205 theorem, canonical rigidity,
prior subwidth result and two-direction theorem remain separately identified
dependencies. No sharpness of197, fitting in envelope four, physical
history, supplier or foundational discharge is established.

This is an independent AI-assisted review by Worker C for @CubeJerry.
Credit the author's pencil/Jordan construction and the prior programme
results. No human or formal-kernel acceptance is represented.
