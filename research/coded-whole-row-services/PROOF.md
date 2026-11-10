# Complete coded rows at the actual recursive Controller boundary

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance.
Apache-2.0. This is a source-relative universal interface proof, with bounded
executable corroboration. It is not human or proof-kernel acceptance.

**Publication withheld for predecessor overlap.** The scoped proof and graph
below remain preserved, but this is a validation/control variant, not a new
missing-callback or foundational-assumption result. The exact comparison is in
overlap-review/REVIEW.md.

## 1. Exact source, domain and claim

The base is `e54523517d0f03e58352e647c403a5af3e525a57`. The actual
`Controller` is the byte-identical machine retained by #6999 at
`research/scalar-table-microcontrol/vendor/machine.py`, Git blob
`acf475e4fccaff2fb64bd5b0b3f3fc0d246dc592`. Its original lifecycle package
and proof came from CubeJerry commit
`ab239cb6ee884e7a900dd9101c34448077fad0b0`. The actual `Stack` is #5356's
`research/delimited-continuation-stack/stack.py`. The executable leaf binding
uses #6968's unchanged exact scalar table. DEPENDENCIES.json records every
retained byte, and the original proofs/notices remain in retained/.

The lifecycle theorem alone assumes ordinary row `is_leaf`, `prepare`,
`install` and `collect` services. However, the earlier
`compiled-row-stock-dispatch` at CubeJerry commit
`5c59d247d51c6e1fca0dead3ed2139b6802b3a15` already implements all four
callbacks against this exact machine blob, with encoded production-relative
geometry and cutoff checks. Its proof/table bytes are retained in the current
canonical tree through `current-coded-gaussian-leaf/vendor/binding/vendor/dispatch`.
The present proof describes a narrower supplied-pattern implementation with
per-component validation and exact local clocks. It does not close a previously
unsupplied successful row-service premise. PC, push/pop, dirty retirement and
occupied-owner ascent remain credited predecessor results.

Fix an integer productive width w>=2 and a fixed Controller program. Its q
payload tapes and four outside tapes are fixed before runtime inputs vary.
Reserve one private **nondata** index g as `payloads[g]`, put it in
`protected_ports`, and keep it out of every instruction's data ports and
primitive work. This exact existing bank role is the format guide G. The
Controller's existing `bridge` and `child_header` are used without adding
another tape. In the executable binding g=w, q=w+3, and the two other
private payload roles are the scalar provider's work tapes. G is also a
readonly primitive context in that binding.

A format is a positive finite sequence of positive signed-component widths
(h_1,...,h_c). A component consists of its h_i little-endian two's-complement
bits followed by virtual COMPONENT=2. Every virtual symbol is represented by
the actual Controller code:0=000,1=001,2=010. A complete row has physical
length B=3*sum_i(h_i+1). G contains precisely the corresponding **zero row**:
000 at each numerical bit position and 010 at every component terminator.
This is raw binary descriptor data on G; its physical boundary is LEFT and
its frontier is physical BLANK=6. A zero row contains nonzero separator bits.
It is neither an empty body nor B literal zero bits.

For the full recursive result, each productive field and each currently
issued owner contains R=w^d complete rows of this same format, d>=0.
The provider and emitted-program contracts preserve this common format and
the complete within-row fields, including any spectators. Every PAID site
uses the homogeneous whole-row interpretation below. Any additional data
or source-specific descriptor that a numerical provider needs is a separate
supplied interface; it is not manufactured by these row services.

All data ports enter at their current local origins. Payload markers are
LEFT; bridge and staged header have BASE markers. Bridge/header are empty
at their documented entry points. Ports and their backing are distinct,
ancestors are protected, and old retained blank tails are allowed. The
initial source and G are supplied. Their production costs T_input and
F_format(B) are explicit terms. There is also a separately paid finite
table-assembly/installation cost F_graph(w). None is inferred to be zero.
Current bodies are contiguous, and their higher retained cells are blank
under the valid entry/return contract. A frontier check does not inspect an
arbitrary hidden dirty tail beyond that frontier.

**Theorem.** For every fixed w, `compile_rows(w)` emits one finite graph,
independent of B,R,d and numerical values, on the same seven-symbol alphabet
and the existing w+3 row-service ports. `RowServices` supplies the exact four
callback signatures of the actual Controller. On the stated successful
domain it classifies the actual source, stages/installs the current format,
stripes complete rows into every productive field, and collects every
returned field before pop. All row-service heads return to their origins;
all borrowed bytes and older segments are preserved. The unchanged
Controller then restores every suspended parent and replaces exactly the
issuing owner. The costs in section5 include every new scan, copy and rewind
and every inherited administrative term.

