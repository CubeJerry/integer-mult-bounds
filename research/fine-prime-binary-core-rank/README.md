# Pointwise rank bounds for the exact fine-prime Gaussian core

**Scoped exact theorem; no new kappa.** The preceding arbitrary-order binary
Gaussian theorem left an algebraic exceptional set. This package removes
that exception at the retained narrow-core widths, up to an explicit prime
degree cap.

Let g>=1, N=2^g, let s_i be distinct odd primes, t_i positive powers of two,
and alpha a common positive integer. For

\[
q_i=\exp(-\pi\alpha^2t_i/s_i),\qquad
H=\bigotimes_i\begin{pmatrix}1&q_i\\q_i&1\end{pmatrix},
\]

every vertex ordering of H and its exact inverse has ordinary nilpotent
Stein rank at least

\[
\min\!\left\{2\left\lceil\frac{N+3}{5}\right\rceil,\ \min_i s_i-1\right\}.
\]

This is pointwise for every tuple in the declared family. No coprimality
between the common alpha and the source primes is needed. The theorem
concerns the exact **unshifted normalized two-point narrow core**; it gives
no automatic rank or precision transfer to the shifted, chirped, periodic,
rounded or larger physical matrix.

## Argument and source boundary

An even-path trimming lemma retains smaller principal Gaussian minors with
an isolated ±1 coefficient. Their individual variable degrees stay below
the source primes. Put S=product_i s_i and z=exp(−pi alpha²/S), so
q_i=z^(t_i S/s_i). CRT makes the guarded monomials have distinct integer
exponents in z. Gelfond-Schneider makes z transcendental, so the specialized
minor cannot vanish. Each order's minor is treated separately; multiplying
all N! minors first would lose the degree guard. A Schur-complement/reversal
identity gives the inverse result. [PROOF.md](PROOF.md) is the complete proof.

The retained FINE-PRIME note chooses distinct odd primes, dyadic targets and
`alpha=ceil(sqrt((4/pi) log(16p)))`. GAUGEFREE identifies narrow width
`gamma_i=pi alpha² t_i/s_i`. Exact diagonal similarities remove its linear
shift and chirp to identify the displayed core. Those similarities are not
free and do not preserve ordinary Stein rank in general; an exact control
changes rank 2 to 4 under a diagonal similarity.

The source prime scale is `log s_min=Theta(p^(1−epsilon))`. Groups satisfying
`2^g<s_min` receive the full linear predecessor floor. For
`g=Theta(p^beta)` with `beta>1−epsilon`, the bound saturates at
`exp(Theta(p^(1−epsilon)))`, superpolynomial in p but not linear in 2^g.
An exact ordinary lower/upper Toeplitz generator expression needs at least
that many terms. Separately storing its two full vectors per term takes
at least 2Nr scalar slots. This is a specified dense-format count, not a
runtime or multiplication lower bound.

Exact nonvanishing supplies no useful magnitude lower bound here. No Cp-bit
margin, coefficient-production theorem, shifted/physical rank transfer,
full caller or complete recurrence is provided. A two-point section also
does not automatically control the ordinary Stein rank of a larger matrix:
deleting vertices changes the shift. All five assumptions and selected
#7000 remain unchanged.

## Reproduction and evidence

With Python 3.12 and its standard library, from the repository root:

```sh
python3 -I -W error -B research/fine-prime-binary-core-rank/verify.py
python3 -I -O -W error -B research/fine-prime-binary-core-rank/verify.py
python3 -B scripts/research_package.py --package research/fine-prime-binary-core-rank
```

The direct commands are read-only and print JSON status
`PASS_FINE_PRIME_BINARY_CORE_RANK`. [RESULT.json](RESULT.json) retains the
identical normal/optimized primary output. Gelfond-Schneider is a cited
mathematical input, not a numerical transcendence oracle.

The replay authenticates three retained inputs; enumerates 13,689 complete
guarded exponent-box vectors; checks 219 trimmed unit minors on 44 bounded
orders; explicitly expands and specializes 12 Gaussian minors with 184
nonzero terms; checks 48 exact narrow source-exponent identities; and runs
13 semantic/domain controls. No floating exponential is used. The source
identity fixtures preserve same-cell offsets on declared small fine-prime
intervals; they are not a complete production caller or prime-existence
replay. Finite checks corroborate the written proof.

Controls cover threshold-degree collisions, distinct noncoprime denominators
9 and 27, nonunit numerators, an allowed alpha divisible by a source prime,
zero-alpha rejection, algebraic-root failure, invalid trimming, compression
before shifting, diagonal-similarity rank change and coarse rounding.
Separate review records independent mathematics and exact computations;
no human or formal-kernel acceptance is claimed.

## Pins and credit

Canonical base `e54523517d0f03e58352e647c403a5af3e525a57`, priority revision 8.
[SOURCES.json](SOURCES.json) authenticates canonical provenance;
[DEPENDENCIES.json](DEPENDENCIES.json) pins the retained inputs. The immediate
predecessor is the published
[arbitrary-order generic rank theorem](https://github.com/CubeJerry/integer-mult-bounds/commit/085b30f8e036f69421d5953d0993ac4974ec3f24).
Its proof is retained byte-for-byte and its remote bytes were checked.

Credit Chafik Boukhalfa's [fine-prime work](https://github.com/CrocSwap/integer-mult-bounds/pull/1786),
Vlado Vojdanovski's [phase-cell construction](https://github.com/CrocSwap/integer-mult-bounds/pull/1673),
IdeaOuter's fractional-shift work credited in
[#1758](https://github.com/CrocSwap/integer-mult-bounds/pull/1758),
Jeremy Kothe and the preserved package/source lineage. Original source
notices remain unchanged. Gelfond and Schneider's theorem is an explicit
classical input; the [original Gelfond paper](https://www.mathnet.ru/eng/im4924),
theorem p. 628, was read. CRT, path determinants and Schur complements are
classical. [OVERLAP.md](OVERLAP.md) records a bounded check without a
worldwide priority claim.

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance.
The lead proposed the specialization; the worker removed the unnecessary
alpha coprimality guard and derived the trimming/source proof and checks.
Separate AI review assessed the critical obligations. Apache-2.0. No
selected cold replay, predecessor scientific suites, Lean, Docker or hosted
CI is claimed.

## Open next questions

1. Can a source-specific quantitative minor or singular-value margin justify
   Cp-bit rounded rank? Exact transcendence alone does not provide it.
2. Can the actual shifted/chirped/rounded matrix satisfy a comparable bound
   directly? Diagonal similarity is insufficient and has physical costs.
3. Can noncancellation beyond the CRT box remove the s_min−1 cap? High-degree
   relations among the source parameters already exist.

## Executed independent review

`review/REVIEW.md` records a separate derivation and exact checker with no author imports:53 symbolic minors/1409 terms,119 even trims,730 exponent-box values and11 controls. It checks the classical source citation, exact source bytes and both genuine diagonal-similarity counterexamples. Normal/optimized receipts agree. Run `python3 -I -W error -B research/fine-prime-binary-core-rank/review/independent_check.py --package research/fine-prime-binary-core-rank`, also with `-O`; both are registered in VERIFY.json. No physical or finite-precision rank transfer is inferred.
