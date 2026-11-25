# Independent review of the full-rate formula constructor

Reviewer: Route A. Date: 2026-11-25, S002.

**Verdict: PASS for the finite algebraic construction, bounded generator,
and substitution into the previously accepted physical-template contract.**
The global inversion is written separately in `formula-extraction-theorem.md`.
This is a mathematical source audit with exact finite supporting checks;
it is not formal kernel certification or execution of a complete multiplier.

## Material reviewed

I independently read Sections 1--10 of
`../B/formula-full-rate-linearization.md`, including FL1--FL11, and compared
its common-algebra and generator bounds with
`../C/FORMULA-CYCLOTOMIC-GENERATOR.md`. The reviewed B proof snapshot had
SHA-256

    32a94e05a1f20941e156bfd6219ef218dc1e564b37397264ded05c3a63a6d512

I also read the actual B checker, copied it to the isolated
`formula-review-replay/` directory, and ran that copy. Its SHA-256 was

    91c23c56a5539b07122cfc61a6544e899ad019a709ead39db737dcdb2ee54c97

The physical interface was checked against the already audited A notes:
the finite rational-address list, the physical compiler ledger, the sharper
parameter margins, and the common-cap/restart proof. Root and C separately
confirmed the arbitrary-width source batching from the source text.

## 1. Cyclic products and full occupancy

The invariant requires every cyclic product to equal f times the entire
identity matrix. This is strong enough for the block-cycle construction
and remains true when f=0 or the coefficient algebra has zero divisors.
The proof never infers a rotated identity from a single product by dividing
by a possibly singular factor.

For multiplication, the two tensor-coordinate factor families commute.
Any cyclic rotation can therefore gather the other family's factors to its
scalar whole-identity product, leaving a valid cyclic rotation of the first
family. Constants can multiply one factor and identity padding preserves
the invariant. This validates unequal degrees and zero constants.

For addition, the cycle operators satisfy YX=xi XY, including the grade
wrap, since xi^d=1. In the integral variant the interior Gaussian-binomial
coefficients are divisible by Phi_d as integer polynomials. Their vanishing
therefore specializes to every commutative target algebra; it remains valid
when the characteristic divides d. No inverse of d is used. Restricting
the resulting degree-d scalar power to the successive total-grade spaces
gives exactly d affine factors on d*r*s independent rows. Each grade has
the same square size and every starting grade returns to itself after d
steps. Hence every input coordinate is transformed; there is no discarded
workspace occupancy.

The characteristic-two odd-part/Frobenius variant is also correct, but the
integral variant alone suffices for the original-source global theorem.

## 2. Formula size and syntactic degree

The coefficient recurrence explicitly copies subexpressions. Thus its
bound concerns an actual arithmetic formula, not a small circuit whose
sharing would disappear during factorization. At a leaf, the binary
coefficient has degree zero or one. In the order-three variant, the affine
T-squared coefficient still has query degree one, at most its T-degree two.
Induction therefore gives syntactic degree at most h for the coefficient
of T^h. Weighted sums and degree-zero scalar factors preserve the budget.

The recurrence T_r<=4(D+1)T_(r-1), with the displayed polynomial overhead
for the outer truncated series and sum, gives the conservative bound
[8(D+1)]^{ceil(log2 m)+3}. Cancellation is not used to reduce degree, and
no homogenization assumption is needed. Fixed formula shape and prescribed
degree budgets make the row size independent of the shift and of accidental
zeros after reduction. The final D stages are no more than the source's
previous padded b>=D stages.

Every sum gate multiplies the dimensions by at most D and each product
multiplies the two child dimensions, so the final dimension is at most D^S.
Intermediate matrix dimensions are bounded by that same final dimension.
For D=O(sqrt(m log m)), the actual tree has size 2^{O(log^2 m)}, giving
R<=2^{2^{O(log^2 m)}} after all binary shifts.

## 3. Common algebra, repair and specialization

The conductor is chosen only after the pre-descent formula width R is
known. Taking M=M0*2^a, M0=lcm(1,...,D), supplies all sum-gate roots.
The specific element Z^{M0} has power-of-two order 2^a in characteristic
zero and provides the required check-node subgroup. Its pairwise node
differences are units by explicit denominator-two products, even if other
parts of the cyclotomic quotient become nonreduced modulo an odd prime.

