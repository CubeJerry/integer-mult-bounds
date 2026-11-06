# Ordered even query blocks cannot repeat an endpoint face

No new κ. This is a scalar-projector obstruction, not a supplier construction
or an impossibility theorem for arbitrary caller roots.

## 1. Exact model and result

Work over a field of characteristic different from two. Let n≥4 be
even, and use the canonical shortest-word queries on V=F^n:

\[
u_i=e_i\ (0\leq i<n),\quad u_n=(-1,1,-1,1,\ldots)^t,
\qquad (v_i)_j=\operatorname{sgn}(i-j),\quad v_n=\boldsymbol1^t,
\qquad R_i=u_iv_i.
\]

Here v_i's displayed entry formula is for i<n. For internal indices,
v_i e_0=1, v_i u_n=-1 and v_i e_j=sgn(i-j).
The application to arbitrary scalar shortest roots uses the inherited
simultaneous-conjugacy normal form, not a bounded coefficient search.

Suppose P_0 and P_n are distinct, commuting rank-two idempotents supporting
the endpoint queries on both sides:

\[
P_0R_0=R_0P_0=R_0,\qquad P_nR_n=R_nP_n=R_n.
\]

Their simultaneous eigenspaces have dimensions (1,1,1,n-3); write them
as <a>, <b>, <c>, H, with endpoint masks ab and ac. A **left-face bank**
is an idempotent Q commuting with both endpoints, equal to the identity on
<a,b> and zero on <c>. A **right-face bank** is the analogous bank with
mask ac and zero on <b>. Its action on H may be arbitrary.

A query group I consists of m distinct internal sites i_1<...<i_m.
Its bank Q supports every query in the group on both sides. The group is
**even and minimal** when m is positive and even and rank(Q)=m+2.
Groups in a family are **ordered** if every site in each group precedes every
site in the next. They need not be consecutive internally.

**Theorem.** In an ordered family of even, minimal, pairwise commuting
left/right-face banks, there is at most one left-face group and at most one
right-face group. If both occur, the left-face group precedes the right-face
group. The theorem holds for every even n, every nonzero endpoint parameter,
and every allowed group size. Prefix commutation is not needed for the
obstruction; imposing that additional caller obligation cannot evade it.

**Pair corollary.** Three disjoint ordered adjacent query pairs cannot all have
rank-four common banks of these two faces. If such three face banks exist,
at least one has rank at least five. This does not prove the rank-six floor
observed in the finite three-pair pilot in CrocSwap/integer-mult-bounds#6726.

## 2. Endpoint coordinates, with no parameter excluded

This rederives the endpoint chart used for rank-three single-site banks in
CrocSwap/integer-mult-bounds#6398, now in arbitrary even dimension.
Set a=P_n e_0. The endpoint support equations give v_n P_n=v_n and
v_0P_0=v_0. Thus v_n a=1 and a is nonzero in the common endpoint image.
Also P_0u_n is in the common image and v_0P_0u_n=v_0u_n=-1, so it is
nonzero. Distinct rank-two commuting projectors therefore have a one-dimensional
intersection. Put r=-v_0a. Since P_0u_n is proportional to a, r is nonzero
and P_0u_n=a/r.

Define

\[
b=e_0-a,\quad c=a-ru_n,\quad z=e_0-c,
\quad w_0=e_0+u_n.
\]

Then b and c are nonzero vectors in the other two endpoint atoms, and

\[
a=e_0+ru_n-z,\quad b=-ru_n+z,\quad c=e_0-z,
\quad e_0=a+b,\quad u_n=(a-c)/r.
\]

The common kernel H lies in K={x:x_0=0, v_nx=0}. Also z belongs to K and
P_0z=e_0, so K=<z>⊕H. These facts justify the coordinates for every r≠0,
including r=1 and r=-1.

For a left-face bank supporting R_i, its image contains e_i and its kernel
contains c. The latter gives v_i c=0 and hence v_i z=1. If
e_i=αa+βb+d with d∈H, applying v_n and v_0 gives α=1 and β=1-1/r.
Consequently its H-image must contain

