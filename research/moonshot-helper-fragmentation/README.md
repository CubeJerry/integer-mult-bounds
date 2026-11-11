# Sharp helper-fragmentation requirements for κ = 0.005

**No new κ.** On the selected #7000 caller, no partition of each original
helper into at most two independent descendants can make the retained raw
moment favorable at any price C≥1/200, C<1. Even granting arbitrary partitions
and free implementation, the sharp requirement is **22,954 extra targets**, or
**1,276 per native** when the same native is repeated 18 times. The latter
optimal profile requires 554 of the 595 current rank-nine helpers to become
3+3+3. This is a precise constructive target, not an implemented supplier.

## Mathematical scope and significance

The starting selected saving is κ=0.00363005817 at canonical commit
`e54523517d0f03e58352e647c403a5af3e525a57`. Every original helper is debited,
all 117,612 paid positions are retained, and the caller's 3,952 root targets
remain fixed. Source and chosen profiles are in [RESULT.json](RESULT.json).

| Relaxation at exponent 199/200 | Best raw margin, approximately |
|---|---:|
| Unchanged selected helper profile | −567.716010608 |
| At most two descendants per original helper | −99.619914463 |
| At most three descendants | +173.658146676 |
| Identical-native sharp extra-target threshold | +0.274312646 |

[PROOF.md](PROOF.md) proves balanced-partition optimality, decreasing marginal
increments, sharp greedy allocation and the binary ceiling over a continuum
of prices. The continuum proof uses 24 exact integer-product inequalities
and summation by parts, rather than extrapolating a numerical search.
The receipt contains strict rational intervals and adjacent failing/passing
integer budgets. Independently derived dual and Abel certificates appear
in the integrated review evidence.

The sharp repeated profile is `{1:13,2:18,3:1808,4:408,5:109}`. It has only
about 0.0152395914436 of additional paid moment per native before losing its
raw slack. Other profiles can have more slack. None of these numbers proves
that 554 ternary cuts exist or fresh inputs remain independent. The companion
[compiler specification](COMPILER-SPECIFICATION.md) proves sufficient downstream
arithmetic for this explicitly unbuilt profile and identifies a compatible
unbuilt BIT supplier; it does not admit either physical supplier.
The five foundational assumptions remain unchanged: native_all_columns,
owned_erasure, compiler, precision_tape and analytic_recovery.

## Sources, reproduction and verification

