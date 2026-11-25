# A fixed-array tape schedule for the rational Walsh template

Status: **proved source-specific physical component; independent review
pending**. This strengthens the predecessor's polynomial-in-m proportional
space claim. It retains polynomial-in-m local time and the original
shared-endpoint recursive invoice, while using an absolute number of
numerical payload arrays. The whole multiplier and the two-scale analytic
transfer remain separate statements.

Sources are OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, Fourier
`build/kernel.tex`, subsections “The endpoint Fourier transforms” and
“The finite saving and recursion”, Fourier `build/binary.tex`, and tape
`build/walsh.tex` and `build/permutations.tex`. Programme predecessors at
`a2d9c4b00c02dadf7bdc970acf9190dfabf9ec32` are
`routes/B/pairwise-newton-division.md`,
`routes/B/polynomial-auxiliary-cost-audit.md`, and E002
`route-b/polynomial-walsh-precision.md`. Their finite algebra and the
normalization identity are imported. The scheduling and uniform storage
strengthening below are explicit.

## 1. Quantified interface

Fix one sufficiently large admissible odd integer m and its rational
template. Its arity A, base/completed independent row counts, number of
labels, rectangle and coordinate descriptions, coefficient heights, and
finite unrolling length have the fixed polynomial bounds of the cited
operation audit. In particular `2m<=A<=4m`, the completed row count
`W_m<=m^K`, and every scalar coefficient needed outside child calls has
rational numerator/denominator bit length at most `m^K`, for one absolute
integer K after enlargement. The normalized child-volume coefficient is
the exact finite-template coefficient `sigma_m/W_m`.

Let the outer address parameter be k. Every numerical record has width
R with `c k<=R<=C k`, for fixed positive c,C, and every selected spatial
field has its complete range. Arbitrary complete spectator coordinates
are preserved. Let V denote the encoded numerical bit volume of a local
batch, including its original independent rows and all spectators. V
does not include temporary destination headers, which are removed before
every numerical child.

The setup and record guards are

```
k >= m^K1,    R >= c k,                                (RW1)
```

for one sufficiently large absolute K1. These guards hold eventually for
the E003 choice `m=2^(Theta(Phi(log a)))`, since `a<=k` and this m is
`k^o(1)`. The bounded exceptional range can use the fixed direct branch.
The statement below does not assume a polynomial number of data records.
It bounds work per encoded volume, with setup separately charged.

## 2. Dense small row maps without one payload track per role

Consider p source roles and q destination roles, `p,q<=m^K`, aligned at
each spatial/spectator address. A coefficient `c_(i,j)(z)` may depend on
the address z, but must be computable from its prescribed spectral or
ordinary address bits in polynomial-m work plus the paid O(k)-bit scan.
It must have polynomial-m rational bit height. The required map is

```
Y_i(z) = sum_j c_(i,j)(z) X_j(z).                       (RW2)
```

Keep the unchanged source array and a zero destination accumulator.
Process ordered pairs `(i,j)` successively. A role scan extracts the
selected source role; its records are still ordered by the complete
common address z. For each record, generate the required coefficient,
apply the exact rational short-coefficient scaling of E002 W1, and
round to the common fixed-point grid. Merge this term into destination
role i in the accumulator. Reuse the same extracted-term and merge
regions at the next ordered pair. Even rescanning every source and
destination role for every pair costs only `m^O(1) V`.

The input, destination and term/merge regions occupy an absolute
multiple of their input-plus-output volume. A role is an index in a
polynomial-size set, not a physical tape. A description table, exact
coefficient matrix, and arithmetic registers occupy `poly(m,k)` bits
and are reused. There is no stored coefficient matrix per spatial
address. If desired, the whole small coefficient matrix is recomputed
at every record; its polynomial-m work still has the stated bill.

For the rational spectral repair, E002 W2 computes the actual defect set
and the selected small rational matrix in polynomial-m bit operations.
The m query parities are supplied at the **spectral** boundary by the
source column scans. Reading all O(k) address bits per numerical record
is paid by R. This schedule neither scans a `2^m` archive per record nor
moves a spectral table through an unperformed converter.

For a rectangular check or lift, the check-row volume is at most the
parent volume. In a finite repair phase it has its exact smaller
fraction. The output-zero initialization is workspace and is never
counted as new independent template input. The original full-rate row
count and the recursive call numerator are unchanged.

