# Wave61 checkpoint: relation-family scope remains pending

This folder is an honest freeze checkpoint, not a completed family proof.

## Frozen evidence already checked

- Exact source: #7481 `WORD.json.gz`, SHA256 `acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9`.
- Independent exact-Q single-circuit receipt: `../public-cache-interface-review/ONE-CIRCUIT-REVIEW.json`, SHA256 recorded separately by the package builder if needed. It certifies all 7,780 initial/arrival rows are independent across 979 exact frames, only `U=-e1459-e705+e885` is in final frame 189, and its only strictly-earlier-provider circuit is event 40710 (rank 8) with providers initial `e1459` and event 40708 `e705+e943`.
- B59's independently source-bound singleton result `worker-b/rank1-zero-public-caches/PROOF.md` records that `e1459=0` enables only event 52236 (public rank 1), no whole-zero MOVE, and a rank-1 lost original target.
- Existing A54 analysis of event 40710's fixed-history preparation cost is conditional on demoted `e1459` being unavailable; the B57 provider list shows why that premise is material. It is not combined into an unconditional physical or global saving claim.

## Unfinished exact extension

`../public-cache-interface-review/check_one_circuit.py` was extended to test the full two-dimensional space `L=span(e885-e705,e1459)` and finite family `u_lambda=(e885-e705)+lambda*e1459`. That extended version was not completed: a fresh exact-Q replay was stopped at the project verification cutoff before it emitted a receipt. Do not use its `L` assertions or output as evidence. The pre-existing `ONE-CIRCUIT-REVIEW.json` is only for the single direction U above.

No Wave61 claim is made about all finite lambda, all directions in L, or global reuse of same-promise credits. Root may close these claims using source support and the two independent frozen witness packages.