The ring is finite free over Z[1/2], and all formula identities and repair
identities are in this same ring. The source Hermite argument requires the
stated node units; it does not require the whole algebra to be a field.
The completed target has base coefficients. Thus basis descent multiplies
both independent inputs and recursive calls by the same finite rank and
preserves the per-input call ratio. Nodes are not regenerated after descent,
so there is no circular width/conductor enlargement.

The descended width can have odd factors. The source allows arbitrary W
with explicit leading-row padding; the existing quarter pre-padding margin
absorbs a factor of two. B's optional full-batch/remainder wrapper is sound
but unnecessary for the original-source application. The proof must not
claim that an arbitrary module can be replicated to an exact power of two.

## 4. Actual finite construction and heights

The conductor obeys M<=2R^2 for all sufficiently large m because
D log(D+1)=o(m). The bounded remaining range has a correct fixed fallback.
Cyclotomic construction by enumerating divisors and exact monic polynomial
division has polynomially bounded loop counts, degrees and intermediate
bit heights in M. The bound follows from the explicit arithmetic, not an
unjustified output-size estimate.

In the formula constructor a product gate copies/tensors with identities;
it does not multiply two variable-dependent affine factors into one factor.
A sum gate copies entries and twists them by root powers. Scalar constants
have polynomial-m input heights. Consequently the unreduced coefficient
height is polynomial in formula size and input height; there is no hidden
chain of repeated squaring. Exponents may first be reduced modulo M, since
Z^M=1, and monic cyclotomic reduction adds a polynomial-in-M bit bound.

Check-node inverses are explicit products with at most 2R factors and a
denominator two. The bounded-degree Hermite construction and at most R
such products in an interpolation entry give polynomial-in-R heights and
actual arithmetic work. All 2^m shifts/frequencies fit since 2^m<=R.
Matrix listing, repair, scalar descent and the fixed finite verification
loops remain polynomial in R after a fixed enlargement of that polynomial.

The unchanged rational label/address list has numeric magnitudes at most
2^{m^c}. This is absorbed in the common envelope
P_m<=2^{2^{C(log(m+2))^2}} for a sufficiently large absolute C. The
numerical scalar heights are bit heights; the address coefficients and
radix are numeric magnitudes, as required by the physical ledger. This
distinction is preserved.

## 5. Physical substitution and global scope

Each stage is still an affine pencil in the source's commuting query maps,
with arbitrary fixed row matrices. This is exactly the source shared-pencil
interface. There are no free spectral transforms, variable-width uncharged
copies, or constant-time operations in the larger algebra. The construction
replaces only the old finite evaluator, with at most the old stage count.

The unchanged label conversions, repair count, ordinary scans, recursive
child volumes, leading padding and reserves therefore satisfy the earlier
uniform call inequalities. The completed finite parameters meet the same
polynomial-in-P physical compiler contract. In particular the fixed input
cutoff is max{U_abs,2^{P^K}}, with the source's absolute prime-shape cutoff
retained separately. The candidate generator and retained workspace stay
inside the common-cap attempt.

With log m_j=O(J^3 log J), the resulting candidate logarithmic prefactor
and logarithmic-logarithmic threshold are at most
2^{C J^6(log J)^2}. Selecting a dyadic J of order
[log s/(log log s)^2]^{1/6} makes both at most sqrt(s), and thus proves
eligibility as well as the stronger overhead envelope. Full details are
in `formula-extraction-theorem.md`.

## 6. Exact replay and limits

The isolated checker passed 196 formal-polynomial cyclic matrix identities
over F_p[z]/Phi_12 for p=2,3,5,7 and factor lengths 2,3,4,6. It includes
nonreduced specializations, zero children, unequal degrees, products and
zero/nonzero constants. It rejects wrong root twists, wrong total-grade
indexing, and a single-product construction lacking the cyclic invariant.
It also passed 264 unfolded coefficient-formula size/degree cases.

The replay compares every formal coefficient of its one query variable and
the whole square matrix. It does not constitute an exhaustive test of all
formulas, all cyclotomic conductors or the tape compiler. Those claims rest
on the proofs and separately recorded audits.

The graded tensor sum is an existing d-fold matrix-factorization operation,
as attributed in B and C. The contribution assessed here is its quantified
full-rate application and the effective source-to-physical composition.
No novelty claim for that tensor operation, lower bound for multiplication,
benchmark exponent, practical implementation, or proof-assistant certificate
is implied by this PASS verdict.
