## Summary

The preceding direct CRT point service is literal, but its complete per-wire
row loop still uses outer symbol-action control. This package replaces that
specific loop with one fixed **10,123-instruction, twenty-owner graph**, with
forward and inverse entry ports. Encoded row initialization/updates, the
physical target cursor, every point call/return and final retirement are
literal; no decoded height, current row or host loop chooses a query.

Exactly `2h-1` unchanged point-consumer calls execute on the current physical
address. Four fixed control copies share the same owners and historical
backing. For every admitted `h>=1,p>=h+1`, the additional bills are

```text
forward = 14p + 36h - 12 - 7 popcount(2h-2)
inverse = 14p + 72h - 38 - 14 popcount(2h-2).
```

The complete bound still includes each point call's
`1024(h+3)^2+128(p+h+3)` allowance. Private history uses a fixed per-owner
union of O(p+h), independent of the number of queries; earlier larger extents
remain charged. Every head returns, borrowed headers/width stay unchanged,
the inactive owned row frame becomes zero and point scratch returns blank.

Canonical base: `e54523517d0f03e58352e647c403a5af3e525a57`. Exact scientific
predecessor: [CubeJerry commit be17dd21](https://github.com/CubeJerry/integer-mult-bounds/commit/be17dd21af36a8b0546942299ebca7b1c83c4675),
`research/current-crt-direct-switch-consumer`. Only
`research/literal-current-wire-row-controller` is added.

## Evidence and actual caller

Normal and optimized primary runs produce identical receipts. They cover
1,764 complete routes: every forward/inverse case through h=3, every
offset/address at h=5,s=17 in both directions, and h=1/7/9, p=2049,
translated-origin and older-history boundaries. All 10,000 embedded point
instructions and return edges are compared against the exact predecessor.
The written induction and carry identity prove the unrestricted typed result;
finite coverage is corroboration.

Seventeen controls detect wrong current-row updates, inverse order, cursor
turnaround, stale current wire, omitted retirement, malformed domains/frames,
aliases and actual source-offset/inverse defects. Four semantic mutants
return with complete head/private restoration but incorrect outputs.

One exact `route_address` seam joins the graph to the retained actual #7388
four-tag source and radix payload path. Both the original modulus-2 case and
the modulus-3/left-2 current-wire discriminator restore the same source and
payload after forward/inverse execution. The original case costs
22,402/22,558 literal instructions: unchanged 21,910 point steps plus 492/648
controller steps. Source/radix/storage receipts match the exact predecessor;
742 outer symbol actions per leg remain separately reported.

```sh
python3 -I -W error -B research/literal-current-wire-row-controller/verify.py
python3 -I -W error -B -O research/literal-current-wire-row-controller/verify.py
python3 -I -W error -B research/literal-current-wire-row-controller/independent_check.py
python3 -I -W error -B -O research/literal-current-wire-row-controller/independent_check.py
python3 -B scripts/research_package.py --package research/literal-current-wire-row-controller
```

Expected direct markers: `PASS`, 10,123 instructions, twenty tapes, 1,764
routes, two actual roundtrips and seventeen controls. Default verification is
read-only. Independent model-assisted review passes in `REVIEW.md`. Its separate sparse
interpreter checks 50 routes and 366 point calls (1,667,878 literal steps),
four returning semantic corruptions, the exact carry-count argument and an
actual modulus-3 source/payload roundtrip. Both reviewer modes emit identical
receipts. All 38 retained files match their exact origins. No human or
formal-kernel acceptance is claimed.

## Novelty, limitations and credit

The point arithmetic, canonical network and radix algorithm are credited
predecessor work. The new result is the exact full-row controller at their
physical current-wire interface and its complete local invoice. Actual
numerical lease/header production, all-wire enumeration and payload/radix
providers are retained, not rebuilt. Their outer tariffs stay separate.
Consistent h/width/p frames, distinct owners, blank private grants, acquisition
and initial source access remain explicit premises. Rejected-route rollback
is not asserted. No complete CRT, E(p,ell), ROM-reuse speedup, foundational
assumption discharge, selected-frontier change or **new kappa** is claimed.

Open next work is a literal numerical lease/header boundary or the outer
variable-size key enumeration, with all access and history costs retained.

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance in
research, proof, implementation, verification and independent model-assisted
review. Credit Nick Petalas #7504; the exact B4/B5 point service; CubeJerry
#7388/#7352; Ali Romman #5625; JoyboyBrian's numerical/row/ROM/key/radix
interfaces; Cinna Davis's canonical Beneš/CRT construction; and all retained
notices. Apache-2.0. Changes are confined to the isolated research package.
