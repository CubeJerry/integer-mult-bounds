# Complete literal row control for one current CRT wire

One fixed **10,123-instruction graph on 20 physical owners** now executes
every row of a current wire's canonical padded rotation, in either direction.
Four fixed control copies of the exact preceding point consumer share the
same backing. Encoded row initialization and carry/borrow, the palindromic
target cursor, point entry/return and final retirement are literal operations;
no host row loop or decoded height chooses a query.

For h>=1, p>=h+1 and the explicit consistent-frame ABI in [PROOF.md](PROOF.md),
each entry executes exactly 2h-1 current-address queries. The additional
controller bills, including both complete row scans, are exactly

```
forward: 14p + 36h - 12 - 7 popcount(2h-2)
inverse: 14p + 72h - 38 - 14 popcount(2h-2).
```

The full bill still includes every preceding point call, each bounded by
`1024(h+3)^2+128(p+h+3)`. A fixed per-owner interval union bounds private
history by O(p+h), retaining every earlier larger extent. All heads return,
borrowed headers/width stay unchanged, the inactive owned row body becomes
zero and point scratch returns blank. Supplied owner/window/acquisition and
header-width consistency premises remain explicit. Rejected-route rollback
is not claimed.

## Evidence and actual caller

Normal and optimized primary replays pass 1,764 complete routes: all 668
forward/inverse routes through h=3, all 1,088 at h=5,s=17, and eight boundary
routes covering h=1, carry boundaries at h=7/9, p=2049, translated origins and
older history. Every point entry is checked against the original canonical
network for its encoded row, current address and physical target. All 10,000
embedded point instructions are compared with exact source relocation,
including return edges. The written proof covers all admitted heights;
finite checks do not establish that quantification.

Seventeen controls include four returning semantic mutants with all heads
and private histories restored: lost row increment, wrong inverse direction,
premature cursor reversal and stale wire. The stale-wire fault uses a separate
21-owner test graph, outside the 20-owner theorem. Omitted retirement,
malformed domains/frames, aliases and actual offset/inverse defects are
detected separately.

One exact `route_address` substitution connects the graph to the preceding
actual #7388 four-tag source/payload caller. Both its original modulus-2 case
and a modulus-3/left-2 current-wire discriminator complete forward/inverse
roundtrips on the same physical source and payload. Numerical lease/header,
all-wire enumeration, source commit and radix providers are retained and
credited. The original case uses 22,402/22,558 literal forward/inverse
instructions: unchanged 21,910 point steps plus 492/648 controller steps.
Each leg retains 742 outer symbol actions; source, payload, radix and storage
receipts match the exact preceding package. Different tariffs remain separate.
No wall-clock, ROM-reuse, E(p,ell), complete supplier or kappa gain is claimed.

The exact predecessor is CubeJerry commit
[`be17dd21af36a8b0546942299ebca7b1c83c4675`](https://github.com/CubeJerry/integer-mult-bounds/commit/be17dd21af36a8b0546942299ebca7b1c83c4675).
Canonical base is `e54523517d0f03e58352e647c403a5af3e525a57`.
[SOURCE-PINS.json](SOURCE-PINS.json) authenticates 38 retained files;
[RESULT.json](RESULT.json) and [RESULT-O.json](RESULT-O.json) contain identical
computed primary receipts. Independent model-assisted review passes in [REVIEW.md](REVIEW.md):
a separate sparse interpreter checks 50 routes, 366 point calls, four returning
semantic corruptions and an actual non-power-modulus source roundtrip. Human and proof-kernel acceptance are unclaimed;
all five foundational assumptions retain their selected status.

## Reproduce

```sh
python3 -I -W error -B research/literal-current-wire-row-controller/verify.py
python3 -I -W error -B -O research/literal-current-wire-row-controller/verify.py
python3 -I -W error -B research/literal-current-wire-row-controller/independent_check.py
python3 -I -W error -B -O research/literal-current-wire-row-controller/independent_check.py
```

Expected output includes `PASS`, 10,123 instructions, 20 tapes, 1,764 complete
routes, two actual roundtrips and 17 controls. Default execution is read-only;
`--receipt PATH` explicitly saves generated results. The canonical gate is
`python3 -B scripts/research_package.py --package research/literal-current-wire-row-controller`.
No selected cold replay or complete multiplier run is implied.

## Open next questions

1. Lower one actual numerical lease/header-production boundary to the same
   literal interface, charging source reads, acquisition and retirement.
   This service starts after compatible headers are physically available.
2. Lower outer variable-size wire/key enumeration and multi-target order.
   Start with the exact preceding `prepare_keys` and its physical record ABI;
   preserve source, payload and history contracts.
3. Compare a complete repeated workload against retained-ROM reuse under one
   tariff, including source work, histories and disposal.

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance.
The original network, Nick Petalas #7504 arithmetic, B4/B5 point service,
#7388/#7352 source lifecycle and numerical/radix lineage remain credited in
[NOTICE.md](NOTICE.md). Apache-2.0.
