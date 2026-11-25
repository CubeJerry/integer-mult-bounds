# Radix conversion for field interchange without volume inflation

Status: **proved wrapper lemma; independent review requested**. This is a
physical fixed-tape reduction between interchange primitives. It is not a
complete multiplication theorem and does not discharge the local field or
numerical Walsh execution obligations.

Session: S004, 2026-11-26 (Melbourne). Source comparison: OpenAI
`math@3344da59991ed94f9ba711217b29c1d760badfa6`, November tape paper,
`build/interchange.tex`, final paragraph of the radix recursion. The source
embeds each binary range into a complete radix range and pays a `<b^2`
volume factor. The construction here uses disjoint real subrectangles and
a small residual strip. It therefore separates radix choice from
proportional visited space.

## 1. Interface and conclusion

For `M>=2`, let `I(M)` denote the exact permutation

    (p,x,g,y,t) -> (p,y,g,x,t)

on a stream in lexicographic order with index ranges
`[P] x [M] x [G] x [M] x [B]`. Every entry is one fixed-alphabet symbol;
equivalently, its fixed-width binary payload can be included in B. Write
`V=P G B M^2` and `u=ceil(log2 M)`. All dimensions are supplied in binary.
The implementation uses a fixed number of one-dimensional tapes and
charges every head movement.

Suppose a single callable processor `R_b(e)` interchanges equal fields
of length `b^e` for arbitrary positive P,G,B, using at most

    V F_b(e) time,       S_b V + D_b(e,log(2V)) visited cells,       (NP1)

where `b>=2`, `e>=1`, and `F_b` is replaced by its nondecreasing majorant
if necessary. Setup common to the processor is charged separately and
retained only once. The constant number of tapes and alphabet must be
uniform in b; a family of unbounded-tape machines is not this interface.

**Theorem NP.** There is a fixed-tape wrapper, using R_b as specified, with

    time <= C V [F_b(floor(log_b M)) + b^2 Q^2 + 1] + preprocessing,
    visited cells <= C(1+S_b)V + max_(e<=E, v<=V) D_b(e,log(2v))
                    + preprocessing,
                                                                  (NP2)
    Q = min(floor(log_b M)+1, 1+ceil(log_b(u+1))).

The `F_b(0)` term means the identity and can be taken as 1. Preprocessing
uses a fixed polynomial in `u+log(b+1)+log(PGB+1)` operations and cells;
the usual fixed-degree descriptor bound absorbs it into the displayed
volume coefficient. Crucially, **b^2 occurs in time, not in proportional
space or in the input volume supplied to R_b**.

If `b>M`, use the direct binary-field implementation below. Its O(uV)
time is within `O(b^2 V)` and its space is O(V), so assume b<=M thereafter.

## 2. Elementary fixed-tape operations used

1. **Extract and merge a prescribed interval rectangle.** Given intervals
   I,J in `[M]`, extract the entries with x in I and y in J by a sequential
   pass. They occur in the restricted lexicographic order
   `[P] x I x [G] x J x [B]`. A second pass merges a returned stream into
   the prescribed output rectangle. These scans cost O(V), use O(V)
   temporary cells, and do not attach an address word to each symbol.
   Nested range counters use low-end ripple updates; run boundaries are
   computed before their complete runs. A fixed number of range fields
   suffices. Their fixed-degree setup is included in preprocessing.
2. **Move a small field.** A coordinate of cardinality R can be moved past
   any fixed collection of fields, without changing their relative order,
   in O(RV) time and O(V) cells. For each of its R values, extract the
   corresponding subsequence and merge it into its destination positions.
   R may be large; the time is charged and no R streams are held at once.
3. **Generic dyadic rectangular transpose.** Pad a nonempty range of
   length a to the next power of two, less than 2a. For two resulting
   dyadic fields of widths p,q, move their p+q individual binary fields
   one at a time across the intervening fields, using operation 2 with
   R=2. Explicitly, move the q bits of the later field, in their original
   most-significant-first order, to immediately before the remaining
   earlier-field block. Then move the p bits
   of the earlier field, in reverse order, to immediately after
   the arbitrary gap [G]. Each move preserves the other fields' order;
   every move costs O(V_rect) and O(V_rect) space. Thus the number of
   moves is p+q<=2u+2. Removing known
   padding gives an arbitrary a-by-c rectangular interchange in
   O(u V_rect) time and O(V_rect) space when a,c<=M. The gap G and outer
   P,B fields remain spectators throughout.

These are explicit sequential stream algorithms. The runtime proofs do
not treat a coordinate permutation as a free arithmetic instruction.

