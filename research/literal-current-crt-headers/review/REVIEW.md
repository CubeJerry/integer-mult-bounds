# Independent review of the literal current-source leaf headers

Status: **PASS**. No scientific change requested.

Reviewed frozen package: `literal-leaf-headers`, canonical base
`e54523517d0f03e58352e647c403a5af3e525a57`.

| Object | SHA256 |
|---|---|
| Written proof | `67f6312067c1eb7f41888c9a425eda36331e16c16bd66c1e3580a4905321acb9` |
| Header compiler | `9c270a0b6af2f1eb53e5246acf1df85202ca029493b2cd2ae81776d75baee78f` |
| Fixed graph | `267752d474d8b1565ceb0415609b34e75797d8c6b735600242ceb410613b0508` |
| Retained B7 graph | `8f5ae62b89de8308eb021920185269d884f07f625a5b3ee10b39f27aee5a393b` |

The graph has 21,513 locations and 27 fixed physical roles: a new prefix
of 378 locations and one unchanged relocated 21,135-instruction B7 child.
This review independently derives the new grammar, loop invariants,
costs, histories and source interface. Its sparse-tape interpreter imports
only the frozen offline compiler and its retained compiler dependencies.
No contributor interpreter, verifier, fixture, header decoder, expected
cost helper or numerical source provider is executed.

This is review by a separate OpenAI research agent, prepared for @CubeJerry,
not independent human or formal-kernel certification. All prior source,
controller, key-pass and arithmetic credit remains with the authors and
originating PRs named in the package.

## 1. Domain and the boundary between supplied and implemented work

The proof correctly treats these as typed streams. The borrowed source
starts at its first body cell after LEFT and contains `m+2` records,
each `ROOT ONE^w WE bits_w WE bits_w RE`, followed by RIGHT. The axis
has `ONE^m STEP` with `m>=1`; its remaining suffix is preserved. The
guide is `ONE^p` then blank, with the admitted relation `p=u+h+1>=4`.
The first result field contains exactly `p` bits for the current value
`a`. The right modulus has `h` bits for `s`, with `1<=s<2^h` and
`0<=a<s`. The graph copies that actual field; it does not prove the
arithmetic/current-lease relation or reconstruct the numerical producer.

The output windows, private mode cell and record-width scratch must be
granted and disjoint. Owner identity is checked by the physical binder;
the graph does not construct owner capabilities or solve global stock.
The source/axis/guide/result roles are borrowed. The new compiler has no
write instruction targeting any of these four roles. The source symbol
renaming is a fixed mapping of the retained numeric alphabet, and no
word decode occurs in that adapter.

Both source and output guard conventions are explicit. A source first-body
head is one cell to the right of its LEFT; a marker output enters at the
blank cell where its L will be placed. An absent or interior LEFT is
outside the typed grammar. Malformed streams may reject after writes;
the proof properly makes no rejection cleanup, rollback or head-return
claim. Its stronger local grammar fixtures do not establish additional
numerical source admissions, including the unit-modulus case.

## 2. Complete record validation and header invariants

For every skipped prefix record and the left record, the graph manufactures
the width scratch by one local copy per unary source mark. It terminates
the temporary guide with R and returns to its first body cell. Each of
the two fields is then read under a full scan of this same guide. The
source delimiter is checked only after exactly that many bits have been
read. Thus there is no delimiter-only shortcut, host width lookup or free
unary guide. The temporary guide, including its R, is erased and its head
returns before the next record.

The two copies of this finite record subroutine have different fixed
continuations, one back to the axis loop and one to the final right record.
No return address or call stack is encoded by host control. The prefix
count is read from the actual axis stream. The left-record width can be
small while an earlier skipped width is arbitrarily large.

The H and zero-row outputs are initialized by two scans of the actual
guide. On the right-record loop, every unary source mark both appends one
WIDTH bit and increments H. By induction, after `k` such iterations H
stores `k` in exactly `p` little-endian bits. The carry is held in finite
control and the full remaining width is scanned before returning to L.
The domain gives `h<p<2^p`, so those increments cannot overflow.