At a single boundary installation/collection work for every positive
multiple R of w. The power-of-w premise is needed for this particular
one-row stopping rule to yield a complete recursive caller. It is not the
selected variable-rank, remainder/padding or numerical-cutoff interface.
No new kappa or complete selected-assumption discharge is claimed.

## 2. The format parser is physical finite control

The graph has only read-and-branch, one-cell write, unit move, halt and
reject instructions. Every row names a fixed physical port. The Python
dictionary is the emulator's representation of a fixed finite control
table, not runtime lookup in an input-dependent program. Assembly uses w
only. There is no instruction for an address, length, row number, decoded
integer, division, slice, allocation, host recursion or whole-word clear.
Optional observers and step counters are absent from the mathematical
machine and cannot affect a transition.

Within a row the state holds a phase modulo3, whether the current component
has a bit, whether a component has already ended, and which of the two
possible guide-code prefixes is being read. At phase0 the guide and source
must both start with 0. At phase1 a guide0 requires a source0, whereas a
guide1 requires source1 and a previously nonempty component. At phase2 the
guide must be0. Its numeric prefix00 permits source0 or1 and marks the
component nonempty. Its separator prefix01 permits source0 only and marks
the component complete. A guide frontier is legal precisely at phase0,
after at least one completed component, with no unfinished component.

Induction on complete three-bit codes proves that the guide is a positive
canonical zero format, the source has exactly the same delimiters/widths,
and only numerical bit positions may differ. Induction also proves the
converse: every source row of that format follows the accepted transitions.
Thus a different canonical layout of the same physical length is rejected;
the comparison is stronger than a length check. For complex scalar callers,
c must additionally be even. That numerical-provider condition is separate
from generic signed-component row transport, and the actual scalar fixtures
use complete complex pairs on a common component width.

The parser has 14 reachable guide states,16 guide-to-source edges and 20
source-bit edges. A copying row routine has 133 states; its scanning-only
version has 73. A positive descriptor copy has 16 states. Counting the
rewinds, frontier probes and terminals gives exactly 273w+125 graph states.
In particular runtime component widths do not appear in the state count.
Every accepted transition reads/writes only the current segment or its
own marker. Rewinds stop at that marker and never traverse an ancestor.

## 3. The four services

### Classification and preparation

`is_leaf` checks one complete row of productive field0 against G, using
unit moves on both tapes. At the end of this row it tests field0's next
physical symbol. BLANK means exactly one row and returns leaf; a binary
symbol means more data and returns inner. It restores both heads. On the
promised R=w^d domain this is equivalent to d=0. It does not read d or R.
The rest of the field is not prevalidated by this one-row scan; the full
format/geometry contract remains the entry premise and installation checks
the complete owner when it is distributed.

`prepare` physically copies the positive raw binary G into the empty
child_header and returns both heads. Its source marker is LEFT and its
destination marker is BASE. Thus the staged descriptor has H=B cells and
preserves the actual component delimiters. The header contains this format
guide alone. Calling it a production e/f/K/rho descriptor would be false.

### Installation

After the actual push, all current child payload segments are empty.
`install` first copies child_header into the newly empty current G and
returns both heads. It then reads the existing complete owner bridge and
cycles through the fixed fields j=0,...,w-1. One row uses G as its actual
format delimiter; it copies exactly that complete row, verifies the source
format and each destination blank, then fully rewinds G.

After a successful batch t, field j contains precisely input rows
j,j+w,...,j+(t-1)w in their original order. This follows by induction on
the fixed field phase and the scanned code bits. End-of-input is accepted
only at the next field0 boundary, after at least one full batch. Partial
rows and partial productive batches reject. Hence R=wn rows produce n
rows in every field, and input row r goes to field r mod w, local row
floor(r/w). These indices describe the proof; the machine computes neither.

It finally rewinds every productive field and the bridge. G and the staged
header are already at their origins. The bridge and header still contain
their complete inputs: the actual Controller subsequently retires them.
Their cleanup is included in the inherited administrative invoice.

### Collection

