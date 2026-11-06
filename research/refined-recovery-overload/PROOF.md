# Sharp zero-fiber recovery at the first overloaded depth

The matrix M is the exact 112-by-8 integer matrix in the hash-pinned
`research/precision-state-frontier/FIXTURE.json`. Let R round to the nearest
integer, with half ties away from zero, and put

    K(z) = z - M R(M^T z / 52).

Let G consist of all U in GL_112(Z) with M^T U = M^T. Frames are fixed and
known, not functions of the input. For 26 frames from G define

    z_1 = K(2x),    z_(j+1) = K(U_j z_j),    y = z_27,

where x ranges over all Z^112. There is precisely one relative refinement
bit, before the first call; all later calls use the same integer grid.

Write

    A = (13^8 + 14*13^4 + 1)/16 = 51,008,161,
    B = (13^8 -  2*13^4 + 1)/16 = 50,979,600,
    D = (13^8 - 1)/16           = 50,983,170.

## Result

**The exact minimum zero-output fiber, over all such frame sequences, is**

    Z_min = A^27 + 3 A B^26 + 12 A^2 B^25.                 (1)

A deterministic construction of integer unimodular frames attains (1).
The same construction has at most 16 A^27 preimages at every output.
Moreover,

    2^695 < A^27 + 15 B^27 <= Z_min <= 16 A^27 < 2^696.    (2)

Consequently **696 is the exact minimum worst-case fixed binary recovery-tag
length** among all frame sequences in this interface. The exact minimum
worst-output *cardinality* is not determined: the output attaining the maximum
for the constructed frames need not be zero. The two assertions must not be
conflated.