The modulus scan consumes exactly the `h` source modulus bits under WIDTH,
then pads with zeros until the current guide ends. The right coordinate
field is independently validated by another complete WIDTH scan. Its
RE and the terminal source RIGHT are checked. The source, axis, guide and
WIDTH heads all return by literal moves. The offset copy consumes exactly
`p` current-result bits, checks WE, emits `| R`, and restores the result
and guide heads. Therefore the exact returned headers are

`H=L bin_p(h) R`, `S=L bin_p(s) R`, `A=L bin_p(a) | R`,
`J=L 0^p R`, and `WIDTH=L 1^h R`.

The proof does not charge work according to a decoded width at runtime.
All appearances of `h,p,m,U,W` in the bill are analysis of local-symbol
loop counts, not inputs selecting graph size or a host loop.

## 3. Independent instruction accounting

I independently counted instructions from the literal program, using
one unit for R, W, unit M, J and H. A rewind from distance `d` to marker
L costs `3d+1`; a native rewind from cell `k` to first-body cell 1 costs
`3k`, including the initial left and final right movements.

The elementary counts agree with the proof:

| Operation | Independently derived count |
|---|---:|
| One guide-driven zero header | `12p+13` |
| One skipped width-w record with both fields, scratch manufacture, erasure and fixed continuation | `32w+39` |
| Height increment with c trailing one digits before increment | `6p+c+8` |
| Offset copy, delimiters and both returns | `17p+32` |
| Retirement of one marker output with n body symbols | `7n+9` |

For a record, the width-manufacturing part is `9w+15`, the two field
passes are `16w+12`, and complete temporary-guide cleanup plus fixed
continuation is `7w+12`. Their sum is `32w+39`.

For the `h` increments starting from zero, the propagated carries sum
to `h-pop(h)`: every zero-to-one bit flip increases population by one,
and every propagated one-to-zero flip decreases it by one. Summing the
population change over all increments yields this identity for arbitrary
`h`, including long carry chains.

The full construction partitions as follows:

| Portion | Count |
|---|---:|
| Entry checks, two zero headers, prefix and left record | `24p+32U+42m+91` |
| Right record, height loop, modulus, coordinate validation and returns | `6ph+12p+9U+15m+42h+74-pop(h)` |
| Offset construction and returns | `17p+32` |
| Final mode read and BUILD halt | `2` |

Hence

`BUILD = 6ph+53p+41U+57m+42h+199-pop(h)`.

The five retired bodies have total length `4p+h+1`. Five entry/end
constants and one final halt give

`RETIRE = 7(4p+h+1)+5*9+1 = 28p+7h+53`.

Each combined key direction spends `BUILD+2` before its unchanged child
entry: one mode write and one extra instruction in the cleared fixed
continuation account for the difference. Adding the child and retirement
therefore gives exactly

`T_key+6ph+81p+41U+57m+49h+254-pop(h)`.

The retained key bill remains
`sum_i T_B6(direction,i)+2^h(156h+126)+18h+203`; its source access,
payload movements and all-wire loop have not disappeared.

The five native port action subcounts also check independently:

| Port | Reads, writes and moves already inside the literal bill |
|---|---:|
| Source | `12U+17m+12h+41` |
| Axis | `4m+8` |
| Guide | `16p+20` |
| Result | `4p+14` |
| Width scratch | `18U+26m+30` |
| Total | `30U+47m+12h+20p+113` |

These are overlap counts, not additional work to add. The source caller's
meter already includes the numerical bank and iterator counters. In the
retained `Bank.open`, `adapter.Port` is `Bank.take`; `NodeEntry` obtains
its guide from that adapter, and the context's port allocation is the
bank's Reentry override. Thus guide and result belong to the bank already
present in `numerical`. The suspected guide/result omission is correctly
recorded as resolved, rather than claimed as a new bug.

## 4. Historical cells and restoration

One source record uses `3w+4` body symbols. Its terminal RIGHT is therefore
at distance `Q=3U+4m+3h+9` from source LEFT. The exact native intervals
visited by construction are

