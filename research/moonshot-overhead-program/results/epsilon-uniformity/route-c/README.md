# Route C: finite representation, nonstationary recurrences and scoped barriers

This directory records Route C's contributions to the three-hour session.
The consolidated accepted multiplication theorem and complete parameter
ledger are maintained in [THEOREM.md](../THEOREM.md) and
[PARAMETER-LEDGER.md](../PARAMETER-LEDGER.md). Every lower bound here names
the representation or scheduling family to which it applies; none is a
general multiplication-time lower bound.

The late concurrent S002 checkpoint `848fbf1d7a5e192aa352d79b4d3e36fa06be21ee`
subsequently establishes the stronger fixed-field IP4 representation by
polynomial-size characteristic-two count formulas. Its finite algebra,
degree, copied-size, generator and full-row interfaces pass the independent
[S002 count-formula review](S002-COUNT-FORMULA-REVIEW.md). This uses
nonmultilinear spectral formulas and therefore is outside the literal
multilinear lower-bound family below. Its whole-input physical synthesis
and stronger global rate are maintained in the consolidated parent notes.

## Main representation result

[FORMULA-FACTORIZATION-COMPRESSION.md](FORMULA-FACTORIZATION-COMPRESSION.md)
constructs the source's original integral predictor as the `b`-th power of
an affine dyadic matrix on **every independent input coordinate**, with
`b=O(sqrt(m log m))` and actual expanded generator/row budget
`exp(exp(O(log^2 m)))`. A balanced degree-preserving formula is compiled
using standard cyclic tensor factorizations, followed by one cyclic block
assembly and finite free coefficient descent. All shifts have equal rank;
odd-characteristic specialization requires no factorial division.

Route A's [complete transfer](../route-a/formula-template-transfer.md)
then gives finite-template budget `S_j<=E2(C Z_j^2)` and complete schedule
cost/threshold profiles `d_j,b_j<=E1(C Z_j^2)`, with
`Z_j=(j+2)^3 log_2(j+3)`. The resulting fixed-tape, exact, common-linear-space
rate is stated in the consolidated theorem. The stronger
`exp(poly(m))` matrix-root target remains conditional.

The local construction and generator were independently reviewed by
Route A and the lead. The lead also replayed the finite exact checker in
isolation. Concurrent S002 independently obtained the same construction
and envelope at commit `58c754b583815e4fe40d333ec9d71e4c254749ba`; both
derivations and the common matrix-factorization literature are credited.

## Results and their limits

| Note | Established result | Scope |
|---|---|---|
| [Formula recipe lower bound](FORMULA-RECIPE-LOWER-BOUND.md) | Matching `exp(exp(Theta(log^2 m)))` row scale at the source window, using Hrubeš--Yehudayoff and a count of high-degree sum nodes. Independently reviewed by A and lead. | Literal unreduced cyclic compilation of syntactically multilinear, degree-preserving formulas; does not cover arbitrary matrix roots, invariant summands or nonmultilinear quotient methods. |
| [Nonstationary recursion](NONSTATIONARY-RECURSION.md) | A complete rounded recurrence criterion with summable normalized excess and tolls; conditional endpoint interface. | An algorithm must establish the listed physical child-volume, movement, precision and space bills. |
| [Input-dependent radix](INPUT-DEPENDENT-RADIX.md) | Compatible prime radix with bounded or reciprocal-slack volume inflation, explicit forbidden-prime handling and search costs. | A local constructive padding repair; the other endpoint invoices remain necessary. |
| [Source padding barrier](SOURCE-PADDING-BARRIER.md) | Literal fixed-radix full-grid padding has large losses on some variable-arity plateaus; sparse radix menus have a coverage bound. | The specified full-grid schedule, not every tape implementation. |
| [Window predictor depth](WINDOW-PREDICTOR-DEPTH.md) | Exact parity on a contiguous count window requires its full width in affine-query degree; the specified window/repair resource is `Theta(sqrt(m log m))`. Independently reviewed by the lead. | A unit-of-two coefficient ring and the stated all-shift/window-marked conversion invoice; no unconditional normalized-call or time lower bound. |

## Independent reviews contributed

- [Complete original compiler and tower audit](ELEMENTARY-TOWER-REVIEW.md).
- [Explicit binary kernel and repair-table compiler](ROUTE-A-COMPONENT-REVIEW.md).
- [Refined rational geometry and generation](RATIONAL-GEOMETRY-REVIEW.md).
- [Formula and stronger conditional MR transfers](FORMULA-TRANSFER-REVIEW.md).
- [General formula-size transfer](FORMULA-SIZE-TRANSFER-REVIEW.md).
- [Repeated-root symmetry and finite-free localization](SYMMETRY-REDUCTION-REVIEW.md).
- [S002 characteristic-two count formulas and IP4](S002-COUNT-FORMULA-REVIEW.md).
- [Interchange rank/reserve/count obstruction](ROOT-OBSTRUCTION-REVIEW.md).
- [Literal modulo-prime-squared lift obstruction](PADIC-LIFT-REVIEW.md).

These are written mathematical reviews with explicit scope. They are not
formal proof certificates or human referee reports.

## Finite exact checks

Each script runs with `python3 -I -B`; its adjacent JSON records the result.
The file-writing scripts also emit that same complete JSON to stdout, so
redirecting stdout to the receipt does not replace it with a shorter summary.
They check the named finite algebra and rounding cases; they do not prove
the asymptotic bounds or execute the complete multiplier.

| Script | Receipt |
|---|---|
| [Formula factorization](check_formula_factorization.py) | [84 predictor cases, 152 cyclic products, 72 full matrix roots](formula-factorization-verification.json) |
| [Rounded recurrence](check_recurrence.py) | [Recurrence receipt](verification.json) |
| [Dynamic radix](check_dynamic_radix.py) | [Existence/search-selector receipt](dynamic-radix-verification.json) |
| [Fixed-radix padding](check_padding.py) | [Padding receipt](padding-verification.json) |
| [Window depth and tails](check_window_depth.py) | [Degree/tail receipt](window-depth-verification.json) |
| [Prime-squared lift review](check_padic_lift_review.py) | [Spectral/valuation receipt](padic-lift-review-verification.json) |

The formula check includes non-Boolean query examples, every selected
shift, all off-diagonal matrix entries, a deliberately wrong phase and a
nonsemisimple characteristic-three specialization. Further finite tests
would not resolve the remaining representation or endpoint proof gaps.
