## What this changes and why

The current direct CRT payload caller still enumerates physical records and emits destination keys through a host loop. This package lowers exactly that `prepare_keys` seam into one fixed 21135-instruction graph on twenty-two physical roles. It invokes the unchanged published whole-row controller, writes into the actual original key cells, preserves opaque payloads and pays every move needed to return the payload head.

**Scope: exactly the fixed thirteen-bit codeword / arbitrary twelve-bit opaque payload ABI.** Height, precision and record count are uniform. General payload widths and the full CRT/multiplier caller are outside this contribution.

## Exact result

For h>=1, p>=h+1, N=2^h and the stated compatible descriptors/owner grants, both forward and inverse entries execute exactly N complete wire routes and N(2h-1) point queries. They produce the correct padded-rotation destinations, restore all heads/private histories and leave the owned row zero.

The complete cost is the sum of all N unchanged route costs plus **N(156h+126)+18h+203** literal instructions. The included payload-action subcount is **N(117h+66)+156**, with exactly 13Nh validated key writes. History is charged as a fixed per-role union, preserving prior larger extents.

The inverse entry generates inverse keys; it does not undo arbitrary key overwrites. Full forward/sort/inverse/sort restoration of original keys requires their original physical-position invariant. The proof and a counterexample explicitly expose that boundary.

## Novelty and exact predecessors

Canonical base: `e54523517d0f03e58352e647c403a5af3e525a57`.

The immediate dependency is [CubeJerry commit 4ccf407](https://github.com/CubeJerry/integer-mult-bounds/commit/4ccf407db96c7797dc3c83d90b033551f7d52c76), `research/literal-current-wire-row-controller`. Both whole-row copies are instruction-for-instruction authenticated, with only fixed control-flow relocation and return substitution. The B5 point adapter/current caller is inherited from [be17dd21](https://github.com/CubeJerry/integer-mult-bounds/commit/be17dd21af36a8b0546942299ebca7b1c83c4675).

CrocSwap/integer-mult-bounds#7504 supplies Nick Petalas's rotation formulas; CrocSwap/integer-mult-bounds#7388 and CrocSwap/integer-mult-bounds#7352 supply the actual encoded-source/payload lifecycle. The prior literal binary key/radix work, including CrocSwap/integer-mult-bounds#4982 and CrocSwap/integer-mult-bounds#5015, is retained credited work. This package's new result is the complete physical all-wire control and exact invoice, not those primitives.

## Reproduction and checks

```sh
python3 -I -W error -B research/literal-all-wire-crt-keys/verify.py
python3 -I -W error -B -O research/literal-all-wire-crt-keys/verify.py
```

Both author modes report PASS and produce identical receipts. Checks cover all 47 retained source objects, every one of 20246 embedded route instructions, 112 complete key passes, 1008 wire routes and 6096 point queries, with exact costs, key writes, full history and physical head restoration. Two actual current-source forward/sort/inverse/sort joins preserve the original source, opaque payload and identity keys. Returning semantic corruption, missing cleanup/head return, malformed ABI, owner alias, stale actual offset and wrong inverse controls are detected. The default verifier is read-only.

The actual modulus-three/left-two case costs 24421/24577 literal key-pass instructions and retains the exact B6 query/route workload. Full source, remaining marker/payload and radix costs are separately reported without double counting. Finite replays do not substitute for the uniform proof.

## Limitations and kappa status

The actual source/header provider, owner/window acquisition and remaining source/radix orchestration remain inherited. The graph is a fixed finite-alphabet machine with an actual unit-bit payload port; no unproved common whole-caller symbol/bit tariff is asserted. Failure rollback and arbitrary-key-overwrite inversion are not claimed. Prior larger backing is retained rather than treated as freed stock.

**No new kappa.** This is a uniform literal-interface/verification contribution and a bounded actual caller join. All five selected foundational assumptions remain, and the complete multiplication bound remains conditional.

## Credit

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance in research, implementation, proof, model-assisted independent review and packaging. Nick Petalas, Ali Romman, JoyboyBrian, Cinna Davis and the originating source packages are credited in `NOTICE.md`; exact original notices and Apache-2.0 license files are retained. Independent review evidence is separate from author regression receipts and does not claim formal-kernel or human acceptance.
