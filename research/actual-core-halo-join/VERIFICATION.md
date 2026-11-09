# Verification, reproducibility and evidence boundaries

Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.

## 1. Completed scientific verification

The complete actual `N16/L8/K2/g1` Core/halo command finished with its frozen
entry64 driver, and the execution session returned exit zero after trailing
teardown. PHYSICAL-RESULT.json, PHYSICAL-EXECUTION.log and the separately
labelled operator attestation PHYSICAL-EXIT.json preserve the exact evidence.
The independent original-matrix observer passed normally and with `-O`,
producing byte-identical receipts. ROOT-FINAL-ACCEPTANCE.md records the
conditional scientific acceptance and the remaining publication gates.

The bounded registered replay reviews this frozen physical receipt and its
completion record. It does not launch the multi-hour transaction. Its
separate semantic Core execution is explicitly labelled. The final bounded
commands and their receipts are recorded in Section 9 and RESULT.json.

At the earlier prephysical checkpoint, the explicit `replay.py --prephysical-only` branch passed
normally in 76.95 seconds and with `-O` in 74.17 seconds, in a separate
execution directory. PREPHYSICAL-NORMAL.json and PREPHYSICAL-OPTIMIZED.json
retain those runs. Both explicitly say
`retained_actual_physical_reviewed=false`; neither is a completed attachment
receipt. These historical runs predate the final physical acceptance and
completion-record guard. The canonical metadata/source-pin check also passed.

## 2. Actual physical entry point

```sh
python3 -B research/actual-core-halo-join/verify.py --output /tmp/core-halo-physical.json
```

The fixture is the original `Reference(15,1,2,1,3,64)`, period 16, with
two ordinary length-eight windows at origins 0 and 8. Each admitted
interior is the scalar coordinate 7: A is identity; the complete Q matrices
are coupled. The source plan uses the admitted physical halfwidth W2,
one halo term, zero dependency halo and first-face boundary one.

The exact preflight requires 477 dense events over three complete global
dense calls. There is one global inverse sparse stage and one global forward
sparse stage. Each visits both contexts; the per-context payload child-call
counters are therefore two inverse calls and two forward calls. These are
not four global sparse stages. The common grid and
carrier are P246/w270; dense input and return widths remain W0259 and
Wd368, with actual exact conversions. The halo grid is q28 in h31 words.
Whole-field R0=4 funds all 16 original inputs; R_in=1 and R_halo=2 are
separate pointwise bounds. The single normalizer is two.

`verify.py` builds the actual immutable dense controls, exact rational
sparse pages, original routes and encoded parameters. The unchanged
native standard root and real sparse payloads execute with payload decoders
disabled. A fixed certified metadata-floor specialization is inherited
and its misses must be zero. Every stage observes its actual current input
and output; these passive observations are excluded from production cost.

The receipt records the complete original input, actual unnormalized Core
return, normalized current source, saved original halo stream and final
merged output. It verifies source-port restoration, no new online native
tape roles, unchanged private role identity, immutable saved source, exact
lift and toward-zero normalization, stage continuity, kept-row preservation
and private historical cleanup.

The primary receipt timestamp is 9,424.753 seconds after driver start;
its online timing interval is 5,389.720 seconds. The first dense input was
observed at 4,035.353 seconds. These are wall-time observations of their
declared intervals, not a separately controlled setup benchmark.

| Native meter window | Reads | Writes | Moves |
| --- | ---: | ---: | ---: |
| Setup | 10,471,971,830 | 1,224,893,364 | 7,079,322,454 |
| Attached online transaction | 10,406,453,317 | 4,149,839,475 | 9,898,877,192 |

The observed native private backing is 872,994 cells; all constructed native
roles retain 2,424,867 cells. The native inventory contains 11,651 fixed
private roles and creates no new native Tape during the online call.
The separate finite-alphabet transport reports 313,059 actions and 3,569
retained cells; the binary consumer/archive reports 5,263 retained cells.
These role and alphabet conventions remain distinct.

The J1 primary halo performs zero recurrence products and eight final
roundings over four saved/returned records. The separate J2 fixture
executes 120 actual recurrence products and 80 roundings, with 28 saved
records and twelve returned records. Its Core is explicitly semantic.

### Meter boundary

Native setup meters begin before dense-control and sparse-bank construction;
native online meters surround the actual attached transaction. Specifically,
`native_online_actions` stops immediately after `owner.run`, before
`transport.erase_work`; the later transport snapshot includes that erasure.
The binary
consumer and finite-alphabet transport maintain their separate inherited
meters. Host Reference construction and finite source admission have an
explicit source-production bill and source-height inventory; they are not
mislabelled as measured native tape operations.

