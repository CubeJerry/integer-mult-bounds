# The outer source transfer for variable local arity

Status: **proved source-substitution gate, conditional on the stated exact
interchanger and numerical Walsh suppliers**. This closes V18's outer gate;
it does not independently certify V7, V8 or V17. Their separate reviews are
required before a stronger global theorem is admitted.

Reviewed B `variable-arity-transfer.md`, SHA256
`cb357755f43172cbba7ba3a4bc9fddbdd6574a02ec3786905cf755e7fb47ea2c`;
companion space proposal SHA256
`71cf477715f4991a0c67ccf25df0ee3ad6669a1eea7ac29658faf01b7d96c300`.
Source: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, November
tape `build/permutations.tex`, `build/walsh.tex`, `build/integers.tex` and
`build/uniformity.tex`. In this pass I reread the full permutations and
integers source. The complete Walsh and normalized Fourier audits were
performed earlier in this session. This is a written physical analysis,
not a complete machine replay.

Put Phi(y)=(y+1)^(2/3)(log2(y+2))^(1/3) and
E_C(t)=2^{C Phi(log2(t+2))}. Constants are absolute. Increasing C absorbs
a fixed number of these factors and every fixed power of log(t+2).

## 1. Exact interfaces used in the transfer

**I.** On two complete U-bit fields with arbitrary occupied spectators and
original bit volume V, one fixed processor gives an exact interchange in
`C V sqrt(U+1) E_C(U)` time and `C V E_C(U)` visited cells. Its field
encoding, internal radix conversions, coefficient arithmetic, dispatch,
keys and generation are charged. All borrowed coordinates are restored.

**W.** On N=2^k numerical records of absolute Theta(k) width, a selected-bit
normalized Walsh layer on s<=c k/log(2+k) positions, and its adjoint, take
`C Nk sqrt(k+1) E_C(k)` time and `C Nk E_C(k)` visited cells. For fixed
absolute norm/error allowances, absolute O(k) integer/fractional precision
controls all intermediate arrays. Numerical local control calculations
belong to the pinned fixed grammar with polynomial(m,k) bit complexity,
and the variable numerical family has m<=k^{o(1)} above a fixed threshold.

Finite preparation may additionally have cost

    A(k)<=2^{C k^eta} k^C + 2^{k^{o(1)}},   eta<1 fixed.        (VO1)

A larger fixed eta<1 absorbs a polynomial number of distinct preparations.
I already includes its preparation; VO1 also safely covers preparing its
width chains upfront. Nothing this expensive is repeated per input record.
The source fixed O(k log k) short multiplier remains the algorithm for
general k-bit products. No per-record phase product is replaced by k^2 work.

## 2. The guard parameter remains an absolute O(log k)

The packed-XOR proof uses a fixed menu of controls, offsets and exceptional
rank calculations. In CRT and short-transform calls their descriptions
and evaluation have fixed polynomial-k bounds. In numerical Walsh, the
polynomial(m,k) bound is also at most k^e for one fixed e once m<=k.
This holds eventually uniformly over all active widths. On-demand rational
coefficient work is separate scalar work, not an arbitrary program passed
to the guard primitive.

Take G=C_G ceil(log2(2k)), with one fixed C_G covering those degrees.
Each guarded target fibre has at least 2^G records and pays its prefix
offset calculation. Counters and head returns use the source amortized
scans. An arbitrarily long spectator prefix is advanced, not reread for
every symbol. The exceptional fraction is at most 80k*2^-G. Its k^e rank
calculations and O(k) stable sorting passes are O(V) after enlarging C_G.
O(k)-bit destination tags increase Theta(k)-bit records only by a constant
factor; they are removed before any call requiring the original payload.

The interchanger's parameter generation is not part of every offset
calculation. It is paid by I once per invocation or by VO1 once per retained
width plan. No expanded archive is searched for a control value. Its
existence therefore does not require a growing-degree guard polynomial.

## 3. Packed XOR, positions and controlled blocks

For common chunk width L<=Ck, each of the source eight shifts uses a fixed
number of I interchanges, plus complete-fibre rotations and scans. One
exact guarded pass thus costs `O(V sqrt(L+1) E_C(L))+A(k)`. The number
of residue classes and high-bit exceptions is O(log k). If L<G, the direct
bit bill is LV<=GV and fits the same bound. All auxiliary Z values are
restored, including occupied data. This gives

    XOR time <= C V sqrt(L+1) E_C(L)(1+log k)+A(k),
    XOR visited <= C V E_C(L)+A(k).                         (VO2)

