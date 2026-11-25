# Independent review of the fixed-array rational Walsh executor

Disposition: **pass as the stated source-specific physical component**.
The reviewed schedule supplies P-W of the two-scale transfer when its
interchange supplier and exact leading-row divisibility are supplied.
This is an independent review of A's executor, not an independent review
of Route B's own global recurrence.

## Material actually read

Reviewed E003 A `RATIONAL-WALSH-CONSTANT-SPACE.md`, SHA-256
`11cfd491f2f1153ab9a534e8625308f45577093b31a25a6ae641bd74a3b8e9b2`.
Read the complete file, rather than inferring its statement from a status
message. Re-read E002 `polynomial-walsh-precision.md`, SHA-256
`7dbc8926b2e68840e54f1ce981b5a827f53ab3f29dbe0ea7420ba25093a0ce19`,
including exact rational scaling, on-demand spectral repair, local norm
gain and the explicit numerical threshold.

OpenAI source commit is
`3344da59991ed94f9ba711217b29c1d760badfa6`. The relevant Fourier files are
under `preprints/The-logarithmic-exponent-of-finite-Fourier-transforms-November-24-2026/build/`:

| File | SHA-256 |
| --- | --- |
| `kernel.tex` | `f960a1c403134df527daafcb9b9e312057750cda922ce930b04e251e1382e361` |
| `binary.tex` | `5979011cb813600f02b695af5cb320fe926f6e4ccbfaeb05073c9789e63f5fd7` |

Read the kernel's rectangle, endpoint, finite-saving and uniformity
arguments, and the whole binary normalization proof. Also read the full
tape `permutations.tex`, `walsh.tex` and `integers.tex`; their hashes and
the separately checked outer transfer are in `OUTER-REDUCTION-TRANSFER.md`.
The predecessor finite algebra/label identities remain attributed imports.

## 1. The dense role schedule does not retain one array per role

For a small p-by-q rational row map, A keeps the original sources, one
destination accumulator, and a fixed number of selected-term/merge
regions. Processing pairs `(i,j)` serially may rescan the whole array
polynomially many times, but p and q have fixed polynomial bounds in m.
Hence time remains `V poly(m)` while array storage is an absolute
multiple of source-plus-destination volume.

In every cited use, that volume is bounded by a constant multiple of the
parent volume: square predictor/pencil maps preserve the row count;
check and lift maps have their stated smaller ports. Initializing an
accumulator is workspace, not a new arbitrary independent input.
The row role is a counter on a fixed tape, not a new tape or permanent
payload track. Rational coefficient scratch is reused record by record.

The supplied defect set depends on address-spectrum bits, not on the
numerical values. Thus the selected operation is still a linear map on
the represented numerical vector. E002 W2 calculates the actual defect
set and tests nonzero gaps before inversion. Its polynomial matrix is
computed from the spectral key at the spectral boundary; the schedule
does not commute it through a Fourier conversion.

## 2. The free endpoints really remain shared

The source kernel gives `H subset d_v^perp` at every source endpoint,
and `H^perp subset d_w^perp` at every destination. Consequently the
first transform, including its auxiliary phase, is independent of the
query j. The j-dependent distinguished phase is constant on each coset
and belongs in the middle monomial operation. A prepares the first
transform once and retains that source subset.

At the destination, all middle-query contributions are expressed in
one prepared destination layout before summation. The pencil row
matrix acts on the independent row coordinate and has coefficients
independent of the spatial address. It therefore commutes with the
final partial Fourier transform, which acts on address coordinates.
This is the actual tensor-factor commutation used by the source; it
does not extend to an arbitrary spectral mask. The schedule sums over
j first and executes the last endpoint once.

The kept source and destination sets are each subsets of the labels,
so each occupies at most one parent volume. The query copy and common
sum add a fixed number of such regions. Charged rectangles use one
common sum and the source-billed kernel calls. Sequential rectangles
reuse all scratch. No incidence-by-incidence array family is retained,
and no endpoint is silently repeated for every query. The original
sum-of-child-volumes invoice is preserved.

## 3. Tape work is priced separately from Fourier calls

