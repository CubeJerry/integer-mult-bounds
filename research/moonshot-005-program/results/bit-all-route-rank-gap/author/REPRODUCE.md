# Reproduce the all-route rank-gap package

`PROOF.md` is the universal argument. `check.py` reconstructs the complete caller
from its pinned receipt and uses outward 2^-160 integer-root arithmetic. It also
checks every directed rank edge at t=199/200 and finite relaxed facet-route
counts. The analytic inequalities, not those finite cases, establish the whole
target interval.

```bash
python3 -I -B check.py --caller /absolute/path/bit-eight-packet-target/author/RESULT.json --native /absolute/path/BIT-NATIVE-WORD.json.gz --output /tmp/all-route-budget.json
python3 -I -B native_controls.py --native /absolute/path/BIT-NATIVE-WORD.json.gz --engine /absolute/path/engine.py --output /tmp/all-route-native-controls
```

Expected markers are `PASS_ARBITRARY_PUBLIC_AND_OWNED_ROUTE_TARGET_BUDGET` and
`PASS_ACTUAL_NATIVE_PUBLIC_ROUTE_SHARPNESS_AND_REVISITS`. The latter reproduces
three deterministic compressed words and their all-input receipts.

`engine.py` is the lead's actual-history extractor. It uses independent rational
chart reduction and a dual-basis rectangular inverse, without importing C's
theorem checker or any construction-worker replay. For this root-authored new
theorem and these three root-authored controls, it is author evidence; a separate
review is required. Its predecessor independently audited the coupled C5 source.

All source pins are in `PROOF.md` and the receipts. Every word is explicitly
partial; the Y endpoints that remain unchanged are not silently counted as
completed targets. All five foundations and both strict suppliers remain.
