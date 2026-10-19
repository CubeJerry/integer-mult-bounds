# Exact arithmetic for the streamed QQ16 decoder

**Scoped numerical certificate and paired-axis reference lowering. No new κ.**

PR4015 removes temporary full-cover banks by hosting its query in nine deferred
outputs. Its proof explicitly leaves finite precision and intermediate range
open. This package supplies a sufficient **all-depth exact format for that
literal hosted word**, including native interiors, and an executable two-axis
lowering with its scratch return charged. It does not admit a physical supplier.

For tensor depth λ>=1, put k=ceil(λ/2). If every borrowed physical real/imaginary
component lies in h Z and has magnitude <2^P h, then the complete decoder can
use quantum **q=h·2^(-(3k+6))** and **W=P+6k+22 signed bits**, without additional
decoder rounding. The largest certified triangle-envelope coefficient sum is
171043 (255115 for the original 336-call word under the same method). These
are sufficient, not minimum, precision and range bounds.

Pairing tensor axes changes the direct native arithmetic from **4λD real ADDs
and 2λD HALVEs** to **4kD ADDs and 2kD HALVEs** per complete array of D complex
coordinates. For λ>=2 it needs nine scalar scratch words instead of five,
all returned zero. Across the 224 native calls the unit-cost arithmetic saving,
after the four extra clears per call, is `1344 D floor(λ/2) - 896`. The existing
448 wrappers, 352 cover maps, source access, output hosting and recursive
interface obligations are still paid or explicitly unresolved. This is an
operation-count comparison on identical inputs, not a physical runtime claim.

## Inspect and reproduce

From the repository root, with Python 3.12 and no third-party dependencies:

```sh
python3.12 -B scripts/research_package.py --package research/qq16-streamed-exact-format
```

Expected final marker: `PASS_REGISTERED_RESEARCH_PACKAGE`. The registered
commands regenerate the complete typed certificate and cut trace, run the
separate Gaussian-coefficient oracle, compare integer/rational/paired execution,
and test a Git-free export under normal and optimized Python. No predecessor
executable, Lean, network access, or full selected-frontier replay is used.

* [PROOF.md](PROOF.md) states the entrance contract, all-depth induction,
  paired schedule, full conditional cost recurrence and remaining obligations.
* [RESULT.json](RESULT.json) contains both complete format receipts and all 224
  final output envelopes. [TRACE.json](TRACE.json) contains every completed cut
  and native-interior envelope, not selected samples.
* [verify.py](verify.py) uses exact nonnegative polynomials/max-affine grids.
  [independent.py](independent.py) imports no primary or predecessor executable:
  Gaussian-integer coefficients and numerical-depth recurrences check **65,472
  cut bounds** at depths 1,2,3,4,7,8,15,16.
* [paired_kernel.py](paired_kernel.py) is the in-place metered scalar model.
  [LOWERING.json](LOWERING.json) records same-input before/after instruction
  counts, including cleanup, at six depths (1,2,3,4,7,8).
  [test_numerical.py](test_numerical.py) checks 1,250 pair cases, 13,122 two-axis
  cases, and six complete-word fixtures: **22,848 cuts and 102,144 pair calls**.
  The fixtures use synthetic noncommuting cover permutations, not the actual
  73-axis source geometry. Native/frame correctness is inherited, not reaudited.
* [test_package.py](test_package.py) rejects source, manifest, receipt and trace
  corruption, including Boolean/integer receipt substitution; it verifies
  generation refuses overwrite and that exported bytes remain unchanged.
* [TASK.json](TASK.json) records OS seed **53**, candidate selection, overlap
  checks, the local coordination claim, stopped scope and next questions.

## Pins, novelty and limits

Base: `bb4bccbf42844d2801487450727c2f63e10d1d0f`.
PR4015 source: `0fff81d8997cef646538bcd4f60d7d455cf93b8e`.
[RETAINED.json](RETAINED.json) authenticates its four unchanged files by SHA256
and Git blob. [SOURCES.json](SOURCES.json) pins canonical inputs and provenance.
Only four declared canonical inputs are needed at runtime; the retained native
Python file is data/evidence and is **never imported**. The repository NOTICE
at the PR4015 head is byte-identical to the base's retained root NOTICE.

PR3985/4015 already supplied the smaller decoder and output-bank hosting.
PR4043 (`aeeca9ffb50203b56924ee3f1325deab4029f4d9`) established relative
rounded-trace transfer but explicitly left an absolute numerical certificate
open. PR2807 supplied a different rounded-format treatment of the old word;
PR3303/3652 treat producer interiors. The Gaussian parity and tensor denominator
principle are established prior work, notably PR45. **New here** is their
source-bound application to every cut of the reduced streamed word, its exact
range/grid receipt, and the verified paired lowering with a complete local
arithmetic/cleanup invoice. No priority is claimed for the kernel identity.

This is a written all-depth argument supported by exact finite certificates and
bounded tests, not formal-kernel verification or independent human review.
An approximate producer still needs its own error bound. Actual owner/frame
geometry, caller admission, all physical transports, recursive child prices,
format return, productive stock and both supplier caps remain unresolved.
The selected frontier, upstream sources and existing packages are unchanged.

## Open next questions

Bind one real producer's **physical** output grid and magnitude to this entrance
contract, then price one actual full-cover native/map pair in its caller's
layout. Compare the complete entrance, movement, scratch and return bill before
expanding this module. The paired arithmetic count alone cannot decide whether
such composition is affordable. The structured questions and blockers are in
[TASK.json](TASK.json); no broader search or new supplier is proposed here.

## Credit and license

Contribution for **@CubeJerry**, prepared with substantial **OpenAI Codex**
assistance in mathematics, code, verification and prose; one agent, no human or
proof-assistant review. New work is Apache-2.0. Credit Chris R / Clear1nsight
(PR3985/4015/4043), ywz65 (PR2707), Arham Tahir (PR2681 and the retained native
lineage), Nick Petalas (PR2807/3303), ToikY (PR3652), and Alejandro Zarzuelo
Urdiales (PR45 Gaussian parity and tensor execution). Their existing notices
and the repository's upstream/community attribution remain in force. See
[NOTICE.md](NOTICE.md) for the unchanged retained source attribution.
