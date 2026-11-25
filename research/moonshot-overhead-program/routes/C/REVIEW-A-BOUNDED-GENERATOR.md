# Independent review of the bounded original-source generator

Reviewer: Route C, 2026-11-25. Status: **finite algebra and generator-growth
audit passed; physical compiler remains a separate review**. One batching
convention should be explicit. No complete multiplication theorem is
certified by this note alone.

Reviewed Route A versions:

| File | SHA-256 |
|---|---|
| `scalar-template-growth.md` | `c780dee7c7df136589a279f7fbcdf676426e0b0b8623ec684be7b08f243256cf` |
| `bounded-source-generator.md` | `9093636dfc5c2446bb0e087ab035bd9a5b85434a4c425cfebaab7d729b0d299b` |
| `interchange-label-growth.md` | `1424bbe49b55516c2d00a3e9b69c1601e6c04d74255bf5aeb6d64965d5cd456a` |

I compared the claims directly with pinned OpenAI `math`
`3344da59991ed94f9ba711217b29c1d760badfa6`: Fourier `repair.tex`,
`kernel.tex`, `binary.tex`, and tape `interchange.tex`.

## 1. Generic matrix root and full-rate descent

Each binary count-generating factor is `1+I_j T`, with I_j affine in q_j.
The predictor is multilinear and has at most 2^m collected monomials.
For sufficiently large m its degree D is at most m. Negative binomial
coefficients from `(1+T)^(-u)` are integers. Expanding at most D+1 Newton
terms and the affine indicators gives dyadic coefficient bit heights
O(m^2), a conservative bound.

The source matrix root uses one b-dimensional tensor factor per monomial,
where b is the least power of two at least max(2,D). A coefficient goes
in one affine factor of its monomial: no root of that coefficient is
extracted. Thus `d0=b^h`, `h<=2^m`, `b<=2m`, and

    log2 d0 <= 2^m log2(2m) <= 2^(2m).

All shifts give `R=2^m d0`, a power of two. A primitive R-th root eta
supplies both the b-th root and R check nodes. Its extension degree over
Z[1/2] is exactly R/2, so descent gives at most R^2 independent base rows.
The per-input call ratio is unchanged. The ring identity specializes to
every odd characteristic, including primes much smaller than D.

This does not contradict the count-residue obstruction: integral divided
powers retain more than the count modulo the data prime.

## 2. Cyclotomic inverse heights and actual table generation

For rho of order 2^a,

    product_(v odd mod 2^a) (1-rho^v) = 2.

Removing v=1 gives an explicit inverse numerator with denominator 2 and
at most R/2-1 factors. Reduction by `eta^(R/2)=-1` does not increase
coefficient l1 norm, so the numerator bit lengths are O(R). This works
even when reduction modulo an odd prime is a split algebra rather than
a field: unit differences are sufficient.

For j selected nodes, each Lagrange polynomial uses j-1 numerator factors
and j-1 inverse differences. Its numerator coefficient bit lengths are
O(jR), and its dyadic denominator exponent is O(j). Using the first j
check rows gives a left inverse; padding and transposition give the right
inverse needed by Hermite repair. A bounded number of matrix products
and sums over at most R terms preserve the O(R^2+m^2) height envelope.

The predictor's evaluated integer values outside the window have O(m^2)
bits. The binary Hermite factor `-(p_i+2z)/2` does not divide by a predictor
error or introduce a forbidden small-characteristic denominator.

Listing all 2^m spectral patterns, dense row matrices, and all R/2 basis
coordinates costs a fixed power of R. The tensor root has at most h<=R
summands. Dense listing and schoolbook polynomial/integer arithmetic
therefore give an actual polynomial-in-R constructor. This is not a
runtime claim inferred from output size alone.

## 3. Explicit finite controls

`verify_scalar_generator_review.py` passed on Python 3.12.14 and saved
`scalar-generator-review-verification.json`:

* 120 exact integer cyclotomic inverse products, orders through 64;
* 480 reductions over F_3,F_5,F_7,F_17;
* 184 Lagrange/Vandermonde inverse entries in split and nonsplit algebras;
* 48 specialized tensor matrix-root identities at b=2,4;
* 257 conservative target-parameter and local-call invoices.

These are finite algebra and logarithmic-invoice controls. They are not
executed enormous source templates or tests of a physical tape compiler.

## 4. The sixth-power search bound has ample explicit slack

Write J=j+2. Choose `100J<p<=200J` prime and even `L=100J`.
For `m=2^u+1`, the binary repair uses at most
`40 sqrt(m(u+2))` pencils when u is sufficiently large. A general address
change on d fields costs at most d-1 recursive swaps in the source.
Rectangle preparation and low-rank deliveries give a safe per-pencil
bound `64 D(1+lambda)` once `m rank(P_*)/N<=1`. This generous constant
already includes the bounded rank factor. R is absent from this averaged
call coefficient; its pointwise work is paid separately.

With h=2p-1 and t=log2 q, convenient integer logarithmic upper bounds are

    log2 Cr <= (p+1)(1+(p-1) ceil(log2 h)),
    t <= ceil((u+1+log2 Cr)/p^2),
    log2[D(1+lambda)]
      <= 2+ceil(log2 h)+(3p-1)t+(p+1)h
                         +p(p-1)ceil(log2(max(1,t))).

For Fourier there are at most `2^L q^(L/2)` charged rectangles and at
most `2(2+t)^L` incidences per label on either side. Together with
`D<=1+Lq`, the safe per-pencil invoice is `16D(2+t)^L` when
`q^(L/2)>=m`.

