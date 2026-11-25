# An absolute-space schedule for the actual shared swap pencil

Status: **proved source-specific local schedule; independently accepted by
Route B** in `../route-b/REVIEW-PHYSICAL-SUPPLIERS.md`.
The schedule retains the source shared-endpoint call bound up to an absolute
factor while replacing a template-dependent number of full-volume tracks
by a fixed collection of arrays. Its decisive observation is the actual
rank guard `m r*/N<=1`: one can retain low-rank intermediates for *all*
queries simultaneously because their total volume is at most one batch.

Sources: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, tape
`build/interchange.tex`, paragraphs “Delivery by rectangles” and “Delivery
at low rank”; the E002 characteristic-two replacement at programme
`a2d9c4b00c02dadf7bdc970acf9190dfabf9ec32`, notably
`route-c/polynomial-interchange-invoice.md`. Scalar execution and comparison
selection use the explicit E002 processors refined in this directory.

## 1. Objects and physical invoice

There are N labels, R independent internal rows at each label, and m
queries. Every row has the same complete spatial volume and opaque
binary-payload width. Let V be the encoded bit volume of the whole batch.
The data-field label matrix has rank r*, with

    I = P* - sum_(L,K) 1_K 1_L^T,
    P* = P*_:J (P*_IJ)^(-1) P*_I:,
    m r*/N <= 1.                                      (PS1)

The off-diagonal rectangles are disjoint as matrix-entry supports, and
each label belongs to at most lambda rectangles on either side. The
source coordinate-change dimension is D. A query pencil has row maps

    A_0 + sum_(j=1)^m A_j Q_j.

The A_j act on the R internal rows; they are implemented by the compact
cyclic-mask structure, not a dense R-by-R lookup. All source maps and
inverse destination maps keep the source's prescribed ordinary/common
address correspondence. Label counts, coordinate dimensions, scalar
field degree, and finite control descriptions are polynomial in m.

The source normalized recursive-call bill is bounded by

    C D(1+lambda)(1+m r*/N)                            (PS2)

per independent input row. The current E002 concrete envelope takes
`C=32` before using (PS1), or its stated `64 D(1+lambda)` final bound.

## 2. The storage observation

For each j, retain a rank-coordinate accumulator U_j consisting of r*
internal-row streams in one fixed common physical layout **for that
query**, recorded in its descriptor. Different queries need not use the
same layout and are never added without their paid destination maps. Its volume is
`(r*/N)V`. Therefore all m such accumulators together have volume

    sum_j volume(U_j) = (m r*/N)V <= V.                (PS3)

Each U_j initially contains the singleton contributions from P*_I:.
Processing a rectangle adds its common sum to the appropriate basis-row
accumulators, using the exact support decomposition in the source. The
necessary layout conversions remain paid. No m copies of the full input
are kept, and no scalar-extension degree has been omitted: all volumes
already count encoded bits as in FP1--FP3.

## 3. First pass: direct rectangles and all low-rank source sums

Retain the original input batch and one final-output accumulator. Initialize
the U_j singleton contributions using the source's paid common-coordinate
conversions on the r* basis rows, for every j.

Process each off-diagonal rectangle (L,K) successively:

1. Copy its source subset, of volume at most V, and prepare its shared
   reserved-field endpoints once. Keep this transformed collection until
   every query j for this rectangle is complete.
2. Allocate a zero destination accumulator on its K-label subset in the
   prepared endpoint coordinates. This is at most V bits. It need not be
   obtained by transforming a nonzero copy of the global output.
3. For each j, the source's lower-triangular maps form the common sum
   X_(L,j). A single R-row common stream, of volume V/N, suffices for
   that sum and a work copy. Preserve the unmodified sum; apply A_j only
   to the work copy and deliver the direct negative
   rectangle contribution into the K accumulator via the source inverse
   lower-triangular maps.
4. Also convert the **raw, pre-A_j** X_(L,j) into the fixed common layout
   for query j and every basis row
   i in I intersect K to which it contributes. Add it to U_j. This is
   exactly the source low-rank source invoice, bounded by
   `O(m R r* D(1+lambda))` calls. It is not recomputed after the
   rectangle's transformed source collection is discarded.
5. After all j, undo the destination endpoint once, add the ordinary-layout
   result to the global output accumulator, and release this rectangle's
   source/destination work areas.

The source endpoint is therefore prepared once per rectangle incidence,
not once per query. The source rank-conversion count is unchanged. All
rectangle data are released before the next rectangle begins.

## 4. Central rank action and second destination pass

After the first pass, every U_j contains precisely `(P*)_I:` applied to
the original input at the correct common address. Apply
`((P*)_IJ)^(-1)` on the rank label coordinate and A_j on the internal
row coordinate. These two maps commute because they act on different
indices. Their input-plus-output accumulators for all j occupy at most
2V by (PS3); process scalar coefficients and individual j sequentially.

