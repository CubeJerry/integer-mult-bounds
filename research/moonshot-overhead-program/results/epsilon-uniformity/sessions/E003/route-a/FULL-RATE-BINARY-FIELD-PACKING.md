# Full-rate binary packing for changing coefficient fields

Status: **proved fixed-tape encoding component; independently accepted by
Routes B and C**, reviews at `../route-b/REVIEW-PHYSICAL-SUPPLIERS.md`
and `../route-c/REVIEW-A-BINARY-FIELD-PACKING.md`.
This removes an otherwise artificial product of scalar-extension degrees
from the recursive bit-volume invoice. It is not a complete variable-
template interchange or multiplication theorem.

Sources: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, Fourier
`build/kernel.tex` scalar descent after the finite-saving inequality;
tape `build/uniformity.tex` common-tape serialization and
`build/interchange.tex` arbitrary input streams. Immediate programme
predecessors: S002 `routes/A/fixed-field-extraction-theorem.md` and E002
`route-c/polynomial-interchange-invoice.md`,
`route-c/succinct-cyclic-executor.md`, and `route-c/small-radix-batching.md`,
at `a2d9c4b00c02dadf7bdc970acf9190dfabf9ec32`.

## 1. The invariant is an arbitrary binary payload

An interchange call permutes address fields and returns their original
payloads exactly. It must work on **arbitrary** binary records of any
positive width b. Their contents may encode a parent's finite-field symbol,
a numerical record, several earlier basis coordinates, or unrelated bits.
The child is not permitted to assume that unused coordinates are zero.

The coefficient field used internally at one node may be
`E_m/F2`, of degree `d_m`. Its arithmetic and its chosen binary basis are
specified by a compact description of polynomial size in m. For the current
shift-check construction, `E_m=F_(4^r)` with `r=ceil(log_4 B_m)` and
`B_m=O(m)`, so `d_m=2r=O(log(m+2))`. The statements below allow any
`d_m<=poly(m)` whose exact field arithmetic is polynomial in m.

No embedding of the parent's field into E_m is needed. The parent payload
is treated as a vector of independent binary coordinates during the
permutation. Only the child's coefficient arithmetic uses E_m.

This field-change permission applies to a **completed spatial permutation**
call. A finite repair child whose target is the order-three transform F
or F inverse is not such a call; it retains its parent's coefficient
field and finite template throughout that local unrolling. FP3 does not
authorize reinterpreting those nonpermutation algebraic children.

## 2. Exact full-rate packing

**Lemma FP1.** Suppose a linear template over E has W arbitrary input
and output rows, each with the same full spatial address set Omega, and
its completed target is a permutation Pi of Omega on every row. Let
`d=[E:F2]` and fix an F2 basis of E. For every b>=1, the template induces
the same permutation Pi on `dW` arbitrary rows of b-bit records, with
no change in the total number of encoded input bits.

**Proof.** Write an input bit as `x_(i,c,omega,t)`, where i in [W],
c in [d], omega in Omega, and t in [b]. For each i,omega,t pack

    X_(i,omega,t)=sum_(c=0)^(d-1) x_(i,c,omega,t) e_c in E.

This is an F2-linear bijection from the d input bits to E. Run every
template scalar map coordinatewise in t, and every spatial permutation
with t as an untouched payload coordinate. Thus the calculation takes
place on the E-vector space `E^b` rather than on E alone. Every linear
identity remains valid after tensoring with the identity of that vector
space. At the output,

    Y_(i,omega,t)=X_(i,Pi^(-1)(omega),t).

Unpacking its basis coordinates gives the required permutation on every
original binary row. All dWb|Omega| input bits were independent, and all
remain occupied. No coordinate was supplied as initialized padding or
silently discarded. ∎

If the template makes sigma full-row permutation calls, each encoded call
contains `d b |Omega|` bits and the batch input contains
`W d b |Omega|` bits. Therefore the total child-volume/input-volume ratio
is exactly `sigma/W`, as before scalar descent. Merely multiplying the
symbol width by d while retaining dW *encoded E rows* would double-count
the extension and is not this construction.

## 3. Packing is a bounded-tape operation

**Lemma FP2.** The map between layouts

    [group] x [basis_d] x [spatial_Omega] x [payload_b]
    [group] x [spatial_Omega] x [payload_b] x [basis_d]

and its inverse can be implemented in `O(d V)` payload moves plus
`V poly(log(2d))` control work and fixed-degree descriptor setup, with
`C V+poly(d,log(2V))` cells ever visited. C is absolute, and V is the
identical encoded volume of the two layouts. There are a fixed number of
physical tapes.

**Proof.** For c=0,...,d-1, scan the original row-major data and extract
the c-th basis row from each group. It is ordered by group, spatial
address and payload coordinate. Merge it with the accumulated first c
basis bits at each such position, obtaining c+1 bits per position.
Each pass reads at most V original bits and at most V accumulated bits,
and writes at most V new accumulated bits. Retain the original input,
one extracted stream, the old accumulator and the new accumulator; reuse
their marked regions at every pass. No tape is assigned to an individual
basis coordinate.

