# S004 first-wave admission and portfolio decision

Prepared during the active three-hour session on 26 November 2026 Melbourne.
This checkpoint does not assert that the requested duration has elapsed.

## Complete multiplication claim

No new unconditional complete overhead bound is admitted from S004 at this
checkpoint. The shared programme now has the stronger S003/E002 written bound

    T(n)=O(n sqrt(L) 2^{O(s^(3/4)(log2(s+2))^(1/4))}),
    L=1+log2 n, s=log2 L, visited cells=O(n).

Those concurrent proofs and their attribution are preserved. The lead read
S003's complete polynomial-profile extraction, explicit dyadic geometry and
compact interchanger. This is a fresh critical-chain audit, not a claim to
have rerun every supplier or independently implemented the multiplier.
Remote E003 checkpoint `df91e4c8e31b1020e05056db5b0eb16169ef3421` was
fast-forwarded before integration; its new two-scale candidate is not
silently promoted to a theorem here.

## Admitted components and scoped obstruction

### A. Radix wrapper without whole-square padding

The corrected wrapper in `../route-a/no-padding-radix-wrapper.md` is admitted
under its explicit equal-radix processor contract. It converts arbitrary
field sizes using retained radix intervals, a small residual tail, and
sequential rectangular extraction/merge. Its total time is

    C V [F_b(floor(log_b M)) + b^2 Q^2 + 1] + preprocessing,

and its proportional space is `C(1+S_b)V`, with the stated additive setup
and maxima over actual call sizes. It does not introduce a whole-volume
factor `b^2` into space or prove an absolute bound for the supplier's `S_b`.

Lead review caught the need for real field moves around an arbitrary gap
and maximization of the additive oracle bound over actual local volumes.
C found and corrected a genuine bit-order error: move Y bits forward
before X, then X bits in reverse order after the gap. The accepted proof
hash is recorded in C's review. Lead read that final review, the corrections
and the independent named-bit checker, and replayed both exact checkers.

### B. Spectral matrix rank and repair-free rounding

Theorems B1--B3 and their rare-rank-error consequence are admitted in the
stated common-spectrum linear model. They cover arbitrary matrix
coefficients, independent row payload, initialized workspace and interacting
rank-charged tables. They do not lower-bound general tape multiplication.
The proof uses a quotient module and the classical degree-filtration
method; no priority claim is made.

The lead read the full proof and C's review, checked the cyclic-shift
filtration and moderate-tail summation, and replayed C's independent
finite checker. The newly added B4 is separately lead accepted: at each
ordinary output the missing target input bit remains independent after
conditioning on every other bit. Thus every fixed coordinatewise decoder
has expected error at least one half there; summing expectations gives a
binary input with at least half the ordinary outputs wrong. C's earlier
B1--B3 review should not be represented as a review of that later addition.

### B. Deterministic sparse ordinary-residual correction

The component theorem R1 in `../route-b/deterministic-sparse-residual-repair.md`
is admitted after lead full-proof audit, A's independent physical review
and C's independent complete review. The theorem assumes a proved bound s
on the number of wrong ordinary convolution coefficients. Positions are
unknown.

For its explicit packed volume V and short modulus size k, the corrector
costs `O_alpha(V(1+log2(k+1))^alpha+k^6)` with one common `O(V)` visited cap.
The proof charges Euler-weighted stream formation, long reductions using
short multiplications, signed balanced-radix decoding, all candidate trials,
and a schoolbook fallback when k exceeds V. The product of cyclic moduli
is used only through divisibility, with no coprimality premise.

Under logarithmic digit packing, polylogarithmically many wrong coefficients
can be repaired in `O(n(1+log log n)^(3/4))`, below `n sqrt(log n)`.
This does not provide a fast candidate with sparse residual. The explicit
squared product of cyclic factors defeats a general-verifier interpretation
when the sparsity promise is false. The derivative ratio is established
sparse-interpolation mathematics and is attributed accordingly.

## Exact evidence

Lead copied checkers into isolated scratch replay directories before
running them. Hashes and outputs are preserved in `replays/manifest.json`
and the associated JSON receipts. These are exact finite combinatorial and
algebraic checks, not empirical proofs of asymptotic complexity.

| Check | Observed result |
|---|---|
| Radix wrapper | 65,008 profiles; 230 rectangular decompositions; 1,790 complete finite permutations over 8,705,970 symbols; 54 omitted-correction controls |
| Named bit moves | 1,089 layouts, including empty fields; 1,085 reversed-order controls |
| Spectral rank | 83,652 support shifts; 157,464 ordinary-degree shifts; 44 Hilbert tails; 68 matrix predictors; 18,372 spectral rank evaluations; 32 regular/CRT identities |
| Sparse correction | 33 complete recoveries; 3,618 signed value/derivative folds; 465 long Barrett reductions over 2,811 blocks; collision, false-certificate and rounding controls |

## Conditional geometry and reassessment

The lead's JR hypothesis concerns exact disjoint rectangle partitions with
small local load. The cover/partition distinction is essential. An exact
q=4,k=2 certificate improves a product-partition constant but retains the
dominant logarithm; further tuning of that family is deprioritized.

A independently accepted both the original expanded-profile conditional
transfer and the new Section 9 compact-profile transfer. The old bound is
now weaker than the concurrent unconditional result. The compact theorem
is admitted conditionally:

    JR => H(n)<=2^{O(s(n)^(3/4))}, with one fixed O(n) visited cap.

JR itself is open. The transfer uses outer-product geometry with arbitrary
disjoint inner sides; exhaustive partition generation has exponential
time but polynomial workspace and retained certificate. Adding n>=g_J to
the analytical threshold absorbs that one-time generation without making
the polynomial execution coefficient exponential. Root read A's full
updated review and rechecked those interfaces. No conditional formula is
inserted into the unconditional programme claim.

The repair-free approximation route failed a decisive exact witness and
has pivoted to sparse ordinary correction. The affine factorization route
moved beyond a duplicate determinant argument to an active-query-volume
commutator theorem with inverse gates, now awaiting independent review.
The adaptive source route remains active but is coordinated against the
concurrent S003/E003 work. These are distinct mechanisms; stronger global
rates remain unadmitted until their actual physical suppliers close.

## Limits and credit

Source audit is staged. The lead read the complete pinned interchange and
Walsh source sections, selected-result and repository guidance, and named
critical suppliers. No exhaustive archive or live Discussion audit, full
multiplier execution, Lean refinement, numerical crossover or human
refereeing is claimed. Credits remain with the OpenAI source authors and
prior literature, the separate S003/E002/E003 work, @CubeJerry, and
substantial ChatGPT mathematical and implementation assistance.
