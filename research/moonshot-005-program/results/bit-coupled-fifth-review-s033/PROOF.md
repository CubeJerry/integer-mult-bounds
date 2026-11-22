# A constructive common-response repair and the actual receiver gate

**An exact enabling construction plus a necessary physical-interface bound. No
fifth whole receiver, complete supplier, new exponent, or foundational discharge.**

This independent review follows the S032 four-receiver source/D interpolation
system. Its new point is that an abstract common readout can be improved by
changing the D word on an exceptional algebraic locus, while binding that
readout to the eight actual receiver-95 outputs imposes a stronger condition.

## 1. Literal setup

Work over GF(64), or any coefficient-field extension. The eleven native donors
have eight D input coordinates each, indexed by I(j). Their union V has size
32; the three absent coordinates are 24, 29, 33. The physical D word has 35
inputs and outputs and a 19/16 early/late split. Let T be its invertible matrix.

For r in {6,9,48,73}, let O(r) be the eight actual D outputs and let
S(j,r)=T[O(r),I(j)]. All these sections must be invertible. Let L be the fixed
96-by-32 joined source frame and let K=L W be the fixed 96-by-4 frame examined
in S032. A source map retaining the four prescribed identity readouts has

    P(j) L = E(j) [S(j,6)^(-1), S(j,9)^(-1),
                  S(j,48)^(-1), S(j,73)^(-1)],

where E(j) inserts the eight coordinates into their actual 35 input positions.
Define B(j)=P(j)K and

    Z = [B(j)-B(61)] over j != 61.

Every row outside V is zero. The old word has rank Z=30 and
rank[Z B(61)]=32, so arbitrary common linear readouts have response rank two.
All ranks and the literal source matrix identity are rechecked independently
by `check.py`; it implements its own polynomial-basis GF(64) arithmetic and
does not import the author arithmetic or elimination implementation.

## 2. Why K remains forced in the restricted interpolation family

At donor 61, K lies in the H-observation core C(61,h) at each of the four
modified D parents h=263,481,642,947. The certificate gives explicit matrices
D(h) with C(61,h) D(h)=K. Preserving the H observations therefore fixes all
four modified source quotient maps on K. In the 44-map interpolation family,
the other source quotients are unchanged. Consequently the entire source/H
proper restriction on K at donor 61 remains unchanged, including its old
zero off-D response at receiver 95. This last isolation fact is inherited
from the admitted S032 forced-collision construction; the present checker
does not independently reconstruct every H owner.

Changing the D word does not change membership in that proper inverse fibre:
the off-D records still vanish and the allowed D records remain in D1509.
If the receiver-95 section remains invertible, B(61) has rank four and K is
still a genuine four-dimensional subspace of the entire donor-61 fibre.
Thus a common entire receiver-95 fibre with equal readouts must include K
and must give it the same injective response at every donor.

This inference fixes the literal retained H interfaces, routing, and the
restricted source family. For a more general source modification, it remains
valid whenever all donor-61 source/H proper records on K are preserved. Merely
retaining the four abstract D readouts does not by itself assert that premise.

## 3. Two overlaps give an exact rank-four abstract common response

Let F=(4,5,7,8). Independent calculation gives

    W(6)=W(9)=0,
    W(48)=T[O(48),F] A,
    W(73)=T[O(73),F] B,

where A and B are saved 4-by-4 matrices and H=A+B is invertible. B(61)=E(F)H.
These identities continue to hold whenever the retained-output/F rectangle
is fixed, as in the new S033 affine interpolation family.

Suppose a row vector a on the native coordinates V can be represented in both
retained receiver row spaces:

    a = c48 T[O(48),V] = c73 T[O(73),V].

For every donor j, restricting this identity to I(j) and multiplying its
invertible section gives

    a[I(j)] S(j,48)^(-1)=c48,
    a[I(j)] S(j,73)^(-1)=c73.

It follows directly that

    a B(j)=c48 W(48)+c73 W(73)=a[F](A+B)=a[F]H.