This answers the first overloaded depth left open by Nick Petalas's
[#6660](https://github.com/CrocSwap/integer-mult-bounds/pull/6660), exact head
`b6de532eff668a7daf8f2f98668f97af5af41338`, which proves optimal A^t cardinality
for t<=26 and strict excess thereafter. Its direct predecessor is @CubeJerry's
[#6327](https://github.com/CrocSwap/integer-mult-bounds/pull/6327), including
`research/refined-native-recovery/CHAIN_PROOF.md`. The new claims are the
sharp zero-fiber optimum, its actual source-frame realization, and the optimal
696-bit tag. **No new κ.** Physical memory, runtime and supplier admission do
not follow from these abstract state counts.

## 1. Reduction to a weighted relation code

The actual fixture satisfies M^T M=56 I and

    C = ker_F2(M mod 2) = C-perp,
    |C| = 16,    W_C(a,b)=a^8+14 a^4 b^4+b^8.

These finite source identities are recomputed directly. Thus V=F2^8/C has
dimension four. Parity descends to a nonzero functional p:V->F2; its kernel
is a three-dimensional subspace.

Put W_1=I and W_j=(U_(j-1)...U_1)^-1. Each W_j M induces an injective map
J_j:V->F2^112. For the output y, reverse execution gives the parity condition

    sum_j J_j(q_j mod C) = W_27 y mod 2.                  (3)

The integer quotient vectors are chosen backward. Given the later quotients,
coordinate q_j belongs to

    Q(s + 56 sum_(k>j) q_k),    s=M^T y,
    Q(v) = {q in Z : R((v+56q)/52)=q}.                    (4)

The predecessor interval lemma proves that Q(v) is always a consecutive
nonempty interval of at most thirteen integers, retaining the literal tie
rule. At v=56w, Q(56w)=[-6,6]-14w. Thus at y=0 the correct parametrization is

    q_j = r_j - 14 sum_(k>j) q_k,   r_j in [-6,6]^8.      (5)

In particular q_j and r_j have the same parity. This uses the cumulative
sum of later quotients. Formula (5), reversal and (3) give a bijection with
preimages: forward execution reproduces each chosen quotient, so distinct
histories cannot encode the same input.

Let L=ker(sum J_j) in V^27. A single quotient class v has mass

    f(v) = sum_(u in v+C) 7^(8-wt u) 6^(wt u)
         = A if v=0; B if v!=0 and p(v)=0; D if p(v)=1.   (6)

For completeness, Fourier expansion over self-dual C gives the factor
1/16 and terms 13^8, 13^4 times the signed sum over the fourteen weight-four
codewords, and the all-ones sign. For a nonzero coset the character sum is
zero, so the middle sum is -1-(-1)^p(v). This proves (6); literal enumeration
checks all 256 representatives. Hence the exact zero fiber is

    Z(L) = sum_(v in L) product_j f(v_j).                 (7)

All images J_j lie in red_2 ker_Z M^T, a 104-dimensional space. One direct
proof: the actual image lattice Lambda=M^T Z^112 contains 2Z^8. Therefore
for every integer q one can choose w with M^T w=28q, and Mq-2w belongs to
the kernel lattice while reducing to Mq modulo two. Every W_j preserves
the kernel lattice. Source lattice containment and saturation are checked
in the independent lift construction. Consequently dim L>=108-104=4.

Choose any four-dimensional subspace L_0 of L and parametrize it injectively
by u in F2^4. Its coordinate projections are arbitrary linear maps
T_j:F2^4->V. Positivity in (7) gives Z(L)>=Z(L_0). The u=0 contribution is
A^27. It remains to minimize the sum on the fifteen nonzero u.

## 2. Pointwise reduction to thirty block types

There are only two types needed in a lower relaxation.

* X_k, for a nonzero k in F2^4: a rank-three map onto ker p with kernel
  {0,k}. Its nonzero-u mass is A at k and B at the other fourteen points.
* Y_l, for a nonzero linear functional l on F2^4: an invertible map with
  p composed with the map equal to l. Its nonzero-u masses are D at the
  eight points with l(u)=1 and B at the other seven.

If p T_j is nonzero, replace T_j by a Y map with that functional. On the
odd half both masses equal D; on the even half a possible original zero
has mass A>=B. This is pointwise domination. If p T_j=0, its image has
dimension at most three, so choose any nonzero kernel vector k and replace
it by X_k. At k both masses are A; elsewhere the original mass is A or B,
never below B. This also is pointwise domination. Lower ranks are therefore
covered, rather than assumed absent. Existence of the comparison maps is
ordinary basis extension. The verifier separately checks all 65,536 binary
four-by-four linear maps, not just the nonsingular ones.

Let x_k count X_k blocks, and let the multiset of Y functionals have size y.
Write o_u for the number of those functionals taking value one at u. With

    a=A/B,    d=D/B,    sum x_k=27-y,

the relaxed nonzero-u objective divided by B^27 is

    sum_(u!=0) a^(x_u) d^(o_u).                          (8)

No assumption that the dominated maps remain a realizable relation family
is used for the lower bound. Attainment is established separately below.

## 3. Exact minimization of the finite relaxation

With y=0, convexity of a^x for a>1 shows that two multiplicities differing
by at least two can be balanced with a strict cost reduction. Since 27 is
15+12, the exact value is

    3a + 12a^2.                                         (9)

For y>=4 apply arithmetic-geometric mean to the fifteen positive terms
in (8). Since every nonzero functional is one on eight nonzero vectors,
their product is a^(27-y)d^(8y). Exact integer arithmetic verifies

    D^8 > A B^7,
    15^15 A^23 D^32 B^350 > (3 A B^26+12 A^2 B^25)^15.    (10)

The first inequality makes the AM-GM lower bound increase with y. The
second is exactly the fifteenth power of the strict bound at y=4, after
clearing the positive denominators. Thus every y>=4 is strictly worse
than (9); no floating-point logarithm or root is part of this exclusion.

For y=1,2,3, the complete multiset domains have 15,120,680 members. For each
multiset, minimize (8) over nonnegative x summing to 27-y. A bin with current
value d^o a^x has next marginal increase (a-1)d^o a^x. These marginals increase
within each bin. Taking the globally smallest available marginal therefore
selects the 27-y smallest entries in the union of those increasing lists:
any selected later list entry automatically includes its smaller predecessors.
This proves greedy optimality, including ties.

The primary checker uses exact fractions for that greedy algorithm. Every
positive-y minimum is strictly above (9). A separately authored dynamic
program explores every allocation without using the greedy rule. Together
with y=0 these are 816 exact finite cases. This finite arithmetic is the only
computer-assisted part of minimizing (8); the quantified reduction to that
domain is the argument above. A search cap is not substituted for coverage.

Combining Sections 1-3 proves the lower bound (1) for every allowed frame
sequence, including relation kernels larger than four dimensions. A larger
kernel adds strictly positive summands beyond any chosen L_0.

## 4. Attainment by actual integer frames

For each of the fifteen nonzero vectors k of F2^4 choose a map X_k as above.
Take k=1,2,3 once and k=4,...,15 twice, where these labels encode ordinary
binary vectors. The combined map

    u |-> (X_(k_1)u,...,X_(k_27)u)

is injective and defines a four-dimensional subspace L_* of V^27. Every
nonzero word has support 25 or 26: its zero coordinates are precisely the
one or two occurrences of its kernel label. In particular L_* has no
nonzero word supported on one coordinate. Its weight in (7) is exactly (1).

Let Q=V^27/L_*, of dimension104. Each coordinate V embeds in Q, since a
one-coordinate relation is impossible. Identify Q with H=red_2 ker_Z M^T
so that the first coordinate embedding is the actual map induced by M.
Each remaining coordinate embedding is an injective map V->H and extends
from the first embedding to an automorphism of H.

The integer kernel lattice K_Z=ker_Z M^T is saturated: its quotient is the
free abelian group Lambda=image_Z M^T. The actual source has an explicit
integer direct sum Z^112=K_Z plus a rank-eight complement. Its construction
and checks are in [LIFT_PROOF.md](LIFT_PROOF.md) and `lift.py`. Any binary automorphism
of H lifts to GL_104(Z) by elementary swaps and transvections. Extend that
integer automorphism by identity on the complement. This gives W_j in G
inducing the required embedding, with W_1=I. Finally put

    U_j = W_(j+1)^-1 W_j.

These are legitimate fixed integer unimodular mode-preserving frames and
have the required cumulative inverses. Thus the prescribed relation is
L_*, not merely an unconstrained abstract code.

The separate construction algorithm starts with the pinned source matrix,
verifies the kernel/complement decomposition, constructs the quotient and
binary embeddings, emits finite integer swaps and shears, and checks the
complete 112-column source identity and inverse for each of 27 W_j. The
finite exact lift attests this particular attaining construction; it does
not assume that every formal quotient can be implemented for free.

## 5. Uniform output bound and the exact binary tag

For the constructed maps, the sum map V^27->H has rank104 and kernel L_*
of dimension4. For any y, equation (3) has no solution or exactly16 quotient-
syndrome sequences. Fix one such sequence. Count quotient histories backward
using (4). At each step its eight coordinates range over a product of intervals
of length at most13, and their parity lies in one specified coset of C.

The number in any such box and coset is at most A. The character expansion
of the coset indicator gives 1/16 times a sum indexed by C. Zero-coordinate
factors have absolute value at most13; nonzero-coordinate alternating sums
have absolute value at most1. The triangle inequality and weight enumerator
therefore give (13^8+14*13^4+1)/16=A. This remains true when the interval
endpoints depend on already chosen later quotients. Sequential conditioning,
not a joint Fourier majorant over all stages, now gives at most A^27
histories for the fixed syndrome sequence. Summing gives at most16 A^27
preimages at every output.

Conversely every frame sequence has a four-dimensional relation subspace.
Its zero syndrome contributes A^27, and its fifteen nonzero words each have
weight at least B^27. This already gives the lower bound used in (2).
Both endpoints of (2) are checked by exact integer comparisons. Thus no
695-bit tag can distinguish every input in the zero fiber, while 696 bits
suffice for every fiber of the constructed fixed map. Sufficiency here means
an abstract fixed-cardinality encoding: order each finite fiber and retain
the input's index. No efficient codec, memory layout or clean physical
implementation is asserted.

## Scope, unfinished obligations and credit

The exact maximum-fiber cardinality of the attaining frames, the exact
minimum maximum-fiber cardinality, depths above 27, mode-changing or
input-dependent frames, additional refinement, finite input ranges and
favorable physical callers remain distinct questions. The frame operations
may be costly. Any physical adoption must charge them, the codec, range,
source access, workspace, routing, restoration, cleanup and precision.
The selected frontier and native_all_columns, owned_erasure, compiler,
precision_tape and analytic_recovery assumptions remain unchanged.

The predecessor source and interval/fiber mechanisms are credited to
@CubeJerry/#6327, zxv/#5444, Ali Romman/#5323, Brian/#5035 and the retained
native lineage. Nick Petalas/#6660 supplied the longer-chain quotient
formulation,104-dimensional limit and the explicit open question. Binary
linear algebra, code-character duality, AM-GM, discrete convex allocation
and elementary unimodular lifting are classical. Prepared for @CubeJerry
with substantial OpenAI Codex assistance in separate mathematical,
constructive and independent-checking roles. Apache-2.0. No human or formal
proof-kernel acceptance is claimed.