## 3. Sequential rectangles retain Fourier sharing

A source pencil has an original input batch and an accumulated output
batch. Keep both, and process one rectangle at a time.

For a charged rectangle, sum its source labels in the prescribed common
layout into a temporary row batch, make the source-billed common-kernel
axis calls, apply the row map, and distribute the result to the output.
The common temporary has no more volume than the parent batch. It is
released before the next rectangle.

For a free rectangle `I x J`, prepare its first endpoint once on each
incident source row. The source proves that these transforms use only
the auxiliary axes and are independent of the query j. Keep this
prepared source collection; I is a subset of the labels, so its volume
is at most V. Allocate a zero destination accumulator on J in the
prepared final-endpoint coordinates, also of volume at most V.

For each query j, copy the prepared sources into one work collection.
Make the charged common-representative coordinate/sign changes, sum
the source rows, apply the small row map by Section 2, and deliver into
the same destination accumulator. The source proves that the middle
maps are monomial coordinate/sign changes and row mixing; they contain
no child Fourier calls. The matrix on the row coordinate commutes with
the final partial transform. After all j, apply that final endpoint
once to every incident destination row, return to ordinary coordinates,
add into the global output, and release all rectangle scratch.

This is exactly the source endpoint-sharing order. Only ordinary work
is overcounted polynomially. Neither endpoint is repeated once per
query. Every sum occurs in the source's specified common layout or in
the same prepared destination layout. An arbitrary different layout
cannot be added without its paid coordinate change.

The simultaneously retained numerical collections are the original
input, global output, one prepared source subset, one destination subset,
one query work subset, and a fixed number of common/term streams. Every
collection has volume at most V. A fixed number of marked V-sized
regions therefore suffices, independent of m, the number of rectangles,
and the number of incidences. Successive rectangles and queries overwrite
the same regions. This bounds cells ever visited, not only live payloads.

## 4. Physical changes of coordinates and scalar work

Binary elimination decomposes every source column map into O(A^2)
slot exchanges/additions. The source packed-XOR lemma applies to three
complete slots, with the unused slots and arbitrary leading rows as
spectators. Slot widths never exceed the active width a. Substituting
an exact interchange supplier with per-volume cost I(a,k) gives a
coordinate-change bill

```
V m^O(1) (1+log(k+2))^O(1) [1+I(a,k)]
  + poly(m,k).                                         (RW3)
```

The packed-XOR guard is `G=C0 ceil(log2(2k))`. Its control-description,
offset and exceptional-destination computations are polynomial in m
and k with fixed absolute degrees. Under `m<=k`, these have one fixed
polynomial-k bound. Choose the fixed integer C0 after that bound. Then
the source `O(k) 2^-G` exceptional fraction pays the exceptional
polynomial computation and radix-sort work. Narrow slots `a<G` use
the source direct bit moves. No guard constant depends on the actual
value of m.

A temporary full address has O(k) bits, so tagging a numerical R-bit
record increases its size by an absolute factor. The sort uses a fixed
number of arrays and strips the tags before invoking a numerical child.
Coordinate changes call the interchanger on original records, not on
an indefinitely accumulating sequence of old keys. Interchanger work
may itself have a `poly(log k)` visited-space factor; that is the only
such proportional factor retained in the statement below.

E002 W1 scales a k-bit fixed-point numerator by an exact rational of
height h in `O((k+h+1)(h+1))` actual fixed-tape steps and `O(k+h)`
visited cells. Under RW1, h fits O(k). Thus rational scalars have
`m^O(1)` time per encoded bit and absolute O(k) per-record scratch.
No approximate division by a full k-bit coefficient is treated as
constant time. Signs are exact, and the one direct odd-bit butterfly
uses the source separately charged O(k)-bit irrational coefficient.

## 5. Predictor, repair, and actual unrolling count

The rational Newton predictor has two live parent-sized arrays and
`D=O(sqrt(m))` successive pencils. The current Newton array is updated
by a pencil while its partial-sum array is parked. Section 3 implements
one pencil with a fixed number of arrays; its regions are reused at the
next Newton step. Its stage count increases time and call count, not
payload-space multiplicity.

The division repair keeps the original input, its first predictor
output, check/returned arrays and the current lifted correction in a
fixed number of parent-sized regions. Its two full-conversion phases
each have exactly one eighth of its volume. The direct depth-zero
leaf uses A axis transforms. At finite height

