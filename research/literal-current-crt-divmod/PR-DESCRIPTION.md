## Why this change is needed

The current source-to-header/key path still relies on the encoded CRT
producer's source arithmetic. Its exact Word implementation of division
does not itself supply a literal physical call at changing allocator slots.
Replacing it also changes temporary allocation events, so the earlier
unchanged-event entry argument cannot simply be carried over.

## Exact result

This package implements one fixed336150-location68-role graph for the
actual one-left/one-right current leaf's sixth raw division. The proof
identifies that call as left modulus divmod right modulus and derives its
unsigned high-bit margin from the actual precision guide.
The64 numerical roles are eight borrowed guards and56 existing owned Word
ports. Four six-bit descriptors use paid literal64-port dispatch and explicit
eight-cell grants on existing pre-header private owners.

For P>=4 the exact logical count is
`18P²+36P+458+(12P+9)popcount(floor(N/D))`.
Numerical reads expand to30 literal instructions and writes/moves to31,
including selector returns. Full literal setup/division/output retirement
costs at most `2^14(P+2)²`; finite-slot metadata and physical allocation
remain separately charged. A weak live/free-slot bijection proves the
unchanged source continuation despite different temporary allocation events.
Unordered disjoint cleanup is handled explicitly, and histories are charged
on their real physical owners.

## Novelty and dependencies

This is an actual-call implementation and ownership-interface result.
Restoring division, CRT arithmetic and generic finite composition are prior
work. Exact dependencies include CrocSwap/integer-mult-bounds#5053,
CrocSwap/integer-mult-bounds#5219, CrocSwap/integer-mult-bounds#5353,
CrocSwap/integer-mult-bounds#7352 and CrocSwap/integer-mult-bounds#7388.
The immediate unchanged header/key dependency is
[CubeJerry commit4c7cee36538bb48dc2598806af2ca42554fa63c0](https://github.com/CubeJerry/integer-mult-bounds/commit/4c7cee36538bb48dc2598806af2ca42554fa63c0).
Base remains `e54523517d0f03e58352e647c403a5af3e525a57`.
Exact byte/blob pins and all predecessor notices are included.

## Verification

From `research/literal-current-crt-divmod`:

```bash
python -I -W error -B check_dispatch.py
python -I -W error -B test_core.py
python -I -W error -B test_join.py
```

Each prints status PASS; all three also run under `-O`.
The structural check covers every numerical access at all64 slots. The
bounded arithmetic check covers124 cases through P=33 and retained larger
histories. Six actual current source/payload roundtrips include24 separate
old-divmod counterfactual owner comparisons at six allocator fingerprints.
Meter checks establish that HostedWord actions charge the arena once and
the backing Port zero times; descriptor actions are separately counted.
Malformed and returning controls detect wrong ports, stale descriptors,
incorrect quotients, live-input corruption and incomplete retirement.
Independent review is integrated separately by the lead before publication.

## Limitations and kappa status

**No new kappa.** The full multiplication bound remains conditional. This
does not discharge any of the five full foundational assumptions. Other
source primitives/control, numerical admission, source lease/acquisition,
finite metadata binding and complete source/radix tariff remain explicit.
The actual payload join inherits fixed13-bit codewords with arbitrary12-bit
opaque payloads. Costs are a complete vector of existing models; no speedup
is inferred by adding unlike units. Malformed-core rejection does not claim
rollback or head cleanup.

## Credit

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance.
Credit JoyboyBrian, Ali Romman, Nick Petalas, the exact current source/leaf
authors, and the CubeJerry B4--B9 predecessor packages. Apache2.0 notices
and exact source provenance are retained in the package.

## Executed independent review

`review/REVIEW.md` uses a separate sparse CPU, direct integer oracle and allocation-only source model: all22272 dispatch paths, five full lifecycles, two actual roundtrips and twelve boundary bijections. A returning wrong-phase mutation passes endpoint restoration but fails source typing; malformed and returning corruption controls also pass. Normal/optimized receipts agree. Both review commands are registered in VERIFY.json. The complete package gate executed all eight commands successfully.
