# One fixed gauge per endpoint leaves at least half the label rank charged

Status: **proved within the individual-monomial-route model; independent
review pending**. The lead independently checked the displacement
identity before this note was written. This result allows arbitrary
asymmetric free weights and a changed charged label matrix. State-walk
and state-tree sharing use multiple gauges and are outside its scope.

## 1. Precise statement

Retain A's source-compatible partial-Fourier model: norm-one label
directions d_v in a nondegenerate paired binary space, one input gauge
`U_v subset d_v-perp` and one output gauge `V_v subset d_v-perp` per
label, fixed across the retained routes. An individual route v to w has
monomial middle only if `V_w=U_v-perp`.

Let N be the number of labels. Let F be any N-by-N scalar matrix over
a field K, with

    F_(w,v) != 0  only if  V_w=U_v-perp.                               (CR1)

It may be asymmetric, weighted, overlapping or chosen by a different
label identity decomposition. Put `C=I-F`.

**Theorem CR.** In this model,

    rank_K(C) >= ceil(N/2).                                           (CR2)

Thus every exact weighted rank-one rectangle decomposition of C has at
least ceil(N/2) nonzero summands. This concerns the label matrix and the
specified gauges, not arbitrary numerical algorithms or tape runtime.

## 2. A diagonal displacement proves the bound

First, `U_v != V_v-perp` for every label. Otherwise both U_v and U_v-perp
would lie in d_v-perp. Taking complements puts d_v in both U_v and
U_v-perp, making its self-pairing zero, contrary to norm one.

Let S be the finite set of subspaces appearing among the U_v and
V_v-perp. Choose pairwise distinct scalars gamma_W for W in S. If K is
too small, pass only for this rank argument to a field extension K'
with sufficiently many elements. Matrix rank is unchanged by a field
extension, since the nonzero-minor criterion is unchanged.

Define diagonal N-by-N matrices

    A_(v,v)=gamma_(U_v),        B_(v,v)=gamma_(V_v-perp).

The preceding observation makes B-A invertible. Condition CR1 gives
`BF=FA` entry by entry. Consequently

    B-A = B(I-F)-(I-F)A = BC-CA.                                      (CR3)

Rank subadditivity and multiplication cannot increase rank, so

    N=rank(B-A) <= rank(BC)+rank(CA) <= 2 rank(C).

Rank preservation under the scalar extension proves CR2 over K itself.
The keys gamma_W are a proof device; no unbilled field conversion or
numerical operation has been inserted into an algorithm.

The argument does not require F to retain all originally free edges or
to preserve the original charged polynomial. It applies to every F
supported on the individually monomial routes admitted by the single
input/output gauges. Norm one and that support condition are essential.

## 3. Sharpness for the native labels

For native binary-Gram labels `[q]^ell`, q=2^t>=2, match each label with
the label obtained by flipping one fixed alphabet bit in one fixed
coordinate. Let pi be this fixed-point-free involution and P its
permutation matrix. Matched labels have Hamming distance one, hence
orthogonal norm-one directions.

Choose

    U_v=span{d_(pi(v))},         V_v=d_v-perp.                           (CR4)

Both are auxiliary at label v, and every matching route satisfies
`V_(pi(v))=U_v-perp`. Set

    F=-P,                       C=I+P.

On each matched pair, C is the all-ones two-by-two block. Therefore
`rank(C)=N/2` over every field. These blocks are exactly N/2 charged
rectangles, and F is supported on the allowed free matching routes.
This proves sharpness throughout the native alphabet family, including
q>=4. It does not claim that the retained original charged polynomial
itself has rank N/2.

## 4. Consequence only for the retained charged routine

If the charged part is still implemented by the source's 2D-axis common
kernel for every charged rectangle and every one of m queries, then its
declared call invoice per original label row is at least

    (2D) m ceil(N/2)/N >= Dm.                                         (CR5)

This is the same retained-routine convention as A's q=2 rank argument,
now valid for every label alphabet in the one-gauge model. The source
provides that 2D-call implementation; CR5 does not turn an implementation
upper bound into a lower bound on all implementations. A different
charged executor, rank-aware row processing, residual transforms,
multiple gauges, or multi-path synthesis requires a separate analysis.

In particular, the new state-walk/tree schedules deliberately change
prepared gauges between states, so CR2--CR5 do not obstruct those
constructive sharing improvements. No new complete multiplication bound
or physical runtime lower bound follows here.

## 5. A finite number of gauge channels

The lead supplied the following extension during review. Suppose there
are g>=1 fixed gauge channels. In channel a, retain one input/output
gauge at each label as above, and allow an arbitrary matrix F_a supported
on that channel's individually monomial routes. Put

    F=sum_(a=1)^g F_a,             C=I-F.

Then

    rank_K(C) >= ceil(N/2^g).                                      (CR6)

To prove this, apply the scalar-key construction separately to each
channel, after one common field extension if necessary. It supplies
diagonal A_a,B_a with B_a-A_a invertible and B_a F_a=F_a A_a. Define
the linear displacement operator

    L_a(X)=B_a X-X A_a.

All the L_a commute, since all their left and right coefficients are
diagonal and left multiplication commutes with right multiplication.
For each a, the product of all g operators kills F_a: commute L_a next
to F_a and use L_a(F_a)=0. Thus

    (L_1 ... L_g)(C)=(L_1 ... L_g)(I)
                    = product_(a=1)^g (B_a-A_a).

The right side is diagonal and invertible, so its rank is N. Expanding
the product of operators gives at most 2^g terms, each a diagonal left
and right multiple of C, with a sign. Every term has rank at most
rank(C), and rank subadditivity proves CR6. This proof also covers
overlaps and cancellations between the channel matrices.

The factor 2^g is sharp in the abstract norm-one model. Let N=2^g,
take the binary ambient space of dimension N with orthonormal label
directions d_v=e_v indexed by bit strings v, and in channel a set both
U_(a,v) and V_(a,v) to the span of basis vectors e_w whose a-th bit
differs from v's. These are auxiliary at v. When v and w differ in bit a,
V_(a,w)=U_(a,v)-perp, so that route is admitted by channel a. Let F_a
have entry -1 on ordered label pairs whose first differing bit is a,
and zero elsewhere. The channel matrices sum to minus the off-diagonal
all-ones matrix, leaving C equal to the all-ones N-by-N matrix of rank
one over every field. This shows equality in CR6. It makes no claim of
sharpness for the native Gram labels when g>1.

Under exactly the retained charged-routine convention in Section 4,
this gives the charged invoice

    (2D)m ceil(N/2^g)/N >= 2Dm/2^g.                               (CR7)

The channel count is a hypothesis of CR6--CR7, and no channel setup,
transition or sharing is declared free by the proof. Compositions of
several routes are not automatically a supported sum of these channel
matrices. State-walk/tree schedules can change gauges with their states;
they are not subject to the g=1 consequence, and applying CR6 to any
such schedule requires first establishing its stated fixed-channel
representation. No runtime lower bound is inferred.

Dependencies: A's `ROUTING-GLOBAL-ENDPOINT-GAUGE.md`; C's independent
source review and `ONE-GAUGE-GRAPH-CLASSIFICATION.md`; the pinned OpenAI
Fourier endpoint construction. The diagonal-displacement argument and
native matching sharpness were derived in C during final review; the
finite-channel extension and abstract sharpness were derived by the
lead and checked algebraically in C.

Credits: @CubeJerry; E003 A's exact gauge model; lead independent check;
substantial AI-assisted derivation. No priority, formal-proof or human-
refereeing claim is made.
