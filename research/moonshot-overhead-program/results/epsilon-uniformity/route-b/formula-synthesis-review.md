# Independent adversarial review of the formula theorem

Reviewed on 2026-11-25. **The local formula construction, complete transfer
and new Theorem F pass this independent audit. No mathematical blocker was
found.** This is Route B's separate review of Route C's algebra and Route A's
generator/physical transfer, followed by the lead's global synthesis. It is
not a formal proof build, a human referee report or execution of the complete
multiplier.

## Exact reviewed snapshot

Hashes were taken at 16:01:45 UTC. Paths are relative to
`results/epsilon-uniformity/`.

| File | SHA-256 |
|---|---|
| `THEOREM.md` | `1bc208878ed7f61edb03099218b4acc3dc63ed3bd09882a8131ab928aff378c6` |
| `route-c/FORMULA-FACTORIZATION-COMPRESSION.md` | `a2801471b10b7b0553ce5fd6ce1a14ce5b1cc1eafd65ea70632af796adadc65d` |
| `route-a/formula-template-transfer.md` | `a603ed47cba7c21532e9249ef61b5edf9f0cdb9db9405504eb3e7fbb05d498a4` |
| `ROOT-FORMULA-REVIEW.md` | `ed17719943222815496a13bf389a7d44551c36820a38cc9aaba057adb8c767ef` |
| `route-c/FORMULA-TRANSFER-REVIEW.md` | `0e3a0d782d70fb0510f66e07fad57e3f5dc63fb800e226a0925b9ed462fa2359` |
| `route-a/rational-geometry-height.md` | `468001742bf99bba977beb8e8c72f266e98e62c6f0fc416b1d4ee332833191f1` |
| `route-a/compiler-invoice.md` | `5ecd20dd366da0d62b1d3b399d07d67fb8e10a1c939a862c723c40eb2395657d` |
| `BASELINE-THEOREM.md` | `6e814bff4ae85f44cebd5a8fcab74a2c8383b47e0628b486de9add34a56e6097` |

The baseline hash agrees with the theorem reviewed at checkpoint
`0961d2083f80429dde4b6ec5197585f727c7f87b`; it has not silently acquired
the new statement. A subsequent status-only header change should be recorded
as such rather than attributed to these exact bytes.

The primary-source pin is OpenAI `math` at
`3344da59991ed94f9ba711217b29c1d760badfa6`. In addition to the five requested
new proof/review files, this audit read the refined rational-geometry proof
and directly rechecked `F/repair.tex`, `cor:swap-repair`, the batch grouping
in `F/binary.tex`, and the batch/padding paragraphs in `T/walsh.tex`.

## Algebraic checks

**Degree and constants.** The generating-function coefficient extraction
gives integer `c_a` of `O(D log(m+2))` bits. Balanced convolution constructs
a formula with all repeated children counted. Its size is
`2^{O(log(m+2) log(D+2))}` and its maximum syntactic degree is `D`.
The nonzero top coefficient preserves degree `D`. Degree-zero expressions
are evaluated as scalars; multiplication by a scalar changes one factor,
and a scalar summand is padded by identities. These conventions do not
add a stage. Repeated internal rounding to powers of two would invalidate
this argument; the actual construction rounds only once at the end.

**Every cyclic product.** In a product composition, the two tensor families
commute across families. After any cyclic cut, each family's subsequence
is a cyclic ordering of its original list. Regrouping therefore gives
`fg I` at every starting grade. Identity insertion preserves that invariant.
Scaling exactly one factor scales every cyclic product exactly once.

For sums, write `A=delta_U tensor I` and `B=Z tensor delta_V`. The specified
degree-minus-one convention gives `BA=zeta^(-1) AB`. The mixed Gaussian
coefficients vanish as integral cyclotomic polynomial identities. Thus
`(A+B)^d=(f+g)I`, with no division by `d` or by root differences. The
total-grade components all have rank `d a_1 a_2`; restricting transitions
between them gives the claimed cyclic factorization. The case `d=1` is
ordinary addition. Neither commutativity within one factor list nor a
preferred starting grade is being assumed.

**Mixed root orders and descent.** The common order
`M=lcm(1,...,D)` contains every internal factor length, and `M<=D!`.
Cancellation is first proved over the integral characteristic-zero ring.
The regular multiplication representation on its free dyadic basis sends
the final scalar polynomial to `P I`. Consequently the final pencil is
dyadic before any reduction modulo an odd prime. A prime dividing `M`
causes no obstruction: no primitive-root, reduced-ring or semisimple
property is needed after reduction. Only powers of two were inverted.

**Independent rows and shifts.** The final cyclic block matrix has
`L^b=P I` on every block because all cyclic products were established.
Regular descent retains every basis coordinate as independent input data.
For a shifted predictor, query sign substitution plus a sign on one factor
gives the required global sign. Multiplying the whole pencil by that sign
would fail for even `b`; the proof correctly avoids that operation. Every
shift has equal dimension, preserving the source exceptional-row fraction.

## Generation and source transfer

The rank bound is `log K<=F log max(2,D)`, yielding
`E_2(O(log^2(m+2)))`. Factor entries are copied, shifted by root monomials,
added or scaled by known integers. Tensor concatenation never multiplies
two arbitrary affine entries. Thus dense expansion does not conceal a
repeated coefficient-squaring process. Redundant root arrays, numerator
bits and denominator exponents have the stated polynomial bounds in the
explicit finite parameters.