Deliver the resulting rank-coordinate vectors through `(P*)_:J`, using
the source destination support decomposition. Singletons use their paid
common-to-ordinary layout conversions. Process destination rectangles one
at a time. For each rectangle start a fresh zero accumulator in its
prepared destination endpoint coordinates, add every j contribution by
the paid common-layout conversion and inverse triangular operations,
then undo the endpoint and add the ordinary result to the global output.

This second pass is permitted because direct and low-rank terms add
linearly in the **same ordinary output coordinates**. It does not require
retaining direct rectangle output in every endpoint layout. It repeats
the destination endpoint return at most once relative to the paper's
combined schedule. It never repeats an endpoint m times. A factor four
in the complete source endpoint/call bound is a safe overestimate of all
such duplicated endpoint work; rank-coordinate conversions are already
charged in their original source/destination counts.

Finally add the A_0 term in ordinary layout and return the output.
Every cancellation is at the same physical address z, as required by the
source equation. The schedule changes ordering and stores intermediate
linear sums; it does not change any algebraic identity.

## 5. Actual resources and complete local statement

**Theorem PS.** Under the stated source geometry, compact scalar executor,
rank guard and legal ordered-affine processors, the shared pencil has:

* normalized recursive-call bill at most four times (PS2);
* `V poly(m)` nonrecursive actual bit work, plus the separately stated
  finite plan/descriptor setup;
* an absolute constant times V payload-and-key visited space, plus
  polynomial compact descriptions and registers.

For the space claim, the simultaneous collections can be bounded by the
original input V, global output V, all U_j and their central outputs 2V,
one transformed source subset V, one destination subset V, and a fixed
number of common/term streams of size at most V. A fixed upper allowance
of twelve complete V-sized payload regions covers these named arrays;
each primitive may require its own fixed number of scratch copies, so
enlarging twelve to one absolute implementation constant covers them too.
The same regions are cleared or overwritten for successive rectangles,
queries and scalar terms. No factor N, R, m or lambda multiplies space.

The coefficient/rank dimensions are polynomial in m, and each compact row
map has polynomial-m per-volume work. Serial label/rank/rectangle scans
therefore preserve polynomial-m local time. Their recursive coordinate
changes retain the source paid call counts; dense ordinary arithmetic may
be overcounted, but spatial recursive calls may not. HFS supplies an
unconditional absolute-space affine scaler; alternatively G1--G4 give
the same result under their explicit source field guard. CL supplies all
comparison labels with one current control tuple instead of m mask tracks.

## 6. Consequence for finite repair and spatial stacks

Apply PS successively to the predictor stages. Their number multiplies
the local time and call invoice, not payload storage. The characteristic-
two finite repair has four sequential child phases of volume V/16. Its
parked payloads therefore have a geometric bound independent of m.
The final product word also runs sequentially in the same work areas.

The concrete E002 complete spatial call bound

    Lambda_m <= 2^17 sqrt(m) D_I(1+lambda)

may conservatively be replaced by

    Lambda_m <= 2^19 sqrt(m) D_I(1+lambda).            (PS4)

The additional factor is absolute and does not change its logarithmic
parameter-growth scale. A fixed-exponent admission margin must be
rechecked with this actual coefficient; it cannot retain an old exact
constant silently. For a nonstationary recurrence, PS4 is the charged
coefficient to use **with the preceding E002 geometry**. If the newly
reviewed S003 explicit dyadic geometry is substituted, its doubled ambient
dimension and elementary-factor count must be included too: use a fresh
absolute `C_geom sqrt(m) D(1+lambda)` until that numerical constant is
recounted. The rate proof requires only an absolute C_geom, but a concrete
admission certificate requires its actual value.

A grouped main spatial child within one label has at most 2V/N<=2V/3
after the existing leading padding. Park other payload arrays and reuse
their intervals after return. A full-volume reserve child is launched
only after main payloads have been merged and cleared, so it parks only
descriptors. These are the source's actual stack rules. With FP3's
volume-preserving field changes, their geometric payload proof remains
uniform across parameter choices. Additive descriptor/generator space
still needs its own whole-stack bound.

This result does not establish a complete variable-template algorithm:
radix compatibility, all active-width/row guards, constructor cost,
numerical precision, and final multiplication assembly remain separate.
It establishes the previously missing actual absolute-array schedule for
the source pencil, with its extra endpoint expense explicitly paid.

Open next question: independent adversarial review of the two rectangle
passes and of storing all m rank-coordinate arrays via (PS3). A naive
schedule retaining every transformed rectangle is not an alternative proof.

Credits: @CubeJerry; pinned OpenAI rectangle/low-rank identities and endpoint
sharing; E002 compact processors and rank guard; substantial AI-assisted
E003 scheduling proof. No new algebraic label construction, global lower
bound, formal build or human review is claimed.
