# Complete BIT query-layer deletion still misses kappa=1/200

**Proved exact target-budget condition. No new kappa.** Fix the paired#7001
caller/#6726 native paid and productive profiles. Keep native and IDLE_ONE costs
and every target fixed. Grant arbitrary original QUERY deletions for free, even
without a provider. Added fees must be nonnegative. The raw1/200 gate still fails.

There are exactly four QUERY events,196,198,201,349, each charging111 rank-one
jobs. Their entire credit is444. The old margin M=sum_r(T_r-P_r)r^(199/200) is
approximately -444.06321643233964098. Hence M+444=-0.06321643233964098...<0.
Smaller credits or additional nonnegative fees cannot improve that upper bound.
The free deletions are a relaxation, not claimed algorithms.

The verifier freshly counts native MOVE dimensions,437 helper endpoint ranks,
36 LOCALs,32 IDLE_ONEs,four QUERYs and38 productive diagonals, reproducing every
rank in the107352-paid/19950-target ledger. With D=2^88, integer bisection gives
a_r^200<=r^199 D^200<b_r^200. Summing [a_r/D,b_r/D], reversing endpoints for
negative coefficients, bounds the deficit after all free QUERY deletions by

[9782269091752093092810873/154742504910672534362390528,
611391818234505818304597/9671406556917033397649408].

Both bounds are positive. Decimals are explanatory. If integer rank-one unit
removal is the sole improvement,445 credits are necessary:444 fails,445 passes
the raw arithmetic only. The actual QUERY layer contains444 units. A claimed
fifth original QUERY is rejected. Normal/-O agree; explicit checks remain active.

## Relation to open#7177

ToikY's CrocSwap/integer-mult-bounds#7177 at
f59cf773c6038d72bc3b5aeae204cbe1923b34bf changes18 LOCAL phases and proposes
removing QUERY349. Its README/price code were read; no independent admission
of its formal caller or unbuilt provider is claimed. Granting its111 credits
leaves deficit333.06321643233964098..., requiring334 further integer unit
credits. If equally spread over18 changed calls,18 further net units per call
fail and19 pass only the raw arithmetic. Provider expenses reduce net credits.

The proposal may improve a lower exponent. This theorem concerns only the
exact.005 gate with other profiles fixed; even deleting ALL queries needs an
outside-layer change. No global single crossing, unrestricted impossibility,
provider or new kappa is claimed. Complex supply, compiler, outer and five
foundational obligations remain open. Independent review is recorded separately.

Prepared for @CubeJerry with OpenAI assistance. Credit ToikY#7177 for the phase
lead and#6726/#6834/#6980/#7001 for native/invoice/caller, with retained lineage.
The new result is the1/200 whole-query-layer budget exclusion, not the caller identity.
