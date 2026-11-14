# Independent review of all-current-division integration

**Verdict: PASS, after clarifying the exact-eight physical Entry ABI.**
Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance.
Base `e54523517d0f03e58352e647c403a5af3e525a57`; retained B10 publication
`c4ab5dab6914a04cb86d1fe54eb763b35cc7eeb1`.

Reviewed binding SHA256:
`1b62577836ffc5906bd749b3705cfb3873cf9b15380224648fff924315efc8c9`.
Final proof SHA256:
`cc65e3f5d559501fa854e263a46b647be18ef0bdbd6eab0e0e57d803f0714b11`.
The graph remains the already independently reviewed B10 graph
`d36e8220def8efb2baed793d0bea6f0a19b0903b5b005b730652b5bb7d121194`.
No new numerical or physical-dispatch implementation is hidden in this join.

## What was independently executed

`review_core.py` is the exact frozen independent B10 checker, SHA256
`316aace11634045aa0381cb96a22e393f6f9bf857794cf1f6223b9dcfcdf5f2e`.
The new check imports its separately written CPU, backing adapters and
allocation-only oracle. It does not repeat B10's complete dispatch or
standalone arithmetic suite. The author hardware and old divider are not
used as the expected arithmetic or owner-relation oracle.

The new integration executes:

- One complete Endpoint source forward/inverse roundtrip with nonleaf
  groups in both directions.
- One complete source/payload/key roundtrip with padded coordinates.
- 192 actual raw divisions, including 28 unit divisors, across 11 producer
  invocations, with 11287911 new literal instructions.
- A full independently constructed 64-slot boundary bijection for every
  division, actual eight-borrowed/56-owned backing identity, all incoming
  bytes/heads, the separate template, and entire blank inactive tails.
- Exact source-method code-object and call-line provenance at each raw
  interception, beyond matching a function name or sampled ordinal.
- Four operational controls: outside producer, foreign arena, returning
  swapped source descriptors and attempted old-provider fallback; plus
  explicit checks that omitting either meter-overlap subtraction changes
  the expected workload bill.

All actual replaced execution runs with the old divider unavailable.
The old source is used separately for forward-output regression and cost
comparison, not to choose or supply results to the new graph. The numeric
oracle is integer quotient/remainder. The producer oracle uses the sum of
CRT idempotents, rather than the source's incremental Garner recurrence.
Normal and optimized runs agree exactly; `RESULT.json` retains the evidence.

## Source admission and exhaustive interception

The exact source has only two raw-call expressions: `remainder` and the
Euclidean loop in `inverse`. The forward and inverse variants have the same
two expressions; their actual line numbers differ by the retained header.
The checker identifies their code objects and exact AST call positions.
The source is otherwise the pinned current producer, with fault=None.

Every remainder divides by an admitted modulus M>1 with a zero high bit.
Every executed Euclidean division has a nonzero current remainder strictly
below M, including the final divisor one. All numerators remain complete
P-bit Words. No N<D assumption is needed. Distinctness follows from the
real allocation lifetimes: newly read modulus/value, held prefix/lower,
fresh quotient, and the separate Euclidean copies/remainders cannot alias
their still-live partners. The original source's live bound leaves room for
the two new outputs. New peak occupancy is no larger than the old divider,
which also held its scan copy.

The wrapper contains no numerical decode, half predicate or ordinal gate.
It verifies an active exact producer and arena, then always calls the
reviewed divider. The saved prior method is used only to restore the
namespace after the scope. Both scope controls fail before any graph
instruction; the deliberate fallback edit reaches the unavailable-provider
sentinel. A descriptor swap still reaches the unchanged graph's DONE halt,
but the independent source-value oracle rejects its wrong output.

The source numerical theorem permits up to eight borrowed live Words, but
the physical Entry initializes **exactly** roles0..7 live and the binder
requires them. I requested this distinction in the theorem statement.
The final proof now makes it explicit. Those eight dirty values can be
arbitrary or unused; a generic Arena with fewer protected live roles is
outside this physical join. No code change was necessary.

## Repeated weak ownership relation

