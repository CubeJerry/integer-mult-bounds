# Independent review of the two matrix-root transfer statements

Reviewer: Route C, 2026-11-25. Files reviewed:
`../route-a/formula-template-transfer.md` and
`../route-a/single-exponential-root-hypothesis.md`.

**Result: no blocker found in either downstream implication.** The first uses the proved local construction in `FORMULA-FACTORIZATION-COMPRESSION.md`, whose author is this reviewer; its algebra therefore requires the separate Route A, Route B and lead reviews. This note independently checks Route A's downstream work. The second remains explicitly conditional on the stronger MR generator hypothesis.

## Formula construction transfer

The critical finite-data distinction is sound. The formula size is
`T=2^(O(log^2 m))`, while the pencil stages remain `O(sqrt(m log m))`.
Ranks grow multiplicatively through composition, giving
`log K<=T log max(2,D)`. Replacing stage count by formula size would have
destroyed the contraction estimate; the note does not do this.

The stated coefficient invariant is sufficient. Dense factor expansion
copies or adds inherited entries, shifts root phases and scales by known
integers; it does not run an uncontrolled repeated coefficient-squaring
process. Redundant arrays of length `M<=2D!` are legitimate intermediate
representations. Cyclotomic polynomial generation and regular
representation have polynomial bit cost in `M` and prior heights.
All these parameters fit `exp(exp(O(log^2 m)))`.

Regular representation is applied to the full identity, whose target
polynomial is dyadic. Its target becomes exactly `P I` on every new
coordinate. No zero-initialized auxiliary streams are assumed. Reducing
the descended identity modulo an odd prime is valid even if the prime
divides an internal cyclotomic order. The alternative auxiliary
power-of-two root used to supply shifted signs is also valid; the local
factor-list construction can instead scale one factor by the sign and
avoid that extension.

All shifts have equal rank, so multiplying the number of independent rows
preserves the exceptional fraction. The power-of-two Hermite nodes have
unit differences by the displayed geometric-sum identity. Explicit
Lagrange products give polynomial coefficient heights and generation in
the already expanded row dimension. This is a structured interpolation
bound, not a generic inference from a polynomial arithmetic-operation
count. The same replacement is made in both interchange and Fourier.

The norm estimate is conservative and sufficient: logarithmic row-sum
norms, number of finite instructions and logarithmic product gain are
fixed powers of the finite budget. Thus no extra exponential is needed
in the working precision. The independently reviewed source compiler
depends on that budget through fixed powers, so it applies with
`S_j<=E2(C Z_j^2)`, where `Z_j=(j+2)^3 log_2(j+3)`.

The refined rational address budget is `E2(O(Z_j))`, strictly inside
this bound. Literal radix search polynomial in its value, all monotone
pieces and binary padding remain within it. Aggregate setup clocks,
cell fences and preserved-input fallback still establish the all-length
space contract; finite-data generation is not free.

Finally `log S_j<=E1(CZ_j^2)`. Squaring `j+log S_j` for the specified
sum-diagonal pairing still gives `E1(C'Z_j^2)`, as do logarithms of
chunking constants and thresholds. Hence both the scheduling cost profile
`d_j` and threshold profile `b_j` have that single-exponential bound.
The advertised one-tower improvement follows at the complete physical
profile level.

## Stronger conditional MR transfer

MR bounds the actual generator, dense output, basis degree, numerator
bits and denominator exponents by `exp(poly(m))`, with one fixed
polynomial degree. That condition is substantially stronger than the
formula result. The proof properly retains the distinction.

The power-of-two order is at most twice its basis degree, so it is
controlled by the hypothesis. Adjoining the `2b` sign root and the
Hermite-node root takes their maximum order, preserving the
`exp(poly(m))` bound. All-shift replication, field/algebra basis descent,
table generation, numerical norms, address geometry, radix search,
physical compilation, chunking and the specified schedule stay within
`S_j<=E2(CZ_j)`.

The final conditional optimization is correct: for
`z=log_2(x+16)`, a small constant times
`(z/log_2(z+2))^(1/3)` makes `CZ_j<=z/2`. The resulting feasibility and
cost terms are at most `O(sqrt x)`, and the exponent loss is
`O(x(log_2(z+2)/z)^(1/3))`. The hypothesis is neither a field-existence
assertion nor a circuit with initialized workspace; it explicitly pays
for a full-occupancy affine matrix root and its uniform bit generator.

This review does not claim MR, endpoint time, a practical crossover,
formal verification, or execution of the astronomical templates.
