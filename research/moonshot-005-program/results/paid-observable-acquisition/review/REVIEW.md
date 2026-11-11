# Independent review of both actual observable acquisition prefixes

**Verdict: PASS for the explicitly scoped finite acquisition prefixes. No new κ.**

This review covers the two literal artifacts in `paid-observable-acquisition`, with all 13 frozen author-file pins in `REVIEWED-FILES.json`. The direct collecting-chart architecture originated with the S003 lead; the cheaper facet-lift architecture originated with the construction worker. The adversarial worker implemented both words. This review is an independent implementation and mathematical check, not a claim of independent discovery.

## Independently reconstructed source rows

`review.py` reads the pinned original native and the emitted acquisition artifacts/receipts. It imports no author verifier. Fresh reverse adjoints of the original source prefix before event 30824, starting from owned role 1481 and main role 130, derive both targets. Initial helper differences are zero because the two copies have equal arbitrary helper inputs. The rows have supports 59 and 26; their union has 60 raw main inputs: 8 initially at chart 3 and 52 elsewhere. The receipt contains both exact rows.

This confirms acquisition of the actual updated owned row r and current-main row s, not the incorrect earlier three-input approximation. The source cut specifies the linear forms only; neither physical prefix puts the whole machine at source cut 30824.

## Full 1,880-input exact replay

The independent interpreter starts with 1,880 formal basis inputs: all 1,480 arbitrary common inputs u, including dirty helpers, and 400 independent second-main inputs v. Every instruction of both literal artifacts is checked using exact rational coefficients. ADD operands must be physically cochart. Public MOVEs must be strict ascents; owned MOVEs require the correct ownership bit and nested actual chart spaces. INIT/CLEAR must respect live ownership, source-owned label reservations and exact chart location.

At completion all 1,480 common rows and charts equal their original values. All 400 raw difference rows equal v_i−u_i. Both owned output rows equal the independently derived source forms applied to those differences. This checks all 1,880 independent input directions, not numerical samples. Linearity establishes the identities for every scalar assignment and componentwise for every field volume under the inherited complete-field MOVE contract.

Exactly two owned outputs, roles 1931 and 1932, remain at chart 541. All 51 original common-owned labels are untouched. Three additional labels are used, with peak three live owned fields. The two final outputs still require actual consumers and charged retirement.

## Route, operation and lifecycle audit

The checker reconstructs all selected donors' original main MOVE occurrences directly from the source. Each physical raw MOVE corresponds to exactly one selected source occurrence with identical charts and rank. All selected routes are used once in original relative source order. No unreserved raw MOVE is present. All other raw donors remain at their initial locations.

| Checked quantity | Direct | Facet copies |
|---|---:|---:|
| Instructions |730|783|
| ADD, including 400 input conversions |487|493|
| INIT |4|10|
| CLEAR |2|8|
| MOVEs |237|272|
| Reserved raw main occurrences |233|262|
| Unexecuted raw main reservations |1477|1448|
| New owned MOVE profile |{7:2,2:2}|{1:8,2:2}|
| Owned lifetimes started |4|10|
| Fresh labels / peak live |3 / 3|3 / 3|
| Live outputs at chart 541 |2|2|

These independent counts match the author receipts. Complete target tariffs are separately checked in `relay-acquisition-budget`.

Five independent mutants per variant are rejected: wrong owned-output coefficient, input difference changed to a sum, broken reserved-route source chart, false public descent, and erasure of a required live output. Normal and optimized review receipts are identical.

## Scope and remaining obligations

The arbitrary common source state is preserved because it is unexecuted. These are actual physical acquisition prefixes, but they do not execute the original 13 relay consumers, current-main continuation, other S8 observers or full native output map. Retiming 52 or 60 raw carriers spends genuine source route reservations and changes intermediate locations. A continuation must meet every remaining duty without spending a reservation twice.

The two Gaussian budget profiles are positive when provisionally added to S8, as separately verified. Ordinary scalar costs, output retirement, peak storage during a future continuation, numerical precision, uniform supplier admission and all five foundational premises remain separate. This review certifies no full conditional multiplication improvement, unconditional theorem, or physical composition with all S8 requirements.

## Reproduction

```sh
python review.py --repository "$REPO" --package "$ACQUISITION" --output /tmp/acquisition-review.json
python -O review.py --repository "$REPO" --package "$ACQUISITION" --output /tmp/acquisition-review-optimized.json
cmp /tmp/acquisition-review.json /tmp/acquisition-review-optimized.json
```

Expected status: `PASS_INDEPENDENT_BOTH_1880_INPUT_ACQUISITION_PREFIXES`.

Research by @CubeJerry with AI assistance. Original source and programme predecessor credit are retained; the design and verification roles are distinguished above.