The source two-involution position-permutation construction uses a fixed
number of such bulk-XOR operations on O(k)-bit chunks. Its cycle tables
have fixed polynomial-k preparation. Its time and space are VO2 with
L replaced by k. These bounds follow from the operations of the proof;
we are not substituting a changing exponent into a fixed-rho theorem.

The controlled-block construction retains an absolute free-control
fraction delta. Each target block has c log(2k) bits for fixed c and a
per-control table computable in fixed polynomial-k steps. Its Beneš
construction uses O(log k) block batches and O(log k) stages, each with
bounded position routing and guarded flips. Therefore

    block time <= C V sqrt(k+1) E_C(k)(1+log k)^3+A(k),
    block visited <= C V E_C(k)+A(k).                       (VO3)

Passes, block batches, scalar tables and exceptional sorts reuse marked
regions. Their logarithmic count multiplies time but not visited volume.
Tags remain O(k) bits. Complete ranges and borrowed occupied coordinates
are preserved and restored exactly by the original source identities.

## 4. The unchanged integer shape and source layer list

For a v-bit digit call, use b_digit=ceil(log2 v), h=ceil(v/b_digit),
k=ceil(log2(4h)), N=2^k. Then Nk=Theta(v) and k=Theta(1+log2 v),
with absolute constants. The source's coprime cyclic axes have at most
20 ceil(log2 k) bits each, total width k, and product at least 2h.
Prime enumeration and trial division are fixed polynomial-k work. The
existence theorem has one absolute cutoff independent of the variable
families. Actual size/coprimality/width tests and exact fallback are retained.
The new composite *address* radix does not replace these outer factors.

At each balanced CRT-tree level, external controls occupy at most
k/2+O(log k) bits. This leaves the fixed free fraction needed in VO3.
Rotation tables are generated from O(k)-bit positional integers and
polynomial-k target ranges. O(log k) levels in either direction add only
a fixed logarithmic factor and reuse the same work regions.

The source synchronized short transform has blocks of four to seven axes,
with at most 140 ceil(log2 k) bits. Their routing, matching, schedules and
phase tables therefore have fixed polynomial-k construction. Retain the
pinned occupied-neighbor identity, its absolute amplification count and
its bounded-away-from-zero phase denominators. It acts correctly on
arbitrary borrowed data and restores them before the next batch.

Its O(log k) global unitary layers are exactly: a VO3 permutation, a phase
stream or a W selected-bit Walsh layer. W's selected-bit condition is the
source O(k/log k) count. Prefix streaming of the phase products writes
fewer than 2N records and uses the source O(k log k) short multiplier, so
the full phase generation/application costs O(Nk log k). Two alternating
prefix tapes use O(Nk) cells. No full product of block possibilities is
searched separately for each coefficient.

## 5. Absolute precision gives an exact full product

Invoke W with the source allowances: represented norm at most 2^(13k)
and absolute local Walsh error at most 2^(-50k). Its absolute O(k)
precision includes variable-template intermediate growth and rounding.
Prepare phase coefficients and products to 2^(-70k) error using a larger
fixed absolute multiple of k bits. Exact permutations have no rounding.

Every completed exact layer is unitary. The source induction over O(log k)
layers therefore gives transform error at most 2^(-40k) on norm at most
2^(12k) inputs. Do not insert the internal Walsh amplification factor again
at a completed unitary boundary. Intermediate Walsh norms are covered by
W itself. The source product inequality bounds the coordinatewise-product
error by 2^(-30k), with norm at most 2^(12k). Its adjoint transform and
sqrt(S) scaling then put every convolution coefficient within Euclidean
error less than 1/2. All arithmetic operands have absolute O(k) width.

Nearest-integer recovery and the ordinary carry scan consequently give the
exact complete 2v-bit product, contiguous and most-significant-first.
The carry has O(k) bits. No approximate answer is returned and no borrowed
occupied coordinate is treated as zero workspace.

## 6. The derived V18 profile

The source layer list and the two suppliers give

    time <= C Nk sqrt(k+1) E_C(k)(1+log k)^C+A(k),
    visited <= C Nk E_C(k)+A(k).                           (VO4)