\[
d_i^L=e_i-w_0+z/r.
\]

For a right-face bank, the kernel contains b, so v_i z=-r. Applying the
same two rows to e_i=αa+γc+d gives α=1/r, γ=1-1/r, and

\[
d_i^R=e_i-w_0+z.
\]

Write C_I for the rows v_i restricted to H, and D_I for the columns d_i
of one group. The restriction E_I=Q|_H fixes those columns on the left and
those rows on the right. For either face,

\[
C_ID_I=K_m(s),\qquad K_m(s)_{jk}=\operatorname{sgn}(j-k)+s,
\qquad s=1/r\text{ for L},\quad s=-r\text{ for R}.
\]

This follows directly from v_iw_0=0 and the displayed values of v_i z.

## 3. The even-block inverse and forced projector

Let A_m have entries sgn(j-k), let J_m=11^t, and let
q_m=(1,-1,...,1,-1)^t. For even m, direct multiplication of entries gives

\[
(A_m^{-1})_{jk}=(-1)^{j+k}\operatorname{sgn}(j-k),\qquad
A_m^{-1}1=q_m,\quad 1^tA_m^{-1}=-q_m^t,\quad 1^tq_m=0.
\]

For completeness, in the product A_m times the claimed inverse, the diagonal
entry is -∑_{k≠j}(-1)^{k+j}=1 because the full alternating sum is zero.
For j<l, the off-diagonal entry is
1+(-1)^(j+l)+2∑_{j<k<l}(-1)^(k+l)=0, by the finite alternating sum.
The case j>l is the same calculation. This proves the inverse in every
characteristic different from two.

The rank-one update has the especially simple inverse

\[
K_m(s)^{-1}=A_m^{-1}+s q_mq_m^t,
\qquad 1^tK_m(s)^{-1}1=0.                 \tag{1}
\]

Multiplying out proves (1): the linear terms cancel and the quadratic term
vanishes since 1^tq_m=0. In particular K_m(s) is invertible for every s;
no generic-parameter argument or division by s±1 is used.

Thus rank(D_I)=rank(C_I)=m, and any such face bank has rank at least m+2.
At equality, its restriction to H is uniquely forced:

\[
E_I=D_I K_m(s)^{-1}C_I.                   \tag{2}
\]

Indeed im(E_I)=im(D_I); writing E_I=D_IX and using C_IE_I=C_I gives
K_m(s)X=C_I. Equation (2) follows. This uniqueness is why minimal rank
is essential to the theorem.

## 4. Ordered banks of the same face cannot commute

Let I precede J and have even sizes m,p. For two banks of the same face,
the cross-pairing matrices are

\[
C_ID_J=(s-1)1_m1_p^t,\qquad
C_JD_I=(s+1)1_p1_m^t.                    \tag{3}
\]

Substitution of (3) in (2), followed by (1), gives

\[
E_IE_JE_I=0=E_JE_IE_J.                  \tag{4}
\]

If idempotents E_I,E_J commuted, E_IE_JE_I=E_IE_J and the reverse product
would be equal to it. They would both vanish. Because D_I,D_J are injective,
C_I,C_J are surjective and the K matrices are invertible, (2)-(3) imply
E_IE_J=0 exactly when s-1=0, while E_JE_I=0 exactly when s+1=0.
Both cannot hold in characteristic different from two. This includes the
exceptional s=±1: one product is zero and the other is nonzero.

Commutation of the full banks implies commutation of their H restrictions,
so this proves the claimed one-per-face restriction.

## 5. The left face must precede the right face

For an L group before an R group, direct pairing gives both cross matrices
zero, compatible with commutation. For an R group before an L group, they
are -2·11^t and 2·11^t. Formula (1) again makes both triple products zero,
whereas both double products are nonzero. Hence this reversed order is
impossible for commuting banks. The theorem follows.

## 6. Connection to the changed-root investigation

