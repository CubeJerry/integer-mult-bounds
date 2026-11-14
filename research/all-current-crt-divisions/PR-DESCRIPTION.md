## Why this change matters

The current CRT numerical producer still depended on its raw `Unsigned.divmod` provider after the previous literal package replaced one actual singleton-leaf call. This package removes every such fallback at the exact admitted source interface, including calls inside nonleaf production and Euclidean inversion. It does not change the selected certificate or claim a new multiplication exponent.

## Exact result

The unchanged 336,150-location, 68-role divider from CubeJerry/integer-mult-bounds@c4ab5dab6914a04cb86d1fe54eb763b35cc7eeb1 now serves both raw call sites in the pinned forward and inverse current producers. The new source binder dispatches every call in those producer scopes to that graph. No half selector, call ordinal or arithmetic fallback remains.

For `m` left records, `t` right records, `v` valid right records and Euclidean lengths `e_i`, the exact count is `J = 3m + 2t + v + 2 sum(e_i)`. The retained numerical admission proves `J <= (P-2)(4P+5)`. All divisors satisfy the existing literal core's positive, strict half-range bound. The complete new division subset costs at most `89 + J*(930P² + 1395P + 14322) < 2^15(P+2)^4` literal instructions. Finite owner metadata and grant services are separately charged, not hidden in that bound.

The old and new output allocations are related by a weak slot bijection fixing all incoming live values. The proof composes this relation through the actual source and unordered final cleanup, and charges the actual physical history unions instead of transferring old per-slot histories. The physical Entry ABI has exactly eight protected guard roles and 56 owned Word roles, plus four explicitly enlarged descriptor grants.

## Novelty and predecessors

CrocSwap/integer-mult-bounds#5053 already proves the numerical ranges and constant live stock; those results are credited and reused. CrocSwap/integer-mult-bounds#5219 and CrocSwap/integer-mult-bounds#5353 supply the entry and mixed-row interfaces. CrocSwap/integer-mult-bounds#7388 supplies the actual current leaf payload boundary. The preceding literal divider at `c4ab5dab6914a04cb86d1fe54eb763b35cc7eeb1` supplied the graph and one singleton-leaf substitution. This change adds complete source-provider elimination and its repeated owner relation, rather than a new generic division algorithm. All exact origin bytes and notices are retained in `SOURCE-PINS.json` and `inputs/`.

## Reproduction and checks

Run from this package directory:

```sh
python -I -W error -B source_check.py
python -I -W error -B verify.py
python -I -W error -B -O source_check.py
python -I -W error -B -O verify.py
```

The registered source checker authenticates 76 retained objects, the two exact raw call sites in each producer, and the unchanged divider graph. The primary replay executes 355 literal raw divisions, including 52 unit divisors and 104 incoming allocator fingerprints, in 21,984,763 divider instructions. Three actual source/payload roundtrips and one complete source-only roundtrip include forward and inverse nonleaf production, longer Euclidean chains, padding and reused histories. Every normal and optimized receipt is byte-identical.

During actual positive execution the old provider is unavailable and its call count is zero. The old/new full numerical, source, key and payload outputs agree. Counterfactual allocator checks run only after the physical legs, never as runtime providers. The meter audit subtracts exactly the old raw-divmod actions and includes every new native and descriptor action once. Out-of-producer calls, foreign arenas and an inserted fallback are detected. A separate independent review uses its own sparse CPU, direct CRT-idempotent and allocation-only oracles; it passed 192 calls and returning descriptor/fallback/scope controls. Review assets are integrated separately by the lead.

## Limitations and open obligations

The source binder, finite allocator metadata, descriptor acquisition and the other arithmetic and source controllers remain supplied and charged. The complete invoice is a vector of the retained models; no unproved common tariff or global compiler closure is asserted. The source/payload join retains the fixed 13-bit record code and arbitrary 12-bit payload contract. The separate complete source-only roundtrip does not extend this to a full payload transform. Verification counters, snapshots and replay watchdogs are test instrumentation, not literal-machine state or part of the universal theorem.

**Kappa status: No new kappa.** The selected full multiplication bound and its inherited assumptions remain unchanged. The next source-specific questions are the combined remaining compare/add/subtract providers, finite encoded owner control, and the eventual common physical tariff.

## Credit and assistance

Contributed by Jerry Chen / @CubeJerry. Predecessor research and originating pull requests are credited above and in `NOTICE.md`. OpenAI assistance was substantial in derivation, implementation, proof writing, independent model-assisted review and publication preparation. The proof and bounded checks are distinct evidence; neither is presented as an unconditional multiplication theorem.
