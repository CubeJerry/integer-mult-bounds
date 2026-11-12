# Exact reverse-rank gates for reciprocal continuation

**Proved algebraic interface with exact source instances. No new kappa.**
The matrix statements do not acquire a row at a chart, create a second bank,
restore a donor, or grant an unspent route. They are admission tests for a
literal implementation. Prepared for @CubeJerry with OpenAI assistance.

## Source and normalization

Use the programme's pinned 104-column rational root matrix, with each root
having squared length 8. Restrict to the 96 hosted ports; the eight coupled
ports have no independent reverse bank and are excluded here. Write A for
this 8-by-96 matrix and G=A^T A/8. Thus G has diagonal 1. All statements below
hold over Q and every characteristic-zero extension of Q, at every positive
field volume, by tensoring the displayed maps with the identity. The general
block-rank statements hold over any field where their matrices are defined.
The equality rank(A_S^T A_S)=rank(A_S) uses this rational real Gram source;
it is not asserted for an arbitrary matrix over an arbitrary field.

The independent hosted inputs are b_i=q_X2_i and d_i=q_Y2_i. The target
reverse update is b-d. A literal paired forward correction with coefficient
-G_ij for donor j and receiver i adds +G_ij d_i to b_j. Consequently if R
records the actually implemented transpose additions, the remaining reverse
coefficient matrix is M=I+R. The number of additions, the rank of R, and the
rank of M are different quantities.

## 1. Complete receiver rows give an exact matroid-nullity gate

Let S be a set of hosted receivers and let P_S be its coordinate projector.
Suppose, as a physical premise, the complete off-diagonal correction row of
each i in S has been implemented reciprocally on every hosted donor. Do not
infer that premise from selected coefficients or from a root identity. Then

    M_S = I + (G-I) P_S,
    rank(M_S) = 96 - |S| + rank(G_SS)
              = 96 - |S| + rank(A_S).

**Proof.** In coordinate order S,U, where U is its complement, the matrix is
[[G_SS,0],[G_US,I_U]]. The identity block eliminates G_US without changing
G_SS, proving the first rank formula. For the rational real source, a vector
x satisfies x^T A_S^T A_S x=0 precisely when A_S x=0, so the second follows.
Extension of rational matrix ranks to any characteristic-zero scalar field
preserves the statement. In particular G_US x=0 for every x in ker(G_SS).
The right kernel consists exactly of vectors supported on S whose root sum
is zero. The same formulas hold at volume V with every dimension multiplied
by V. QED.

This identifies exactly what a complete selected receiver set earns: its
root-dependence nullity, not its size alone. The existing eight receivers
B=[5,56,65,69,77,96,100,103] have G_BB=I_8 and form a root basis. Their
complete transpose rows initially have zero rank gain. For every S containing
B, however,

    rank(M_S) = 104 - |S|.

Each further **complete** hosted receiver row then lowers the reverse rank by
exactly one. A kernel basis is

    k_j = e_j - sum_{b in B} G_bj e_b,    j in S\B.

No larger physical native is supplied by this formula. Under this particular
complete-row architecture, residual dimension at most r requires
|S| >= 104-r. Eight residual dimensions require all 96 hosted rows; sixteen
require at least 88. Other partially filled matrices can have different
rank behavior, as the next section proves.

An explicit minimum algebraic residual basis is also available. Put
p_b=d_b+sum_{j in S\B} G_bj d_j. The residual outputs at selected rows are
sum_b G_ib p_b; at unselected rows they are d_i+sum_b G_ib p_b. Thus the
eight p_b plus the 96-|S| original unselected d_i span exactly the residual
row space. These are linear combinations, not physically delivered packets.
Acquiring and routing the p_b is a separate obligation.

## 2. General finite-rank update gate

Let an actually admitted residual M be invertible, and let an added literal
update have coefficient matrix UV^T with U,V each n-by-m. Then

    nullity(M+UV^T) = nullity(I_m+V^T M^{-1}U).

The correspondence is z -> -M^{-1}Uz from the right-hand kernel to the
left-hand kernel, with inverse x -> V^T x. Both are injective on the indicated
kernels: if Uz=0 and (I+V^T M^{-1}U)z=0, then z=0. Substitution proves both
directions. This is ordinary exact matrix algebra, not a new general identity;
its role here is to test source updates using the **current** residual.

The source premise must establish U,V from authentic current rows after all
earlier transformations. Reusing an old input label after it has changed is
not justified by this identity. Neither is summing separately cheap routes.

## 3. Feedback-star completion of the admitted frame

Put U=H\B, and let L be the 88-by-8 matrix with L_ib=G_ib. The committed
paired-eight residual is exactly

    M_0 = [[I_8,0],[L,I_88]].

It is invertible, with inverse [[I_8,0],[-L,I_88]]. For T contained in U,
let C be the 8-by-|T| matrix C_bt=G_bt. Add only the transpose coefficients
from receivers T back into the eight B donor rows. In block form these are
the upper-right block C E_T^T. No claim is made that any other correction
coefficient is present. The exact result is

    nullity(M_star(T)) = nullity(I_|T| - C^T C)
                       = nullity(I_|T| - G_TT).

The second identity follows because the eight B roots are an orthonormal
basis after dividing their Gram products by 8. The first follows from the
previous update gate; equivalently eliminate the I_8 block.

For a kernel parameter z with C^T C z=z, the full right kernel vector has
B part -Cz and U part LCz. Its T coordinates equal z automatically. This
description includes all U coordinates: ignoring them generally produces an
incorrect kernel certificate.

Every source t outside B has precisely four B contacts, each +/-1/2. Hence
C^T C=[1] for a single t, and one four-contact feedback star drops reverse
rank from 96 to 95. It does so with only four new forward correction terms,
not a complete 48-term forward row. This is why a complete-row requirement
cannot be promoted into a general necessary condition.

For pairwise orthogonal T, G_TT=I and the rank drop is |T|. For two distinct
nonorthogonal source roots, G_TT=[[1,g],[g,1]] with g=+/-1/2. The two-star
Schur determinant is -g^2=-1/4, so the rank returns to 96. Rank progress from
partial corrections is therefore **not monotone**. This exact counterexample
rules out the inference that individually good stars can simply be added.

Even with arbitrary additional coefficients confined to the eight B output
rows, the total added matrix has rank at most eight. Thus this fixed-output
extension class has residual rank at least 88. It cannot by itself reach an
eight-dimensional reverse residual. More output rows, a changed earlier
residual, or a different coupled implementation is required. This is a
restricted algebraic statement, not a lower bound on all shared codes.

## 4. Literal source instance and next physical gate

The companion construction uses t=0 and contacts
5:+1/2,56:-1/2,69:-1/2,100:+1/2. All five roles are hosted, not coupled.
It has an actual 77,814-operation word, complete 1,880-input prefix comparison,
unchanged common suffix and an exact rank-95 residual. Its residual right
kernel is recorded in RESULT.json and checked against actual interpreted
source rows. The other 95 directions, 4,597 forward coefficients and all
coupled duties remain.

The next constructive step is a compatible orthogonal multi-star whose four
contacts can be acquired jointly before the B routes terminate. An algebraic
G_TT=I certificate is necessary for this particular clean rank-drop pattern,
but the cohort encoder, inverse, actual reverse readings, route consumption,
owned records and full price must all be supplied. In particular a second
star must not receive fresh direct routes already consumed by the first.

All five foundational assumptions and both strict supplier requirements
remain. No complete conditional or unconditional multiplication saving is
claimed by these gates.
