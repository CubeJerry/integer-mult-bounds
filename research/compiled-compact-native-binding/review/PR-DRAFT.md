# Bind retained Compact XROW to the current coded field and descriptor

Base: `7c49fe32c55de02c2c873655c804b16e4c3fef0a`.

The current compiler/row dispatcher emits selected-bit XOR records but leaves
their complete coded-field provider explicit. This package supplies a
source-level fixed-control physical refinement of that boundary using the
retained #3055 Compact engine and #5445 record semantics.

It constructs the native layout from the current 23-field encoded descriptor,
converts the selected-bit offset, maps the retained alphabet to actual
twelve-physical-bit codewords, preserves every numeric delimiter and spectator,
and erases the full current-call workspace. Both source orders and the separate
width-one physical operation are implemented. The complete bill includes setup,
guards, bridge scans, ordinary calls, exceptional repair, cleanup and per-role
retained backing.

The actual physical fixtures execute four/twelve ordinary calls and four/ten
rotations, compare every complete output record with an independent address
oracle, and test translated origins, unchanged context and whole-workspace
return. Additional controls cover incorrect rho, omitted cleanup, malformed
codes, nonempty parking, source drift and larger-history reuse. A separately
authored sparse-hardware review checks 8,232 codec triples and seven negative
controls. Exact source pins and normal/optimized receipts are included.

Reproduce with Python 3.12 and the standard library:

```sh
python -I -B scripts/research_package.py --package research/compiled-compact-native-binding
```

Expected final status:
`PASS_REGISTERED_RESEARCH_PACKAGE research/compiled-compact-native-binding outcome=completed`.
Executed checks comprise both full physical endpoint modes, both portable
independent codec modes, and the package metadata/pin validator. The detailed
commands, deterministic hashes, times and limitations are in `VERIFICATION.md`.

This is XROW-only. The package does not emit A's flat transition tables or claim
execution through `Controller.execute_table`; the source-to-table exporter is
explicitly open. It retains the existing Compact/ordinary, record-lift,
compiler/lifecycle and phase predecessor credit, including #3087. The historical
ordinary exponent exceeds the selected node exponent by
`5000439/3500000000`, so this result does not establish the selected tariff.
**No new κ.** All five selected assumptions remain unchanged.

Prepared for @CubeJerry with substantial OpenAI assistance in research, proof,
implementation, verification and prose. No independent human or proof-kernel
admission is claimed.
