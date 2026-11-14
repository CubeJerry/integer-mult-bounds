## Result

Prove a linear generic ordinary Stein-rank lower bound for **every** vertex
ordering of an unshifted binary Gaussian tensor. For N=2^d and
H=⊗_i [[1,q_i],[q_i,1]], one proper real algebraic exceptional set suffices
so that every ordered forward matrix and every exact inverse has rank

`rank(A−ZAZᵀ) >= 2 ceil((N+3)/5)`.

Here Z is the ordinary nilpotent one-step shift. The good tuples are dense
and full-measure in `(0,1)^d`. This is a scoped universal theorem with exact
finite corroboration; **no new kappa** and no foundational-assumption discharge.

## What changes and why it matters

Earlier lexicographic rank results constrain the flattening order; earlier
orbit/symmetry results constrain the successor construction. This theorem
permits every simultaneous vertex order for the stated generic binary family.
It closes an arbitrary-order loophole for a linear rank floor without assuming
that the order follows a global symmetry.

The new proof uses XOR translation matchings. Their signed one-step
displacements consist of an even path and alternating cycles. Removing two
adjacent vertices per cycle leaves a principal minor with determinant ±1,
which is an isolated Gaussian polynomial coefficient. Two complementary
cycle counts imply the bound; a Schur-complement identity transfers it to
inverses. The coefficient proof works formally in every characteristic,
without claiming a good specialization exists over every finite field.

An exact sum of ordinary lower/upper triangular Toeplitz products needs at
least that many terms. Separately storing both full generator vectors per
term therefore takes Ω(N²) scalar slots. This is a dense-format count, not
a runtime or general multiplication lower bound.

## Reproduction and checks

```sh
python3 -I -W error -B research/arbitrary-order-binary-gaussian-rank/verify.py
python3 -I -O -W error -B research/arbitrary-order-binary-gaussian-rank/verify.py
python3 -B scripts/research_package.py --package research/arbitrary-order-binary-gaussian-rank
```

The primary standard-library replay checks all 5,047 translation-normalized
orders through d=3 and all 35,299 associated nonzero masks, exact unit minors,
characteristic-two ranks, 19 explicitly expanded polynomial coefficients,
four rational forward/inverse fixtures, two kernel vectors, three generator
identities and eleven domain/semantic controls. Exact d4/d5 witnesses show
that the stronger connected-mask criterion is not universal. Normal and
optimized receipts agree. The full theorem rests on PROOF.md.

Separate AI-agent review derives the mathematics independently and checks
full multivariate minors by a different subset-DP implementation, including
the displayed exceptional-order determinant factorization. The lead's
independent proof/rank checks are recorded separately. These are not
independent human or formal-kernel certification. Publication validation and
exact commands/receipts are preserved in the package.

## Limitations and open obligations

The full generic rank-N conjecture remains open for arbitrary d. At the
actual tuple `(1/2,1/3,1/5)`, two specified orders have rank 6 rather than 8;
distinct parameters alone do not prove full rank. Equal positive factors
can also fall below the new generic bound. Finite full-rank samples and
structural perfect matchings do not prove polynomial noncancellation.

No actual fine-prime sequence is proved generic. Such a discrete source
family may lie inside an exceptional variety. No rounded rank, conditioning
margin, free gauge, full physical caller, setup/access/restoration bill or
complete multiplication recurrence follows. Implicit/shared/sparse/tensor
or alternative-displacement algorithms remain outside the dense-format
obstruction. All five selected assumptions and the accepted #7000 frontier
remain unchanged. No selected cold replay, predecessor scientific suites,
Lean, Docker or hosted CI is claimed.

## Pins, novelty boundary and credit

Canonical base `e54523517d0f03e58352e647c403a5af3e525a57`, priority revision 8.
Only this scoped package is added. Exact canonical provenance pins,
predecessor commits and bounded overlap coverage are in SOURCES.json,
README.md and OVERLAP.md/OVERLAP.json.

Credit the prior CubeJerry lexicographic rank package
`326844a3e0c570fdafa4f3737095cd37154743a6`, orbit constructor
`8f1a09fb4f696bd5f20e1953210936308571416e`, optimal symmetry-cycle scale
`2ae2fa14eeefe301652f62313b137a97036ab13d`, heterogeneous symmetry theorem
`be76d6ae53fc887f977a04ceaa6ef56bb9e98fb7` and their preserved lineage.
CrocSwap/integer-mult-bounds#1754 concerns structured boundary applications;
CrocSwap/integer-mult-bounds#4198, CrocSwap/integer-mult-bounds#6228,
CrocSwap/integer-mult-bounds#6239 and CrocSwap/integer-mult-bounds#7263
concern rational generator preparation/normalization and rounded interfaces,
not this all-order rank theorem. Their scientific suites are not replayed.

Classical displacement generators, alternating matchings, Schur complements,
polynomial coefficients and zero-set facts retain their credit. See also
Olshevsky–Oseledets–Tyrtyshnikov, DOI 10.1016/j.laa.2005.03.040, for
multilevel tensor/displacement background. No worldwide priority claim.

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance.
The lead proposed the question and complementary matching/inverse ideas;
the worker derived the unit-minor and combined-count proof and wrote the
primary checker. Separate AI agents checked the critical proof and exact
computations. Apache-2.0.

## Executed independent review

`review/REVIEW.md` records a separate proof derivation and standalone symbolic/rational checker. Normal and optimized runs agree. Coverage includes 22 fully expanded small minors, 35,299 exhaustive translation graphs, 872 larger sampled graphs, 33 exact rational rank/minor checks, the full exceptional determinant identity and seven failure controls. This evidence corroborates the written all-d proof; it does not establish source-specific nonvanishing or a rounding margin.

```sh
python3.12 -I -W error -B research/arbitrary-order-binary-gaussian-rank/review/independent_check.py
python3.12 -I -O -W error -B research/arbitrary-order-binary-gaussian-rank/review/independent_check.py
```
