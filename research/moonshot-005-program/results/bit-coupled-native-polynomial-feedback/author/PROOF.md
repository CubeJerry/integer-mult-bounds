# Noncommuting polynomial feedback with universal propagation slack

**Exact source theorem and finite ordinary-donor/early examples. No common
H word, complete physical invoice, return, or new kappa.**

This family changes all quotient maps while keeping every two-plane
inverse-fibre propagation span at most9k. The admitted array-anchor test
requires15k, so its saturation premise fails everywhere. This is uniform
over all centres, rather than protection of a selected finite subgraph.
It does not solve common-H alignment; a zero-intersection obstruction
remains in the displayed, ungauged polynomial coordinates.

## 1. Field blocks and the feedback family

Work over F=GF(64), binary modulus z^6+z+1, or an extension. The authenticated
global nodes a_H are the28 zeros of q(a)=a^9+a^18+a^36. For v nonzero, put

    B_v={a:q(a)=0, b(v,a)=q(v)+1}.

Its monic16-root polynomial P_v has lower coefficient support
S={0,1,2,4,5,8,14}. The retained field identity is

    v² P_v(z)=L_v(z)+q(v)+1,
    L_v(z)=v z^8+v² z^16+v^4(z^14+z^5)
           +v^8 z+v^16 z²+v^32 z^4.

Let G={3,6,7,9,10,11,12,13,15}. For any k>=1, organize a donor's input
x in F^(16k) into16 width-k blocks. Choose a k-by16k feedback matrix V_j
with arbitrary k-by-k blocks at G and zero blocks elsewhere. No blocks
need commute. Define

    F_(j,H)x=([1,a_H,...,a_H^15] tensor I_k)x
              +(a_H^16+1)V_j x.                         (1)

h(a)=a^16+1 never vanishes at an allowed node: a^16=1 implies a=1, and
q(1)=1. Thus nonzero feedback changes every literal quotient.

## 2. Explicit inverse of every ordinary source cut

Let c_v be the16 lower coefficients of P_v(z)+1 and put C_v=c_v tensor I_k.
At each a in B_v, [1,a,...,a^15]c_v=a^16+1. If A_v is the Vandermonde on
that16-node block, its complete source view is

    A'_v=(A_v tensor I_k)(I+C_v V_j).                    (2)

c_v is supported in S, so V_j C_v=0 regardless of the noncommuting block
choices. Therefore (C_v V_j)^2=0 and, in characteristic two,

    (I+C_v V_j)^(-1)=I+C_v V_j.

Every ordinary geometric view is invertible at every k and for every
allowed feedback assignment. This is an algebraic identity, not a generic
determinant argument.

A larger conditional family allows all16 blocks of V_j. If every
k-by-k matrix I+V_j C_v is invertible, the source cuts are invertible and

    (I+C_v V_j)^(-1)=I+C_v(I+V_j C_v)^(-1)V_j.

The propagation bound below holds in this larger family as well. The
nine gaps supply unconditional invertibility, not the rank-envelope bound.

## 3. Uniform propagation bound at every distinct H/R pair

Fix distinct allowed nodes a,b and let v range over blocks containing both.
Write g_(v,a)=P_v/(z+a). The old fifteen-quotient inverse fibre has basis
K_(v,a)=g_(v,a) tensor I_k. In the gap-supported family the new basis is

    K'_(v,a)=(I+C_v V_j)K_(v,a).                        (3)

In the larger conditional family use the inverse from Section2. In either
case the new columns differ from the old ones by elements of im(C_v).

Because a is a root, q(v)+1=L_v(a). Hence

    v² g_(v,a)(z)=[L_v(z)+L_v(a)]/(z+a),
    v² c_v=L_v(z)+L_v(a)+v²(z^16+1),

where the degree16 terms in the second expression cancel. Both coefficient
maps are binary-linear in v. Seeing a and b gives the nonzero linear
equation b(v,a+b)=0, so all such v lie in a five-dimensional binary
hyperplane. The old fibre columns therefore span at most5k dimensions,
and all correction columns span another space of at most5k dimensions.
Their feedback multipliers may vary with v and need not commute; every
correction still lies in the second space. Their sum has dimension at most10k.

