# E002 independent review of E003 packing and pencil scheduling

Status: **accepted for the stated components and local interfaces**. This
is a review of concurrent E003 work, not E002 provenance for those results
and not automatic admission of E003's whole multiplier.

Reviewed E003 files at programme checkpoint df91e4c8:

* `route-a/FULL-RATE-BINARY-FIELD-PACKING.md`, SHA256
  `a2ee7273eb75e258e5e63bb7f85db998a185173c2012239c905a367fdee8da09`;
* `route-a/SHARED-PENCIL-CONSTANT-SPACE.md`, SHA256
  `4ba63e969bdd95b276d6e25909978516420bcb7d0ff678f3d8ed500f6e4a108a`.

I read both notes in full, including the final revised call allowance.
Their source is the pinned OpenAI arbitrary-stream scalar descent and
shared rectangle/low-rank implementation, already read during E002.

## 1. Full-rate packing

FP1 is an F2-linear bijection: d independent binary rows become the d
basis coordinates of one E row. An arbitrary b-bit payload means the
calculation takes place over E^b, so tensoring the template with its
identity is legitimate. The final permutation acts on spatial coordinates
and is identity on every basis/payload coordinate. It therefore returns
all dW independent bit rows, without initialized extension coordinates.
Both the input volume and each child volume include d in the same way;
the normalized sigma/W invoice is unchanged.

FP2's serial extraction/merge layout is realizable on fixed tapes. Each
basis pass scans at most a constant number of V-sized streams; original,
extracted, old accumulator and new accumulator need only fixed reusable
regions. The inverse's group-by-group repeated scans preserve the specified
basis-row order. Its O(dV) work is polynomial m for the supplied degree;
its payload space has an absolute multiplier. It does not allocate d tapes.

FP3 is valid for the *spatial permutation* children named in its statement.
A child's opaque binary payload may encode a parent's field record, but
need not embed that field into its own. Packing changes row count and
record width inversely, preserving actual bit volume. The degree product
may occur in a record-width descriptor but not as a hidden volume factor.
Finite predictor/converter operations that are not themselves permutations
continue to use their local template's coefficient algebra; FP3 is not a
license to reinterpret an unfinished non-permutation operation.

The dW leading batch width is explicitly charged. Temporary final-batch
padding is below two, log(dW) remains polynomial m, and grouping by label
keeps the same label fraction. Separate variable-radix, stack and numerical
interfaces are still required, exactly as the note states.

## 2. Two-pass shared-pencil arrays

The rank guard makes the key storage equality exact:
all m rank-coordinate collections have total size (m r*/N)V<=V.
Keep these collections through the first rectangle pass. Each rectangle
is processed through all queries before its source preparation is released.
Its query sum is consumed into both direct cancellation and the appropriate
basis-row vectors. Thus no endpoint is reconstructed m times and no
m-by-rectangle family of full arrays is kept.

The middle rank matrix acts on label coordinates while A_j acts on the
internal rows; they commute. The second destination pass adds its low-rank
contribution after returning it to ordinary physical coordinates. This is
valid because both contributions are linear and at precisely the same
ordinary output address. They need not have remained together in one
prepared endpoint array. Only the destination return is duplicated; the
source and rank-conversion invoices are unchanged. A factor four in the
complete endpoint bound is a safe conservative charge.

The listed live arrays have an absolute total payload multiplier: original,
final output, all rank inputs/outputs, one rectangle's source/destination
subsets and a fixed number of sum/term buffers. Reusing them across queries
and rectangles removes the lambda space multiplier while retaining lambda
in the time/call invoice. This is the actual two-pass source-specific
schedule, not a claim that arbitrary streamed circuits have constant space.

This review accepts that schedule with its supplied legal affine/scalar
processors and descriptor contracts. Its unconditional header-free scaling
and comparison supplier are separate files, not automatically certified by
this note. Under E002's long-fibre guards our own HS/HA implementation
supplies the required constant-volume affine subroutine. Any S003 dyadic
geometry substitution must retain its added absolute call factor; the
reviewed E003 note explicitly does so rather than reuse the old constant.

## 3. Isolated packing replay and scope

I inspected and copied the supplied packing checker into
`replay-e003-packing/` and ran it in isolation. It passed 420 single-field
shapes, 3,500 scalar round trips, 756 nested-field shapes and 24,576 leading
batch cases. It tracked 37,800 single-stage and 136,080 nested payload bits.
Its basis-order, zero-embedding-volume and lost-independent-coordinate
negative controls all fired. These are exact finite structural checks,
not a tape-transition execution or an asymptotic proof.

The fixed-field bit-packing idea independently suggested inside E002 uses
the same full-rate vector-space principle; the written general changing-field
component above is attributed to E003. A separate E002 root proposal to
pack a low address block into coefficients and swap its leftover bits is
reviewed as a wrapper in `LOW-BIT-COEFFICIENT-PACKING.md`. It is not a
replacement for E003 provenance or an automatic strengthening of V.

Credits: E003 component authors, Jerry Chen (@CubeJerry), the pinned OpenAI
source, S002/E002 predecessors and AI-assisted independent review.
