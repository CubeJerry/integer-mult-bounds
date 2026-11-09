# Verification record

Prepared for @CubeJerry with substantial OpenAI assistance. This records finite
execution, source authentication and a scoped proof review. It is not theorem
admission, a proof-kernel certificate, or independent verification of the old
Compact/B1 theorem.

## Environment and frozen sources

The reported runs use Python 3.12.14, standard library only, on 2026-11-09.
The repository base is `7c49fe32c55de02c2c873655c804b16e4c3fef0a`.
`DEPENDENCIES.json` authenticates 32 exact public exports and 51 bounded archive
members before executing them. `SOURCES.json` records 13 canonical base
provenance rows. The task card is copied exactly from its pinned catalogue.

The current-input exports are the public fork commits
`ab239cb6ee884e7a900dd9101c34448077fad0b0` (owned lifecycle) and
`5c59d247d51c6e1fca0dead3ed2139b6802b3a15` (row/occurrence dispatcher).
The retained Compact export is canonical #3055. The ordinary and reference
exports retain their exact #2899 and #2250 heads, archive anchors and notices.
No mutable branch name supplies runtime code.

The final computational files have these SHA256s:

| File | SHA256 |
|---|---|
| `provider.py` | `3b7bb4f7940ffa9fafd34d25bbb1a9225e1b671924ed194ad012cb26251d7460` |
| `codec.py` | `60f94c991568981c1ae8633bbc9c4d3c259e2df0654e8720d7f4554737d8e136` |
| `binding_sources.py` | `e3b1cd40a2436381b3688aa3a5a740d402d08d0611dc43a629634bb1a6f7b299` |
| `source_binding.py` | `0682b173bc0ae9be2a79cf4338ffe35018dfe3a5cd2a4ebb5ec2c04a0809c169` |

The final whitespace gate removed one extra EOF newline from `provider.py`,
`codec.py` and `source_binding.py`. `review/WHITESPACE-REFINEMENT.json` records
the exact earlier/final hashes and compiled module hashes. Compiling the old
and final bytes produces identical serialized Python code objects in both
normal and optimized modes. `check_review.py` reconstructs the old bytes by
appending that one newline and repeats the equality check on every replay.
The full physical receipts below executed the earlier compiled modules; their
transfer to final source bytes uses this exact code-equivalence check. The
independent codec observer was separately rerun on the final file bytes.

## Complete physical replay

The normal result-generation run executed:

```sh
python -I -B research/compiled-compact-native-binding/verify.py --write-result
```

It passed all physical endpoints and controls in 505.432 seconds. The frozen
deterministic receipt hash is
`c2b3451c98c4f716e7c1e1e40ad0c1c2c68579f182ea49b3e69b9e3b5ec30357`.
The elapsed time is excluded from this hash. The complete output is retained in
`review/normal.log`; `RESULT.json` contains the full structured receipt.

The complete optimized comparison also passed:

```sh
python -I -O -B research/compiled-compact-native-binding/verify.py
```

It took 475.299 seconds and reproduced the same entire deterministic receipt;
its output is `review/optimized.log`. The comparison includes all physical
actions and retained-cell counts, not only the logical output or a PASS label.

The exact registered normal comparison then passed in 519.163 seconds:

```sh
python -I -B research/compiled-compact-native-binding/verify.py
```

Its complete output is `review/normal-replay.log`, with the same receipt hash.
Its modules were already loaded before the EOF-only cleanup; the code-equivalence
record above states exactly how this execution transfers to the final bytes.

`VERIFY.json` registers the complete normal and optimized receipt comparisons,
plus normal and optimized portable independent codec reviews. Each complete run
has a 580-second timeout allowance; each independent review has 20 seconds.
Those allowances total 1,200 seconds and are not observed running times.

The physical endpoints check all output records against a separately written
address oracle, original field extent, unchanged context, restored origins,
blank private segments and ancestor sentinels. Earlier/later `f=2` cases use the
actual retained Compact engine. They perform respectively four/twelve ordinary
calls and four/ten rotations. The separate `f=1` endpoint performs a real digit
permutation. No identity supplier or host payload callback is substituted.

