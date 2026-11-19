# A receiver-covariant irreducible native target at return excess b/30

**Proved algebraic target. No physical source/H/D/K realization and no new
complete kappa.** This strengthens the structural compatibility of S027's
irreducible target. It does not improve its return-rank ratio.

## 1. Exact statement and inherited source geometry

Let F be any field of characteristic two. Use the authenticated native 111
roles and their foreign-contact matrix O. Let S=F^16 carry the binary
split Clifford representation gamma of the native eight-dimensional
quadratic space. The pinned construction has

    gamma(v)^2 = q(v) I,
    gamma(v) gamma(w) + gamma(w) gamma(v) = beta(v,w) I.

All native roots have q=1, and distinct native roots are foreign exactly
when beta=0. For every positive integer s, put

    G = S tensor F^(60s),       b = dim G = 960s,
    Gamma_i = gamma(i) tensor I_(60s).

There is an explicit binary-coefficient block matrix B on G^111 with:

1. B_ij=0 on every nonforeign pair, including the diagonal; every foreign
   block B_ij is invertible.
2. `rank(I+B)=9b+b/30`. The retained canonical repair rank is also b/30.
3. `B_ij Gamma_i = Gamma_i B_ij` for every foreign pair (i,j).
4. The transport representation is irreducible: if W_i<=G and
   B_ij W_j is contained in W_i at every foreign pair, then either every
   W_i=0 or every W_i=G.
5. There is no positive-dimensional flat input subsystem and no
   positive-dimensional flat output quotient, even with vertex-dependent
   embeddings or quotient maps.

The Clifford covariance in item 3 is receiver-wise. It does not say that
B_ij intertwines Gamma_j with Gamma_i. There is no contradiction with
irreducibility: the different Gamma_i are not a single common commuting
operator.

Write a=80 and d=10. Independently reconstructing the native roots checks:

- K=I+O has rank 9, and the native undirected contact graph is connected.
- a and d are distinct and nonforeign, with degrees 62 and 61.
- K restricted to columns outside N(a) union {d} has rank 9.
- K restricted to columns outside {a} union N(d) has rank 9.

These are the same pinned geometric separation facts used in the first
irreducible target. The present change is the block assignment, not a new
graph or a change of native support.

## 2. Two actual Clifford involutions give a binary adapted basis

Set A=gamma(a)+I and C=gamma(d)+I. Since q(a)=q(d)=1 and
beta(a,d)=1,

    A^2=C^2=0,                 AC+CA=I.                 (1)

These relations imply ker A=im A and dim im A=8. Indeed Ax=0 gives
x=ACx, and A^2=0 gives the other inclusion. Choose a binary basis
e_1,...,e_8 of im A. Then

    (e_1,...,e_8, C e_1,...,C e_8)

is a basis of S: applying A to a putative relation first kills the last
eight coefficients, and then the first eight vanish. In this basis,

    A = E_01 tensor I_8,       C = E_10 tensor I_8.      (2)

The checker emits the actual 16-column change of basis and checks both
identities. No extension field or diagonalization assumption is required.

Let w=8s and write

    G = F^2 tensor W,
    W = direct_sum_(l=0)^59 W_l,
    W_l = F^8 tensor F^s,      dim W=60w.

This is the adapted S basis followed by a fixed permutation of tensor
coordinates. Let P be the coordinate projector from W onto W_0.

## 3. The 62 row generators and 61 column generators

Inside W_0, with basis u_0,...,u_(w-1), define the open Jordan shift and
its closing edge:

    J = sum_(k=0)^(w-2) e_(u_k) e_(u_(k+1))^T,
    E = e_(u_(w-1)) e_(u_0)^T.

For l=1,...,59 let T_l map W_l identically onto W_0 and vanish on all
other banks. Define the ordered row list of 62 operators on G by

    I_2 tensor J, I_2 tensor E,
    I_2 tensor T_1,...,I_2 tensor T_59,
    E_01 tensor P.                                  (3)

Define the ordered column list of 61 operators by

    I_2 tensor T_1^T,...,I_2 tensor T_59^T,
    E_10 tensor P,
    0.                                             (4)

J is nilpotent of index w, and every other nonzero operator in (3)-(4)
is square-zero. Here w>=8, so the closing edge E is square-zero.
Consequently I+N is invertible for every assigned perturbation N.

