# Independent review: spectral rank and all-row affine programs

Reviewer: Route C, session beginning 2026-11-25 22:01:15 UTC.
Reviewed draft: `route-b-work/spectral-rank-barrier.md`, read in full on
2026-11-25. Status: **B1, B2, B3 and the stated rare-error consequence pass
this independent mathematical audit**, with the scope qualifications below.
This is an AI-assisted proof review, not human refereeing or formal kernel
certification. No new complete multiplication bound is established.

## 1. Why the quotient really supports matrix powers

Let

    A=K[x_1,...,x_m]/(x_1^r-1,...,x_m^r-1),
    D=chi I-P,  chi=product_i x_i,  Q=A^W/im(D).

The image of `D` is an `A`-submodule. The matrix `P` need not commute with
its individual coefficient matrices or be diagonalizable. What matters is
the exact identity `PD=DP`, since `chi` is scalar. Therefore `P` induces
an endomorphism of `Q`, and the relation `chi=P` can be iterated there.
This is the decisive step: replacing `chi^h v` by `P^h v` is valid even
for arbitrary nonsymmetric matrices and varying frequency eigenspaces.

For every reduced exponent vector alpha and every `h=0,...,r-1`,

    x^alpha e_j = x^(alpha-h1 mod r) P^h e_j  in Q.

Support degree is subadditive under multiplication and reduction. Averaging
the displayed representative degrees over `h` gives

    (r-1)m/r + (r-1)t/2.

At least one representative has integer degree no greater than the floor.
There is no recursive reduction termination argument to supply: each
monomial receives a representative in the claimed low-degree span in one
step. This directly bounds the dimension of `Q`.

The Chinese remainder decomposition is valid because `char(K)` does not
divide `r` and all roots lie in `K`. It converts the dimension of `Q` into
the sum of spectral nullities, not ranks. Taking the complement gives the
claimed rank **lower** bound. Its direction is correct.

## 2. Correct degree metric for the order-three source

An affine source pencil may contain both `q_i` and `q_i^2`. Its ordinary
degree is at most two, but its support degree is at most one. The latter
metric is preserved by the proof and gives, over `F4`,

    average rank(chi I-P)/W
      >= Pr[Bin(m,2/3)>floor(2m/3+t)].

Thus the support-degree formulation is a real strengthening of the safe
ordinary-degree substitution `d=2t`; it does not count `q_i^2` as a free
second degree-one ordinary monomial. Route B and this reviewer independently
identified this useful convention during the audit.

For `r=2`, support and ordinary degree agree. The separate injection proof
is also correct: on degrees at most `a=floor((m-t-1)/2)`, multiplication
by `chi` lands at degree at least `m-a`, while multiplication by `P` lands
at degree at most `a+t<m-a`. The two supports cannot cancel. If `a<0`,
the zero-dimensional subspace merely gives the trivial bound, as required.

The weight argument can be stated more generally. For any nonnegative
subadditive weight `w` on the cyclic exponent group with `w(0)=0`, define
the degree of a monomial as the sum of its coordinate weights. If every
entry of `P` has degree at most `d`, the quotient is spanned in degree at
most

    floor(m * mean_{a in Z/r} w(a) + (r-1)d/2).

The corresponding normalized dimension tail is the distribution of the
sum of `m` independent uniform weights. Ordinary and support degree are
the two instances used by B. This observation is an extension of the
same proof, not a separate global result.

## 3. Scalar-algebra extensions do not create a loophole

Suppose the source coefficients lie in a nonzero finite-dimensional
`F4`-algebra `E`, possibly with zero divisors. Expand multiplication and
all row operations in an `F4`-basis of `E`. A `W`-row predictor becomes a
`W dim_F4(E)` square matrix over `F4`; its entry support degrees do not
increase. The target phase lies in the base field, so it becomes
`chi I` on every expanded coordinate. The theorem applies to this actual
base-field rank.

One must not use an undefined rank over a non-domain coefficient algebra.
For coordinate-error estimates, at most `b` erroneous `E`-rows implies
base-field rank defect at most `b dim_F4(E)`, so normalization preserves
the bound. General rank defects after basis expansion are directly covered.
There is no requirement that all good eigenspaces have a common basis.

For a target `chi C` with a query-independent invertible matrix `C`, replace
`P` by `C^-1 P`; rank and support degree are unchanged. Constant endpoint
row maps therefore do not evade the obstruction. A map mixing the common
query eigenspaces is a different interface and remains outside its scope.

## 4. Interacting repair gates and actual path degree

The telescoping proof of B2 is valid for rectangular input/output maps and
arbitrary finite workspace: embed the computation in one fixed state space
using constant injections, zeroing, projections and copies. Replacing one
table gate changes the final transfer by `L Delta R`, whose rank is at
most `rank Delta`, even when the other gates still contain spectral tables.
Adding all changes gives the total width bound without requiring the
corrections to be independent or their row spaces to be disjoint.