The exact eight-field root retained from CrocSwap/integer-mult-bounds#6726
has common banks at pairs (1,2) and (6,7), of rank four, and endpoint ranks
two. Its native masks are ab+h_L and ac+h_R, where h_L,h_R now each have
dimension two. Our independent rational normalization reconstructs r=-1,
the forced projectors (2), all native prefix commutators, and the allowed
L-before-R zero cross-pairings directly from its query matrices.

That predecessor's finite ten-field pilot found a rank-six middle pair
inside 20 tested placements. The present theorem removes any dimension,
coefficient-height or parameter-search bound for the two stated faces, but
only proves that three rank-four pair banks are impossible in that class.
The single-site rank-three predecessor in CrocSwap/integer-mult-bounds#6398
uses one-dimensional H projections. Here the H projections may have any
positive even rank, and the decisive identity is zero triple product with
nonzero double product. No claimed allocation-only extension or native
promotion pilot is rerun.

The desired optimistic extension would add a third pair with the same
rank-four common-bank cost as each existing fragment. It fails a necessary
algebraic obligation before any new caller or complete invoice exists.
Therefore this package makes no numerical bound claim. A rank-five bank,
another endpoint face (a, bc, abc), equal/higher-rank endpoints, interleaved
groups or a genuinely coupled-port model requires a new
analysis and complete physical, ownership, restoration, native and outer
budget. None is excluded here.

The exact replay checks finite instances and all polynomial coefficients
of (1) through m=16, plus a pinned source fixture and fault controls.
The all-dimension result is the written proof above, not an extrapolation
of those tests or formal-kernel verification.

## 7. Independent-review extension to odd groups

The independent adversarial review also removes the even-size restriction
from the one-per-face conclusion. It retains the same minimum bank rank m+2
and all the same endpoint and ordering hypotheses. The even theorem above
continues to hold over every field of characteristic different from two.

For odd m, put q_m=(1,-1,...,-1,1)^t and let B_m have entries
(-1)^(j+k)sgn(j-k). Direct alternating sums give

\[
A_mq_m=0,\quad B_m1=0,\quad 1^tq_m=1,
\quad A_mB_m=I-1q_m^t,\quad B_mA_m=I-q_m1^t.
\]

Since s is either 1/r or -r, it is nonzero. Thus

\[
K_m(s)^{-1}=B_m+s^{-1}q_mq_m^t,
\qquad k_m(s):=1^tK_m(s)^{-1}1=1/s.
\]

For even m, equation (1) instead gives k_m(s)=0. In either parity K is
invertible and the minimal projector formula (2) remains valid.

For ordered groups with cross-pairings α11^t and β11^t, the product E_IE_J
has rank one whenever α≠0, and cyclicity of trace gives

\[
\operatorname{tr}(E_IE_J)=\alpha\beta\,k_m(s_I)k_p(s_J).       \tag{5}
\]

If the idempotents commute, their product is an idempotent. A nonzero rank-one
idempotent has trace one over any field (write it xy with yx=1).

For two banks of the same face, (5) is zero if either group is even, and
otherwise is 1-1/s², which is never one. At least one of the two product
orientations is nonzero, including s=±1, so commutation is impossible.
Consequently **at most one group of each face is possible for arbitrary
positive group sizes**, over every characteristic different from two.

For a reversed R-before-L pair, αβ=-4. If either group is even, the trace is
zero. If both are odd, s_R=-r and s_L=1/r give trace four. Therefore the
left-before-right ordering conclusion also holds for arbitrary positive group
sizes in characteristic different from two and three, including characteristic
zero. Characteristic three with two odd groups is a genuine exception to the
order conclusion; the independent finite-field witness supplied with the
review exercises the support-and-commutation statement only; it is not a
physical caller: its prefix commutators fail at both internal sites 1 and 2. It is not an exception
to the original even theorem or
to the all-size one-per-face bound.

Prepared for @CubeJerry with substantial OpenAI Codex assistance. Endpoint
coordinates and scalar normal form retain Ali Romman's and the cited
predecessors' credit; the retained root and its original NOTICE are unchanged.
Apache-2.0.