Assign (3) to the 62 ordered neighbors j of receiver a, and assign (4)
to the 61 ordered neighbors i of donor d. Put

    B_(a,j)=I+R_j,       B_(i,d)=I+C_i,

and put I at every other foreign block. Put zero at nonforeign blocks.
The row and column stars are disjoint because a and d are nonforeign.
Every native edge retains at least one identity orientation. In
particular, the final zero column perturbation simply leaves an identity
block; it does not delete a native edge.

## 4. Exact return rank and full matrix algebra

Let Delta=B-O tensor I. The row-star perturbation has image F^2 tensor W_0,
and one I_2 tensor T_l is already onto this image. Its rank is 2w. The
column-star perturbation depends only on F^2 tensor W_0, and one
I_2 tensor T_l^T is injective on that input. Its rank is also 2w.
Their input supports and output supports are disjoint at the native-role
level. Therefore

    rank Delta = 4w = b/30.                          (5)

Its entire row support is inside N(a) union {d}, and its entire column
support is inside {a} union N(d). The exact geometric restrictions in
section 1 imply

    row Delta intersect row(K tensor I) = 0,
    col Delta intersect col(K tensor I) = 0.

The retained rank-additivity lemma then gives

    rank(I+B)=9b+4w,
    rank([K tensor I; I+B])-9b=4w.                  (6)

For completeness, if Delta=UV has rank r and both separations hold, row
separation makes V onto F^r on ker K. Thus im(K+UV) contains im U and
then also im K. Column separation makes their sum direct, proving the
rank formula without a genericity argument.

The generators in (3)-(4) generate all of M_b(F). First,

    J^(w-1-r) E J^t = e_(u_r) e_(u_t)^T

for 0<=r,t<w. The T_l and T_l^T transport these units to every pair of
W-banks. Hence the generated algebra contains I_2 tensor M_(60w)(F).
Multiplication of E_01 tensor P on both sides by these secondary units
gives E_01 tensor every secondary matrix unit; the E_10 tensor P
generator does the same for E_10. Their products give E_00 and E_11
tensored with every unit. These are all b^2 matrix units.

For invariant W_i, invertibility in both orientations gives equal
dimensions along every edge. The identity orientation then gives equality
of the two subspaces. Connectivity gives a single common W, invariant
under the full matrix algebra, so W is zero or G. This proves item 4.

For flat embeddings Z_i with B_ij Z_j=Z_i, identity orientations and
connectivity likewise make all Z_i equal. The common kernel of the row
generators is zero: the T_l eliminate every bank except W_0 and J,E
eliminate W_0. Thus Z_i=0. For flat quotients P_i with P_i B_ij=P_j,
all P_i again coincide. The row-generator images contain F^2 tensor W_0;
the reverse-transfer images span every remaining bank. Their total image
is G, so the common P_i must vanish. Both conclusions persist when all
blocks are tensored with any identity body. Finite-bank irreducibility
does not in general persist under that replication and is not claimed.

## 5. Receiver covariance is built into the assignment

At receiver a, Gamma_a=(I_2+E_01) tensor I_W in the adapted basis.
Every row generator (3) commutes with it. At a receiver i foreign to d,
the reverse transfers I_2 tensor T_l^T act as the identity on the entire
spinor S and only move the 60 right-factor banks. They commute with
every Gamma_i. The remaining nonzero column generator has the form

    E_10 tensor P = (gamma(d)+I) tensor P_right,

where P_right projects F^(60s) onto its first s coordinates. Since i is
foreign to d, gamma(i) commutes with gamma(d), and P_right acts on the
other tensor factor. Thus this generator commutes with Gamma_i as well.
Unmodified identities commute trivially. This proves item 3 for all 6,470
native foreign blocks over every characteristic-two field.

The original S027 irreducible target does not meet this natural
restriction: its row-80 relative-block generators have scalar commutant.
Indeed J and E generate the projector onto its first w-dimensional bank
U and every matrix unit on U. A commuting Z must therefore be block
diagonal for U plus the remaining 59 banks, with Z on U equal to cI.
The identities Z T_l=T_l Z then say that the l-th block row of Z on
those remaining banks has cI in position l and zero elsewhere. For all
l, these identities force Z=cI on the entire original bank. Thus the
old row generators cannot all commute with the non-scalar Gamma_80. The present
assignment retains full algebra globally while permitting the prescribed
non-scalar commutant separately at each receiver.

## 6. The mixed left/right source motivation and its precise scope