The visible quotient at b annihilates every new a-fibre. On the correction
block C_v it equals h(b)I_k in the gap-supported family, or
h(b)(I+V_j C_v) in the larger conditional family. This restriction is
surjective, since h(b) is nonzero and the small view matrix is invertible.
Its kernel therefore removes at least k dimensions from the10k envelope.
The sharper conclusion is

    rank span_v im K'_(v,a) <=9k <15k.                  (4)

This holds for every donor, every distinct pair of source planes, and any
native subset of their common receivers. The scalar checker exhausts all
756 ordered node pairs: each has20 geometric receiver parameters and
ranks(5,5,10) for the old space, correction space, and their union.
The all-width result follows from the two linear maps, not extrapolation
from the finite width-three example.

Any invertible whole-input donor gauge preserves (2) and (4), by applying
its inverse to all fibres at that donor. Invertible quotient-output gauges
also preserve kernels. Thus this source slack survives the donor gauges
required by a possible common-H continuation.

## 4. Literal ordinary-donor witnesses

The finite instance uses k=3 at all100 native donors without a singleton
source plane. Its slot3 feedback is a3-cycle P and slot6 feedback is E_00;
the other seven blocks use the recorded deterministic coefficient stream.
The nine products P^r E_00 P^s, 0<=r,s<=2, span M_3(F). At every node the
literal coefficient blocks generate this algebra: h(a) is nonzero and
the input-block0 coefficient is I. This is genuine noncommuting coupling
on the declared copy axis, also after field extension.

The checker reconstructs and verifies every actual ordinary geometric and
native source cut. It also reconstructs100 actual96-by96 early bases on
two component copies using native per-plane early quotas and recorded
frame seeds. These are literal early-existence witnesses; the theorem
does not say every possible feedback has every early basis invertible.
The11 singleton donors are not replaced by this finite certificate.

Each of the100 arrays has a recorded sixteen-plane observation of rank
below48. The old RS system is injective on all such observations. The
different number of distinguishable outputs proves genuine source changes
under arbitrary whole-input and separate-output bijections, beyond the
copy-axis algebra invariant. The checker additionally evaluates all756
matrix-valued propagation spans for the frozen donor0 feedback; all756
have rank27=9k, so the sharper bound is attained by this concrete array.

## 5. Scope and the remaining H obstruction

Uniform nonsaturation is not H compatibility. At native H263, a donor pair's
off-H node sets have intersection9 and union21. If x belonged to both
feedback kernels in the displayed common polynomial coordinates, evaluation
at one common node, where h is nonzero, would imply V_j x=V_l x. The two
degree16 vector polynomials would then be identical and vanish at21 distinct
nodes. They must be zero, forcing x=0. The checker verifies zero common
inverse fibre for donors0,61 at all33 native H263 receivers. A donor gauge
changes that common-coordinate premise; no compatible gauges are built.

An unsupported coefficient14 feedback block is a negative control. Choosing
it so V_j C_v=I lowers one actual source cut from48 to45. This tests the
essential gap-support requirement independently from the ungauged H failure.

No complete bank3840 word, singleton replacement, common H/D/K/facet map,
low return, or complete caller invoice is claimed. All five foundations
remain. Finite dense ADD compilations exist for the displayed early
matrices, but an uncomputed compiler or owner cost is not inserted into a
kappa comparison.

## Replay and open next questions

    python -B research/moonshot-005-program/results/bit-coupled-native-polynomial-feedback/author/check.py --repo REPO --out FRESH

The optional unchanged field_rank accelerator must match the default
receipt. Parameter, global-node, and source hashes are retained.

Next solve the donor-gauge/common-H equations in this structured family,
or a related family retaining the same global slack. The larger conditional
family reduces native invertibility to63 small k-by-k tests per donor.
A successful continuation still needs actual early bases, singleton
handling, common middle maps and the full source/middle/return invoice.

Credit @CubeJerry and the retained native/source authors. S030 root supplied
the geometric and global bilinear identities and the ungauged intersection
objection. Worker A derived the square-zero feedback family, universal
propagation envelope and noncommuting source/early witnesses. Substantial
OpenAI assistance; independent review is separate.
