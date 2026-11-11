# Hot-source inventory for the encoded CRT inverse refinement audit

**Status: work in progress; projection lemma not yet independently verified.**
Prepared for Jerry Chen / CubeJerry with substantial OpenAI assistance.
Canonical base `e54523517d0f03e58352e647c403a5af3e525a57`; immutable inverse
package `c84b0e619c4afb249fe65f568751858f5f1d0c83`,
`research/encoded-balanced-crt-inverse`. Exact file bytes, Git blobs and
read-only local paths are in SOURCE-PINS.json. This audit changes no frozen
source and does not implement or claim a literal compiler.

## Question and preliminary finding

Does the retained existential fixed control-refinement constant C_inv have
a hidden unbounded host dependency on the actual successful hot call path?
The intended exact result is a source-relative projection lemma, not a
generic assertion that every Python field is finite. Unbounded head indices,
backing containers and measurement counters really occur in the source.
The first two represent the tape configuration; the measurement counters
must be erased explicitly. All other inspected scientific control values
have fixed finite domains or are references to encoded tape words.

This presently corroborates a retained premise. A written successful-domain
normalization does not itself emit a binary machine or discharge a selected
compiler/precision/analytic assumption. Publication novelty is undecided.

## Actual inverse call closure

| Source | Reachable component | Excluded same-file components |
| --- | --- | --- |
| inverse_frontend.py | bind; derived Iterator constructor and halving hook | none |
| endpoint.py | Endpoint constructor, run/step, stage/commit, record/field/updated scans | none |
| frontend.py | Iterator construction, shape, record scan, guard preparation, entry, next, base doubling, advance/close; NodeEntry and NodeLease | none on the successful endpoint path |
| owner.py | Bank initial acquisition/take/open/release, Reentry.new_port, Lease.close | external supplied-port constructor case is not used by Endpoint |
| entry.py | Port primitives; Extent comparison with literal4; Entry construction, word setup, pad, invoke, output factory, consume/close; HostedWord aliases | Extent.__int__; Entry.new_port's fresh-Port implementation is overridden by Reentry |
| inverse_producer.py | produce and Arithmetic methods | fault parameter is fixed None by actual invoke |
| words.py | need, Meter initialization/update; Word read/write/step/rewind/msb/zero/erase; Arena zero/literal/copy/free/free_many; Unsigned constructor, compare/add/subtract/subtract_exact/shift_add_bit/divmod | Word/Arena constructors, inspect/input, rollback, times_small, increment_in_place, Ring |
| records.py | fixed tags, read_word, append_word | Tape constructor is replaced by output_factory; Stack, Program, Fields, finite metadata readers and fixtures are unreachable |
| bridge.py | canonical_end | original RowEntry's decoded compiled geometry is not called; frontend supplies its own bridge |

`Arena.zero`'s fallback constructor branch is unreachable under the inherited
64-slot inventory: Entry constructs all slots, eight are protected, and the
producer uses at most24 additional live slots. A free slot therefore exists
whenever a new one is requested. `Arena.literal` receives only the compiled
constant1; its bit_length/range operations are not runtime numerical decoding.

## Bounded scientific metadata

There are 79 private physical roles and one supplied source role. The bank
cursor is in0..63. Entry.control is bounded by124 per current context (64
slot iterations plus60 private Port handoffs). The numerical capacity is64;
live/protected/keep sets are subsets of those fixed slot tags. The available
list has at most56 private tags. Its order is finite metadata, not an
unbounded array. Native slot lookup and role identity tests can use finite
dispatch; they do not use a coordinate value as a host address.

The role map is fixed: bank B0/B1/B2 are guide/canonical-left/canonical-right;
numerical slots8..63 use B3..B58; template uses B59; padded left/right/output
use B60/B61/B62. Numerical slots0..7 alias the eight protected guards. The
seven topology roles and one staging role are disjoint additions.

All phase/shape flags are Boolean. Symbols belong to the14-symbol record
alphabet. Unsigned comparisons return -1,0,1; digit carry/borrow operations
have fixed finite domains. Arithmetic values themselves remain word-role
references. `arena.bits` is the encoded-guide Extent object; its sole width
observation is `>=4`, implemented by four local reads and a paid rewind.

The callbacks, dictionaries and object fields have fixed schemas and fixed
provider bindings. Per-node Entry/Arena/Lease/wrapper objects are metadata
for the one current context. Their identities do not feed numerical data.
The public proof uses linear leases; arbitrary retained stale external
handles and generation-token validation are not in its physical contract.
Unreachable old Python heap cycles are not claimed as literal tape storage.

## Unbounded fields and required projection

| Host construction | Required explanation |
| --- | --- |
| Port.head / Word.head integer | actual tape-head coordinate, never a finite-control register |
| cells[head] | read/write at that actual head, not arbitrary indirect addressing |
| Port read past list length | infinite blank tape extension represents the default BLANK |
| append at list frontier | ordinary write at current blank cell; valid paths do not jump over a gap |
| Word.step's head/length assertion | a successful-domain invariant: head stays between origin and current RIGHT, inside retained backing |
| Bank head==1 assertions | consequences of inherited actual head-return and retired-role invariants |
| id(backing), alias sets | finite equality pattern of the80 admitted physical roles; absolute addresses are irrelevant |
| Meter.reads/writes/moves/allocations | unbounded diagnostic counters; scientific branches do not read them |
| Meter.peak_live | diagnostic update; finite anyway because the slot inventory is fixed |

Erasing a guard is justified only if the admitted-domain invariant implies
it. The pending proof must separately cover one-sided head safety, current
word delimiters, source/guard/bank separation, clean ownership and all erased
assertions. It must not claim equivalent rejection on arbitrary malformed
streams or malicious port mutations.

The measurement counters are read to update themselves; this is not the
stronger false assertion that no production statement reads them. The
relevant noninterference claim is that no read reaches a scientific branch,
symbol write, role choice, movement direction or numerical return.

## Literal representation still to distinguish

A14-symbol alphabet has a fixed four-bit encoding, with logical BLANK
mapped to the all-zero codeword. Encoding choices need not preserve the
source integers' binary spelling: source BLANK is integer4. A source step
can be simulated by a constant number of bit reads/writes/unit moves if
roles and control are already finite and cell alignment is maintained.
This generic observation is known; it is not yet an emitted compiler.

The actual caller must still supply this encoded source, its precise role
ownership, initial head alignment, private blank storage, and any needed
serialization/conversion/return costs. An abstract source supplied as a
Python list does not supply a physical caller serialization theorem.

## Narrow predecessor comparison

- Canonical #5486, `crt-complete-binary-refinement`, proves literal lowering
  of the exact fixed8,242-instruction u2/t2/y8 repair program, with emitted
  blocks and an explicit constant. It explicitly excludes variable geometry
  and external ROM/raw source production. It is not a theorem for this
  changing-precision numerical/endpoint closure.
- #5219's Entry proof gives source-operation representation refinement and
  explicitly stops before a literal finite machine.
- #5505's owner proof gives changing-precision reuse and historical-tail
  safety, explicitly leaving complete binary numerical lowering open.
- The current frontend/endpoint proofs already assert a fixed-control
  refinement existentially. A source audit that validates that claim alone
  should be recorded as confirmation, not sold as new implementation.

## Next action

Complete the assertion/noninterference case split and finite-metadata
normalization. Any newly discovered scientific dependency on a host head,
length, counter or stale identity requires a counterexample or a separately
priced replacement. Stop with a novelty-negative checkpoint if the exact
audit confirms only the retained source-model premise.