For an A2 plane H generated by roots j,k, define on End(S)

    tau_H(X) = [gamma(j),[gamma(k),X]],

where the characteristic-two commutator is the sum of the two products.
The local algebra Cl(H) is M_2(F); its commuting algebra on S is M_8(F),
and tau_H is the local partial trace onto that commuting algebra. For
C,D in Cl(H), a donor-dependent source map of the form

    X |-> tau_H(CX)v + tau_H(DX)w                    (7)

is left-equivariant under every L commuting with Cl(H): F(LX)=L F(X).
This follows by moving L through the two commutators and C,D. It allows
genuinely mixed left/right matrix functionals and is not the pure-column
ansatz X|->Xu. The latter has scalar coefficient blocks in common matrix
column coordinates and is excluded by the fully early commuting-source
gate for the current exact target and routes.

In particular, (7) is gamma(i)-equivariant whenever i is perpendicular
to H. Any proposed H/D/K construction whose local maps preserve that
left action, and whose receiver map intertwines it with Gamma_i, must
have proper blocks commuting with Gamma_i. Examples of compatible local
operators are left multiplication by elements of Cl(H), then Cl(D) along
H contained in D, and elements commuting with Cl(K) at a final K
containing i, together with arbitrary right-factor operations. This is
only a closure condition. It does not prove shared H-output, D-target,
causal phase, or K full-demand compatibility. Matrix transposition
interchanges left and right actions and cannot be included in this
closure statement without a separate intertwining argument.

The present B removes one algebraic conflict between such a covariant
architecture and a low-return irreducible target. It does not prove that
(7) has the complete required simultaneous source bases, nor that any
physical H/D/K network realizes B.

## 7. Full target budget and remaining obligations

The normalized movement ratio is unchanged from the previously admitted
irreducible target. If a physical retained proper word realizes this B
with an invertible pure-Y map and restores all original X values, exact
one-way completion needs q=9b+b/30 returned symbols. With [j]=j^(199/200),

    Q=(4451/8)[1]+(7213/16)[2]+24[4]+(9+1/30)[8].

The pinned exact interval certificate gives positive limiting room
0.0141984734149543689553724953605943768942721 through
0.0141984734149543689553724953605943768949537125. The first successful
even paired multiplicity is 870; 868 fails. These are inherited movement
checks, not a complete covered-BIT supplier.

Compatibility with original banks End(S)^r requires 960s=256r, so
s=4t and r=15t. The minimum is b=3840, w=32, h=128, q=34688. This is
eight copies of the actual b=480 atlas. At b=11520, h=384 and q=104064.

For a GF(2^e) realization, the unchanged conservative retained complete
ordinary bounds would apply with M=111be, C=qe, C0=9be:

    ADD <= 18M^2+53M+111C0+2MC,
    INIT and charged dirty CLEAR <= 5M+C,
    peak public-plus-auxiliary records <= 7M+C.

They are conditional on a physical realization satisfying the retained
atlas accounting assumptions. Dense source maps, phase inverses,
snapshots, and any new local compilation must be charged and reconciled;
the source theorem's larger separate invoice is not silently absorbed
into these bounds. A return bank does not provide a missing source or
decoder. The exact D-stage shared-function and phase criteria, every
native K donor-rank demand, the total ordinary price, the uniform complex
supplier, the complete recursion, and all five foundational assumptions
remain explicit unresolved dependencies. No new kappa is asserted.

## 8. Verification and provenance

The author implementation reconstructs the native mask and
Clifford representation, emits an actual binary adapted basis, verifies
all modified blocks' covariance at the minimum spinor bank, and checks
the rank-separation identities. It checks literal full native matrices
at smaller auxiliary bank widths (where the rank and algebra theorem
still applies but no 16-dimensional covariance claim is attached), and
checks exact generator identities and actual-width support ranks.

Negative controls remove one off-diagonal spinor generator, mutate a
column generator to one that fails receiver covariance, and replace a
nilpotent generator by a diagonal unit that makes a foreign block
singular. The result is source-pinned and reproducible. Universal claims
rest on the written identities above, not finite checks.

Credit: S027's native irreducible target and exact Clifford reconstruction,
the earlier one-star and two-star targets, the near-minimum foreign-rank
and paid return-bank packages, and the exact retained budget. Work by
@CubeJerry with AI assistance. This is one continuation of the permanent
moonshot programme.