A deliberately excessive explicit stopping point is the least power of
two u at least `2^30 J^6`. To check it uniformly, use p<=200J, h<=400J,
`ceil(log2 h)<=9+J`, and `log2 u<=31+6 log2 J<=31+6J`.
The interchange log cost beyond sqrt(m), including the fixed split,
repair and reserve factors, is bounded by

    0.06 u/J + 10^7 J^3.

The available exponent gap is u/(2J). Because `u>=2^30 J^6` and J>=2,
that gap absorbs the displayed bound and a factor-two margin. Fourier's
corresponding extra log cost is at most `0.02 u/J+10^5 J^2`, smaller
still. Thus the first successful doubling-search value satisfies
`u<=2^31 J^6`, without emitting the enormous scalar tables in failed
trials. The finite verifier checks the displayed conservative invoices
at 257 indices; the preceding inequalities are the all-index argument.

## 5. Make the Fourier batching convention explicit

The reviewed acceptance test is `sigma/W<=A^rho/2`. The generic source
padding bound is `(sigma/W)(1+W/2^r)`. Applying that bound unchanged gives
a strict saving, but not automatically a half margin. Either of the
following resolves the bookkeeping:

1. Here W is a power of two: root blocks, all-shift multiplicity, scalar
   descent and q^L labels are all powers of two. At least log2 W inactive
   bits provide exact complete batches, with padding factor one.
2. Accept only `sigma/W<=A^rho/4` and use padding factor at most two.

Both choices preserve all growth bounds. The interchange test already
charges its factor-two digit split and its occupied reserve descents.

## 6. Rational addresses and G4/G5

At the successful parameters, interchange has N<=m^5 labels and Fourier
has at most m^3. Directed rectangles number at most the ordered label
pairs. Gram entries have polynomial-m bit heights. Determinant-minor
formulas or fraction-free elimination give quotient bases, complements,
dual bases and triangular factorizations in polynomial dimension. A
bounded chain of these derived matrices keeps rational bit lengths
polynomial in m. Their numeric magnitudes can be exponential in a
polynomial in m and must be included in the finite-data envelope.

These magnitudes, the scalar program, and dense F_p low-rank factorizations
fit a fixed power of `Rhat(m)=2^(2^(m^C0))` for a sufficiently large
absolute C0. A radix prime above every required nonzero numerator,
denominator and batch width makes the specified rational units compatible.
Trial division up to twice this maximum costs polynomial time in Rhat.
The failed doubling trials are also covered; there are O(log J) of them.

The Fourier rectangle weights are dyadic by the source's valuation
argument. Integer products, gcd cancellation and the triangular basis
conversion generate them with polynomial finite-data cost. The optional
sqrt(2) for odd-width normalized calls is a fixed degree-two extension,
handled separately by the numerical compiler.

The finite algebra and G3--G5 growth extraction pass this review. G6, the
uniform physical compiler with digit-time, visited-space and threshold
bounds, is separate. Conditional on G6, the exponential inversion has
the advertised order: `log prefactor, log L(threshold)<=2^(2^(O(J^6)))`
permits j a small constant multiple of `(log2 log2 s)^(1/6)`. This is a
conditional statement here, not independent certification of the complete
integer multiplication theorem.

## 7. Follow-up review: concrete address chain and resolved margin

At 14:32 UTC I checked the revised generator (SHA-256
`3955cb00811a2830cdf9acb27d9485738ace68fdb1f283a1e96d3679cb17a225`)
and `rational-address-and-generator-bounds.md` (SHA-256
`344f168d38361d770e7654c2ef246ed7be58181ce1ebbcf053e19770251cd0e4`).
The revised generator requires the robust pre-padding quarter margin;
Section 5's bookkeeping point is resolved.

The explicit rational dependency chain is valid. Independent columns of a
symmetric Gram matrix represent a basis of its nondegenerate quotient, so
their principal Gram submatrix is nonsingular. The listed complements,
rectangle difference spans and lifted bases therefore have the asserted
dimensions. Determinant-ratio height bounds apply to the selected-basis
solves. In the ordered triangular factorization, each pivot inverse and
elementary inverse is included in the retained unit list; multiplying the
polynomially many factors has polynomial height. The chain is bounded
independently of m and the target exponent. With matrix size <=4m^6, fewer
than one hundred applications of the stated K^10 height bound fit
m^10000 after an absolute starting cutoff. This verifies AG1.

The constructor and optional certificate loops in AG3 are explicit and
fit a fixed power of `2^(2^(m^100000))`. In particular formal degree-b
matrix verification has at most `(m+b+1)^b` monomials, whose logarithm is
O(m log m), far below log R. Fixed scalar-algebra coordinates are encoded
once and reused at every interchange recursion depth. No R-per-level
alphabet expansion is needed. AG2 and AG3 pass this review.

I also checked that the physical ledger's revised PC3 has exponent
`1001+ceil(log2 P)`, allowing the extra factor for root pieces on top of
the degree-1000 local setup envelope. This is a consistency check of that
revision; the complete physical-compiler audit remains the lead's review.

Final Route C gate: **finite scalar, rational-address, actual generator,
and G3--G5 bounds approved for the specified original-source constructor**.
The pre-padding margin issue is resolved. Promotion of the global bound
still depends on the separate physical compiler and common-cap assembly
reviews; this note supplies no assertion beyond its own gate.