The physical receipt is written after work erasure and output checks, before
the final disposal of immutable source archives, prepared routes, controls
and banks. Those disposals execute immediately afterward, but their actions
are outside the displayed receipt counters. The complete theorem invoice
includes those scans and every historical backing extent. The receipt is
therefore a labelled set of machine observations, not an exact sum of all
binary transitions in the complete theorem.
Successful process exit after the trailing teardown, not merely the earlier
receipt write or printed PASS line, is required for the final execution status.
PHYSICAL-EXIT.json binds that observed process exit to the exact driver,
numerical receipt and copied execution log. It is a process-completion
record, not a second physical replay. The bounded hook requires this
additional record before accepting a completed retained physical witness.

## 3. Complete nonidentity-interior semantic fixture

```sh
python3 -B research/actual-core-halo-join/semantic_halo.py --output /tmp/core-halo-semantic.json
python3 -O -B research/actual-core-halo-join/semantic_halo.py --output /tmp/core-halo-semantic-optimized.json
```

SEMANTIC-RESULT.json and SEMANTIC-OPTIMIZED-RESULT.json are complete
independent process runs. All scientific fields agree; only runtime is
allowed to differ. This fixture uses `Reference(31,1,4,1,3,192)`, period 32,
two length-sixteen windows, and two genuinely coupled A2 interiors at local
coordinates (1,2). The actual complete emitted H/D programs supply 2,691
dense semantic events. All three dense stages perform nonzero truncations;
the staged sparse algorithms consume the actual intermediate values.

The Core is interpreted by the retained source semantics. The returned
integers are explicitly emitted as semantic data; no physical Core claim
is made. The new bridge, unchanged two-term halo and actual transport/merge
then execute literally. W2 gives dependency halo two, boundary three,
20 kept rows and 12 returned rows; four rectangles save 28 records.
The common P356/w381 carrier, R0=8, q56 halo grid and separate radius-two
output carrier are recorded. The original-Q inverse check is independent
of the staged expected values.

At the earlier q28 grid, every kept normalized Core value coincided with
the rounded two-term halo value. The original-matrix reviewer first
rejected an overly strong witness-discrimination gate; all correctness
checks had already passed. The reviewer changed that gate to a reported
distinction flag and retained an active one-unit kept corruption control.
The subsequent q56 fixture does numerically distinguish the branches.
The earlier receipts remain labelled outside the final successful fixture;
they are not silently relabelled as q56 executions.

## 4. Independent literal bridge review

```sh
python3 -I -B research/actual-core-halo-join/review/bridge_review.py --package research/actual-core-halo-join --output /tmp/core-halo-bridge.json
python3 -I -B -O research/actual-core-halo-join/review/bridge_review.py --package research/actual-core-halo-join --output /tmp/core-halo-bridge-optimized.json
```

The separately assigned reviewer uses its own sparse payload/scratch
hardware and exact signed oracle, with the real retained Count controls.
Nineteen successful cases include production dimensions h31/w270/P246,
minimum negative words, d greater than w, equal grids, zero results,
translated origins and unequal normalizer contributions. Nine rejecting
cases cover malformed or negative-zero input, carrier overflow and cleanup.

A short call after a large call performs exactly 347 payload actions,
identical to a fresh short call. Its already cleared historical scratch
extent remains 151 cells, versus five for a fresh role. This checks both
current-body erasure and retained backing. Normal and optimized receipts
are identical. The composite caller still has the explicitly stated
valid-domain contract: a Core supplier exception before return leaves
lifted input for caller cleanup; no composite rollback is claimed.

## 5. Independent asymmetric source and layout review

```sh
python3 -I -B research/actual-core-halo-join/review/axis_binding_review.py --package research/actual-core-halo-join --output /tmp/core-halo-axis.json
python3 -I -B -O research/actual-core-halo-join/review/axis_binding_review.py --package research/actual-core-halo-join --output /tmp/core-halo-axis-optimized.json
```

The reviewer invokes the actual new family factory with actual W4 source
archives and retained prepared routes. Halo periods (16,128), L8, boundary
one and one spectator bit give 4,096 original addresses, 64 contexts and
18 distinct intended source windows. All 1,152 selected source entries
match direct original-coordinate entries.

Naïve coarse-label decoding is wrong at 3,584 addresses; local rebasing
changes 224 source entries. Actual encoded bridge Counts [31,80,28,64,39]
use unequal normalizer shifts (1,2), so the test detects a maximum or one
shift substituted for their sum. The producer rejects a same-period foreign
Reference, reversed source rows, a W1 archive with honest source IDs,
insufficient global radius, insufficient output headroom, coarser P and
an inadequate lift carrier. The retained structural route validator alone
accepts a same-period foreign Reference; the new source producer rejects it.
Normal and optimized receipts are identical. This is source/route evidence,
not another numerical Core execution.