An A-bit column map has a binary elimination list of polynomial-m
length. Every slot addition is implemented by the source packed-XOR
routine with complete source, target and auxiliary ranges. All slots
not currently selected remain full spectators. A permutation of the
slots may first put the required controls in the permitted order; its
interchanges are part of the paid coordinate-change list.

The guard length `G=C_0 ceil(log2(2k))` can have a fixed C_0 because
every offset, control and exceptional destination calculation has a
fixed polynomial degree in m and k, and the numerical guard ensures
`m<=k`. Sparse exceptional tags use O(k) bits on records of width
Theta(k). A fixed number of tagged streams therefore costs a constant
factor in space. Their keys are stripped before numerical children.
Narrow slots use O(log k) direct moves, not an uncharged general sort.

E002's exact rational scaling primitive charges h shifted-add passes
and long division for a coefficient of height h. Under the explicit
`k>=m^K_1` guard this is polynomial-m time per numerical bit and O(k)
word scratch. In particular an arbitrary k-bit coefficient is not
assigned unit cost. These facts justify RW3, with interchange time and
space charged as their own suppliers.

## 4. Both kinds of recursion shrink parked payloads

For the finite two-port repair tree at
`h=ceil(log2(m)/4)`, the exact count satisfies
`2^(h+1)-1 < 4m^(1/4)`. Its two sequential child phases each occupy
one eighth of the parent volume. Thus the finite unrolling has
polynomially many actual local occurrences, not merely polynomially
many symbolic operation types, and an absolute geometric bound on
parked payload.

The completed numerical spatial template has polynomial row count
`W_m>=2`; one original work-row child has volume `V/W_m`. The parent
and its parked data can therefore remain while the child runs. Mixing
these two kinds of descents still contracts at every actual recursive
edge. A fixed local array count times their geometric series bounds
visited payload regions. Setup and descriptors are additive and remain
separately charged. Sequential siblings overwrite the same intervals.

The finite repair descendants retain their own m and rational template.
Only a completed numerical spatial child may select a fresh smaller
width/arity. This distinction is necessary for both algebraic validity
and the recursion count.

## 5. Precision and normalization are compatible

The source binary proof supplies the normalization from the `2D`
one-axis calls of a common kernel. The two free partial transforms
together use those same axes. In a complete spectral conversion the
normalization commutes through its row matrix and cancels with its
inverse. Hence the nonchild coefficient list has no unaccounted
f-dependent powers of two.

There are polynomially many local numerical array operations. Each
small rational block has polynomial dimension and coefficient bit
height; its operator norm has polynomial-m logarithm. The same bound
applies to physical partial sums and copies. Multiplying these finite
bounds gives a polynomial-m logarithm for every input-to-intermediate
and intermediate-error-to-later **numerical** map, not merely the
completed target. A spectral-key selection is block diagonal over
addresses, so its norm is a maximum over blocks, not the number of
keys times that maximum.

Exact interchange calls are counted as completed record permutations.
Their internal bit encodings are not floating-point linear maps and
create no rounding events; they return the identical records in the
new order. They need no intermediate numerical norm interpretation.
All numerical operations occur at the specified record boundaries.

For the E003 variable arities, the explicit guard
`k>=m_max^K_2` can dominate all local record and gain exponents.
Polynomially many array events and the two-ancestor-path gain argument
then justify one fixed O(k) format. A failed numerical guard selects
the exact fallback. A time or space cap alone would not justify
rounding accuracy.

## Conclusion and limits

The reviewed schedule supplies the P-W local time, full-rate child
volume, absolute array count, actual node-count and numerical-gain
interfaces, conditional on the already specified exact interchange
supplier and leading-row divisibility. No additional polynomial-m
proportional-space term is forced by the listed scalar, rectangle or
finite-repair operations.

This disposition leaves the local finite identities as attributed
imports, and the two-scale recurrence/common-space wrapper as separately
reviewed arguments. It does not independently establish a new programme
best exponent; remote E002 had already admitted the same two-thirds
scale during this session. No full physical multiplier was executed,
and no formal-kernel or human review is claimed.

Credits: @CubeJerry; OpenAI source authors and their cited predecessors;
E002 rational scalar/precision suppliers; E003 A's fixed-array schedule;
substantial ChatGPT multi-agent assistance.
