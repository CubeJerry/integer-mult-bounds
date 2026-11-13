# General helper-constraint funding for the assigned14-zero/two-cache block

This is an optimistic fixed-native-history funding obstruction with arbitrary
scalar-linear helper constraint dimension. It concerns cached owned events
35152(rank2),45656(rank1) and zero events32681,39855,39857,39859,45659,
45661,45663,45698,45701,45706,51637,57989,58936,76469. Global block decomposition
and allocation of funding across blocks remain parent/C scope. No measured
rank, support or scalar provider identity here certifies a physical supplier.

The exact #7481 gzip SHA256 is
`acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9`.
The executable checks all1101 helper-column target ranks against actual native
entrance/exit frames and each zero candidate's paid rank against its literal
MOVE. Input hashes for the full rational source rows, targets, L_E/past-history
bases and assigned arrangement are retained. Preparation, cleanup, historical
storage, ordinary work and owned private erasure are optimistically free.

## Funding lemmas

Let beta(U) be the minimum sum of f(R_h) over a coordinate-column basis for
constraint rowspace U, where f(r)=r^(1-kappa). It is the optimistic target
debit, not a construction cost. Column greedy selection gives
beta(U)=sum_k(r_k-r_{k-1})f(k), with r_k the rank restricted to columns R<=k.

The fourteen source zero rows are independent. Every nonzero support column
h of row j has R_h>=its paid rank r_j. For any selected subset S, put
Z=span(S), z=sum_j f(r_j). Any nonsingular coordinate minor has a determinant
permutation matching each row to a distinct nonzero column. Hence z<=beta(Z)
for every increasing f. This is verified from exact source supports.

If W is contained in U, any column basis for U projects to a spanning family
for W, and contains a W-basis subset. Positive prices imply beta(U)>=beta(W).
If u is outside Z and EVERY nonzero column of Z+span(u) has target rank>=k,
a column basis of that rank-rho+1 space contains a rho-column Z-basis and one
additional column priced at least f(k). Therefore

    beta(U) >= beta(Z+span(u)) >= beta(Z)+f(k).

This remains valid if U contains arbitrarily many further constraints.
It allocates only these selected necessary within-block constraints.

## Requested pilot and full generic-union relaxation

Case0 credits the selected zero rows and already-enabled caches against
beta(Z). Case1 grants BOTH caches for only one generic extra u in L_union,
even if no such u enables both. Its prefix rank is
min(rank Z_k+1,rank[Z;L_union]_k). L_union has dimension19. Every zero support
has R>=4, while L_union has R3 support; thus the generic extra row costs
exactly f(3) beyond beta(Z). The formula is checked for every mask.

The first256 masks completed in0.18s. All16,384 completed in2.79s. Case0 has
maximum0. The loose case1 maximum is f2+f1-f3=0.00723708699970433008... at
.0038. That positive relaxation is not an actual compatible provider.
Only184 distinct signed price histograms occur; all signs use directed
rational bounds. RESULT.json retains the full executed census.

## Exact zero-only cache geometry

35152 remains outside the full zero quotient span (rank13), so no subset
enables it. For45656 the full zero quotient rank is5 and its exact witness is

    Q(x45656)=-(1/4)Q(z45659)-(1/4)Q(z45661)
              -(1/4)Q(z45663)+Q(z58936).

For each of these four events, the target is outside the span of ALL other
thirteen projected zero rows when that event is omitted. The witness gives
sufficiency, and these four omission tests give necessity. Thus45656 is
enabled iff all four are selected. The complete census agrees:15360 subsets
enable neither cache;1024 enable45656 alone.

Three required rows are distinct units e1344,e1347,e1346, each with paid
rank1 and target rank4. Their coordinates occur in no other zero row.
Their funding cost splits from the remaining selected constraints, whose
zero credit is still at most its basis price. With45656 already enabled,
case0<=4f1-3f4<0. Without it, case0<=0.

## Cache-specific refinement, arbitrary constraint dimension

For cache E, define L_E=(P_E+span(x_E)) intersect helper space, with P_E its
original strict past history. If U newly enables E relative to Z, some
u=x_E-p lies in U intersect L_E but outside Z. Otherwise E was already
enabled by Z. The support minimum of the ENTIRE L35152 is3, and that of
the ENTIRE L45656 is4; basis support verifies these for every combination.
All selected Z supports have R>=4.

If45656 is NEW, every column of Z+span(u) has R>=4. The funding lemma forces
beta(U)>=beta(Z)+f4. Even granting both cached deletions gives
z-beta(Z)+f2+f1-f4<=f2+f1-f4<0.

If45656 is not new but35152 is NEW, every column of Z+span(u) has R>=3.
The extra necessary funding is at least f3; adding its credit f2 worsens
case0 by f2-f3<0. If neither cache is new, beta monotonicity bounds the
profile by case0. These cases exhaust arbitrary constraint numbers without
assuming one generic row enables both caches.

The directed branch upper bounds at .0038 are:

| Branch | Native upper bound |
| --- | ---: |
| case0_no_cache | 0 |
| case0_cache45656 | -7.9369511909344299410004099284383723 |
| new_cache45656_grant_both | -0.98424471722944524443052953506699821 |
| new_cache35152_extra_over_case0 | -0.99276291300029566991811085473190172 |

The overall native upper bound is0, attained by the unchanged empty profile.
It holds uniformly for0<=kappa<=.01: zero-credit dominance uses increasing
prices; f2+f1<=3<f4, certified by4^99>3^100; f3>f2; and4f1-3f4<0.
This is a power-price interval result, not every concave tariff.

## Executed validation and limits

Normal and python -O runs agree on ALL16,384 census records and the refined
result. Only runtime fields and the runtime-dependent full-receipt hash are
excluded from semantic comparison. The256 pilot matches the full prefix.
Normal receipts were restored byte-for-byte after optimized-mode testing.

Four actual semantic corruption controls were executed with read-only source
files unchanged: excessive zero-row credit, a dependent/omitted zero row,
a wrong cache target, and a wrong rank4 column weight. All were rejected at
the corresponding funding, rank, quotient-provider or support-minimum check.
CHECKS.json records commands, outcomes and normal receipt hashes; optimized/
retains optimized receipts/logs. These are executed failures, not unchecked
expectations.

The proof grants all preparation and services free and only charges necessary
target funding. It does not admit circuits, grids, ordinary-cost constants,
new histories, changed frames or physical cached replacements. Global direct-
sum/Laplace allocation across other arrangement components is independently
reviewed outside this assigned block. All five framework assumptions remain.

Replay:

```sh
python3 -I -B worker-a/mixed-cache-budget/pilot.py --limit 256
python3 -I -B worker-a/mixed-cache-budget/pilot.py --limit 16384
python3 -I -B worker-a/mixed-cache-budget/refine.py
python3 -I -B worker-a/mixed-cache-budget/checks.py
```

REFINED.json is the compact geometry/price receipt. CENSUS-SUMMARY.json omits
only the bulky record list. VALIDATION.json freezes sources and artifacts.
