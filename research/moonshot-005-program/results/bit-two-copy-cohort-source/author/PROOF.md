# Two paid physical copies realize the packed cohort source with scalar ADDs

**Literal two-copy partial source; independent review pending. No new κ.**
This representation removes the unadmitted lane instruction by expanding
every bank into a separate full physical record. The actual word uses only
INIT, ADD, MOVE and CLEAR. It acquires19 dimensions of the30-dimensional
two-copy W code, preserves all W30 in actual history, restores all original
X records, and completes the two native Y0 outputs. All doubled records,
movements, native jobs and caller costs must remain explicit.

## 1. Full records, not free subarrays

For every two-lane record A in the frozen conditional circuit, introduce two
distinct physical records A_b0 and A_b1. Each is a complete ordinary field
with arbitrary input and the same positive column multiplicity as every
other record. The two fields are independent productive/borrowed inputs when
A is an original input, and two distinct zero-born owners when A was owned.
They are not half-width physical carriers priced as one wide record.

In particular there are222 original X records and222 original Y records,
with444 independent symbolic input columns. Native source lines and target
facets repeat with the two copy labels. The geometry does not identify the
values of these copies. All cocharted scalar ADDs may mix the two copies
because they are ordinary distinct complete roles in the same chart.

## 2. Exact expansion theorem

Translate each conditional instruction by

| Conditional instruction | Fully paid scalar sequence |
|---|---|
| INIT A at C | INIT A_b0 at C; INIT A_b1 at C |
| ADD A into B | ADD A_b0 into B_b0; ADD A_b1 into B_b1 |
| ADD_LANE A[a] into B[b] | ADD A_ba into B_bb |
| MOVE A to C | MOVE A_b0 to C; MOVE A_b1 to C |
| CLEAR A | CLEAR A_b0; CLEAR A_b1 |

**Lemma.** After every translated instruction bundle, the two scalar record
values and charts equal the corresponding two conditional coordinates and
chart. All source restoration and target identities are preserved.

**Proof.** Identify the two coordinate slots of each conditional record with
the two complete scalar roles. Each table row is then the same linear map
on all original input columns. INIT and CLEAR also have the same liveness
change under that identification, with both physical events explicitly paid.
For ADD_LANE within one conditional record, a!=b, so its expansion is still
an ADD between distinct physical records. A conditional MOVE is replaced by
two separate legal comparable MOVEs; no other instruction is interleaved
between them. At the next bundle boundary all required co-locations hold.
Induction proves the claim for the entire finite word.

The emitted verifier checks the complete translation at every recorded
bundle boundary, then independently executes the scalar word on all444 input
columns with exact rational chart containment. It does not admit the earlier
conditional instruction as a new primitive. This expansion works for every
positive full-record column multiplicity by the ordinary scalar-word lift;
there is no parity restriction on each physical record's width.

The earlier constant-record invariant remains true. It forbade packing the
prescribed forms into two wide physical records using a restricted local
grammar. The expanded construction instead uses four physical records for
that two-lane/two-run cohort. Its record count and transport bill changed.
No contradiction, uncharged masking operation or free fractional array is
being used.

## 3. Actual source and code acquisition

The original conditional source is the fixed two-coordinate realization of
the optimal cohort-capacity construction. All its formation and inverse
CNOTs now become ordinary scalar ADDs between complete roles. Cohort carriers
are still restored at Hub before any packet seed. Every actual cache deposit,
packet read, original-y capture, feedback and correction appears in the
expanded word with its own physical owners and chronology.

There are160 scalar raw caches. Their actual row space has dimension80 and
intersection dimension19 with the two-copy W30 code. The remaining11 W
directions are actual terminal fields. Consequently all222 displayed W rows
lie in literal packet history; their span is dimension30. The checker gives
an explicit history witness for each W row and each of the160 raw caches.

The history has rank93, original-y projection rank2 and pure-X dimension91.
The terminal space has rank13 and W intersection11. The fields P6_b1,
P7_b0 and P7_b1 are actually zero. They remain paid packet lifetimes, not
free information coordinates. There are16 actual descending packet paths.
The two completed outputs are Y0_b0 and Y0_b1; all other original Y values
remain unchanged, with their final ascents included in the closed invoice.
Every one of the222 original X records restores to its own independent input
at Hub.

These are exact binary identities and rank certificates. They hold over
all characteristic-two extensions and lift to arbitrary whole-record widths.
The acquisition average is9.5 W dimensions per original copy. This gain comes
from joint coding between two independently paid native copies, not from
relabeling the scalar one-copy optimum9 as9.5.

## 4. Complete physical counts and the caller boundary

The actual closed word has

    400 INIT, 2126 ADD, 990 MOVE, 400 CLEAR.

There are397 dirty retirements and three zero packet fields. All400 owners
are distinct zero-born records:222 point caches,160 raw caches,16 packets
and two original-y masks. The source and its inverse are both counted.
The778 formerly conditional lane calls each become one ordinary ADD; the674
full conditional ADDs become1348 ordinary ADDs. Thus2126 is an actual scalar
instruction count, not an assumed lane-service tariff.

The full movement profile is

    366[1]+24[2]+238[3]+142[4]+220[7],

with rank-length3236. Every count is exactly twice the one-wide-record profile
because there are two independently paid physical MOVEs. Its moment is
`Q^(2)=2Q` at every exponent. No concavity discount `[2r]` replaces two actual
rank-r calls.

A whole-system use must also count both copies of the native bodies,
productive target jobs, decoder duties, interface overheads and caller terms.
If every term of the retained caller is duplicated, its movement test scales
homogeneously by two and the normalized per-copy comparison is unchanged.
This package proves the actual doubled source invoice; it does not infer a
complete caller or supplier from source-only scaling. In particular no new
κ follows from changing the denominator to two outputs while keeping only
one output's costs. Root's separate bank-expansion/caller analysis records
that interface explicitly.

All ordinary, owner, precision, cover, recursive and completed-decoder costs
remain owed. The usual retained primitive/compiler assumptions and all five
foundations remain. The source has no new masking instruction, but a complete
native unit and the compatible complex supplier are still open.

## 5. Reproduction and verification

```sh
python3 -B expand.py --source /path/to/conditional-packed/output \
  --out /path/to/two-copy-packed/output
python3 -B check.py --repo /path/to/programme \
  --word /path/to/two-copy-packed/output/CLOSED-WORD.json \
  --conditional /path/to/conditional-packed/output/CLOSED-WORD.json \
  --out /path/to/two-copy-packed/verification
```

Expected status: `PASS_TWO_COPY_SCALAR_SOURCE`.
The author verifier checks exact translation boundaries, every scalar opcode,
actual co-location, every physical direction,444 independent input columns,
all source and target endpoints, all owned handoff values, W/cache witnesses
and full costs. Six mutants reject: omitted cross-copy formation, omitted Hub
inverse, omitted second-copy MOVE, omitted second-copy feedback, omitted
second-copy retirement and a one-copy accounting claim. Independent review
is pending; these are author checks rather than a new independent audit.

The live word is an exact prefix of the closed word. Source, circuit, proof,
checker and evidence hashes appear in MANIFEST.json. Credit @CubeJerry,
source/cohort predecessors, Worker C's explicit block circuit, and root's
paid-bank representation repair and caller analysis. OpenAI assistance is
disclosed. This is one continuing construction with a more faithful physical
representation, not an unrelated branch or a claimed multiplication theorem.
