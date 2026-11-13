# Independent review: funded cross-D pair

**Verdict: PASS within the stated partial-source scope.** I found no causal, chart-phase, endpoint-map, or m=3 invoice error in the frozen package. The construction preserves its parent's current first-X, first-Y, and D maps, changes exactly two B outputs, and lowers the hosted reverse residual rank from 58 to 57. It does not complete the remaining forward/reverse endpoint obligations or supply a full multiplication word.

## Frozen inputs

The reviewed author package is `worker-a/next/funded-cross-pair`, manifest SHA256 `b5bfd431477d9d423961fd679b8c940273594530f11c2f6629d2ae523d6342ac`. Every file listed in that manifest matched its size and SHA256 when reviewed. The principal pins are:

- Parent Q: `a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc`.
- Cross-pair word: `787ae38760119ce9b628c3b9eff0244271b3c0ad65b646c725730a2142d6dc1a`.
- Native 1,480-row source: `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
- Three-copy word: `de58d2b0b769d9947444d11fb5adb27fb5eb4a3a97ddfc34871323b9be0919c0`.
- Pinned full-caller invoice: `d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7`.

The independent replay uses its own sparse `Fraction` interpreter, exact GF(2) chart inclusion, and independent row-rank elimination. It imports no author extractor, builder, map checker, or source interpreter. Its `COPY` path applies the encoded coefficient, so a non-unit coefficient cannot be silently treated as a literal copy. The phase review separately constructs canonical frame operators and compares signed Pauli tableaus plus exact Gaussian vacuum states, which also detects global phase.

## Causal audit

The port-to-row bindings are correct: logical B1/B106 are public rows 209/298, and logical D106/D1 are public rows 394/305. In the parent, rows 394 and 305 each have exactly one use/write, their original direct public MOVE to charts 226 and 129. They remain at chart 3 through the first 40 source events, so the 130 Y-precode ADDs at events 40–169 read their original values before the two literal MOVE operations are hoisted to events 170–171. Hoisting changes chronology but preserves each donor's original route and endpoint chart.

I independently reconstructed the first two packet encoders and decoders from the parent word. Each packet has 65 actual first-Y recipients; the support union has 76 rows. The precode consists of the exact 65+65 decoder coefficients, including their fractions. The literal handoffs are:

- Packet 0: Hub 127 → facet 226 → source line 1 → chart 3; read D106 at 226 and add the negative packet into B1 at line 1.
- Packet 1: Hub 127 → facet 129 → source line 99 → chart 3; read D1 at 129 and add the negative packet into B106 at line 99.

All six moves are nested. The existing decoder therefore sees `P0 + d106` and `P1 + d1`; the precode subtracts the same `β0*d106 + β1*d1` contributions at the same first-Y rows. The independently replayed first-X and first-Y endpoint maps equal the parent exactly.

The B handoffs occur while B1 and B106 are still their original independent unit rows at their initial source lines. Their first old reads in the parent are events 530 and 534. I separately propagated two formal tags through the full parent suffix: there are 76 tag-bearing operations, and at the end tag 10000 appears only in row 209 with coefficient 1 while tag 10001 appears only in row 298 with coefficient 1. This directly checks the suffix transfer instead of inferring it from the parent’s full-word identity. The two controller cleanups then rebuild the actual original packet encoders from unchanged first-X rows at Hub before any later source mutation.

The output difference is exactly:

| Endpoint row | Difference from parent |
|---|---:|
| B1 (209) | `-e394 = -d106` |
| B106 (298) | `-e305 = -d1` |

Every other one of the 400 output rows is exact parent. The two new residual rows become exact negatives, the hosted reverse residual rank is 57 rather than 58, and the same 24 prior hosted rows remain completed. No new completed reverse row is claimed. The original-coordinate forward debt remains 4,920 nonzero terms.

The parent-event map also checks causality at instruction granularity: every original operation is retained literally except the two packet descent MOVEs at parent events 3528 and 3661; the D MOVEs are retained literally at their hoisted positions. The full replay retires all 402 owner lifetimes and returns all 400 public rows to the parent charts.

## Exact phase review

The six new ordered chart pairs are `(127,129)`, `(127,226)`, `(226,1)`, `(129,99)`, `(1,3)`, and `(99,3)`, with ranks `1,1,7,7,1,1`. For every pair I independently reconstructed the canonical source and target frame circuits and checked the emitted recipe's signed Pauli action and exact phase. A phase-only mutation of each recipe kept the tableau but changed the exact state, so the phase check has a negative control.

## Whole-word and three-copy checks

The partial Q word has 5,510 instructions, 844 MOVE events, 402 owner lifetimes, and peak 29. Relative to its parent, it adds 264 ADD and 4 MOVE instructions; its exact movement-rank delta is `{1:+4, 7:+2, 9:-2}`. The public/raw MOVE multiset is unchanged. All six ordered chart-map recipes pass exact signed/global-phase checks.

I replayed the explicit three-copy composition on all 2,280 basis directions and compared all 1,480 common outputs and all 800 private outputs against the separately composed exact map. All endpoint coefficients and final charts matched. The complete caller profile reconstructed from the pinned invoice is:

- 83,881 ordinary instructions, 7,998 MOVEs, 858 owner lifetimes, peak 43.
- Productive count 31,296; paid count 156,060; integer rank surplus 4,380.
- Independently tightened 199/200 movement moment per rail is at least `12318403638244423212792142894049/1200000000000000000000000000000` (about 10.2653363652).

The frozen result uses a slightly more conservative lower enclosure: its 30-decimal root routine rounds the exact rank-1 root `1^(199/200)` upward by one `10^-30` unit. The resulting lower moment is smaller by only `20499/250000000000000000000000000000` before division by 36; its interval still contains my independently tightened interval and remains strictly positive. This has no effect on the invoice conclusion.

The three-copy invoice is for this exact partial rail. It does not establish a complete endpoint map: the 4,920 original-coordinate forward debt and 57-dimensional reverse response remain. The separate uniform compiler, precision, analytic-recovery, and strict-supplier obligations remain outside this review.

## Frozen review files

- `replay.py`: full 400-input exact replay, causal sequence and tag checks, endpoint rank and bill.
- `phase_check.py`: independent signed-phase verification of all six new chart maps.
- `replay_m3.py`: full 2,280-input composition replay and exact invoice/profile check.
- `RESULT.json`, `PHASE-RESULT.json`, `M3-RESULT.json`: machine-readable receipts.

The exact reviewed source and reviewer-file hashes are recorded in `MANIFEST.json`.
