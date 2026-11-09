# Current coded-field binding for retained Compact XROW

Prepared for **@CubeJerry**, with substantial OpenAI assistance in source
analysis, mathematics, implementation, tests and prose. Apache-2.0.

This package implements one current native service: the selected-column XOR
record emitted by the compiler/occurrence route binder. It reads the actual
twenty-three-field binary descriptor, runs the retained physical Compact
implementation on the current coded field, and returns the complete field,
unchanged descriptor and blank private current segments. Both source orders and
the separate width-one case have executed through the actual physical codec.

The result is a **source-level finite-control, fixed-tape refinement**. The
package does not emit A's flat transition-table format, and does not claim a run
through `Controller.execute_table`. That remaining exporter does not change the
proved geometry or encoding endpoint, but it is still a concrete integration
task. The quantified theorem and its retained premises are in [PROOF.md](PROOF.md).

## What this adds

The retained [#3055 Compact implementation](https://github.com/CrocSwap/integer-mult-bounds/pull/3055)
already supplies its identity, exceptional repair, rotations and ordinary
boundary. [#5445](https://github.com/CrocSwap/integer-mult-bounds/pull/5445) already
supplies the selected-column record lift. The current source
[owned lifecycle](https://github.com/CubeJerry/integer-mult-bounds/tree/ab239cb6ee884e7a900dd9101c34448077fad0b0/research/compiled-owned-bank-lifecycle)
and [row dispatcher](https://github.com/CubeJerry/integer-mult-bounds/tree/5c59d247d51c6e1fca0dead3ed2139b6802b3a15/research/compiled-row-stock-dispatch)
leave numerical providers explicit. This package connects those specific
interfaces:

* It derives the retained ten-field Compact layout using encoded arithmetic.
  Existing suffix coordinates become opaque complete records; the preparation
  step moves no field data. Arbitrary non-power-of-two row quotients are allowed.
* It converts the current left-counted offset to the retained low-bit offset:
  `rho_native = K - 1 - rho_B`. It preserves all other address bits and complete
  signed numeric records, including both component delimiters.
* It maps every old symbol `0..13` to four virtual binary symbols, each encoded
  by A in three physical bits. Thus one old symbol occupies exactly twelve
  physical positions. Reads, writes, movement and local origin checks are
  actual counted operations on A's ports.
* It imports and exports the complete field with lockstep guides and exact
  frontier checks. No generic binary length counter is decremented once per
  payload bit. Native work starts in blank current segments and cleanup erases
  this call's whole reached prefix.
* It binds actual `selected-bit-xor` tokens emitted by the pinned compiler,
  lifecycle lowerer and route binder. The separate `f=1` operation is a physical
  four-bucket digit permutation, rather than an invalid zero-length call to the
  retained positive-width Compact control.

The complete numeric record has two fixed-width signed little-endian components
with delimiters. Address helpers and spectators may be dirty. They are restored
by the inherited complete Compact endpoint, rather than assumed zero.

## Full cost and its precise limit

Let `C` be the actual outer/row product, `J` the complete physical row length,
`V=CJ`, `h=(f-1)G`, and `a'=back_start+h`. The opaque suffix record has
`R=record_bits*2^(within_bits-a')` bits, so `2^a' R=J` exactly. Put
`M=C*2^a'`, `A0=2+a'+ceil(log2(R+1))`, and

```
delta = min(1, (f-1)*(2*2^(-G) + 8*2^(G-K))).
```

With the completed ordinary bill `T_B`, the retained source charge is

```
T_compact <= s * sum_(j=1)^C T_B(J,(f-1)G)
            + O(V + M*A0^6 + delta*M*A0*(R+A0)),
```

where `s=4` for an earlier source and `s=12` for a later source. Each row really
causes those calls. The new coded wrapper adds a fixed simulation factor,
`O_N(V+(E+1)^4+Q)` setup/bridging, and `O(Z+Q)` physical retirement, where `E`
is header length, `Q` is the fixed role count, and `Z` is the sum of current-call
high-water extents. The complete source-control factor includes local guard
checks as well as primitive symbol operations. Every newly reached cell already
costs movement or writing, so cleanup preserves this complete bound's shape.

For production geometry `H=dG`, `f<=d/2` yields `R>=record_bits*2^(dG/2)`.
With the retained root regime and actual `G=4ceil(log2 p)+6`, `K=128G`, the
extra polynomial and exceptional terms are absorbed. A completed supplier with
exponent `tau_B` therefore gives the scoped favorable rate
`O(V*(1+((f-1)G)^tau_B))`. Its workspace and per-role retained backing remain
explicit in the proof. Fresh blank current segments prevent a small later call
from scanning an earlier larger call's backing; they do not shrink that backing.

The historical supplier has `tau_B1=99830289/100000000`. The selected #6030 node
requires `tau_node=872264919/875000000`, and

```
tau_B1 - tau_node = 5000439/3500000000 > 0.
```

Consequently this historical upper bound alone does **not** establish the
selected tariff. This is an upper-bound implication limit, not an algorithmic
lower bound. The package makes no selected `.0034` saving claim, no new kappa
claim, and no change to the selected assumptions `native_all_columns`,
`owned_erasure`, `compiler`, `precision_tape`, or `analytic_recovery`.

## Executed evidence

The complete normal and optimized programs compare the same exact result in
[RESULT.json](RESULT.json). The payload fixtures contain 128 distinct complete
signed records, totaling 3,840 physical input bits. The helper widths are
deliberately small; a `q=2` elementary ordinary supplier makes actual execution
feasible and is not an eligible-prime faster-rate certificate.

| Actual endpoint | Ordinary calls | Rotations | Physical actions | Retained work cells |
|---|---:|---:|---:|---:|
| Earlier source, `f=2` | 4 | 4 | 703,700,513 | 674,070 |
| Later source, `f=2` | 12 | 10 | 1,459,898,328 | 674,310 |
| Separate `f=1`, `K=2` | 0 | 0 | 25,637,106 | 240,282 |

The addressed-record oracle is separate from the implementation. Each fixture
checks every output bit, exact field frontier, restored heads, unchanged header,
blank private segments and untouched ancestor sentinels. A six-row reuse case
retains 215,934 cells; the subsequent smaller call takes exactly its fresh-call
7,566,433 actions while retaining that larger backing.

Separate encoded producer cases satisfy `H=dG`, include nonadjacent pairs and
an outer count above `10^70`. The record-lift check covers 2,040 complete column
cases. Actual negative controls catch incorrect rho conversion, omitted cleanup,
wrong owners, malformed codes, altered source bytes and invalid geometry.

The independently authored codec review uses sparse physical storage. It checks
8,232 neighboring-symbol triples, all fourteen symbols at three translated
origins, 32 fresh-blank extension steps and seven adverse controls. Its scope is
the new codec and local ownership guards; it is not an independent verification
of the old B1 or Compact theorem. Exact copied hashes and commands are in
[VERIFICATION.md](VERIFICATION.md).

## Replay and source integrity

Use Python 3.12 and the standard library. From the repository root:

```sh
python -I -B research/compiled-compact-native-binding/verify.py
python -I -O -B research/compiled-compact-native-binding/verify.py
python -B scripts/research_package.py --package research/compiled-compact-native-binding --check-only
```

The complete normal run takes approximately eight to nine minutes on the recorded
environment. `VERIFY.json` registers both complete modes and both independent
codec modes within the repository replay budget. `--suite quick` is a shorter
development check; it does not reproduce the two full Compact endpoints.

`DEPENDENCIES.json` pins 32 exact public exports and 51 bounded runtime/NOTICE
archive members by Git blob and SHA256. The ordinary archive hashes are anchored
in the authenticated public loader. All replay dependencies are package-local;
no network, repository checkout, archive download or external package is needed.
The bootstrap replaces repository discovery, not the retained theorem verifier,
and does not claim to replay the old complete selected proof chain.

## Open next questions

1. Export this bounded source control into A's flat transition-table syntax and
   run the actual lifecycle controller with these native events. Start with the
   fixed codec/parking fragments and emitted service tokens; preserve the exact
   role inventory and successful-return contract.
2. Bind a completed ordinary supplier with a sufficiently small exponent. Its
   all-size endpoint, complete time bill, stock and backing contracts must meet
   the current caller. The historical B1 estimate cannot simply be renamed.
3. Join the remaining phase/nonpermutation services to the current signed
   record format. Credit the existing physical Gaussian phase predecessor
   [#3087](https://github.com/CrocSwap/integer-mult-bounds/pull/3087); the remaining
   work is its current-format/descriptor/cost binding, together with the other
   retained precision and recovery obligations.

Credit remains with the Compact identity and guard/repair authors, Jose Manuel
(`jmbarrancoml`), Douglas Colkitt, Mark (`Matarener`)'s record lift, and the
contributors credited by the unchanged NOTICE and ordinary exports. This
package claims no independent human review or proof-kernel admission.
