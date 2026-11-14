# Literal all-wire destination-key pass: bounded feasibility

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. Exact host loop: B5,
CubeJerry `be17dd21af36a8b0546942299ebca7b1c83c4675`, package
`research/current-crt-direct-switch-consumer`, `caller.py:prepare_keys`.
The unchanged called whole-row service is frozen B6 graph
`f8f0bd615531c914efc110d8a9d5ce2fafa2b00c8a568bdbfb86bf24868a0ef7`;
its publication pin is pending. No B7 graph is implemented by this note.

## Source gap and actual payload domain

The host `prepare_keys` builds an encoded h-bit index from unary width,
copies it to address, routes that current wire, writes the returned key,
clears address, increments index until carry, then checks/rewinds the
payload and retires index. B6 lowered the called route; this surrounding
per-record controller remains unlowered. The proposed result is its
complete physical pass for every encoded h, not a new point/radix algorithm.

The actual source ABI is **fixed 13-bit codewords**. `binary.py` sets
WIDTH=13; '<','>','0','1' have numeric codes 5,6,2,3 respectively, LSB-first.
An opaque record t has code 4096+t for 0<=t<4096: twelve arbitrary payload
bits followed by tag one. `RecordTape.pass_payload` skips precisely twelve
bits and checks this tag. The theorem will permit zero, duplicate and
correlated 12-bit payloads; distinct nonzero fixture tags are only observers.
It will not claim arbitrary payload width or another codeword alphabet.

The supplied frame is '<', then N=2^h records, then '>'. Each record has
one opaque codeword followed by h allocated key-bit codewords, MSB-first.
Address/index are LSB-first. Existing keys may be arbitrary valid h-bit
values because the caller authorizes their replacement. The frame contains
`13[2+N(h+1)]` physical bits. Payload entry/exit is the first bit of '<'.
Framing, exact record count and existing key allocation are explicit input
contracts; arbitrary malformed-input rollback is not claimed.

## Proposed theorem and physical roles

For h>=1,p>=h+1 and B6's explicit consistent header/unary-width ABI, one
fixed finite graph with forward/inverse entry ports writes pi(i) or pi^-1(i)
into record i for every 0<=i<2^h, where pi is the canonical padded rotation.
It preserves all opaque payload bits/markers, returns every head and
retires index, address and point scratch. No host record loop, decoded h,
index or key, or callback chooses a query or payload operation.

Keep B6 roles 0..19; role18 is now initially blank owned address storage.
Add role20, initially blank owned index, and role21, the actual binary
payload with exclusive key-write authority. There are 22 fixed owners.
Source/header production, grants, disjointness, prior backing and external
acquisition remain explicit; source numerical and sorting roles are outside.

Two fixed B6 control copies can carry parent direction continuations while
sharing all owners. Only fixed PC and successful-return edges change.
Initialize index to h zero bits by scanning width. Each iteration skips the
actual payload, copies index to address, invokes the unchanged whole-row
entry, reads its address high-to-low to validate/write the existing key
codewords, clears address and performs literal index carry. The carry
wraps after exactly 2^h records. A final endpoint check and 13-bit-aligned
reverse scan return the payload head, and index is fully erased.

The loop invariant ties index i, physical record i, prior destination keys,
unchanged payload and restored point bank. Payload tags prevent the aligned
reverse scan from mistaking an opaque word for '<'. No decoded N is stored.

The inverse entry computes inverse-routing destinations; it is not an inverse
of overwriting arbitrary old key values. Keys are explicitly disposable
workspace. The full forward/sort/inverse/sort roundtrip restores the original
keys only when they initially encode their physical positions, as in the
actual predecessor fixture. Arbitrary 12-bit payloads remain preserved and
permuted by the corresponding routing composition. This distinction must
remain in the eventual theorem and caller proof.

## Complete optimistic budget and representation seam

Retain the complete B6 route allowance

`R(h,p)=(2h-1)[1024(h+3)^2+128(p+h+3)]+14p+72h`.

For N=2^h, the proposed whole pass costs

`T_keys <= N R(h,p) + 1024 N(h+1) + 128(h+1)`.

The conservative new linear term covers startup, h-bit index/address copies,
each of the thirteen physical bits per validated/written key codeword,
payload/tag scans, carry/return, address erasure, every fixed call/return,
endpoint validation, full payload rewind and index retirement. Literal
carry propagation over the complete counter cycle sums to N-1, but even a
looser O(Nh) charge fits this envelope. Exact emitted-path constants must
replace or justify these provisional coefficients before publication.

The unchanged point bank's fixed historical union is
`p+11h+bit_length(h)+48`. Index/address add at most 2(h+2) new cells,
plus any explicit marker/frontier allowance from the final implementation.
Thus new scratch is O(p+h), independent of N and query count, and retains
every earlier larger extent. The full payload frame is supplied, remains
allocated and is included in entry history; writing keys does not allocate
another copy. Every backing access, first write and head return is paid.

The payload port is physically binary: every read/write is one actual bit,
and each move is one actual bit position. The other twenty-one roles retain
B6's fixed marker alphabet. A static per-port naming of binary0/1 as the
graph symbols '0'/'1' is permissible; a facade decoding thirteen bits into a
host symbol is not. Every thirteen-bit check/conversion must be emitted
explicitly. The local graph invoice counts all R/W/M/J/H instructions;
it is not silently added to a different retained numerical tariff as a
whole-caller binary bound.

An actual caller check can replace exactly B5's `prepare_keys`, keeping the
current source lease/header, source stage/commit and h radix passes unchanged.
Report `(source symbol work, literal key-pass work, remaining outer symbol
work, radix bit work)` separately. The radix bound remains its predecessor's
`h[7740(N(12h+8)+10)+144]`, and all source acquisition and disposal stay paid.
This lowering makes no ROM-reuse, E(p,ell), kappa or full multiplier claim.

## Narrow overlap, verification and stopping rule

Read exact canonical key-port (#4982), paid-key (#4795), transported-key
(#4739), binary-radix (#5015), and complete-repair-control READMEs, together
with B5/B6 source. The key services compile fixed retained exceptional-key
geometry; the radix service already sorts arbitrary finite encoded streams;
the complete repair controller is fixed u2/t2/y8 supplied-ROM geometry.
None supplies this variable-h all-record loop at the new B6 direct route.
These literal primitives and their codec are dependencies, not claimed anew.
Bounded live title/body searches found those same key packages; #6629's
compact routing ROM explicitly leaves finite-control lowering and physical
caller pricing open and changes canonical routing choices. This search does
not cover arbitrary historical diffs or unpublished work.

First verify every B6 instruction/entry/halt relocation. Use direct literal
execution with no per-record callback; test complete key streams at h=1,2,3
and selected h=5, arbitrary/duplicate/boundary payload values, older scratch
history and translated bit origins. Check every physical payload bit, key
orientation, exact 2^h whole-route invocations and scratch/head retirement.
Use returning lost index carry, wrong key orientation, stale address,
premature payload return and omitted clear controls; reject malformed tags,
key codes, short/long frames and aliases within the stated failure boundary.
Then execute the actual #7388 four-tag and modulus3/left2 source-plus-sort
roundtrips using the unchanged providers. An independent interpreter should
check the binary/marker port seam and full-key endpoints.

Stop if an exact predecessor already has this physical loop; if construction
needs a host payload decoder, unbounded dispatcher or input-sized fresh bank;
or if codec/head alignment or complete costs fail. Preserve the narrower
fixed-12-bit payload domain rather than silently claiming a general record
width. No implementation should begin before the lead's scope review.
