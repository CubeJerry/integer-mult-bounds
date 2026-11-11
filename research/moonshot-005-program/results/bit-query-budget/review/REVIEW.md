# Independent review of the entire-query target barrier

**PASS for the stated exact kappa=1/200 gate with pinned native, IDLE and target
profiles fixed.** This is an independent arithmetic and source-census review,
not admission of a changed BIT provider or an open pull request.

The reviewer imports no author code. It independently expands each literal
LOCAL event into the pinned native's2,871 MOVE ranks and437 helper endpoint
ranks, adds every IDLE_ONE and QUERY charge, and reconstructs all diagonal
target entries. The complete profiles have107,352 paid positions and19,950
productive fields, matching the immutable ledger and author receipt. There
are36 LOCAL,32 IDLE_ONE and exactly four QUERY events:196,198,201,349. Each query
has111 rank-one jobs. Event349 is the literal `QUERY 19,20` occurrence.

The independent calculation uses a decimal10^30 grid and integer Newton
iteration for200th roots. The author uses a dyadic2^88 grid and bisection.
Exact200th-power inequalities certify every bracket; rank-one powers are exact.
Signed rational summation gives an interval contained in the author's
enclosure. After freely deleting all four QUERY charges, it is

    [-7902054042455123093346461103 / 125000000000000000000000000000,
     -31608216169820492373385806903 / 500000000000000000000000000000],

approximately-0.06321643233964098. Both endpoints are strictly negative. The
baseline margin is this interval minus444. Thus even free elimination of the
entire original query layer cannot close this exact fixed-profile target gate.

The necessary integral net credit is at least445 rank-one units:444 fails,
while445 passes the raw scalar gate. Removing349 alone supplies111 units, so
334 additional net units are necessary. If a specified construction supplies
the same integer net saving c in each of18 changed calls,111+18c exceeds the
deficit only for c>=19:18 fails and19 passes the raw gate. This review treats
18 changed calls as an explicit condition; it does not independently establish
the PR7177 metadata or admit its changed-provider mathematics.

These are necessary budget conditions. Passing the scalar gate is not a
construction, a complete supplier or a new multiplication exponent. There is
no global monotonicity or single-crossing claim as kappa varies, and changes
to the native, IDLE work or target spectrum are outside the result's scope.

Controls check444 versus445 credits,18 versus19 conditional per-call credits,
and the absence of a fifth original query. Normal/-O review receipts match.
All reviewed author hashes are in `REVIEWED-FILES.json` and both receipts.

```sh
python review.py --repository /path/to/integer-mult-bounds \
  --author /path/to/bit-query-budget --output /tmp/bit-query-review.json
python -O review.py --repository /path/to/integer-mult-bounds \
  --author /path/to/bit-query-budget --output /tmp/bit-query-review-opt.json
cmp /tmp/bit-query-review.json /tmp/bit-query-review-opt.json
```

Expected status: `PASS_INDEPENDENT_BIT_QUERY_TARGET_REVIEW`.
Prepared for @CubeJerry by an independent S003 OpenAI-assisted worker.