`source [0,Q]`, `axis [0,m+1]`, `guide [0,p+1]`,
`result [0,p+3]`, `scratch [0,W+2]`.

The result post-delimiter cell is reached by a paid move but is not
modified; the suffix remains arbitrary. The scratch reaches the blank
cell beyond its temporary R, so its historical extent is `W+3` cells,
even when current `p` is tiny. The output windows occupy
`4p+h+11` cells including all markers. Retirement never crosses their R
and does not require access to any native owner after lease closure.

All these intervals are unions with prior history, rather than reset
capacities. Mode storage uses an existing B7 private cell. New marker
windows are retired, not deallocated or credited as productive source
work. Access, backing, numerical acquisition and any external transport
remain explicit premises/costs. These facts give the claimed local
history bound; they do not provide a recursive global ownership theorem.

## 5. Child and actual source chronology

The independent checker compares all 21,135 child instructions against
their retained compiler output, relocating only R targets and J targets
by the common offset 378. Writes, roles, moves and halts agree exactly.
It also authenticates all 56 retained files by byte length, SHA256 and
Git blob ID. This is an exact local retained-byte check; remote source
reauthentication is left to the publication gate and was not claimed
again by this review.

The original selected-leaf caller has two unique replaced source blocks.
Reversing those two replacements recovers the pinned function exactly.
The new ports are the actual `iterator.source`, axis counter, live guide,
current result and width counter, in the declared order. The wrapper
selects one fixed forward/inverse entry per requested leg; no numerical
value or current width selects a graph loop. The retained numerical
producer, source selection, owner allocation, lease handling and radix
remain external implementations.

Chronology is unchanged: obtain the selected current lease; build
headers and emit all keys; run the retained radix; verify borrowed
restoration; stage the actual result; close the lease; commit the source;
finish the iterator if needed; retire the five marker outputs. The
retirement graph accesses none of the closed native roles. Inverse key
emission is not rollback of arbitrary old keys; the original identity-key
condition remains necessary for the sorted roundtrip.

## 6. Separate sparse execution and controls

The review checker uses dictionaries indexed by possibly negative tape
positions, distinct defaults for marker/numeric versus binary payload
tapes, and explicit head/visited/history state. Its grammar oracle builds
source fields directly from declared widths and compares every returned
header, every tape's complete nonblank contents, all 27 heads and older
history. Expected destinations are direct padded rotations, independent
of any source query or author decoder.

The bounded successful packet set includes carry thresholds through
`h=65`, a skipped width 1009 with current `p=5`, a 61-record prefix,
different large left/prefix widths, and older retained history of 32,771
cells at current `p=5`. It checks all five native action polynomials and
the exact visited intervals on every case. The four complete joins at
`(h,s,a)=(2,3,2),(3,5,4)` cover both directions. Each runs from the real
header entry through the unchanged full key child; a separately observed
seam run has exactly the same total count and endpoint. The sparse engine
observes the seam without injecting any intermediate numeric value.

Returning mutations skip the height increment, corrupt a copied offset,
omit scratch erasure, omit the final result-head return, or omit offset
retirement. They return HEADERS/RETIRED and are rejected by the independent
full boundary oracle. Additional malformed/binding controls cover a
short prefix field, wrong root tag, dirty width scratch, short result
field, shifted borrowed head and owner alias. No failure cleanup is
inferred from those rejections.

Normal and optimized executions produce identical `RESULT.json` and
`RESULT-O.json`. Reproduce after placing the checker beside the package:

```sh
python3 -B independent_check.py
python3 -O -B independent_check.py
```

Or pass `--package /path/to/literal-leaf-headers`. The default prints
only; `--write PATH` explicitly requests a receipt. The author already
replayed the heavy retained numerical/radix caller; this complementary
review does not repeat that whole provider. Exact source-seam and child
preservation, local universal invariants and independent sparse endpoint
checks are the evidence reviewed here. The five foundational assumptions,
complete numerical source lowering and multiplication bound remain open.