`collect` copies one checked row from field0, then field1, through field w-1,
repeating complete batches into the empty bridge. Each individual row is
checked against G, so every returned component delimiter and width is
verified, including zero-valued rows. It accepts the end of field0 only at
a batch boundary, then explicitly tests every other field for its frontier.
Shorter and longer returned fields therefore reject. Empty fields reject.

If each field contains n rows, output row tw+j is exactly returned local
row t of field j. This is the inverse of installation when the fields are
unchanged, and it transports all changed returned fields in the stated
order when a child computes on them. It returns every field, bridge and G
head; the source fields and G remain unchanged. Shape guards do not prove
the numerical meaning of child output. A deliberately reordered collector
can preserve shape while producing the wrong endpoint; the controls detect it.

## 4. Binding to actual suspension and occupied-owner return

The unchanged Controller first copies its actual issuing owner to bridge,
then invokes prepare while the parent G is still accessible. It writes the
fixed-width continuation PC and calls the actual #5356 Stack.push on all q
payloads, including G. Push leaves each parent body intact and installs a
new LEFT marker at its frontier. Bridge and child_header are outside that
bank and survive the push. Install then supplies every productive child
field and its current G. Retiring bridge and header leaves their shared
outside roles ready for another nested call.

Every child field has R/w rows of the same complete within-row format.
If R=w^d and d>0, the child has w^(d-1) rows. The fixed emitted program
advances through its finite instruction sequence, and its recursive calls
strictly decrease d. Supplied terminating leaf/native kernels therefore
give a terminating finite call tree. There is no host depth object or
depth-indexed row descriptor in this construction.

At child RET, the unchanged Controller invokes collect first. The complete
returned owner is now on the outside bridge. It then retires all q child
bodies, including the owned child copy of G, before calling the actual
Stack.pop. The imported stack theorem restores every parent payload,
head and saved PC. This restores the parent's borrowed G as well.
The Controller consumes the physical saved PC, locates the corresponding
PAID owner, retires its occupied old body, transfers the bridge output to
that exact owner and retires bridge. Every other parent word is unchanged.

Induction on the finite ordinary call tree proves this statement at every
return. At the root G is protected and is preserved by root cleanup. It
is important that G is an owned installed copy at a child but a borrowed
descriptor at the root. Protected numerical access alone does not authorize
destroying the parent's descriptor; delimiter ownership supplies that distinction.

This is a successful-call theorem. A malformed return can be detected only
after some earlier complete rows have been copied. Rejection need not erase
partial output, rewind every head or roll back a prepared child header.
No exception-cleanup or hostile-callee containment contract is asserted.

## 5. Complete paid invoice

One emitted read, write, unit move or halt costs one local transition. The
terminal contributes one; every other accepted instruction performs one
raw tape action. The original Controller/Stack administrative counts use
raw reads/writes/moves. Combining them requires adding the new service
transitions, not charging their actions twice. The verifier subtracts each
service's measured transitions minus its terminal from the enclosing raw
meter before comparing the old exact invoice.

Rewinding from offset h costs 2h+3. Positive raw binary copy of B cells
costs 5B for the loop, one frontier read,4B+6 for both rewinds and one
terminal:9B+8. The same copy embedded before another phase omits that final
terminal. A checked copying row costs 7B local actions plus its guide
frontier read and 2B+3 rewind:9B+4. A checked scanning-only row uses 4B
actions before the same frontier and rewind.

Writing L=RB for the owner length and assuming R is a positive multiple
of w, the exact successful service counts are

| Service | Exact local transitions |
| --- | ---: |
| is_leaf |8B+9|
| prepare |9B+8|
| install |13L+4R+R/w+9B+3w+12|
| collect |13L+4R+R/w+4w+4|

For install there are R rows, R/w+1 batch probes,4L+3w+3 final rewind
actions, and the separately paid9B+7 guide installation. Collection also
checks the other w-1 frontiers. These terms give the displayed constants.
No component parsing uses an extra word-sized operation: its finite flags
are carried by the same guide/source-read transitions.

Let S be the actual sum of parent occupied payload lengths, C the actual
sum of child occupied payload lengths just before retirement, q the number
of payload roles and b the saved-PC width. The unchanged machine's
descend-plus-ascend administrative invoice is

    4S+5C+18L_in+13L_out+5H+38q+27b+103.