The feasible payload fixture uses reduced helper widths and an ordinary `q=2`
elementary branch. Its 128 complete numeric records occupy 3,840 physical bits.
It is not the selected full root, a materialized selected uniform template, or
an eligible-prime faster-rate proof. Separate physical encoded-header cases
have `H=dG` and include an outer count above `10^70`; those tests construct
geometry without materializing the corresponding enormous payload.

The record-lift checker executes 2,040 all-column cases using #5445. Six exact
rational guard calculations preserve the exponent gap. Adverse checks actually
alter rho conversion, omit cleanup, bind a wrong owner, request runtime host
backing, introduce malformed symbols, alter a source export or present invalid
geometry. The rejected cases are listed in the receipt.

The reuse check runs the same physical ports through a small, six-row larger,
then small invocation. The two small calls both take 7,566,433 physical actions.
Their retained work backing is respectively 81,438 and 215,934 cells. This tests
current cleanup independently of historical allocation length; the proof states
the contiguous-prefix invariant and per-role maximum accounting.

## Independently authored codec review

The parent research worker authored the sparse-hardware observer independently
of this package's dense fixture/oracle. It uses a dictionary of physical cells,
unit head movement, and a separately written twelve-bit encoding formula.
It covers 8,232 neighboring triples over all fourteen symbols at origins 1, 7
and 19; 32 consecutive fresh-blank extensions; seven malformed/ownership
controls; and fresh-versus-after-large-history cleanup equality.

Its observed maxima per old primitive are 72 physical actions for a read,
68 for a write and 85 for a step. These measurements support the fixed primitive
bound, not a claimed constant for the entire guarded-control expansion. The
proof separately charges all local marker guards with a fixed `C_codec`.

The original files were supplied from the session's `recovery/` directory.
They are copied into `review/` without any source or path modification; the CLI
already takes the package and output paths explicitly. Original and copied
SHA256s agree:

| Exact copied file | Original and copied SHA256 |
|---|---|
| `independent_native_codec.py` | `827491e62d6288720ce54aec4791b34d500cd3edaa126f66b6a770fa82261120` |
| `independent-native-codec-normal.json` | `55975729a6cf56c60d0e7abdc962e4173bc71b4047a3c8dffb304435a042090d` |
| `independent-native-codec-optimized.json` | `55975729a6cf56c60d0e7abdc962e4173bc71b4047a3c8dffb304435a042090d` |

Both original direct portable executions passed. After the EOF-only cleanup,
the unchanged observer was run again in both modes. The resulting files
`independent-native-codec-current-normal.json` and
`independent-native-codec-current-optimized.json` each have SHA256
`c7737d83a48fc522036db751b3391b3724a168bfd444418d0fc7fa3fa92a4960`.
Every measurement and transcript hash agrees with the originals; only the
recorded codec source hash changes.

`check_review.py` checks all copied/current hashes and their relation, checks the
compiled-code equality, runs the unchanged script in an isolated temporary
directory, and compares its entire output with the current receipt. The normal
and optimized wrapper commands also passed:

```sh
python -I -B research/compiled-compact-native-binding/check_review.py
python -I -O -B research/compiled-compact-native-binding/check_review.py
```

This independent review covers the new codec and local ownership guards only.
It does not independently establish the retained ordinary rate, Compact repair
identity, selected Gaussian template, or a complete multiplication theorem.

## Metadata and retained obligations

The metadata/pin check passed with lazy network fetch disabled:

```sh
GIT_NO_LAZY_FETCH=1 python -I -B scripts/research_package.py \
  --package research/compiled-compact-native-binding --check-only
```

Missing local canonical blob objects were populated only from authenticated
package exports after their SHA256 and the base tree's existing Git blob IDs
matched. Canonical refs, index, sparse patterns and checked-out files were not
modified. This object maintenance does not substitute for source authentication.

The all-size proof remains a structured finite-control physical refinement.
No flat A table export, lifecycle `execute_table` join, complete old theorem
replay, selected tariff, phase service, precision discharge or new kappa is
claimed. The historical ordinary exponent and current selected exponent remain
distinct, and all five selected assumptions are retained.
