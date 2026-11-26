# S005 discovery route: proved components and remaining gates

No new unconditional multiplication envelope is claimed here. The
retained frontier is the starting AQ/V/NW bound. This route changed
representations, introduced a distinct CRT caller, obtained constructive
local components, and kept their whole-application costs explicit.

| Component | Established | Still missing or excluded |
|---|---|---|
| SP, `square-product-star-obstruction.md` | Determinant invariant for arbitrary square scalar row mixing and controlled register permutations; quantitative failures for specified star batches | Rectangular row expansion, other physical maps and full-pencil cancellations are outside scope |
| RO, `rowspace-orbit-compiler.md` | Uniform local tape compiler, polynomial rank/unrank, and exact Fourier block ranks including degenerate forms | Cheap ordinary-to-orbit conversion and a closed Walsh-child interface |
| FC, `flag-converter-invoice-and-pivot.md` | Constant-density chart, dual output correction and charged XOR invoice | Generic V a conversion remains too expensive |
| BE, `paired-column-bell-executor.md` | Full-rate common representation for GL maps, Walsh and actual quadratic-key repair tables | Two full-volume half-width encoders and layout conversion; outer products/phases need separate treatment |
| SU, `square-encoder-support-budget.md` | Half-width budget is optimal in the specified full-volume square-encoder class | No lower bound for rectangular encoders, shared endpoints or integer multiplication |
| UC, `unramified-polynomial-crt-caller.md` | Exact full-rate residue representation, small products, integer/carry guards and precision-local inverse lifting | Fast binary CRT and new remainder-digit suppliers remain open |
| FS, `binary-factor-stream-compiler.md` | q b polylog b factor generation on fixed tapes, O(q)+poly(b) space | Global CRT inverses, the degree-q product and remainder maps are excluded |
| FL, `factor-lift-carry-transport.md` | Exact full-module carry transport between nearby lifts; actual modulo-four Hensel factors in q b polylog b time | Fast first-carry supplier and coherent higher-precision construction remain open; extra recursive CRT calls are charged |

SP, RO, FC, BE, SU, UC and FS have passed independent route-c review;
FL has passed independent route-b review in
`../route-b/REVIEW-FACTOR-LIFT-TRANSPORT.md`.
The review files and hashes govern admission. These are written proofs
with agent review, not formal-
kernel verification or practical asymptotic implementations.

## Exact finite checks

- `verify_square_product_star.py`: determinant/spectrum identities,
  actual seed kernels, and controls outside the admitted model.
- `verify_rowspace_orbits.py`: codecs, all-rank address round trips,
  GL actions and exact Walsh block ranks.
- `verify_paired_bell.py`: Bell columns, selected-row Walsh, dense
  rational quadratic-key tables, dependent phases and failure controls.
- `verify_unramified_crt.py`: power-of-two CRT rings, arbitrary payloads,
  quotient products, precision lifts, integer recovery, Lyndon factors
  and two-dimensional Kronecker packing.
- `../route-b/verify_factor_lift_independent.py`: 6,272 exact carry
  transports, complete modulo-four factor products, and wrong-sign /
  omitted-representative-derivative controls, in an independent implementation.

Receipts record exact proof/checker hashes. Dense CRT and brute-force
tiny-field setup in the last checker are verification oracles, not
the fast suppliers being sought.

## Next constructive priority

UC is the most distinct live route: implement binary CRT and K_t,
the map returning only the new t remainder bits from canonical
t-bit input coefficients. Inverse precision lifting reuses the same
K_t. Recursive bit volumes halve, giving the additive precision
budget in UC6. Factor generation has a separately priced schedule.

FL offers a specific first-carry variation: construct the factors of
X^q-X modulo four, then transport a successful K_1 supplier back to
UC's literal factors. With the low remainder already available, the
correction uses one additional binary CRT plus small local work. Applied
only at the bottom precision layer, this changes UC6's binary-term
constant. Applying the correction at every precision would instead add
a recursive child; no such higher-precision saving is claimed.

Retain BE's local executor, but SU closes the attempt to improve its
pairing fraction in the stated class. Continuation needs actual shared
endpoints or a faster combined converter. Route-b separately prices
the encoded outer product and complex phases.

FC records Perles--Weinstein's primary subspace-convolution cancellation
lead with its scalar/arithmetic/indexing scope. A cyclic-qudit Bell
variant was considered but is not a supplier for the pinned outer
caller: its axes are distinct prime CRT factors, while equal-modulus
pairing would require a changed embedding and a new carry bill.
Neither literature lead is promoted to a multiplication theorem.