## 6. Independent original-matrix observation

The separately written `periodic_review.py` reads only the pinned original
Reference and the exported endpoint words. It independently eliminates the
full original periodic matrix and each ordinary principal-window matrix,
checks exact inverse residuals, compares the actual Core to the direct
window inverse, checks exact signed normalization and reconstructs the
rounded global halo recurrence. Every original merged address is checked.
It does not import the producer's Schur factors, staged oracle or rectangle
interpreter.

Its normal/optimized semantic receipt checks all 32 addresses, both
ordinary windows, 20 kept and 12 returned rows, exact radius funding and
the numerical error against the original periodic inverse. Eight corrupted
observations are rejected, including a one-grid-unit kept corruption.
The same frozen observer separately checked the completed physical receipt,
with no code or allowance change. All sixteen addresses, both exact window
inverse residuals, the full periodic inverse residual, normalization, final
merge and eight corrupted-observation controls pass. The paired physical
review receipts are byte-identical with SHA256
`ad7ae7b8f252c7c9436803f5e2d8cb2b2bea5002880330f1e222fc5efdd1496e`.
PHYSICAL-MATRIX-REVIEW.md retains exact pins and the scope of this observation.

The actual Core squared Euclidean error is approximately `3.1165e-147`;
input passthrough would have squared error about `2.5496e-5`. The normalized
Core q-return has component-l1 error about `6.2154e-9`. The final maximum
component-l1 error against the exact normalized periodic inverse is about
`0.00158217`. These decimals only summarize exact rational decisions.
The finite checker uses its independently computed exact kept-row operator
tail; its sharper finite allowance is not a replacement for the uniform
tail bound in PROOF.md.
Reviewing frozen endpoint evidence is not another physical replay.

The separately assigned analytic review in
`review/a4-analytic-cross-review/REVIEW.md` derives the normalized seam,
kept-row and halo bounds independently. It accepts the final PROOF.md hash
`37e7f9995725543917ec593184842c0453e6954d633af4e2573ad835a292b3ac`,
with source and implementation pins in its own SOURCE-HASHES.json.
Its normal/optimized checker verifies only those bytes and public dependency
bindings; it imports no reviewed module and runs no numerical or physical
payload. Its written analytic PASS and its hash-only executable are distinct
evidence. The root's separate source/cost note is retained alongside it.

## 7. Source integrity and failed-check history

All retained bodies are immutable public sources. Git blobs and SHA256 are
checked before loading. The halo public acquisition initially found two
saved README copies that differed from their public pinned blobs; exact
base64 public bytes replaced only the new retained copies. The original
working trees were not modified. PUBLIC-HALO-PINS.json records the exact
public bodies; the final source closure remains reproducible offline.

The first standalone WordProduct probe used W1 metadata. The independent
source review found actual width-two edges (7,9) and (9,7) across the N16
identity hole. The complete execution was started only after changing its
source plan to W2 and checking all original off-band entries. The earlier
probe established only its unrelated scalar-product timing; it did not
admit a complete W1 Core/halo transaction.

Early converter checks exposed an unavailable encoded-add helper and a
scratch cleanup endpoint that needed one explicit step back to its body.
Both were fixed before the frozen independent bridge replay. Failures use
explicit exceptions; optimization cannot erase admission or control checks.

The first proposed A2 semantic source failed the inherited RawGaussian
accuracy gate. Increasing its entry precision alone still failed because
the fixed Reference truncation tail remained. The separately declared
alpha-four source passed the actual gate. No fixed source was silently
assigned a stronger precision guarantee.

The asymptotic source preparation and repeated-archive amortizations are
inherited under the stated growing balanced-group hypotheses. The tiny
one-axis fixtures retain their full generic bill and cannot establish those
rate premises by timing or finite counts.

The byte/style preflight found one extra final newline in the independently
frozen periodic reviewer. Its owner removed only that byte, reissued the
script and receipts, and reran both complete semantic observer commands.
PERIODIC-EOF-EQUIVALENCE.json records identical normal/optimized compiled
code and AST, with scientific receipts unchanged except reviewer hash.
The new frozen files were copied unchanged; no silent local reviewer edit
or changed numerical result was used to pass the gate.

## 8. Separately admitted entry40 fallback, intentionally stopped

Exact rational page preparation made the initial online-only timing estimate
incomplete. The entry64 process was preserved, with driver SHA256
`230cef8659af7b8beaa0db86ecd3376df81ad6aeaf5fbe7f1d7b3e339cae954b`.
It completed its sparse banks and observed the first actual global dense
input at 4,035.35 seconds after start. That timestamp includes the full
prelude; it is not a pure page-preparation microbenchmark.

