# A cross-pinned partition of the retained far-pair geometry

Status: **new constructive combinatorial component; independent review
requested**. This changes the actual rectangle family and reduces its
regular incidence. It does not yet change the admitted asymptotic
multiplication envelope or implement rectangle-volume physical delivery.

Use d>=2, h=2d-1, q=2^t and inner labels U=[q]^h. The counting and
partition identities hold for every integer d>=2; the retained rank
construction separately restricts d to powers of two. Put C=binom(h,d).
The source endpoint contract is cross distance d and no within-side pair
at distance d. Inner coordinate pins on the two sides need not occupy
the same coordinate.

## 1. The new explicit inner partition

Choose a d-subset S of varying coordinates, and let i1,i2 be its first
two coordinates in the fixed natural order. Fix common letters outside S.
Choose a,b in [q]. Define the projections at the first two positions by

    L_i1={a},             K_i1=[q] minus {a},
    L_i2=[q] minus {b},   K_i2={b}.

At each of the remaining d-2 coordinates choose one ordinary directed
first-differing-bit rectangle on unequal t-bit letters. Take Cartesian
products of these projections to obtain L and K.

**Lemma CP1.** These nonempty rectangles partition all ordered inner
pairs at Hamming distance d. Each side contains no two words at distance d.

**Proof.** Every cross pair disagrees in all positions of S and agrees
outside S, hence has distance d. For any such pair (v,w), S and the
outside common letters are determined uniquely. Set a=v_i1 and b=w_i2;
these are forced. The remaining positions have unique first-differing-bit
rectangles. This proves unique coverage. Within L, i1 and every position
outside S are fixed; words differ in at most d-1 positions. Within K,
i2 is fixed instead, with the same conclusion. All opposite alphabets
are nonempty because q>=2. No symmetric pin on the same coordinate is
required for these source interfaces. QED.

For d=2 there are no first-differing-bit choices. The partition is simply
`{a} x ([q] minus {b})` against `([q] minus {a}) x {b}` in the two
varying coordinates. This already gives the regular count q-1 in place
of (q-1)t.

## 2. Exact inner counts

A fixed source word forces its source pin a and all common outside letters.
Its destination pin b has q-1 admissible values; each of the other d-2
coordinates lies in exactly t directed source sides. Destination incidence
is symmetric, with the roles of the two pins exchanged. Therefore

    alpha_new=C (q-1)t^(d-2).                         (CP1)

The number of rectangles is exactly

    R_in,new=C q^(h-d) q^2 [2(q-1)]^(d-2)
            =C 2^(d-2) q^(d+1)(q-1)^(d-2).          (CP2)

The canonical old count is
`R_in,old=C 2^(d-1) q^d(q-1)^d`. Consequently

    R_in,new/R_in,old=q/[2(q-1)^2],
    alpha_new/alpha_old=1/t.                         (CP3)

In particular the rectangle count reduction includes one power of q,
whereas the incidence reduction is one factor of t. These two reductions
must not be conflated.

The new average source-side size, computed as q^h alpha_new/R_in,new, is

    (q-1) [q t/(2(q-1))]^(d-2).                      (CP4)

This can exceed the canonical average by a factor of order q/t. It is
an exact volume identity, not a physical aggregation procedure.

## 3. Outer product and source compatibility

Use the same outer labels V=U^h, N=q^(h^2), with support differing in
exactly d outer positions, each at inner distance d. Choose these outer
positions, fix all other inner words, and use CP1 independently in each
selected position. This partitions exactly the same off-diagonal support
as the retained characteristic-two matrix P*.

Across every outer rectangle the count k of far inner-coordinate pairs is
d. Within either side k=0 by CP1. Therefore the retained rational Gram
block values and orthogonal endpoint relations are unchanged. The same
scalar identity `I=P* - sum 1_K 1_L^T` holds over F2 (where subtraction
is addition), with the same P*, rank guard and rational routing dimension.
All data remain arbitrary independent inputs.

Every label now belongs to exactly

    lambda_new=C^(d+1)(q-1)^d t^(d(d-2))              (CP5)

source sides and the same number of destination sides. Relative to the
canonical old partition this saves precisely t^d. The total count obeys

    R_new=C (q^h)^(h-d) R_in,new^d,
    R_new/N=C^(d+1) 2^(d(d-2))
                (1-1/q)^(d(d-2)).                   (CP6)

No positive power of q remains in CP6. Equivalently the new/old count
ratio is `[q/(2(q-1)^2)]^d`. At d=2 the normalized rectangle count is
exactly C^3=27 for every q, while incidence is C^3(q-1)^2.

## 4. Effect and limits

This partition is a constructive improvement to the literal source
rectangle counts, not just a more accurate count of the old family.
It removes d log t from the outer incidence logarithm and removes the
d log q term from its normalized output-count logarithm, up to the
explicit finite factors above. It retains the same edge support and
within-side endpoint conditions; no low-rank error is newly introduced.

The leading incidence estimate still contains
`d(d-2)log t+d log(q-1)+O(d^2)`. Under the retained sufficient rank
guard and its optimized unbounded d, this has the same Phi(log m)
order. The unchanged rational dimension D also has logarithm O(dt).
Consequently this note does not claim a better unconditional global
rate, a log-free two-thirds multiplier, or an endpoint result.

CP6 may sharpen an open rectangle-volume delivery target, but preparing
and aligning the endpoint arrays is still a separate physical problem.
The new partition does not make incidence sharing automatic, establish
a common source basis, or remove query-dependent coset maps. Replacing
the canonical family in a completed fixed-tape compiler would additionally
require an explicit generator/layout audit; the present result is the
partition, its source algebraic compatibility and exact counts.

Credits: @CubeJerry; the pinned OpenAI directed-rectangle geometry and
retained characteristic-two adaptation; E002 exact-count/frontier work;
independent reviewer A's cross-pinned construction and substantial ChatGPT
multi-agent assistance. No literature priority, complete tape execution
or formal refinement is asserted.

## 5. Exact finite supporting checks

The accompanying `verify_cross_pinned_partition.py` generated the actual
rectangles for (d,q)=(2,2),(2,4),(2,8),(3,2),(3,4),(4,2) and compared their
union with independently enumerated Hamming-distance-d ordered pairs.
It passed 21,912 rectangles, 358,296 uniquely partitioned edges, regular
source/destination incidence at all 1,768 words, and 280,704 within-side
pair checks. Sixteen exact outer-formula cases passed. Fifteen negative
controls checked missing coverage, removal of the required source pin,
and using the old incidence count where t>1. The result is retained in
`cross-pinned-partition-verification.json`. These finite checks support the
explicit partition; the counting proof supplies the unbounded family.
