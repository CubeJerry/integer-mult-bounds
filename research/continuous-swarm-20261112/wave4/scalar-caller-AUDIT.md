# Wave 4: selected scale-wrapper source/ABI stop decision

**Stopped at the specified production-interface gate.** This is a recovery
audit, not a proposed research contribution or proof of nonexistence. There
is no new scalar algorithm, kappa claim, physical wrapper or upstream PR.
Canonical base is `e54523517d0f03e58352e647c403a5af3e525a57`.

## Actual call and existing proof coverage

The exact selected caller contains 3,095 events. Its first native occurrence
is zero-based event 21:

`["J",1,[1,0,19,20],[39,38,"-1","1/2"]]`.

There are 18 J occurrences, at indices
`21,66,117,168,219,270,321,372,423,2166,2299,2399,2497,2593,2687,2779,2869,2958`.
The selected native word has 71,261 source instructions, 1,480 public fields
and 51 owned labels. The selected application checker already proves each
J's injective mapping of 400 main fields and 1,080 fresh public helpers.

For example, at J21 its real source mapping is:

| Native public slot | Exact caller owner label |
|---|---|
| 0 | `(main,0,1)` |
| 112 | `(main,0,0)` |
| 772 | `(main,0,19)` |
| 882 | `(main,0,20)` |
| 17 | `(main,15,39)` |
| 129 | `(main,15,38)` |
| 3 | `(helper,21,3)` |

These labels come from the actual caller's port map, not an invented equal
frame or coefficient class. Main owners are reused across later calls;
helpers include the actual caller occurrence index and are distinct across
calls. Owned native labels are not public inputs and receive no scale-wrapper
conversion in the reviewed count.

Thus the existing 53,280 total is exactly `2*18*1480`, with 26,640 operations
in each direction. It is already supplied by
`pr7000-application/check_exact_scalar.py`, which adds `18*word['public']`
copies of each coefficient to a Counter. The reviewed source does not emit
53,280 corresponding executable table calls. Re-emitting those counts or
attaching new tokens to the same owner map would not establish a new join.

## The exact missing implication

The desired next lemma would say: at the real J21 physical boundary, each
actual public owner is produced as the fixed scalar table's complete coded
field, and one chronological wrapper scales each entrance by 1125, waits for
the complete native invocation, and unscales each exit by 1/1125 on that
same physical owner. It would have to provide an executable public-port
selector and format producer, and price their head movement, codec, staging,
entry work retirement, return and retained history.

The bounded source inspection does **not** supply those entry objects:

1. `pr7000-application/check_application.py` constructs Python tuples such as
   the labels above and checks injectivity and source chronology. It has no
   physical owner/segment constructor, head, encoded bit stream or dispatcher.
2. `shared-wire-split-composition/frozen/physical.py` is a finite-field vector
   verifier of the native word. It is not a producing tape caller.
3. The actual #6968 `source_ir.current_caller` requires the older
   `kind="complex", pairs=16, prefix_pairs=7, ambient_rank=145` family and a
   `physical_events` stream of LOCAL operations. Supplying the exact selected
   #7000 word and caller to that unmodified function finishes the local-word
   check and raises **`KeyError: 'kind'`** at the caller family check. This
   diagnostic is a schema boundary, not a correctness bug in that predecessor.
4. #6968's `source_literal` explicitly leaves whole-job native normalizers
   outside its original scalar grammar. It accepts authenticated old local,
   boundary, outer and query ADD/SCALE events; it is not a #7000 wrapper binder.
5. `selected-compiler-occurrence-layout` is an existence/layout theorem for
   the old selected6030 source. Its README explicitly leaves the generated
   final occurrence stream, dispatcher and numerical machine open. The other
   inspected owner-staging and scalar-stream packages likewise leave actual
   caller alignment/production open or bind earlier sources.

This is a narrowly sourced missing interface. It is not an exhaustive claim
that no repository package or unpublished branch can ever supply it. The
checked overlap included current-scalar-flat-tables, p104-owner-scalar-staging,
p104-exact-scalar-records, selected-owned-dispatch, selected-joined-dispatch,
selected-compiler-occurrence-layout, physical-scalar-stream and source-specific
application checks, plus bounded live searches. None supplies the real J21
physical producer used by the proposed join.

## Why the arithmetic and optimistic budget do not close it

#6968 already provides fixed literal SCALE tables for both coefficients.
For common fractional grid `F=p+D`, the selected application supplies signed
width `W=p+h+2D+3` and padded width `U=W+26`, including its retained exact
division/headroom induction. A common U-bit format can represent the ideal
completed scalar values without adding a new rational-arithmetic premise.

But that numerical format statement does not construct #6968's physical
ABI: complete signed little-endian components, virtual delimiter 2, canonical
three-bit symbol codes, a physical blank frontier and protected local origin,
with separate work tapes and borrowed contexts. The new literal phase/egress
programs use raw MSB-first common-width packets and Gamma headers; value
equality is not a codec.

If an actual producer supplied R positive-even U-bit components and the
required scalar ABI, put `L=R*(U+1)`. The existing blank-work core allowance
would be `2048*(L+1)` per direction, hence
`6062080*(L+1)` for one complete 1,480-field call with equal extents, or
`109117440*(L+1)` for all 18 calls. Unequal extents require their actual sum.
This is only an optimistic core invoice. It does not pay an unconstructed
owner selector or codec, dirty work prefixes, borrowed contexts, source
access, fixed-table setup, or history retained by a physical producer.

For the inherited scalar ABI itself the output and guide work extents are
`3L` and `3L+3`; earlier backing remains allocated. The actual entry K0 and
the producer/codec's extra backing still need a physical interpretation.
Assigning them arbitrary new tokens or manufacturing fixture Tape objects
would silently replace the missing implication rather than discharge it.

## Restart trail

`check_census.py` is a small recovery checker for the exact owner census and
the old-producer schema boundary. Run it with the shared canonical repository
and the already retained selected native bytes:

```sh
python -I -W error -B worker-a4/check_census.py source \
  worker-b3/research/literal-native-quadratic-phase/reference/selected-native.json.gz
```

It is not a physical wrapper replay. It pins scientific inputs, reconstructs
the source owner map and records the compatibility diagnostic in RESULT.json.
No scalar tables or native callbacks are fabricated. The next useful task is
an actual source-to-physical owner/format producer, with a precise machine ABI;
once it exists the fixed rational tables can be joined without a new scalar
algorithm. All five selected assumptions remain retained.

Prepared for @CubeJerry with substantial OpenAI assistance. Credit the
selected #7000 application, #6968 scalar/lifecycle source, prior compiler
layout and owner-staging packages. This audit and its count are not offered
as their results repackaged into a contribution.
