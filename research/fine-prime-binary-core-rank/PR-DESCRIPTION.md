## Result

Remove the generic-exception premise from the preceding arbitrary-order
binary Gaussian rank theorem at the retained exact narrow-core widths.
For distinct odd primes s_i, dyadic targets t_i, common positive integer
alpha, N=2^g and

`q_i=exp(−pi alpha² t_i/s_i), H=⊗_i [[1,q_i],[q_i,1]]`,

every vertex ordering of H and its exact inverse has ordinary nilpotent
Stein rank at least `min(2 ceil((N+3)/5), min_i s_i−1)`.
This is pointwise for every declared tuple, with an explicit prime-degree
cap. No gcd(alpha,s_i)=1 condition is needed. **No new kappa; all five
selected assumptions remain.**

## Change and relevance

The predecessor leaves prescribed source-parameter nonvanishing open.
Even-path trimming supplies smaller principal minors whose individual degrees
are below the source primes. With S=product_i s_i, the common base
z=exp(−pi alpha²/S) is transcendental by Gelfond-Schneider. CRT separates
guarded monomials under Q_i=z^(t_i S/s_i), preserving each nonzero minor.
Each order is treated separately; multiplying all N! minors would lose the
degree guard. A Schur-complement/reversal identity transfers the result to
exact inverses.

The source notes supply the distinct odd primes, dyadic targets, legal
integer alpha and narrow width gamma_i=pi alpha² t_i/s_i. The theorem is
for the unshifted normalized two-point core identified from those factors.
The full linear floor holds when N<min s_i. For larger source groups with
beta>1−epsilon, the cap gives exp(Theta(p^(1−epsilon))), not a linear-in-N
floor. The defined dense ordinary generator format needs at least 2Nr
scalar slots, without a general runtime conclusion.

## Reproduction and checks

```sh
python3 -I -W error -B research/fine-prime-binary-core-rank/verify.py
python3 -I -O -W error -B research/fine-prime-binary-core-rank/verify.py
python3 -B scripts/research_package.py --package research/fine-prime-binary-core-rank
```

The standard-library commands are read-only; normal/optimized receipts agree.
They authenticate three inputs, enumerate 13,689 complete exponent-box
vectors, check 219 trimmed unit minors on 44 bounded orders, expand and
specialize 12 Gaussian minors with 184 terms, verify 48 exact source-exponent
identities and execute 13 semantic/domain controls. Expected marker:
`PASS_FINE_PRIME_BINARY_CORE_RANK`. No floating exponential or numerical
transcendence oracle is used.

Controls include degree-threshold collisions, noncoprime denominators 9/27,
nonunit numerators, an allowed prime-divisible alpha, zero-alpha rejection,
algebraic-root failure, invalid trimming, compression before shifting,
diagonal-similarity rank change and coarse rounding. The universal proof
is written; finite checks corroborate it. Separate AI proof/source and exact
computation reviews are preserved, not claimed as human or kernel acceptance.

## Limits and next obligations

The actual shifted kernel and chirp need diagonal similarities, which do
not preserve ordinary Stein rank. An exact control changes rank 2 to 4;
no physical transfer is inferred. A two-point section also does not
automatically control a larger matrix's ordinary displacement rank.

Transcendence gives no useful magnitude or Cp-bit stability margin here.
Coefficient production, rounding, periodic/cross-cell entries, identity holes,
rectangular interfaces, source access, gauge application, transport,
restoration, children and a complete invoice remain outside the result.
Implicit/shared/sparse/tensor and other displacement representations stay
open. No full-rank theorem, physical service, selected-frontier change or
multiplication improvement is claimed. No selected cold replay, predecessor
scientific suites, Lean, Docker or hosted CI is asserted.

## Pins and credit

Canonical base `e54523517d0f03e58352e647c403a5af3e525a57`, priority revision 8.
Only this package is added. SOURCES.json and DEPENDENCIES.json pin canonical
provenance, both retained source notes and the predecessor proof at
CubeJerry commit `085b30f8e036f69421d5953d0993ac4974ec3f24`; its remote bytes
were compared with the retained copy.

Credit Chafik Boukhalfa / CrocSwap/integer-mult-bounds#1786, Vlado Vojdanovski /
CrocSwap/integer-mult-bounds#1673, IdeaOuter as credited in
CrocSwap/integer-mult-bounds#1758, Jeremy Kothe and the preserved source
lineage. Original notices are unchanged. Gelfond-Schneider, CRT, path
determinants and Schur complements are classical. The original Gelfond
1934 logarithm theorem, p. 628, was read. Exact overlap heads and coverage
limits are recorded; no worldwide novelty claim is made.

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance.
The lead proposed the specialization; the worker derived trimming/source
boundaries and removed the unnecessary common-alpha coprimality guard;
separate AI agents checked the proof and computations. Apache-2.0.

## Executed independent review

`review/REVIEW.md` records a separate derivation and exact checker with no author imports:53 symbolic minors/1409 terms,119 even trims,730 exponent-box values and11 controls. It checks the classical source citation, exact source bytes and both genuine diagonal-similarity counterexamples. Normal/optimized receipts agree. Run `python3 -I -W error -B research/fine-prime-binary-core-rank/review/independent_check.py --package research/fine-prime-binary-core-rank`, also with `-O`; both are registered in VERIFY.json. No physical or finite-precision rank transfer is inferred.
