# Wave 9: literal current CRT leaf headers

Status: implementation approved; the preliminary meter concern is resolved
by an exact physical-bank audit below. Canonical base is
`e54523517d0f03e58352e647c403a5af3e525a57`. No new kappa and no global CRT
or multiplication theorem is proposed.

## Exact source and the premise to remove

Target: `research/encoded-crt-leaf-payload/route.py:emit_headers` at
CrocSwap/integer-mult-bounds#7388, head
`d6f4a69202ad0bba4a915f4d4f3eaba1fe431c86`. The retained B5 caller invokes
this exact Python controller before the already literal destination-key pass.
The variable helpers are the no-target/no-guide specialization of
`frozen/frontend.py:Iterator._record` and
`research/crt-current-row-query/join.py:copy_numeric_field`. Their operations
are local physical actions, but iteration and continuations at this seam
have not been lowered into one finite graph.

Remove precisely this host header-emission controller. Numerical offset
production, lease acquisition and selected-leaf admission remain external.
B7 is pinned to published `f789e7318ef89b26c2e358c4c1eb09ce93d21f73`, tree
`fe3d3c3cda8bc6c1f85a4244bfd1748c55e4019d`; its graph stays unchanged.

## Proposed uniform theorem

At the actual admitted last nonroot leaf, the borrowed axis tape is
`LEFT ONE^m STEP ONE RIGHT`, with `m>=1`; the source has exactly `m+2`
positive-width padded records and terminal `RIGHT`. Each record is
`ROOT ONE^w WORD_END bits_w WORD_END bits_w RECORD_END`. The selected right
record has width `h>=1`, the left record width `u>=1`. The borrowed precision
guide has `p=u+h+1` one marks; retained numerical entry requires `p>=4`.
The actual current result starts `ROOT bits_p WORD_END`; its later fields
stay untouched. Retained numerical admission supplies the semantic facts
that copied fields are the current modulus and offset, with `1<=s<=2^h`
and `0<=a<s`.

One fixed graph constructs exactly `L bin_p(h) R`, `L bin_p(s) R`,
`L bin_p(a) | R`, `L 0^p R`, and `L 1^h R`. It preserves every borrowed
byte, returns borrowed heads to their first body cells, returns output
heads to `L`, and restores the actual iterator width scratch to its blank
body and first-body head. No decoded width, variable host loop, host head
reset or host-selected variable continuation occurs. A separate literal
retirement entry erases all five outputs and returns their heads while
retaining larger old blank history.

The graph may continue statically into unchanged B7 forward/inverse entries.
Headers remain live for retained radix; retirement occurs at the original
post-sort cleanup seam. B7 retains its fixed 13-bit codeword/arbitrary
12-bit opaque payload ABI and physical-position-key condition for a sorted
roundtrip. No variable-width payload claim is added.

## Fixed physical interface

| Roles | Binding and entry head |
|---|---|
| 0--21 | Unchanged B7 owners; marker origins and original binary payload |
| 22 | Actual `iterator.source`, first body cell |
| 23 | Actual `iterator.counters['axis']`, first body cell |
| 24 | Actual `lease.actual.guide`, first body cell |
| 25 | Actual `lease.actual.result['stream']`, first body cell |
| 26 | Actual `iterator.counters['width']`, blank body, first body cell |

Owners are distinct. Roles 22--26 use original numeric alphabet 0--13.
A fixed alphabet renaming maps numeric 0/1/LEFT/RIGHT/BLANK to graph
0/1/L/R/blank tokens and each other tag to its own token; no stored byte
is converted. Output `|` is separate. First-body versus marker-origin head
conventions require charged moves.

No new scratch owner is needed. Prefix widths can exceed current p.
Original `_shape` already scanned every source record through this same
width role, but the standalone theorem explicitly retains the maximum of
old history and newly touched extent.

## Complete optimistic bill

Let `L_source` be the traversed source-body length through terminal RIGHT,
`L_result` the traversed result prefix including tag/delimiter, `W` the
largest skipped width, and `m` the prefix axis count. Construction plus
retirement costs

`O(L_source + L_result + p(h+1) + h + m + 1)` literal instructions.

Pay source-prefix traversal and return; manufacture and erase a unary
scratch for every skipped record; validate both padded fields and every
delimiter. Each of h width marks triggers a paid p-digit height increment.
Pay zero initialization, guide returns, modulus padding, current result
copy, markers, scratch erasure, borrowed head returns and output retirement.
The initial generous target is 512 times the displayed expression; derive
the implemented graph's bill separately before claiming it.

Five outputs occupy `4p+h+11` cells including markers, before any explicitly
paid retirement frontier. Scratch visits at most `W+3` cells including
guard/append frontier. Preserve per-role old historical extents. Borrowed
source/axis/guide/result visited windows, access and owner grants remain
explicit, never free.

The complete same-workload pass adds **all** B7 work:

`T_headers + sum_{i=0}^{2^h-1} T_B6(i) + 2^h(156h+126)+18h+203`.

Retained numeric-source and radix bills stay separate without a proved
common tariff. Initial inspection raised a possible guide/result meter
omission, but the exact bank binding disproves it: `Bank.open` supplies
`adapter.Port=Bank.take`; the actual guide is bank[0] and result bank[62].
Both are included in the existing source-meter sum. Four fresh actual
legs show guide100 and result31 header actions, all included, with exactly
zero omissions. See `METER-AUDIT-RESULT.json` and `meter_audit.py`.
The new literal bill includes all header instructions and subtracts the
true included native actions from retained meters. No mixed-meter vector
becomes a single bit-time assertion.

## Verification and stopping rule

Prove arbitrary admitted-width/prefix invariants. Compare exact outputs
with original helpers and independent arithmetic/source oracles. Include
large skipped width with tiny current p, long prefix, carries, translated
origins, larger retained histories, no borrowed writes, returned heads,
scratch retirement and unchanged B7 static relocation. Test malformed
delimiters/widths and returning wrong-field/stale-offset/omitted-increment
mutations. Failure cleanup is not inferred from success cleanup.

Execute the actual four-tag modulus-three/left-two source caller forward
and inverse with retained radix. Compare full source/payload/keys and cost
vector. Uniform header fixtures do not need whole-source numeric replays.

Stop if existing literal header lowering covers this exact source, actual
lease ports do not match, scratch reuse has an uncharged ownership step,
or a larger extension requires a new numerical dispatcher.

## Bounded overlap evidence

Root live searches found #7388 only. Additional code `emit_headers` search
returned no indexed match; broad literal leaf-header search found unrelated
native material. PR body `"emit_headers"` returned none; `"leaf header"
literal` found unrelated native positive-leaf work. This is bounded search,
not exhaustive novelty certification. B8 remains an overlap stop.

Prepared for @CubeJerry with substantial OpenAI assistance. Retain Apache-2.0
notices and credit #7388, #7352, #7504 and the exact B4--B7 dependencies.
