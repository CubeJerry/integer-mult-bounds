# Independent review of the fresh Gram-return packet obstruction

**Accepted within the explicitly restricted packet interface. No new kappa.**
This review verifies the support-37, all-volume quotient, rank-48 and
complete-budget claims. A separate stronger distance investigation does not
invalidate this package; it should be published as a subsequent result.

## Mathematical review

The 120 projective roots have a signed double exactly equal to the 112 vectors
2(+/-e_i+/-e_j) plus the 128 sign vectors of odd sign parity. The reviewer
derives this from integer Q^9 roots and a_k=(2r_k+r_8)/3, without importing
the author's root function. Summing four signs for each coordinate pair and
using the parity-constrained sign cube gives the stated degree-two, four and
six moments with constants 120,288,960. At degree at most six the sign parity
constraint has the same monomial averages as an unconstrained sign cube.
Separate sparse-polynomial multiplication checks every coefficient, including
zeros, at all three degrees.

The positive factorizations

    1-p(z)=(8-z)(z-2)^2/32,
    (10+15z)/32-p(z)=(10-z)(z-1)^2/32

are correct on 0<=z<=8. The full p-sum is 57. Each omitted orthogonal frame
contributes at most25/4 because its squared normalized evaluations sum to8.
Both displayed frames are disjoint and omitted from the actual hosted source.
The remaining eight omitted roots contribute at most8. Thus retained p-sum
is at least73/2, proving integer support at least37.

The characteristic-zero extension is valid: a prescribed zero pattern defines
a rational kernel, and the hosted root matrix has rank8. A nonzero extension-
field solution therefore yields a nonzero rational solution with no larger
support. For W tensor F^V, choose one nonzero internal coordinate to obtain
a nonzero scalar row of W. Its37-support lower bound is also a block-support
bound. This is an all-V proof, not extrapolation from a finite sample.

For any m-7 packet positions, the quotient of total packet span by their span
has dimension at most7V, whereas W tensor F^V has dimension8V. Their intersection
has dimension at leastV. This proves DISTANCE even for dependent packets and
arbitrary coordinate mixing. COVER follows because no source column is zero.
The capacity min(2^(r-1),96) follows from the odd parity functional on the
r-dimensional binary annihilator. It grants source subsets that may not exist,
so remains a necessary-condition relaxation.

All six analytic integer cases are correct. The first m-7 ranks have total
at most47-7h. For h=5,4,3,2 their capacities fall below37 by the stated bounds.
For h>=6 the eight relevant ranks cost at least48. For h=1, distance forces
at least44 packets; concentrating at most3 excess rank units gives coverage
at most51, below96. Twelve rank4 packets attain only the numerical relaxation.

## Independent exact checks

`check_gram.py` imports no author code. It checks the240-root set identity,
all2,082 moment coefficients, omitted frames via Q^9 Gram products, both
polynomial factorizations and hosted rank8. Fresh rational elimination at
all511 directions gives487 ranks8 and24 ranks7; the latter are exactly the
omitted root normals with distinct annihilator lines. This also verifies
the absence of a nonzero global Gram row at a chart of dimension at least2.

A separate ascending-partition search covers244,755 histograms of rank sum
at most47 with at least8 packets. Coverage passes197,339; distance passes14;
none pass both. Maximum coverage among distance-pass histograms is51. This
corroborates the analytic integer lemma and does not replace the all-V proof.

The complete favorable invoice is rebuilt from all1,710 source raw MOVEs.
Every one of400 raw fields has a dimension-eight ascent. Direct rank8 pricing
is a valid optimistic grant by concavity; all8 forward rank9 calls remain.
Independent integer-power bounds on a2^-110 grid prove the fresh-packet price
exceeds complete headroom by more than0.3958094568833/native. Exact bounds are
in GRAM-REVIEW.json.

Negative controls preserve the distinction between premises: support33 admits
a rank46 histogram; removing total96 coverage admits44 rank1 packets; putting
an actually hosted normal in an omitted frame violates its premise. Every
nonexceptional line direction separately has exact rank8.

## Scope and reproduction

    python3 check_gram.py --repo REPOSITORY --output OUTPUT

Native SHA256:2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883.
Invoice SHA256:b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248.

This covers new whole-field packets at one chart from unchanged hosted Y2
values, with no useful Y-dependent hub side information or funded informative
transport, and the fixed8-forward-rank9 tariff. Mixed current rows, relays,
changed forward tariffs, useful native responses and funded routes require
new analysis. An unfinished reciprocal word is not presumed to have only
the final Gram residual. All physical suppliers and five foundations remain.

Prepared for @CubeJerry with OpenAI assistance. Independent AI proof/source
review is not human acceptance or formal verification.