```
h=ceil(log2(m)/4),
W_h=W_0 8^h,
sigma_h/W_h <= a_m sum_(j=0)^(h-1) 4^-j + A 4^-h,      (RW4)
```

and the construction makes two child phases sequentially. Their
individual volume is V/8, so the parked payload series is bounded by
`V sum_(j>=0) 8^-j=8V/7`, times an absolute local-array allowance.
All these children retain the local template and rational coefficients;
they are finite algebraic unrolling, not substitutions of a new arity.

The binary finite-unrolling tree has at most
`2^(h+1)-1<=4 m^(1/4)` vertices. Each vertex has polynomially many
Newton stages, rectangles, roles and source axis calls, with absolute
degrees from the operation audit. Consequently the fully unrolled
local program has at most `m^K2` actual array operations and numerical
child calls for one absolute K2. Its completed batch width remains
polynomial in m. There is no omitted exponential branching factor.

A numerical spatial child acts on one original work row, hence has
volume V/W_m, with `W_m>=2`. Other arrays are parked while it runs;
sibling calls reuse their marked regions. Combining the finite
contraction and spatial descents gives geometric parked payloads.

## 6. Precision-compatible norm bound

Each rational row operation is a direct sum over addresses of blocks
of polynomial-m side and polynomial-m coefficient bit height. Its
norm is at most `m^K 2^(m^K)` for one fixed K. The number of possible
spectral keys does not multiply this norm: a block-diagonal operator
has norm equal to the largest block norm. Copies, masks, additions
and partial sums have the same coarse bound. Coordinate permutations
are isometries. Completed normalized numerical children are unitary.

Since the fully unrolled local program has only polynomially many
array operations, the logarithm of its largest input-to-intermediate
or intermediate-to-later gain is at most `m^K3`. This includes the
physical partial sums of Section 2 and all parked-array concatenations,
not merely the norm of the completed predictor. Rational scalar
rounding is bounded by one grid unit per real component by E002 W1;
exact interchange calls do not create numerical rounding errors.

For the variable Walsh schedule, the sum of these logarithmic gains
along any ancestor path is `k^o(1)`. Its actual total number of array
operations is polynomial in k because each local count is `m_i^K2`
and `sum_i log m_i<=log a_0<=log k`. The source two-ancestor-path
error argument therefore applies with a `2^(k^o(1))` gain, and one
absolute O(k) signed/fractional record format pays every fault.
The precise outer norm/error exponents remain the caller's choice;
this paragraph supplies the local numerical premise, not the outer
convolution/carry proof.

## 7. Component conclusion and scope

**Theorem RW.** Under the stated source correctness identities, exact
leading-row divisibility and guard RW1, the completed rational Walsh
node has its original `sigma_m/W_m` numerical child-volume invoice,
actual nonrecursive time RW3 plus the charged finite-data setup, an
absolute number of payload arrays, polynomially many actual children
and array operations in m, and logarithmic local numerical gain
bounded by a fixed polynomial in m. Its visited space is

```
C V [1+S_I(a,k)] + poly(m,k),                          (RW5)
```

where `V S_I(a,k)` is the exact interchange supplier's visited-space
bound. If `S_I(a,k)<=poly(log(k+2))`, this is the proportional-space
premise P-W of `../route-b/TWO-SCALE-RECURSION.md`. More conservatively,
all finite generation/storage may be placed inside its allowed
`2^(C m^C)(1+k)^(m^C)` additive term. The streaming executor only reads
compact descriptions and on-demand small matrices; it never rescans
that entire optional archive per numerical record.

The primary proof supplies all scalar, row, rectangle, address and
finite-repair storage mechanisms. It does not independently verify
the predecessor's label decomposition or rational repair identity,
nor the whole multiplication reduction. Exact finite replays are
evidence for specified algebraic pieces, not executions of this
physical fixed-tape algorithm or a complete multiplier.

Open next questions: independently check the interaction of the
fixed-array rectangle schedule with every source endpoint; audit
the all-level leading-row product and the final common-space wrapper.

Credits: @CubeJerry; pinned OpenAI endpoint sharing, normalization,
packed-XOR and numerical stability proofs; programme rational Newton,
division repair and on-demand coefficient suppliers; substantial
AI-assisted E003 scheduling and review. No formal verification or
human-refereed theorem is claimed.
