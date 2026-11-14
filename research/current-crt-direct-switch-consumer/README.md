# Route an actual encoded CRT leaf with direct canonical switch queries

This package connects the actual current numerical lease of
[CrocSwap/integer-mult-bounds#7388](https://github.com/CrocSwap/integer-mult-bounds/pull/7388)
to the [literal direct predicate](https://github.com/CubeJerry/integer-mult-bounds/commit/56335a406469fad85e88ff72820d506d8bea6f63)
and the original physical radix payload mover. It emits a uniform 2500-instruction,
twenty-tape query-and-consume graph. The actual offset, padded headers and current
wire are read from physical tapes; the produced Boolean changes the actual
target bit and is then erased with every private copy.

The predicate formulas are Nick Petalas's
[CrocSwap/integer-mult-bounds#7504](https://github.com/CrocSwap/integer-mult-bounds/pull/7504).
Their fourteen-tape implementation is retained unchanged. The new results are
the paid representation/consumption interface, its exact complete cost, and
the actual source/payload join. **No new kappa.** The full multiplication bound
remains conditional and all five foundational assumptions remain.

## Uniform result and scope

For h>=1, precision p>=h+1, 1<=s<=2^h, 0<=a<s, 0<=j<2h-1 and a current
h-bit address x, supply the stated matching height/unary-width ABI and a
physical target k in 1,...,h. The adapter applies canonical switch bit b to
that target, returning `x xor (b*2^(k-1))`, with all other borrowed bytes and
heads restored and all fourteen private owners blank. For a network layer,
the target must satisfy `k-1=min(j,2h-2-j)`; the caller's encoded counter/head
invariant establishes that relationship.

The exact new overhead is

`30p+74h+6*bit_length(h)+10k+261`.

Including the frozen predicate, the complete local bound is

`T <= 1024(h+3)^2+128(p+h+3)`.

Historical increment is at most `p+16(h+4)` beyond entry backing. Every p-bit
header scan, copy, zeroing, target seek, Boolean consumption and return is
charged. Earlier larger blank histories stay retained. The theorem assumes
distinct owners, physically accessible frames and granted blank windows.
Malformed framing or dirty grants have no general rollback promise.

The retained outer source controller still uses its existing symbol-action
model. This package supplies a complete cost vector and preserves that
limitation. It does not claim a single literal implementation or common
tariff for the whole balanced CRT stage or multiplier.

## Actual source and same-workload evidence

The exact predecessor fixture has moduli `(5,7,3,2)`, widths `(3,3,2,2)`,
coordinates `(3,2,1,1)` and four opaque tags `(293,730,905,3681)`. Its current
lease yields h=2,p=5,s=2,a=1. Forward swaps the first two tags and leaves
the padded positions fixed. Inverse returns the same complete source,
payload, key bytes, physical backing objects and heads.

The original ROM implementation was freshly replayed and matched its
published receipt exactly. On each direction's identical workload the new
path uses twelve direct queries, totaling 21910 literal instructions; the
original ROM producer uses 2363816 instructions. The source counts remain
113295 forward and 372489 inverse, the literal radix count remains 43162,
and payload adapter bit actions remain 1694. These are separate model
components, not a claimed common-tariff or asymptotic speedup. Repeated ROM
reuse may change the comparison.

An actual left-modulus2/right-modulus3 variant exposes stale current wires:
the offset is2, and forward destinations are `[2,0,1,3]`. Additional admitted
source cases cover zero offset, invalid left coordinates and padded right
coordinates. The retained source rejects unit modulus; the standalone point
theorem's broader s=1 domain is stated separately.

## Reproduction and source pins

Canonical base is `e54523517d0f03e58352e647c403a5af3e525a57`. The retained
source caller is #7388 at `d6f4a69202ad0bba4a915f4d4f3eaba1fe431c86`; its
forward/inverse lineage is #7352 at `8c0e55c9ba25ff2c8199b01539a4d56ae71a1473`.
SOURCE-PINS.json binds all thirty retained inputs by bytes, SHA256 and Git
blob. SOURCES.json holds canonical task/selection provenance separately.

```
python3.12 -I -W error -B research/current-crt-direct-switch-consumer/verify.py
python3.12 -I -W error -B -O research/current-crt-direct-switch-consumer/verify.py
```

Both modes are read-only and pass with identical receipts. Only an explicit
`--receipt PATH` writes output. The check covers 2111 point invocations,
five actual forward/inverse source/payload round trips, fourteen controls,
and a complete fresh replay of the old baseline. Controls distinguish stale
offset, stale wire, wrong inverse row order and suppressed Boolean use from
successful cleanup. The exact proof, scopes and all costs are in PROOF.md.

## Open next questions

1. Lower the retained source and row controller into one common literal
   machine with a complete bit tariff. Its present source/numerical and
   outer-controller symbol meters are explicit remaining boundaries.
2. Bind the synchronized two-target path of
   [CrocSwap/integer-mult-bounds#7390](https://github.com/CrocSwap/integer-mult-bounds/pull/7390),
   including target order, current values, all padded fibers and inverse.
   This package deliberately stops at one actual four-tag leaf route.
3. Compare admitted repeated workloads against resident ROM reuse, including
   acquisition, retained history, transport and eventual disposal. The current
   upper bounds and one measured vector do not settle that question.

Credit @CubeJerry and the originating source authors listed in NOTICE.md.
Substantial OpenAI assistance was used in implementation, proof and review.
