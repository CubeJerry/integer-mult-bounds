# Generate all padded CRT keys with one literal physical pass

This package removes the remaining host all-wire/key-emission loop at the exact current CRT payload boundary. One fixed graph enumerates every physical position, invokes the unchanged complete per-wire row controller, validates and writes its destination key into the original key cells, then performs a fully paid scan back to the actual payload origin. It restores all heads and private histories on success.

**The ABI is restricted to one fixed thirteen-bit codeword containing twelve arbitrary opaque payload bits per record.** It is uniform in the encoded height/precision and number of records. It does not claim a variable-payload-width implementation. The inverse entry generates inverse-routing keys; it does not reverse arbitrary key overwrites. A complete sorted physical roundtrip restores the original keys when they initially equal their physical positions, as in the retained actual caller.

## Exact result

For h>=1, p>=h+1, N=2^h and matching admitted descriptors, the 21135-location graph uses twenty-two physical roles and two fixed entry ports. It contains two unchanged copies of the published B6 whole-row controller, all on the same physical owners. Every record receives its correct forward or inverse padded-rotation destination.

If R_d(i) is the complete predecessor route bill for physical wire i, the new exact instruction count is

`sum_i R_d(i) + N(156h+126) + 18h+203`.

This includes all header-independent key-pass work, encoded carry, copies, full old-key validation, every output bit, all private zeroing and the full payload return. Payload reads/writes/moves are already included; their exact subcount is `N(117h+66)+156`, with exactly 13Nh key writes. Private work is a per-role historical union across all N(2h-1) point queries, not a fresh bank per call.

`PROOF.md` gives the full typed ABI, all-height invariant, exact counts, complete footprint and inverse-overwrite boundary. `key_pass.py` is the graph constructor, `hardware.py` the physical instruction interpreter and fixed bit-port rename, and `join.py` the authenticated one-function actual-source seam.

## Actual caller and executed evidence

The primary normal and optimized runs test 112 complete key passes: all heights through three with every legal modulus/offset and both directions; ten h=5,s=17 passes; and translated-origin/retained-history cases. These execute 1008 whole-wire routes, 6096 point queries and 17881356 literal instructions. The direct destination oracle, payload write locations, all physical heads and complete histories are checked.

Both the exact CrocSwap/integer-mult-bounds#7388 four-tag source and the admitted modulus-three/left-two variant execute full forward/sort/inverse/sort roundtrips. The latter preserves the source and original identity keys with literal key-pass costs 24421 and 24577, including the unchanged B6 route bills 22430 and 22586. Per leg, the other measured coordinates are 382 remaining marker actions, 156 remaining payload-bit actions and 43162 retained radix instructions; encoded-source symbol charges are 118045 and 360151. These are a cost vector, not a newly established common-tariff full caller bound.

Controls include a missing embedded return, three returning semantic corruptions with clean heads/private work, omitted index cleanup, omitted paid payload return, malformed key/payload frames, a height/width mismatch, owner aliasing, stale actual numerical offset and wrong actual inverse routing. A separate overwrite example demonstrates why arbitrary old keys are not restored. Finite checks support the source join and error detection; they do not replace the uniform proof.

## Reproduce

From the repository root:

```sh
python3 -I -W error -B research/literal-all-wire-crt-keys/verify.py
python3 -I -W error -B -O research/literal-all-wire-crt-keys/verify.py
```

Expected output reports `PASS`, 21135 instructions, twenty-two roles, 112 complete key passes and two actual roundtrips. The default is read-only. Use `--receipt PATH` to explicitly save the full deterministic JSON evidence. Exact dependency pins are in `SOURCE-PINS.json`; canonical orientation pins are in `SOURCES.json`.

## Novelty and inherited boundaries

The immediate published predecessor is CubeJerry commit 4ccf407db96c7797dc3c83d90b033551f7d52c76, `research/literal-current-wire-row-controller`. Its all-row computation, the B5 current-point adapter, Nick Petalas's #7504 formulas and the existing literal binary radix are unchanged credited inputs. This contribution is the explicit uniform physical all-wire/key pass, its exact return and cost proof, and its actual source/payload join.

Source/lease acquisition, compatible header construction, physical owner/window grants and remaining source/radix orchestration are inherited. Previously larger histories remain retained. Failure rollback is not claimed. No new kappa; the complete accepted multiplication bound remains conditional with all five foundational obligations still present.

## Open next questions

1. Lower the actual encoded numerical lease/header producer into a compatible literal graph, including acquisition, staging, return and full costs.
2. Join the already literal stable radix pass to a fixed complete h-pass controller with its physical register/bucket retirement and no host loop.
3. Specify and lower the actual variable payload-width interface needed for larger caller values; the twelve-bit restriction cannot simply be erased from this theorem.
4. Compare full admitted direct-query and retained-ROM workloads, including source work, backing history and disposal, under one common machine tariff.

The new work was prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original author and predecessor notices are retained in `NOTICE.md` and the bundled source files. Independent review assets are separate from the author's replay.

## Independent verification

The complementary review passes with no scientific edits. A separate sparse
interpreter executes ten complete passes (430,130 instructions), 39
width/carry helper cases through width257 and returning semantic/cleanup
controls. It checks all 20,246 embedded predecessor instructions, the exact
all-record and cost proofs, and the current source cost vector. The 1,356
payload actions inside the four-record graph are counted once; the external
156 payload and 382 marker actions per leg remain separate. The full external
source/radix providers are inherited rather than replayed as new independent
evidence. Both reviewer modes produce identical receipts.

See [the independent review](review/REVIEW.md) for scope and credit. From the
repository root:

```sh
python3 -I -W error -B research/literal-all-wire-crt-keys/review/independent_check.py --package research/literal-all-wire-crt-keys
python3 -I -W error -B -O research/literal-all-wire-crt-keys/review/independent_check.py --package research/literal-all-wire-crt-keys
```