This response is independent of j. The actual shared rows 10 and 30 give
two such vectors. Their F profiles have rank two. The following two further
relations supply profiles e1 and e2, independent modulo those shared profiles:

| Desired profile on F | Coefficients on late O(48) rows 21,22,30,34 | Coefficients on late O(73) rows 20,23,25,30 |
| --- | --- | --- |
| (1,0,0,0) | (12,5,10,28) | (0,49,62,58) |
| (0,1,0,0) | (43,1,0,12) | (12,11,18,63) |

Impose equality of these row combinations only on V. Those are linear
constraints on the unfixed D coefficients. They are consistent with the
fixed rectangle because both combinations have the same F profile. All
involved output rows are late, so the construction does not introduce an
early-to-late forbidden block. Values on the three absent input coordinates
remain available to preserve full-word invertibility.

The construction worker found a literal exact matrix satisfying these
relations, the phases, the source/D interpolation equations, and every
geometric D section. The independent check here verifies the fixed rectangle,
the two actual overlap identities, and the resulting four-row common decoder.
It independently obtains

    rank Z = 28,
    rank[Z B(61)] = 32,
    rank(common decoder response) = 4.

This is an actual improvement of the previously rank-two abstract response.
It disproves the suggestion that all admissible D coefficients in the affine
family necessarily retain response rank two. The full 144-section check and
source interpolation admission are recorded by the construction package and
are not represented here as an independent reconstruction of their geometry.

## 4. Eight actual receiver outputs require rank Z at most 24

The preceding four-row decoder is an abstract linear readout on D ingress.
The actual receiver-95 interface consists of eight specified rows

    O(95)=(10,13,16,18,30,31,32,33).

If these outputs give equal values on K across all native donors, then

    T[O(95),V] Z[V]=0.

The matrix T[O(95),V] has rank eight: restricting its columns to any native
I(j) gives the required invertible eight-by-eight section. Rank-nullity in
the 32-dimensional native input space therefore gives the necessary bound

    rank Z <= 32-8 = 24.

This holds for every proposed linear source/D modification with the stated
support and section contracts, independent of how its coefficients are
chosen. It uses the actual whole receiver, rather than an arbitrary decoder
with only four rows. Under m-fold repeated banks, the same proof gives
rank Z_m <= 24m, provided the receiver has 8m independent actual rows on the
same 32m supported input coordinates. Coefficient extensions do not alter
the argument.

The overlap matrix has rank Z=28 and cannot be a full receiver-95 repair.
Its actual receiver-95 contrast response has rank six. Compared with the old
rank-30 contrast, it removes two ranks; four additional ranks must be removed
before this necessary physical gate can even hold. The bound is not a
sufficient condition: equal outputs, injectivity on K, whole-fibre equality,
all other source views, chronology, and costs must still be established.

The checker contains a small exact countermodel with contrast rank 28 and
abstract response rank four but only four independent common output rows.
It also checks the abstract sharpness of the rank-nullity bound at rank 24,
and rejects a corrupted response. These controls prevent confusing the
two distinct interface requirements.

## 5. Open next questions

Find a physical T and source system with rank Z<=24, an injective actual
receiver-95 response, and complete source/H/fibre validity. The two-overlap
construction shows that exceptional rank-drop loci are worth constructing
directly; random sampling of the 833-dimensional affine family can miss them.
A possible lower bound on rank Z for all admissible T remains unproved.
In particular, the fact that three absent coordinates limit row-space overlap
does not prove that all additional common decoders arise from such overlaps.

All five inherited foundations, the remaining native sources, full H/D/K/facet
word, paid global return, both strict suppliers, and the complete recursive
caller remain open. No new complete kappa.

Credit @CubeJerry, S031/S032 source/H/D and review contributors, the inherited
geometry/compiler authors, and the S033 construction worker implementing the
two-overlap mechanism. Substantial OpenAI assistance. Independent agent
arithmetic and proof review; no independent human or kernel certification.
Apache-2.0.
