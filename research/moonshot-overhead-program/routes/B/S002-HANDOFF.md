# Route B handoff for S002

Prepared November 25, 2026 for the final session checkpoint. Publication
and repository integration remain with the session lead. This route owns
only files under `routes/B/`.

## 1. Current complete result and division of work

The accepted complete composition is A's
`../A/fixed-field-extraction-theorem.md`, Q1--Q13. With
`L(n)=1+log2 n` and `s(n)=log2 L(n)`, it gives a fixed deterministic
finite-alphabet multitape multiplier with exact full products, O(n)
visited cells, and

    T(n)=n sqrt(L(n))
          2^{O(s(n) [log log s(n)/log s(n)]^(1/3))}.

The large-input display has the stated exact fallback for all smaller
lengths. It is a mathematical algorithm/profile construction, not an
implemented complete tape machine or proof-assistant build.

B's distinct contributions supplying that composition are:

* The pairwise-shift rational Newton predictor, inverse-gap repair,
  coefficient/norm bounds and finite batch contraction for numerical
  Walsh: `pairwise-newton-division.md`, the recovered contraction note,
  and `polynomial-auxiliary-cost-audit.md`.
* Adjustable characteristic-two label geometry and its physical shared
  pencil: `characteristic-two-label-geometry.md`.
* Exact order-three/F4 conversion words, fixed-point handling, the two-P
  repair and label-preserving four-child contraction:
  `characteristic-two-order-three-interchange.md`.
* Full-rate cyclic factorization of a degree-controlled formula, with
  every row independent, common algebra and actual generation bounds:
  `formula-full-rate-linearization.md`. The graded sum construction is
  credited to the cited matrix-factorization literature; the source
  predictor application and quantitative accounting are the programme's
  use of it.

A's later carry-bit construction in
`../A/characteristic-two-count-formula.md` proves IP4 explicitly. It is
the key representation improvement beyond B's balanced coefficient
formula. C and the lead independently reviewed the relevant interfaces.
The dated addendum in `order-three-template-profile.md` supersedes its
historical conditional status and links the complete construction.

## 2. Latest independent review records

`review-characteristic-two-count-formula.md` accepts A's B1--B11 and
admission to IP4, including actual copied formulas, negative shifted
counts, degree budgets, full-rate occupancy and bounded common algebra.

`review-fixed-field-physical-composition.md` accepts Q1--Q13, with
explicit checks of the 32768 interchange coefficient, 128 Walsh
coefficient, J^3 log J parameter growth, rational numerical preparation,
the full finite-data envelope, generation and the common physical cap.

`varying-pencil-source-interface-audit.md` checks the actual source:
the downstream repair and routing accept D different fixed pencils.
They require label-independence, not identical matrices across stages.
Powers of P rerun the entire ordered factor list.

`review-power-two-degree-predictor.md` accepts A's optional finite
refinement in `../A/power-two-degree-predictor.md`. Every sum can use a
power-of-two degree budget, so xi=1 and Frobenius keep the predictor over
F4. A bounded finite-field constructor supplies check nodes. This improves
finite scalar structure without changing Q's global rate or constants.

## 3. Exact verification and scope

The formula checker passed 196 complete cyclic formal-polynomial matrix
identities, including ramified specializations, zero and unequal-degree
cases, and negative controls; 264 copied-formula size/degree cases also
passed. See `verify_formula_linearization.py` and its JSON result.

The independent carry checker passed 5,460 binary addition cases,
137,214 shifted Lucas coefficients, 120 actual serialized formula
evaluations, 525 size/degree recurrence cases, and 45,864 F4 predictor
cases. Missing-carry and omitted-phase controls failed as intended.
See `verify_characteristic_two_carry_formula.py` and
`characteristic-two-carry-formula-verification.json`.

Earlier exact verifiers and results remain with the rational repair,
reflection, characteristic-two labels and O3 closure notes. The lead
replayed the pivotal checkers in isolation. Finite tests corroborate
specific identities; the general bounds and physical composition are
mathematical proofs with independent AI review, not exhaustive machine
execution or formal-kernel certification.

## 4. Restricted obstruction and remaining question

`multilinear-formula-width-barrier.md` applies the published
Hrubes--Yehudayoff homogeneous multilinear formula lower bound to the
canonical cyclic compiler. Within that explicitly restricted class it
forces the double-exponential logarithm-squared width scale. Route C's
independent review is `../C/REVIEW-B-MULTILINEAR-COMPILER-BARRIER.md`.
The carry formulas escape the class through nonmultilinear intermediate
polynomials and exact quotient identities; this is explained by a
four-input example in B's count-formula review.

The distinct dyadic representation premise valid across all odd
characteristics remains open. IP4 and that premise are not asserted to
imply one another. No positive polynomial-overhead benchmark exponent,
constant overhead, or lower bound on the true overhead follows from Q.

## 5. Optional next-interface refinement

`structured-shift-check-refinement.md` is optional and unused by Q.
Its finite algebra was independently accepted by Route A and the lead;
see `../A/review-structured-shift-check.md`. It tensors shift-space checks
with the identity on the internal module,
uses O(m) pairwise-independent ternary shifts, and retains exact 1/16
repair phases by explicitly paid check padding. Combined with A's
F4-only predictor, it needs a repair field of degree O(log m). Its
finite review does not assert a physical executor or a better global rate.

This does not pay for physical execution of the exponentially wide
module. The next discriminating task is an actual structured executor
with charged row-index movement, checks, scalar coordinates, generation,
address maps and a common visited-cell cap, or a genuinely better routing
parameter family. Sparse symbolic matrices alone do not supply that
interface. The current complete result remains Q, without this refinement.

Credits: the OpenAI source manuscripts and their predecessors; the cited
matrix-factorization and formula-complexity literature; A/C independent
research and review; Jerry Chen (@CubeJerry); substantial AI-assisted
derivation, verification and integration during S002.