## 3. Leading radix blocks and the residual strip

Write `M=sum_{i=0}^E a_i b^i`, with `0<=a_i<b`, `a_E>0`, and
`E=floor(log_b M)`. Retain the Q highest digit levels,
`i=E-Q+1,...,E`, truncating at zero. Partition the corresponding initial
interval into `a_i` consecutive blocks of length `b^i` at each level.
There are at most `(b-1)Q` blocks. Denote the unretained final interval by
T, of length r. If every level was retained, r=0. Otherwise

    r < b^(E-Q+1),        r/M < b^(1-Q) <= 1/(u+1).              (NP3)

The leading square is the disjoint union of the ordered pairs of retained
blocks. The remainder is the disjoint union

    T x [M],          ([M]\T) x T.

Its total fraction of entries is at most `2r/M<=2/(u+1)`. Apply elementary
operation 3 to these two rectangles. Their direct-transpose work is O(V),
including their less-than-fourfold *local* dyadic padding. Extraction and
merging add a fixed number of full V scans. No full padded M-by-M array is
created.

## 4. A pair of unequal radix blocks

Consider one retained block of length `b^p` on x and another of length
`b^q` on y; offsets are removed on extraction. Suppose p>=q and write
the x index as `(h,x0)` with ranges `[b^(p-q)] x [b^q]`.
Its restricted order is

    (prefix,h,x0,g,y,suffix).

Call R_b(q) on x0,y, with `(prefix,h)` as its prefix. The result is

    (prefix,h,y,g,x0,suffix).

Move the h field past y and g using elementary operation 2. The result

    (prefix,y,g,h,x0,suffix)

is the desired rectangular interchange. For q>p, first move the high
part of y to the front, before x and g, then apply the equal-width
interchange to its low part and x. The high part is now already in its
destination position. One small-field move suffices in either case;
the stated coarse bound allows two. Cases p=0 or q=0 need no oracle.

For local volume V_pq, the cost is

    V_pq F_b(min(p,q)) + C b^|p-q| V_pq.                      (NP4)

The second term may be large for one rectangle. Its *weighted sum* is
small, which is why replacing all terms by their largest coefficient
would lose the result.

## 5. Summing the full bill

There are at most `b^2 Q^2` ordered retained-block pairs. Extract and merge
each by full-array scans, so their total cost is at most `C b^2 Q^2 V`.
The input is read-only; one output accumulator holds the already completed
rectangles. Scratch for one rectangle is reused.

The sum of local oracle volumes is at most V, and every exponent is at
most E. Thus oracle work is at most `V F_b(E)`. For each pair of exponent
levels p>=q, summed over their a_p a_q block pairs,

    sum b^(p-q)V_pq = P G B a_p a_q b^(2p) <= b V,             (NP5)

because `a_q<b`, `a_p>=1` when present, and `a_p b^p<=M`.
There are at most Q^2 ordered level pairs, giving `O(bQ^2 V)` for all
unequal-field corrections. The symmetric p<q case has the same bound.
Together with the residual strips, this proves the time inequality.

At any instant the read-only input, output accumulator and a fixed number
of local scratch streams each have length at most a constant multiple of
V. Only one oracle runs. Its volume is exactly that rectangle's real
volume; its own scratch is at most S_b V. Every region is marked and
reused before moving to the next pair. Therefore the union of all visited
cells has the space bound in NP2. The proof does not merely bound live
storage, and neither the number of pairs nor b multiplies that space.

## 6. Consequence and limits

For a varying parameter m with `b<=m^K`, the wrapper has ordinary cost
`m^{O(1)}(1+log u)^2 V` and adds only an absolute O(V) proportional-space
cost. If m is a sufficiently small power of u, its ordinary work can be
strictly below V sqrt(u). This removes one specific obstruction to
nonstationary recursion: the source's b^2 padding is not an intrinsic
space expense for exact interchange.

The lemma does **not** prove that the full compact local interchanger has
parameter-independent proportional space; it preserves whatever S_b the
supplier actually proves. It does not bound all numerical Walsh endpoint
permutations by the recursive-call count. It does not improve H(n) until
those independent physical and global-caller obligations are discharged.

The associated finite checker verifies block partitions, residual bounds,
the weighted unequal-exponent invoice and exact array permutations. It
uses explicit finite arrays; that replay corroborates the combinatorics,
not the all-size tape-cost argument.

Credits: the pinned OpenAI equal-field interchange and elementary stream
framework; @CubeJerry; ChatGPT multi-agent research. No general radix-
conversion priority claim has been established.