Fixed logarithmic powers fit E_C after increasing C because
log log(k+2)=o(Phi(log2(k+2))). As eta<1, VO1 is o(Nk) above a fixed
cutoff. Phase streams, short-word scratch, constructor areas and numerical
stacks all start at marked positions and reuse them. Thus VO4 bounds the
union of visited cells, not only maximum live storage. With
L(v)=1+log2 v and Nk=Theta(v), k=Theta(L(v)), it becomes

    tau(v)<=v sqrt(L(v)) 2^{C Phi(log2 L(v))},
    visited(v)<=v 2^{C Phi(log2 L(v))}.                    (VO5)

This is B's V18, with an absolute sufficient cutoff and exact fallback,
conditional only on the stated I and W suppliers.

After I and W are independently admitted, choose the actual positional
wrapper's r=2^{O(Phi(log2 L(n)))} with exponent constant large enough for
the space coefficient. Its r^2 chunk products multiply the same overhead
by only r. Since log r=o(log L(n)), chunks remain asymptotically as long
on the logarithmic scale. All setup is sublinear in n and fits the n/16
preparation cap eventually. Exact marked caps and schoolbook fallback
handle every shorter length. Reusing the input/output/wrapper/candidate
regions gives uniform O(n) visited cells and the proposed V20 envelope.
This wrapper is an actual selected algorithm, not a free infimum over
candidate programs.

## 7. Required clarification of the proposed additive bound

The paragraph after V14 and V19's discussion say whole preparation is
2^{k^{o(1)}}, even if optional exponential checks are performed. This is
stronger than the exact-interchanger setup statement, which permits
2^{U^eta} with fixed eta<1 and U as large as a constant fraction of k.
That term need not be 2^{k^{o(1)}}.

Either omit the optional exponential exact-interchanger validation and
prove polynomial compact construction, or use VO1's conservative
2^{O(k^eta)}+2^{k^{o(1)}} bound, with eta<1 enlarged to absorb polynomial
counts. Both are 2^{o(k)}, hence n^{o(1)} at k=Theta(log n). They fit the
same n/16 caps and do not change V18, V20 or the common-space argument.
This is a correction to the stated additive envelope, not an unclosed
proportional cost. The present proof uses the conservative version.

## 8. Remaining admission scope

No additional outer exponential-in-m proportional loss appears after I and
W. This review does not independently prove their growing-arity recurrence
or sharper endpoint space schedule. Those are the remaining separate
gates. Nor does this retain only a finite arithmetic certificate as a full
physical theorem: all source routing, precision, preparation, record
widths and visited-region reuse are explicit in the interface and transfer.

Open next question: complete the independent I/W reviews and bind their
exact versions to this gate before admitting the stronger envelope.

Credits: Jerry Chen (@CubeJerry), the pinned OpenAI tape/Fourier source,
predecessor source-operation audits, B's variable schedules, E002 physical
processors and substantial AI-assisted independent review.

## 9. Supplement: local routing keeps active width a

V12 requires a local sqrt(a) toll, although records have Theta(k) bits and
the full address has k bits. The same physical proofs keep these two
parameters distinct. After initial selected-bit gathering, a numerical
node's active a bits form one complete consecutive field. A child designates
one consecutive f-bit slot, with all other slots spectators. It does not
repeat global k-position gathering. Column exchanges and additions act
inside that active field with complete, restored auxiliary slots.

To permute positions only in the a-bit active field, run the source's two
involutions on three subchunks of width floor(a/3); everything else is a
spectator. Guards still have G=C_G log(2k), but every I call has width O(a).
If a<G, direct bits cost at most GV; otherwise there are O(log k) passes.
Thus local position routing has

    time <= C V sqrt(a+1) E_C(a)(1+log k)+poly(k),
    visited <= C V E_C(a)+poly(k).                         (VO6)

The single global selected-position gathering and inverse occur outside
the selected-bit recursion and fit V17's sqrt(k) cost. Polynomial(m)
local map counts multiply VO6 by 2^{O(log m)}, which is
2^{O(Phi(log(a+2)))} for B's slower numerical schedule. This is exactly
the local toll in V12/V15. Polynomial-k additive preparations, summed over
polynomially many numerical node types, are absorbed by the 2^k-record
volume. No sqrt(k) routing charge is silently replaced by sqrt(a) at each
node, and no global position permutation is inserted into every child.