The polynomial degree must be that of the **entire table-free program**.
In particular, a Hermite path with output `g(P)` has degree up to
`deg(g) deg(P)`; counting just the initial predictor would be incorrect.
Repeated predictor uses in a contraction tree must be included on paths,
and every replaced table occurrence must appear in the width sum. The
draft explicitly includes this qualification.

No conversion from a table width or polynomial degree to tape time follows
without a physical implementation contract. The theorem does not preclude
nonlinear control, nonlinear decoding, or transformations which break the
common spectral decomposition. It also gives no universal lower bound on
the numerical overhead `H(n)`.

## 5. Rare-error constant and numerical interpretation

For fixed `r` and `t=c sqrt(m ln m)`, the displacement in B1 is
`(r-1)t/2`, and the binomial variance is `m(r-1)/r^2`. The moderate-tail
logarithmic exponent is consequently

    r^2(r-1)c^2/8.

The draft's constants are correct: a rank-error budget `m^-a` forces the
liminf stage coefficient at least `sqrt(2a)` for binary queries and
`2 sqrt(a)/3` for ternary queries. The latter uses the proper support
metric. Natural logarithms in this display are essential to those numeric
constants. The bounded-integer rounding changes only lower-order terms.

The lower-tail derivation requires summing a window of
`Theta(sqrt(m/ln m))` masses; a single mass would introduce an erroneous
extra `m^-1/2` factor. The draft includes the needed window and supplies
the resulting matching exponent. It asserts no sharpness theorem for the
ternary case.

The complex norm proof in B3 is independently sound: orthogonality to
the missing full-support character gives squared Frobenius error at least
`W`; the operator norm bound then follows. This proof is over the complex
numbers, not an attempted norm argument over `F4`.

The permutation witness is stronger than a norm heuristic for rounding.
A unit impulse has a required output coefficient at the translation by
`(1,...,1)`. Every support-degree-`<m` monomial misses that coefficient.
The approximated value is exactly zero there, even with exact coefficient
arithmetic, and coordinatewise rounding cannot turn it into one. This is
a claim about that intermediate arbitrary-input transform, not a claim
that all multiplication algorithms must expose such an intermediate.

## 6. Prior-art cross-check and limits of novelty

Before seeing B's rank argument, this reviewer independently derived a
weaker coordinate-error transfer to probabilistic MOD3 polynomials.
Uniform ternary shifts send each Boolean input to a uniformly distributed
spectral tuple. Normalizing the phase and taking

    1 + omega^(-i) p + omega^(-2i) p^2

produces the indicator for `sum x_j=i mod 3` wherever `p` predicts the
phase correctly. In characteristic two, Boolean multilinearization of
the square preserves degree. Smolensky's lower bound then gives the same
square-root-log rare-error scale for coordinate-sparse predictors.

The exact supporting primary statements read are Definition 1 and Lemma 9
of Srinivasan--Tripathi--Venkitesh, *On the Probabilistic Degrees of
Symmetric Boolean Functions*, FSTTCS 2019,
<https://doi.org/10.4230/LIPIcs.FSTTCS.2019.28>, and Lemma 4.8 of
Srikanth Srinivasan, *A Robust Version of Hegedus's Lemma, with
Applications*, TheoretiCS 2 (2023), Article 5,
<https://doi.org/10.46298/theoretics.23.5>.
The latter states the lower bound for error between `2^-m` and `1/(3b)`,
with characteristic coprime to the modulus `b`. Only the cited definitions,
theorem statements, and immediate context were read; the full source
proof of Smolensky's theorem was not independently reconstructed.

B's self-contained quotient proof is stronger in scope: rank-one error
can corrupt every diagonal entry, so a coordinate-sparse theorem cannot
be substituted for it. For example the all-one `W`-by-`W` error matrix
has rank one and all `W` diagonal entries nonzero. The matrix rank theorem
therefore closes a genuine scope gap in the programme's earlier argument.
An exhaustive literature-priority comparison with matrix-valued variants
remains open; no priority claim is warranted.

## 7. Independent exact checks

Command:

```sh
python3 verify_spectral_rank.py
```

The checker passed 83,652 support-shift representative checks, 157,464
ordinary-degree representative checks, 44 exact Hilbert-tail identities,
68 arbitrary matrix predictors with 18,372 exact spectral rank evaluations,
and 32 independent regular-representation/CRT rank equalities. It uses
its own `F4` arithmetic and exact Gaussian elimination. The polynomial
matrices include nonsymmetric and nondiagonal coefficients; they are not
restricted to the source count formulas.

Essential negative controls reject dropping semisimplicity, replacing
rank error by coordinate error, changing the full-product target to an
arbitrary constant target, or treating a non-affine full-product query as
one affine stage. The JSON output binds the checker source hash. These
finite tests corroborate the algebraic identities and error scopes; they
do not prove the asymptotic theorem by enumeration or execute a tape
implementation.

Credits: Route B's quotient/rank and repair-network proof; the independently
identified support-degree convention; the source OpenAI construction and
classical polynomial-method literature; @CubeJerry; substantial ChatGPT
research and verification assistance.