Cyclotomic generation is an actual bit algorithm. Unit-modulus roots give
`O(M)` coefficient bits; monic division has polynomial temporary heights.
Companion powers through exponent `M-1` have polynomial-in-`M` bit heights
by a row-sum norm bound. Constructing those powers and all regular matrices
therefore costs a fixed polynomial in the displayed finite parameters.
This establishes a literal generator, not only small algebraic descriptions.

Hermite repair uses a separate power-of-two node ring, whose differences
have the stated geometric-sum inverses. Those identities survive every
odd-prime reduction. The pinned swap corollary explicitly permits a finite
commutative coefficient ring and finite-free basis expansion, multiplying
input rows and table widths together. Its stage count is unchanged.
Both interchange and Fourier are replaced; retaining the old Fourier
linearization would retain a third tower elsewhere.

The source's binary grouping is into an arbitrary fixed width `W`, with
the last group padded. Its tape variant makes the leading row count a
multiple of `W^J`. Neither requires `W` to be a power of two. The new
dimension's possible odd factors therefore introduce no new model premise.

The refined rational-geometry proof removes the earlier independent third
tower: its choices have polynomial bit heights, fixed-depth determinant
formulas and `exp(poly(m))` literal generation. Address integer values,
the complete bad-value product, radix search and padding are charged.
The baseline physical invoice then applies through fixed powers of the new
finite budget. New logarithmic norms are `poly(S)`, so the existing
common-ancestor precision bound and reused short-word scratch still apply.

## Complete profiles and inversion

For `Z_j=(j+2)^3 log_2(j+3)`, the actual generated budget is
`S_j<=E_2(C Z_j^2)`. This is **not** `E_2(C Z_j)`: the formula costs
`exp(m^{O(log m)})`, not the stronger fixed-degree `exp(poly(m))` bound.
The complete core coefficients, generation, all-length space and sufficient
threshold are bounded through `poly(S_j)`. Actual shape checks, aggregate
setup microsteps, fixed auxiliary marks and preserved-input fallback retain
the previously audited all-length safety argument.

The chunk wrapper and actual-step schedule give
`d_j,b_j<=2^{C Z_j^2}`. They include generation, interpretation, movement,
cleanup and complete output. With `z=log_2(x+16)` and
`w=log_2(z+2)`, choose `j=floor(c(z/w^2)^(1/6))`. It is eventually positive
and at least half its unrounded value. For a sufficiently small absolute
`c`, `C Z_j^2<=z/2`, so both coordinates are at most
`sqrt(x+16)<=2sqrt(x)`. In particular `b_j<=x`: this checks the actual
threshold, rather than optimizing an ineligible candidate. Adding the
remaining `x/(j+2)` gives exactly

\[
 T(n)\le n\sqrt{1+\log_2n}\;
 2^{O\!\left(x([\log_2(z+2)]^2/z)^{1/6}\right)}.
\]

The weaker `z^(-1/8)` exponent follows from
`[log_2(z+2)]^(1/3)=O(z^(1/24))`. The optimizing index is used only in
the analysis of the one fixed schedule. The physical visited-space
constant is uniform, and schoolbook guarantees correctness at every length.
No conditional MR, endpoint family or variable-arity premise is used.

## Verification and provenance boundary

No broad suite or duplicate finite matrix tests were run in this review.
Route C's reported 84 predictor, 152 cyclic-product and 72 full-coordinate
checks, including the characteristic-three degeneration control, remain
their separate finite evidence. This audit supplies the written universal
argument checks and exact-file receipt.

Concurrent S002 has independently admitted the same balanced-formula scale
at commit `58c754b583815e4fe40d333ec9d71e4c254749ba`, as recorded in the
construction and transfer. This audit preserves that separate provenance
and makes no priority claim. The strongest new local obligation is now a
smaller full-rate representation with an actual fixed-degree
`exp(poly(m))` constructor; the present proof does not establish it.
An exact square-root endpoint would require additional progress beyond
that representation bound.

Credits: @CubeJerry; the pinned OpenAI constructions and cited
matrix-factorization literature; the separate S002 derivation; Routes A
and C and the lead. Prepared with GPT-6 Astra Pro assistance.

## Final editorial and scope receipt

At 16:20:50 UTC, `THEOREM.md` has SHA-256
`e93874e88dea84e69449dc37a2753a469acb257c433d3f77a579907816a6ae21`.
The header now records this review's admission and a later S002 advance;
the document also credits the independent same-rate formula construction
and states the scoped multilinear-recipe obstruction. The displayed
Theorem F, `E_2(CZ_j^2)` finite profile, `2^(CZ_j^2)` cost/threshold
coordinates and integer inversion remain the statements audited above.
The recipe comparison is separately recorded in `barrier-overlap-review.md`.

S002's later fixed-field IP4 result reaches the stronger third-root rate.
This receipt does not independently admit that new construction; the lead
and Routes A/C conduct its separate review. The all-odd-characteristic MR
representation interface and the best attained programme rate must not be
conflated. The stronger programme result does not invalidate this separately
proved all-odd-characteristic formula theorem or its historical receipt.