Here L_in=L_out=L and H=B. Adding classification and the three actual
services, with no term removed, gives

    4S+5C+57L+8R+2R/w+31B+38q+27b+7w+136.             (1)

This includes input and output relays, all productive fields, current
guide staging/installation, complete child retirement, occupied-parent
replacement, physical saved PC, push/pop and every stated rewind.
It excludes the numerical child computation, emitted Controller instruction
dispatch, the separate3-action RET parent test, and initial/final input
production. Those are explicit additional costs, not zero-cost operations.

A complete execution charges F_graph(w)+T_input+F_format(B), sums(1) over
nonleaf PAID calls, adds8B+9 and the full primitive cost at every leaf PAID,
adds every SERVICE/INIT/COPY/CLEAR cost, all RET parent tests, root cleanup
and the finite emitted-instruction dispatch cost. Primitive costs must
include their table fetches, coded accesses, work retirement and head
returns. The present row theorem supplies no new ordinary-pass exchange
rate or native numerical allowance.

Because R>=1 and B<=L, these new row services cost O_w(L) at each ordinary
boundary. The inherited administrative toll is O_P(L) only when actual
S,C and occupied private work obey their stated current-volume bounds.
Arbitrary large occupied dirty input retains its real S/C/cleanup charge;
an initial allocation constant does not erase that time cost.

## 6. Fixed ports and historical allocation

The row graph uses exactly the existing productive fields, G, bridge and
child_header. Thus it adds no physical tape at descent. In a single
installation/collection with n=R/w, every productive field stays between
its current marker and offset nB; bridge stays through offset L; G and
child_header stay through offset B. These include the frontier reached by
the final move. Classification only visits the first B cells and frontier
of field0. Preparation only visits G and header. No callback visits an
earlier delimiter, an older control frame or another payload role.

The length of the child guide is B even when its row count is smaller.
Along a path of depth d, guide bodies occupy B(d+1), with their delimiters.
Since R=w^d and w>=2, d+1<=R, so this is at most the root field length
L_root. Productive lengths on a path sum to

    L_root*(1+1/w+...+1/w^d) <2L_root.

Popped siblings reuse the same current origins; blank historical tails are
retained and charged. A conservative rolewise envelope for visits caused by
these row tables and their installed segment layout, beyond arbitrary
retained entry backing K0, is

    K0+(2w+4)L_root+w(d+1)+4 <= K0+(3w+4)L_root+4.

It counts every productive role separately, all stacked format copies,
and the maximum outside bridge/header extents. Additional numerical visits,
including visits on productive fields themselves, must be added under their
own backing bounds. All other payloads, control frames and PC backing retain
the prior lifecycle/Stack obligations and charges.
Under their current-volume premises the new roles preserve the inherited
linear retained-backing conclusion. No maximum of row totals is substituted
for the sum of each physical role's historical maximum.

## 7. Executed evidence, limitations and next obligations

The frozen verifier checks 64 row-service domains,16 one-row classifiers,
4160 exhaustive guide/data pairs of physical lengths 3 and 6 against a
separately written complete-word specification, and 16 negative controls.
Seven runs use the actual unchanged Controller, Stack and #6968 SCALE(-1)
provider with complete complex pairs, widths w2/3/4, depths 0..3, translated
origins, warm blank history and dirty initial work. Their57 ordinary calls
check every original administrative term and the complete expanded bill.
Every actual pop restores all parent words before the issuing owner is
replaced. The complete endpoints agree with independent signed negation of
every original row. These finite examples corroborate the quantified proof;
they do not execute the selected astronomical compiler template.

The tests detect shorter/longer final fields, partial codewords, malformed
separators, all-zero physical pseudo-rows, changed same-length layouts,
nonzero/empty format guides, foreign symbols, incomplete productive batches,
aliased ports, a shape-correct field-order mutant, an omitted final-field
frontier check and omitted format installation cost. They do not certify
an arbitrary numerical child's semantic endpoint.

The weakest next step is a source-specific producer for the complete
production descriptor and its reached stopping/precision domain, or a
separately paid adapter for a changed row/rank geometry. Whole zero-row
padding must preserve010 separators and all complete spectators. Neither
fixed w nor R=w^d may be silently substituted for the selected variable-rank
and stock promises. Numerical kernels, full fixed-tape dispatcher admission,
compiler closure, the physical tariff conversion, analytic recovery and
the five selected assumptions remain outside this result. No new kappa.