For the inverse, process one group at a time. For each c scan its packed
stream and extract the c-th bit from every d-bit field block, appending
the result in original basis-row order. Reuse the same local work areas.
The total scan volume is again at most dV. Counters for c and field-block
position have O(log d) bits. Resets for full spatial/payload ranges are
paid by the ranges themselves, and long spectator counters are only
advanced, as in the source elementary streams. All d-index arithmetic
is polynomial in d or its descriptor and is charged, while all large
shape arithmetic is genuine one-time setup. This proves the stated
fixed-tape and visited-space bounds. ∎

Consequently a compact E_m scalar operation can process the b independent
E_m components successively. Its polynomial-in-m field arithmetic is paid
per encoded d_m-bit element; there is no extra per-bit factor depending
on the parent's record width b. Temporary field registers use poly(m)
bits and are reused. Under the large-field guard of
`GUARDED-CONSTANT-SPACE-STREAMS.md`, this additive space fits an absolute
multiple of the local volume.

## 4. How to obtain the dW independent rows

For exact batches the complete binary row width is

    W_bin=d_m W_E.                                      (FP1)

It may be non-power-of-two. Write q>=2 for the **address radix**, keeping
b for the unrelated payload-record width. Use the predecessor multidigit
leading block with `ell=ceil(log_q W_bin)` and an occupied leading range
of size q^ell. Pad that range to the next multiple of W_bin. Because q^ell>=W_bin,
the resulting row inflation is strictly less than two. This is the
already charged leading-row factor in the source spatial invoice, not
a new factor d_m. Packing and unpacking preserve the padded bit volume
exactly, and padding removal uses known positions, not bit values.

Alternatively any caller supplying a leading row count divisible by W_bin
needs no row padding. The proof does not presume this divisibility without
checking it. Since `log W_E<=poly(m)` and `d_m<=poly(m)`, the new
`log W_bin=log W_E+log d_m` still has polynomial size and the same kind
of polynomial leading-width guard.

Every label in the full batch owns exactly the same d_m basis coordinates.
Grouping field-permutation calls within one label therefore retains the
same label-volume fraction. With the predecessor leading padding, that
fraction is at most `2/N`, independent of d_m. Finite repair phases also
retain their original volume fractions: multiplying each row width by d_m
and reducing the number of binary rows by d_m affects numerator and
denominator equally. The known V/16 characteristic-two repair fraction
and the source descriptor-only full-volume reserve descents remain the
actual ratios if their grouping is otherwise unchanged.

## 5. Nested calls with different fields

**Theorem FP3.** Suppose a rooted family of permutation calls uses at
each node a finite characteristic-two coefficient field with FP1--FP2,
exact full-rate row grouping (or explicitly charged leading padding), and
the same arbitrary binary-record interface. Along an arbitrary descent,
changing the coefficient field creates no multiplicative scalar-extension
factor in child bit volumes. Local field preparation and arithmetic retain
their stated parameter-dependent time costs; local payload space has an
absolute constant multiplier.

**Proof.** At one parent node its current record may have b arbitrary
bits. A child receives exactly these bits, with their recorded boundaries.
The child groups d_child independent rows and regards the b payload-bit
coordinates as spectators. FP1 is valid for every b and FP2 rearranges
exactly the existing bits. Its calls may therefore carry wider records,
but their row counts and total volumes change inversely. The target is a
permutation of address fields with the identity on every payload bit,
so the child returns the parent's original b-bit records in the required
order. Induction proves this interface at every depth. There is no need
to identify, embed or extend the parent's coefficient field at all.

FP2 and the scalar processors retain a fixed number of volume-sized arrays;
their parameter descriptions are separate additive objects. The product
of extension degrees can appear in a record-width descriptor, but never
as a factor multiplying the actual bit volume. Sequential field operations
are charged to every encoded bit once for each polynomial-m local action.
This proves the stated local and child-volume claims. ∎

The theorem alone does not establish a global O(n) visited-space bound.
That also requires uniformly contracting parked payloads, descriptor
accounting, and reuse of sibling regions. The source ratios just noted
supply the payload contraction where the exact layouts are preserved.
Arithmetic-field descriptions must be constructed or retained inside the
stated additive budget. A dense lookup table whose size grows with the
field is not free.

If the opaque records encode approximate numerical values, the intermediate
field-mixed bit words need not encode useful numerical approximations.
The child performs exact bit arithmetic and returns the exact permutation
of the represented input records; it introduces no rounding fault. The
numerical error analysis therefore uses the completed permutation as an
isometry, exactly as in the source physical compiler. It must not assign
a complex-linear operator norm to the child's intermediate bit mixtures.

## 6. Scope and next obligations

This is the full-rate vector-space descent from the source, with its
physical bit packing made explicit for a changing coefficient field.
It is stronger than embedding each input bit as a scalar with d-1 zeros,
which would inflate volume. It does not assert improved algebraic call
counts or a new tensor identity.

Remaining obligations are the changing-radix/shape construction, exact
call invoices for every variable node, whole-stack descriptor bounds,
numerical precision and assembly into one exact full-product machine.
Finite tests can check packing and permutation commutation, but the
universal statement is the vector-space and fixed-stream proof above.

Credits: @CubeJerry; pinned OpenAI scalar descent and tape serialization;
S002/E002 full-rate formulas and multidigit batching; substantial
AI-assisted E003 proof and cost audit. No full multiplier execution,
formal verification or independent human review is claimed.
