# Lead review of the compact rational Walsh component

Decision: **accepted as the conditional numerical component stated in CW1–CW8**. This is not acceptance of the compact interchange premise, the integer caller, or a new complete multiplication envelope.

Reviewed `route-a/compact-rational-walsh.md` and its checker against the pinned OpenAI tape `walsh.tex`, `permutations.tex`, and `uniformity.tex`, the Fourier binary-normalization proof, and S002 `polynomial-auxiliary-cost-audit.md`. The independent E002 `polynomial-walsh-precision.md` and `separated-setup-transfer.md`, imported at `9d5abf18ff741ff6f8b9f82790e0475fc662b4fe`, supply corroborating constructions, not a substitute for this audit. All polynomial exponents here are absolute.

## The decisive numerical distinction

The divisor of a generated rational coefficient has polynomial-in-m bit width, even when the numerical record has k bits. Restoring division retains a remainder below that divisor. Producing p fractional bits therefore costs O(B²+pB) with B polynomial in m. It does not cost k² when k is much larger than B. The checker explicitly detects the different regime in which the divisor itself has k bits. Source short products then cost O(k log k); the proof charges them at every record operation.

The alternative exact rational scaling primitive in E002 W1 is compatible: multiply a long record by a short numerator and divide by the short denominator, rounding only the result. It could remove coefficient-preparation error bookkeeping at those gates. It is not needed for the present bound, because CW's dyadic preparation and its errors are both charged.

## Source-specific coverage

The source kernel selectors are explicit parity sums of linear or bilinear functions on address columns. A scan of the O(k)-bit address for each of polynomially many selectors costs polynomial(m) times k per numerical record; the record itself has Theta(k) bits. This argument is valid for numerical Walsh and must not be transferred to raw small-symbol interchange without a separate amortized mask construction.

Counts, the actual discrepancy set, Newton values, and a Vandermonde inverse are all computed from this key in polynomial(m) work. Inverting the actual defect set avoids zero-gap division. Polynomial matrix dimension and polynomial entry height bound minors and exact elimination intermediates by polynomial bit height. No exponential table is scanned or enumerated per record.

The pinned binary normalization supplies the same axis normalization to common and free kernels; complete repair-conversion normalizations commute through the row maps and cancel. The replacement's remaining exact rational coefficients consequently have height depending on m, not on the active slot width. The exceptional one-bit butterfly is treated separately with its certified square-root preparation.

## Precision and physical bounds

The number of finite row roles, labels, matrices and numerical template instructions is polynomial in m. Their deliberate serial execution can therefore use polynomially many full scans. The source shared endpoint order is retained for recursive calls; overcounting ordinary scans cannot license extra calls. This is an explicit dependency of the component.

With arity A at least m and branching at most m to an absolute power, the tree has at most polynomial(m) times a fixed polynomial in k nodes. The fixed exponent in k is essential. One-level logarithmic gain is polynomial(m), so the source common-ancestor proof gives polynomial(m) times log(k+2) logarithmic propagation gain. The guard k at least an effectively enlarged fixed power of m makes this gain a fixed fraction of k. The same guard absorbs absolute-degree descriptor setup into the exponential array volume. Thus a numerical width C₀k with an absolute C₀ is justified above that guard; the omitted small range is handled by exact fallback.

The packed-XOR guard may grow by O(log m), which changes its number of ordinary passes by a polynomial factor in m. It does not change the power of active width or the polynomial degree in k. Its sparse repair sort, tags, head returns and cleanup remain in the source bound. CW's interchange premise explicitly includes arbitrary spectator ranges, actual generation and description bills; a symbolic matrix representation would not satisfy it.

The padded spectator count is controlled because W is polynomial in m, A is at least m, and the available spectator range is exponential in k. Child streams retain their prescribed untagged volumes. Finite repair descends through V/8 and spatial recursion through at most V/2. Reusing marked regions gives the stated polynomial(m) coefficient for all cells visited. This coefficient still needs the common-cap wrapper in a complete theorem.

## Exact replay and limits

An isolated copy ran under `python3 -I -B` with assertions active. It passed 168 spectral keys, 33 nonempty exact inverse/gap repairs, 1,309 dyadic precision checks, 187 precision-growth checks and 320 source column-selector identities. Negative controls covered growing divisor width and even arity. Source hash, command result and exact output are retained under `lead/replays/compact-walsh/`.

The replay exercises finite identities and arithmetic behavior. It is not a whole tape-machine execution, asymptotic proof, formal verification, or external referee review. CW's physical interchange premise remains a separately reviewable gate. The prior complete H(n) remains the admitted bound until that gate and the global compiler are closed.

Prepared for Jerry Chen (@CubeJerry), with substantial ChatGPT research and review assistance.
