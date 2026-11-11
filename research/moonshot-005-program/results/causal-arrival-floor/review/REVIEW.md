# Independent review of the frozen-main causal arrival floor

**Review outcome:** the scoped causal-arrival theorem and its source count are
correct. This review does not cover a changed-main-prefix construction, an H4
native, physical supplier admission, or a new kappa. All five selected global
assumptions remain. Prepared for @CubeJerry with substantial OpenAI assistance;
independent model-assisted reconstruction is not human or formal acceptance.

## Mathematical review

The lower bound is valid even with proactive, coded, or permanently parked
observations. At each chart, grant a proposed implementation immutable retention
of all past observed rows. Its knowledge space A then contains the greedy
reference space G after every fulfilled demand. The nonnegative potential
`sum_f (dim A_f - dim G_f)` increases by at most one for each incoming normalized
complete field. A free prescribed main arrival is added to both spaces; its
rank increase in A is no greater than in G, so the potential cannot increase.
A demanded row already in A but outside G lowers the potential by exactly one.
Scalar operations cannot create new knowledge. Thus each counted innovation
needs an earlier charged arrival, regardless of anticipation. Importing each
demand at its innovation time attains the count in the arbitrary-teleport
relaxation. The argument is universal linear algebra; the 984 figure is the
pinned finite source application.

A potentially subtle premise is necessary: at every original event boundary,
physical main rows equal the original virtual prefix rows. For an ADD with
nonzero c, permanently caching the old and new destination rows makes the
source difference recoverable as `(new-old)/c`, even if an implementation
never explicitly computes that difference. The independent replay checks all
61,181 ADD/COPY coefficients are nonzero and checks the one COPY's homogeneous
zero destination. No arbitrary demand is silently imposed.

The same restriction is essential for each original **main MOVE payload**: it
must carry its prescribed virtual row, not just return that row at the macro
boundary. A counterexample to a weaker boundary-only premise is `m=d` in chart
A, source observation `e` in A, and an existing copy `p=d` in chart B. Replace
m by `d+e`, carry it on the already paid main route, form `t=m-p=e` in B, then
restore `m-=t=d`. Both macro boundary main values are correct, yet e was delivered
without an extra MOVE. The updated theorem requires literal actual main MOVE
payloads; the generalized inequality counts nonliteral main payloads when they
are permitted. The reviewer executable includes this excluded positive escape.
This is precisely why changed main carriers are a legitimate direction.

The fixed-code helper premise must apply to the **physical payload of each
source helper MOVE**, not merely its contents at source event boundaries. A
macro could otherwise replace a helper temporarily with a differential payload,
transport it using its already paid route, and restore the common code. The
updated proof excludes that operation from the constant-common-payload theorem
and counts it as a useful helper arrival in its generalized inequality. That
scope distinction is essential and correctly stated.

The arithmetic consequences follow only while the H4 target/paid/caller terms
remain otherwise fixed. Positive integer MOVE rank gives `r^(199/200)>=1`.
The exact source-derived upper bound is
`221397923137950577/2250000000000000 < 98.399076951 < 99`. Thus at most
98 extra arrivals fit. This corrects the prior downward-rounded decimal; the
integer arrival conclusions are unchanged. Granting
all 47 original owned arrivals arbitrary useful information leaves a constant-
helper-code deficit at least 984-47=937. In the generalized variable-payload
case at least 984-47-98=839 useful source-helper arrivals are necessary **when main
MOVE payloads remain literal**. Permitting nonliteral main payloads adds their
useful arrival count to the generalized inequality. These
are arrival incidences, not distinct helper labels or an assertion that all
such arrivals are actually usable. They do not exclude changed main histories.

## Independent finite reconstruction

`review_deliveries.py` imports no author verifier. It reconstructs all 71,261
source events using exact `Fraction` coefficient rows, with a separately written
primitive-integer elimination routine using maximum pivots. The author uses a
minimum-pivot rational basis. The replay verifies all source/destination charts,
owned INIT/CLEAR lifetimes, nonzero ADD/SCALE coefficients, COPY zero, and every
post-ADD main row's inclusion in the reference knowledge space.

Every binary frame is reconstructed as a subspace. The sole alias, frame IDs
1091 and 1092, is merged for free; all 1,095 IDs reduce to 1,094 distinct spaces.
The count is unchanged. Exact results:

| Quantity | Independent result |
|---|---:|
| Main inputs | 400 |
| Original events | 71,261 |
| Auxiliary-to-main source demands | 7,988 |
| Greedy fresh arrivals | 984 |
| Free main-arrival innovations | 1,610 |
| Main MOVE occurrences | 1,710 |
| Auxiliary MOVE occurrences | 4,600 |
| Owned MOVE occurrences | 47 |

All 984 innovation event indices and all per-chart counts agree with the
author's exact replay. Matching only a final rank or a scalar total was not used
as independent verification.

The verification also enumerates all 16 subspaces of F2^3, checking 528 paid-
arrival potential steps, 528 common-free-arrival steps, and 147 innovation
steps. These finite controls do not prove the universal potential lemma; the
written argument above does. Additional controls distinguish an early demand
from a later free row, reject double-counting a scaled redundant demand, reject
cross-chart aliasing, and reject source-byte drift. Exact checks remain active
under Python `-O`.

## Reproduction

Pass the source and author certificate explicitly (adjust paths from the review directory):

```sh
python3 -B review_deliveries.py --source research/shared-wire-split-composition/data/final.json.gz --author-certificate ../CERTIFICATE.json
python3 -O -B review_deliveries.py --source research/shared-wire-split-composition/data/final.json.gz --author-certificate ../CERTIFICATE.json
```

Expected marker: `PASS_INDEPENDENT_FROZEN_MAIN_DELIVERY_REVIEW`, innovations984,
free_main_innovations1610. `DELIVERY-REVIEW.json` records every innovation event
and every per-chart count. Immutable source SHA-256:
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.

## Remaining limitations

This proof does not price scalar coefficient services, memory, source/control
movement, rounding, or owned erasure. The lower relaxation grants them for free,
so omitting their positive expense does not weaken the stated obstruction. A
positive implementation would need to pay them. An H4 design that changes the
main differential carriers changes the list of free arrivals and is expressly
outside this theorem. A static main-rank bound and this temporal arrival bound
are complementary constraints, not additive fees.
