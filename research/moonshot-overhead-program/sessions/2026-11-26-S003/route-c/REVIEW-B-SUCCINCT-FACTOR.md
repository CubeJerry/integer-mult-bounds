# Independent review of the succinct scalar factor executor

Reviewer: S003 Route C, independent of Route B's construction. Status:
**accepted in its stated scalar-coefficient interface**. No complete
overhead theorem is accepted by this review.

Reviewed source: `../route-b/succinct-factor.md`, Theorem B1 and Sections
1--4; its complete Python checker; preceding
`routes/B/formula-full-rate-linearization.md`, Sections 1--4. Pins are
programme `0607d044d1d09489580da0e5828588820e1a6775` and OpenAI math
`3344da59991ed94f9ba711217b29c1d760badfa6`.

## Algebra checked independently

On input total grade `t`, use left grade `i` as the stored grade and infer
right grade `t-i mod d`. A left-child step increments stored grade `i`,
while a right-child step retains it; each changes the total grade to
`t+1`. Therefore the two factor branches really use phases `i` and
`t-i`, respectively. These phases depend on input grades, before output
increments. Nested additions merely add independent stored grade fields.

Multiplication concatenates factor lists; its phase chooses one child and
leaves the other's complete row module untouched. It does not multiply
two query expressions in one factor. Padding adds an identity terminal
token, and a scalar scaling node changes its weight only at phase zero.
Thus every terminal token contains at most one affine query leaf, with a
fixed set of grade increments and a computable input mask. The number of
tokens is linear in the explicit formula grammar including padding nodes.
This proves the stated affine masked-rotation sum without enumerating its
exponentially many rows.

Zero scalar nodes and unequal lengths cause no invertibility assumption.
The original full-rate cyclic product identity is preserved because these
are alternative descriptions of the exact same individual factors.

## Physical row scans checked independently

In lexicographic complete-row order, fixing all preceding grade coordinates
leaves a fibre consisting of `d` equal contiguous blocks. Later grade
coordinates and the complete data range are trailing block coordinates.
Moving the last block before the first `d-1` blocks implements the forward
cyclic increment. Two reusable temporary streams implement this by linear
scans and head returns per fibre; processing fibres sequentially visits a
fixed number of regions of total size `O(V)`.

The coefficient mask is evaluated before rotating the token stream. The
computation uses only the stored grade address (`O(S log D)` bits), the
formula and the prescribed phase. A long trailing data-range counter is
advanced amortized; the proof does not need to scan a `log V`-bit counter
for every record. Recomputing the formula path per record costs the stated
polynomial in descriptor parameters. One token at a time keeps workspace
independent of the number of tokens, and complete-region reuse bounds
cells ever visited.

The representation of a finite extension must include its explicit
degree-`h` defining polynomial and coordinate coefficients, as the theorem
states. Ordinary multiplication in these coordinates is polynomial in
`h`; no unit-cost arbitrary field oracle or variable tape count is used.

## Exact finite corroboration and limits

Route C's separately written `verify_packed_grade_rotations.py` compares
the actual complete-prefix block rotations against direct coordinate
permutations, for multiple nested grades, independent leading prefixes,
and positive trailing data lengths. It also checks commuting distinct
grade rotations and rejects the wrong mask order. Its result is
`packed-grade-rotation-verification.json`.

The constructor's algebraic checker was read in full. It independently
builds dense graded factors and masked factors as formal polynomials over
F4, and verifies whole-identity cyclic products. That finite algebra
coverage is useful but is not a full physical multiplier execution.
Route C also replayed the unmodified checker in an isolated temporary
directory: 52 cases, 234 factor columns, 107 cyclic products, and 51
wrong-mask-order controls passed. `independent-b-factor-replay.json`
records its exact source SHA-256. The separate packed-row checker passed
66 rotations involving 4,026 record positions and 162 commuting grade
pairs, and rejected its mask-order control.

The theorem acts on **scalar coefficient slices**. It does not authorize
executing each query separately, which would destroy shared routing. The
shared endpoint realization, full batch creation, spectral table generation,
rank/rectangle maps, numeric address magnitudes, and uniform composition
remain separate obligations. In particular the literal-incidence barrier
in this directory applies to the old billed implementation; it does not
rule out a new physically shared executor.

No Lean build, human review, full tape execution, or new complete `H(n)`
bound is claimed. This is an independent AI-assisted mathematical review.