A separate input source, `Reference(15,1,2,1,3,40)`, passed all unchanged
numerical admissions and the complete 16-by-16 original bandwidth check.
Its hash is `83868eeb82059328a1dde403e6d2cecb64e30c5d12bb19e3c7e5db58592bdf4f`.
The complete geometry, input, radii, common P246/w270 carrier, all 477 dense
events and real numerical/transport providers remain the same. The new
driver changes only that source precision, its output name and its explanatory
docstring. Its distinct SHA256 is
`e116b2199793214a19145eef025e3219f20287dbc1a11b0682ed41d5cb53a13d`.

Before launch, `setup_cost_census.py` mirrored every exact coefficient
serialization reduction, all diagonal inverses and coupling roundings in
the unchanged source-page algorithms. Every computed inverse block is
checked by its exact residual. Both sources use 64 inverse blocks, 1,872
rational reductions, 848 products and 464 roundings.

| Comparison metric over all pages | Entry64 | Entry40 |
| --- | ---: | ---: |
| Binary-division digit visits | 3,293,117,293 | 1,515,218,054 |
| Product operand-bit rectangles | 10,941,786 | 6,481,586 |
| Sequential matrix scan cells | 3,140,927 | 2,787,425 |
| Exact Euclidean division calls | 22,437 | 17,841 |

The first metric sums the operand widths visited by a separate binary
long-division trace. These are **source-derived comparison proxies**, not
measured native Tape actions, measured speedups or wall-time guarantees.
They include both the full exact inverse pages and the pre-rounded forward
lift pages. The dominant comparison falls to about 46.0%, which justified
the separately admitted fallback; a maximum-height ratio alone was not used.

The fallback ran in its own execution directory, preserving both loaded
drivers, source identities, logs and outputs. Its explicit command is:

```sh
python3 -B research/actual-core-halo-join/verify_entry40.py --output /tmp/core-halo-entry40.json
```

The frozen fallback run uses PHYSICAL-ENTRY40-RESULT.json in its isolated
execution directory. The documented command gives a new replay a separate
temporary output. ENTRY40-DRIVER.json and ENTRY40-PREFLIGHT.json retain its
separate admission and source pins.
The census is reproduced independently of either physical execution:

```sh
python3 -B research/actual-core-halo-join/setup_cost_census.py > /tmp/setup-cost-census.json
```

SETUP-COST-CENSUS.json preserves its complete per-page breakdown.

After the entry64 execution exited zero and passed both independent observer
modes, no separate source-precision risk required a duplicate execution.
The fallback was interrupted during T2, after D_Ainv_1, T1 and D_A completed.
The targeted session interrupt returned exit 130. A preceding direct PID
signal attempt had returned ProcessLookupError while the session remained
active; that operator-control history is retained, not called a numerical
failure. ENTRY40-PARTIAL.json and ENTRY40-PARTIAL-EXECUTION.log preserve the
exact source, input, preflight and emitted partial log. No unfinished mutable
tape image was exported. This is not a completed second physical witness.

## 9. Bounded review and process-completion controls

The canonical registered runner exited zero after both commands passed:
71.824 seconds normally and 70.417 seconds with optimization.
BOUNDED-NORMAL.json and BOUNDED-OPTIMIZED.json were extracted from its
preserved REGISTERED-REPLAY.log. Their scientific fields agree after excluding
optimization labels, runtimes, and hashes derived from the fresh semantic
receipt's runtime. The retained physical observation hash agrees exactly.

The registered package commands run the two bounded review modes:

```sh
python3 -B research/actual-core-halo-join/replay.py --output /tmp/core-halo-review.json
python3 -O -B research/actual-core-halo-join/replay.py --output /tmp/core-halo-review-optimized.json
```

They authenticate the execution and reviewer bodies, check preservation of
the independent analytic review's source hashes, replay the separate bridge
and asymmetric source controls, execute the complete semantic Core/J2 halo
fixture, and independently observe that fresh semantic result together with
the retained complete physical result. The exit-record guard runs before
these checks. Neither command repeats the extended physical execution.

The root additionally tested five completion-record mutations in both modes:
missing record, nonzero exit, unfinished teardown, wrong log hash and foreign
Reference. All ten reject before replay starts. The frozen script and
PROCESS-COMPLETION-GATE.json are source-pinned by the bounded hook; those
negative controls are separately reproducible as:

```sh
python3 -I -B research/actual-core-halo-join/review/check_process_completion_gate.py --package research/actual-core-halo-join --output /tmp/core-halo-completion-gate.json
```

The driver, numerical receipt and observed-exit record remain separate
evidence. The completion-record test is neither a physical replay nor an
independent observation of the process itself.