The sole live mathematical input is an exact 25,225-byte export of
[the selected full invoice](https://github.com/CrocSwap/integer-mult-bounds/blob/e54523517d0f03e58352e647c403a5af3e525a57/research/shared-wire-split-composition/FULL-RESULT.json).
Its SHA256 is `d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7`
and Git blob is `ff3256f0d3ffbfc56b062f9ec0fdbbc7b30e76d5`. Both are checked
before extracting the full invoice and native helper census. No native
operator replay or inherited source theorem is silently reverified here.

```sh
python -I -B research/moonshot-helper-fragmentation/verify.py
python -I -O -B research/moonshot-helper-fragmentation/verify.py
```

Both print `PASS_SHARP_HELPER_FRAGMENTATION`. Default replay is read-only and
compares every frozen receipt field. Python 3.12.14 normal and optimized runs
passed after the execution workspace was replaced. These are freshly rebuilt
and freshly checked bytes; the lost original package's review is not silently
transferred. Regeneration requires explicit `--write`. The verifier uses only
the standard library and works without Git or network access. Hosted CI and
formal proof-kernel review are not claimed by local replay.

Controls exhaust all 96 positive partitions of ranks one through nine, reject
eight malformed histograms and two source mutations, and expose false crossings
from omitting 100 paid rank-one jobs or retaining the old helper target.
The proof covers the declared partition class; finite controls test arithmetic
and accounting failure modes, not the complete multiplication theorem.

## Predecessors, novelty and credit

The selected shared-wire composition and full invoice are predecessor work
by Jerry Chen/CubeJerry and the retained native/caller lineage, including
DreamingOfClouds, Ali Romman, unpaidmoon and icekylinx. Ali Romman's helper
split criterion and Matarener's exact split census concern physical cut
admissibility; no new cuts are inferred here. [helper-handoff-r18](../helper-handoff-r18/README.md)
treats an older single-split envelope and reflagging costs. Nick Petalas's
[unit-fee-target-threshold](../unit-fee-target-threshold/README.md) uses a
separate per-fragment fee model and already uses balancing and exact roots.
Related [mixed-target-capacity-ceiling](../mixed-target-capacity-ceiling/README.md),
[sharp-complex-entropy-defect](../sharp-complex-entropy-defect/README.md) and
[kappa010-rank-cap-floor](../kappa010-rank-cap-floor/README.md) have different
hypotheses. This addition is the sharp selected-source fragment budget and its
binary continuum obstruction at the moonshot target; concavity and greedy
chain optimization are standard tools.

Prepared for **@CubeJerry** with substantial **OpenAI Codex assistance**,
including separate research and independent-review agents. Apache-2.0,
following the repository and retained input attribution. No human or formal
kernel review is claimed. [NOTICE.md](NOTICE.md) credits the vendored invoice.

## Open next questions

1. Construct one source-admissible rank9→3+3+3 mechanism preserving each fresh
   input. Begin with one exact two-cut or simultaneous-cut word and its complete
   paid invoice; only then investigate sufficient repeated deployment.
2. Realize the physical inputs of the paid compiler specification below,
   including the complete new ordinary-work, storage and precision constants.
   Its hypothetical arithmetic passes; the required native and BIT suppliers
   remain unbuilt.
3. Escape the unchanged-helper class with a new representation or paid savings.
   State source ownership, precision and recursion before claiming complete
   target feasibility. Structured next steps appear in TASK.json.

## Constructive prerequisite: static 3/6 cuts

[STATIC-CUT.md](STATIC-CUT.md) and [static_cut.py](static_cut.py) separately
certify that the selected word has no standard first3+6 or6+3 cut for any of
its595 current rank-nine helpers, even allowing all coframed public/owned
roles and arbitrary rational coefficients. The complete4,657 cut classes
have4,496 zero pure-prefix images,136 zero pure-suffix images and25 identically
zero local pairing forms. This blocks only the unchanged-source sequential
3+3+3 route; temporal, new-frame and simultaneous constructions remain open.
The exact canonical source word is a declared live input with source pins.

```sh
python -I -B research/moonshot-helper-fragmentation/static_cut.py
python -I -O -B research/moonshot-helper-fragmentation/static_cut.py
```

Expected: PASS_STATIC_3_6_CUT_OBSTRUCTION. The fresh independent reviewer uses
a different kernel construction and checks all 4,657 classes; see
[the signed-off review](review/static/REVIEW.md). No historical review is
silently transferred to reconstructed bytes.

## Sufficient downstream compiler specification

[COMPILER-SPECIFICATION.md](COMPILER-SPECIFICATION.md) gives the full target
restriction and paid splitting inequalities for the sharp repeated profile.
At complex price C=.00500007, product power 1920, paid cap 11^1920 and target
floor 12^1920, the normalized paid-plus-discarded-target bound is below .999.
Every discarded productive field becomes an owned zero input; all intermediate
paid work remains, and initialization and erasure are counted explicitly.
The honest ambient is 153^1920, giving logarithmic exponent 1377 and the stated
finite uniform threshold, with uniform complex saving U=.00500006.

This arithmetic joins the separately published [BIT bootstrap
proof](https://github.com/CubeJerry/integer-mult-bounds/blob/a169504af5d7a394424bb19b10d58f1d1b5d1fce/research/bit-target-bootstrap/PROOF.md):
an unbuilt covered BIT supplier at .0050001 would give ordinary B=.00500007
through two stages, and the current 54+4 outer rows are then strict at κ=1/200.
The actual ternary native, the stronger covered BIT supplier and their new
physical counts remain explicit missing internal inputs. This is a sufficient
specification, **not a complete conditional κ=.005 assembly**.

```sh
python -I -B research/moonshot-helper-fragmentation/compiler_certificate.py
python -I -O -B research/moonshot-helper-fragmentation/compiler_certificate.py
```

Expected: PASS_UNBUILT_PROFILE_COMPILER_SPECIFICATION. An independent rational
log/exp implementation verifies the complete arithmetic in
[review/compiler](review/compiler/REVIEW.md). The eight commands in VERIFY.json
were all executed after packaging, covering twelve author/reviewer normal and
optimized replays; [VALIDATION.md](VALIDATION.md) records their exact scope.
