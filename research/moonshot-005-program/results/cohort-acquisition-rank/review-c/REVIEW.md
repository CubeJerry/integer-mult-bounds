# Independent review: cohort acquisition filtration

**PASS for the stated universal square and rectangular matrix theorems and
their incidence/transpose corollaries. No new complete supplier or kappa.**
Worker C independently reviewed the proof, wrote a separate finite checker,
and did not import or execute root's checker. Exact reviewed file hashes are
in RESULT.json. The proof is valid over every field and positive block width;
the finite controls are supplemental evidence, not the universal proof.

## Mathematical review

For a fixed cohort order, the kernel filtration is correctly oriented: Z_i
contains exactly the fixed vectors of UP supported on the first i cohorts.
The current-cohort projection has kernel Z_(i-1), without any assumption
that U is injective. For a good acquisition row, all source cohorts lie later,
so that entire V-row block of P vanishes on Z_i. The current target block is
the image under U_i of only the bad acquisition blocks. Its image dimension
is at most V times their number, even if U_i is singular or its internal
coefficients are noncommuting matrices. Summing these actual dimension
increments proves the order bound. No simultaneous invariant space or
algebraic inverse has been assumed.

The random-order event has probability exactly 1/(s_j+1): it compares only
the distinct source cohorts with the target cohort. The zero-support case
has probability one. Dependence between different row events is immaterial.
The integrality of the maximum good-row count justifies the ceiling before
multiplication by V, a stronger conclusion than merely rounding a scalar
rank bound. In the rectangular case the same proof bounds the kernel by
(b-good)V, while rank-nullity still uses nV. This gives n-b+good exactly;
negative lower bounds are harmless. Extra acquisition rows genuinely change
b and cannot be inserted into the physical interpretation without payment.

The grouping sharpness example works over arbitrary fields: each all-ones
group matrix has rank one, including when its size vanishes in the field.
It establishes algebraic sharpness, not realizability in native charts.
The separate parity specialization optimizes the two sides of each disjoint
cohort pair, and hence agrees with the stronger 56-mode native parity gate.

The Cauchy--Schwarz incidence consequence follows from positive rational
support counts and is correctly rounded. The transpose statement applies to
the actual local correction L, whose zero diagonal cohort blocks survive
transposition. Counting pure original-record visits is a sufficient physical
premise only while input coefficients do not spread to other records/cohorts.
The corollary explicitly retains that restriction.

## Physical scope

The X-coefficient equation I=G+UP is necessary for the proposed one-stage
architecture even when original Y inputs are arbitrary and a global Y
precode is present. It is not sufficient: the independent Y coefficients,
actual decoding availability, full route histories, ownership and restoration
must still be checked. The theorem does not set them to zero as a service.

Most importantly, rank G is the span of actual available global X histories,
not the number of packet identities. A packet that changes information can
contribute several independent historical modes. The frozen proof expressly
retains that distinction. Multiple local decoding stages or moving acquisition
helpers can also fall outside this single-stage factorization and require
their own paid model. These are real escape obligations, not contradictions
to the theorem.

## Independent finite controls

The checker enumerates every binary vector in each tested kernel, rather than
using the author's rank/filtration implementation. It verifies every cohort
order and each actual filtration increment in 648 cases, including 579 with
singular U. The cases include exhaustive scalar two- and three-cohort inputs,
width-two arbitrary blocks, empty acquisition cohorts, and rectangular
decoders with both excess and deficient acquisition rows. There are 12,976
checked filtration increments. A separate modular elimination verifies 234
sharpness examples over F2, F3 and F5.

Two explicit scope controls attain rank-zero correction when a hypothesis is
removed: P=U=the two-port swap uses a nonlocal inverse decoder; P=U=I reads
the forbidden own-cohort inputs. The native incidence bounds are independently
computed as 1430, 1258 and 1122 for q=8,9,10. Normal and optimized Python
produce identical JSON.

Reproduce from the session workspace with:

```sh
python worker-c/review-cohort-filtration/check.py --package root-work/cohort-filtration --output worker-c/review-cohort-filtration/RESULT.json
python -O worker-c/review-cohort-filtration/check.py --package root-work/cohort-filtration --output worker-c/review-cohort-filtration/RESULT-OPTIMIZED.json
```

Root's literature note correctly avoids claiming the established acyclic
index-coding method as novel. This review establishes the self-contained
matrix proof and its stated applications; it is not an exhaustive literature
novelty assessment. Credit root's filtration argument, Worker C's acquisition
question and displacement approach, @CubeJerry and the cited predecessors.
OpenAI assistance. All remaining programme foundations remain visible.
