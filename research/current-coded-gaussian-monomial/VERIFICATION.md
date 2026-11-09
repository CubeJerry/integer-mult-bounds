# Verification record

Prepared for @CubeJerry with substantial OpenAI assistance. This records exact
executed checks and their limits; it is not proof-kernel or independent human
acceptance of the retained monomial, ordinary supplier, or multiplication theorem.

## Complete author replay

Python **3.12.14**, standard library only. Both complete commands executed
successfully on the final sources:

```sh
python3 -I -B research/current-coded-gaussian-monomial/verify.py
python3 -I -O -B research/current-coded-gaussian-monomial/verify.py
```

Each finished with `PASS_CURRENT_CODED_GAUSSIAN_MONOMIAL`. Their complete
`VERIFY.normal.log` and `VERIFY.optimized.log` are byte-identical, with SHA256
`e3e29810bf70092b43b0d02e9355dbfef03b00203cd589e7e9f30990f153653f`.
The canonical scientific object in `RESULT.json` has digest
`75d4884095a5df712af0054fd2081f737cfcf8f3fb7692ea7bbdd8b407c0a695`.
This latter digest is of its sorted compact `result` JSON, as the verifier
explicitly computes; it is not the byte hash of the pretty-printed file.

The individual normal/optimized case receipts reproduce the corresponding
sections of the complete result. The selected literal export is identical to
its `selected_control.source` section. These equalities were also checked
directly before commit. Physical counts, field values, cleanup and retained
backing are deterministic; elapsed wall time is excluded.

The full replay authenticates 100 copied files by Git blob and SHA256, rejects
an altered signed-phase source before import, checks all five retained selected
assumptions, then executes the actual physical fixtures described in the proof.
The source-controlled entry points use a new bytecode namespace for transitive
imports. Explicit loader imports compile authenticated source bytes directly.
No network, external source tree, native build or package installation is used.

## Separately authored sparse-hardware review

The reviewer was authored by a separate OpenAI-assisted research worker, using
its own serializer, sparse physical hardware, signed/address oracle, and adverse
provider subclasses. It does not import the author's fixture or oracle. The
production adapter is the object under test; the inherited phase and Compact
theorems are not independently reproved by these finite checks.

The review note and checker are copied unchanged:

| Artifact | SHA256 |
|---|---|
| `review/independent_current_phase.py` | `cd2aed187ef6a664f41c7799d3b66a0d1992ce46c1fb4f3546c3c9ca2e68b4ba` |
| `review/PROOF-REVIEW.md` | `feccc98c187c51901e8a8c3aa7ed671e742c9ae6f947470e1a3d8a56290a096b` |
| `review/RESULT.json` | `e07f54aa0d692cf28572eab7f87be3e6de1da59503bcc4eaa16ba274b51eeae4` |
| Reviewed `phase_adapter.py` | `42687d9cd5f8f4a964e2ddd79aa404432ff26f9ebb55e9c069bbba30f0c3044f` |
| Reviewed `phase_binding.py` | `7624e2421c4188f7339231263d6d8504bf7eb3acaf91dcfd745952b87a6f1cda` |

The original reviewer ran normally and with `-O`; its complete receipts matched.
The portable package entry points were then executed in both modes:

```sh
python3 -I -B research/current-coded-gaussian-monomial/check_review.py
python3 -I -O -B research/current-coded-gaussian-monomial/check_review.py
```

Both finished with `PASS_CURRENT_PHASE_INDEPENDENT_REVIEW`. Their complete
`REVIEW.normal.log` and `REVIEW.optimized.log` match byte-for-byte with SHA256
`bb9ccf0fa877c4aba35bfaa65bfe704f60fdc2909f68b3664a2b9390eea5e71d`.
The wrapper authenticates the unmodified checker, uses a fresh bytecode
namespace, passes explicit package/output paths, and compares the complete
generated receipt. The reviewer also checks production source hashes at entry
and exit, so an in-flight source edit cannot be attributed to one frozen run.

Seven admitted/rejected physical calls cover both residue orientations,
three rows, up to eight folded coefficient fields from two original fields,
the repeated constant, inverse phase at the recovered address, representable
signed minima, and a late headroom rejection followed by a valid retry. Two
actual erroneous compositions discriminate a missing residue reversal and
omitted suffix coefficients. Retry equals the fresh 10,193,896-action baseline.

The separately authored source/proof review found no remaining blocker in the
scoped endpoint/cost claim after retaining physical segment disjointness, the
rank-one growth premise, the full descriptor charge, and normalized occurrence
placement as explicit conditions. See its unchanged note for exact methods.

## Package and source controls

The standard check executed successfully:

```sh
GIT_NO_LAZY_FETCH=1 python3 -B scripts/research_package.py \
  --package research/current-coded-gaussian-monomial --check-only
```

It reports `PASS_PACKAGE_METADATA_AND_PINS`, which validates metadata and
canonical pins, not the mathematics. `VERIFY.json` registers both complete
author modes at 520 seconds and both independent modes at 80 seconds, totaling
the standard 1,200-second package limit.

The public current codec/header dependency is pinned at
`CubeJerry/integer-mult-bounds@5629e7772d1720d6727465e328a45694f8620538`.
All five direct exported files match their final published Git blobs and
SHA256 hashes; transitive runtime and current-source exports retain their
individual immutable provenance. No first-round or predecessor file was edited.

The post-commit default `scripts/check_research_commit.py` check passed for all
138 regular package files. The optional stricter `--check-source-history` mode
was also attempted, but it refuses this shared shallow Git repository with
`source-history check requires full Git history`. It is not reported as passed.
No history or checker setting was changed to bypass that condition. The initial
scoped commit has the declared canonical base as its direct parent; all 26
standard provenance rows use that base, and external pending-source exports
are committed inside this package with separate immutable byte pins. Those
facts and the passing byte/pin checks do not relabel the stricter gate's result.

## Limits of the executed evidence

The complete physical packet fixtures are small rank-two monomials with the
actual elementary ordinary branch; the independent format fixtures are rank
one. The actual selected raw `current_local` nine-vector service is compiled and
its current-context phase control executes for f=2,3,4. Its full packet and
intervening Fourier child are not executed. The nested `caller-local` token
emitted by `source_ir.remap` needs a separate token adapter and normalized
header; the raw binding does not supply them. A finite pass does not supply the eligible-prime ordinary
rate, prove arbitrary compiler placement, allocate global numerical headroom,
emit a flat lifecycle table, or remove any selected framework assumption.