The local B10 relation extends across every call. Retained arithmetic is
equivariant under the current live-reference/free-stack correspondence.
At a division boundary, compose that correspondence with the local relation
that preserves incoming live objects, relates Q/R, and pairs remaining free
stack positions. This does not require the global correspondence to become
the identity after each replacement.

The independently implemented old allocation trace uses only input integers
and quotient-prefix decisions; it never runs old numerical Word arithmetic.
At each actual return it yields a full bijection with matching live/free
membership. All physical identities stay fixed within the actual new run.
The equality is between two executions, not a tape permutation or a
transfer of historical capacity.

The unordered final cleanup requires the separate weak step already proved
in B10: disjoint clears commute on bodies and returned heads, followed by
re-pairing free-stack positions while preserving kept/protected objects.
The unchanged consumer and Entry retirement then reach the same protected
terminal set. The observed source-only inventory contains 83 owners; the
two payload legs retain 200 distinct source/adapter histories. They are
different inventories and are not interchanged in the proof or receipt.

Termination follows by induction on the admitted original finite execution,
with the same arithmetic branch outcomes and a terminating P-digit graph at
each call. Malformed-core rollback is not added. Histories remain unions on
each actual owner: max of its earlier history and current P+2 frames, and
max of each descriptor's old extent, eight-cell grant and later header use.
The number of calls does not create new numerical or descriptor owners.

## Independent producer oracle

For left moduli M_i and current coordinates x_i, put M=product(M_i) and
`r_i=(product_(j<i) M_j)*x_i mod M_i`. The direct sum

`sum_i r_i*(M/M_i)*inverse(M/M_i mod M_i) mod M`

is the reconstructed lower value. A padded left coordinate instead makes
the returned lower zero, while retaining product M. On each right record,
the offset is lower times the inverse of the complete preceding prefix,
modulo that record's modulus. The forward/inverse coordinate is shifted by
plus/minus that offset when valid, and otherwise preserved. This derives
the full output stream, lower/product and validity flag independently of
the source's incremental recurrence. Every observed producer boundary
matches, including nonleaf groups and invalid coordinates.

## Complete division-workload invoice

The exact raw-call count is
`J=3m+2t+v+2 sum_i e_i`, since each Euclidean iteration contributes both
its division and quotient reduction. The known bound e_i<=2P+1 and the
product reserve imply m+t<=P-2, so `J<=(P-2)(4P+5)`.

Four setters plus one graph call cost at most
`930P^2+1395P+14322`. One acquisition per descriptor lifetime costs89.
The quartic bound is supported by the exact difference polynomial

`2^15(P+2)^4 - [89+(P-2)(4P+5)(930P^2+1395P+14322)]`

`=29048P^4+259354P^3+742629P^2+1105492P+667419`,

whose coefficients are all positive. The checker independently constructs
this polynomial by integer convolution. It also checks each observed
logical bill and the exact complete graph invoice, including every setter.

Actual numerical actions increment the arena meter and leave backing Port
meters unchanged. Selector actions enter the separate marker meter.
After subtracting those overlaps once, the new residual source invoice
equals the old same-workload source invoice minus every old raw-division
action. The payload marker remainder equals its unchanged same-height
value; it is not assumed universally equal to14. The full source-only
selector meter is exactly the new graph's selector count.

The control invoice is `256+32I+16400J`, with explicit additional grants and
all unchanged native, header/key, radix, payload, source preparation,
serialization and retirement costs retained separately. No speedup is
inferred by adding unlike units, and no complete producer time is replaced
by the division subset bound.

## Reproduction and limits

Place both scripts beside the reviewed package and run:

```sh
python independent_check.py
python -O independent_check.py
```

From this separate directory, use `--package` with its path. The default
prints JSON without writing; `--write PATH` explicitly saves a receipt.
The reused independent core is pinned before loading. Watchdogs, snapshots,
oracles and receipt arrays are verification instrumentation.

This establishes the stated integration review, not a new elementary
division theorem, a whole literal numerical producer, complete source
compilation or multiplication improvement. Other arithmetic, source
admission/access, finite binder lowering, grants and acquisition remain
retained obligations. All five foundational assumptions and kappa remain.
