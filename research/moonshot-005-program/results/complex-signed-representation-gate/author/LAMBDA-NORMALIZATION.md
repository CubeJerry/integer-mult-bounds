# An explicit ordinary involution normalization of the two-head source

**Proved exact source identity and finite in-place scalar implementation. The resulting dihedral caller class is closed by the signed-permutation gate. This normalization remains a source tool for larger interfaces. No new kappa.**

## 1. Operators and actual ordinary service

Let Q_v=C_v^{tensor V} be the collective Gaussian in the pinned canonical source. Its square T_v=Q_v^2 is the ordinary coordinate translation X_v^{tensor V}, an involution. Put
\[
 \alpha=(1+i)/2,\quad \beta=(1-i)/2,\qquad
 \lambda_v=\alpha I+\beta T_v.
\]
The two translation eigenspaces show
\[
 \lambda_v^2=T_v,\quad
 \lambda_v^*\lambda_v=I,\quad
 S_v=\lambda_v Q_v^{-1},\quad S_v^2=I,\quad Q_v=\lambda_v S_v.
 \tag{1}
\]
The lambda operators commute with all Q_a,Q_b and with the fresh body operators. These are field-level linear combinations of collective ordinary translations; lambda is not silently substituted by a tensor power of a one-column phase.

A polynomial in an ordinary permutation is not automatically a pointwise scalar instruction. Here is the complete local implementation. Partition the coordinate indices into the disjoint two-cycles of T_v, and call their current values u,v. Apply the following five in-place scalar operations in order:

1. u <- u-v.
2. u <- ((1-i)/2)u.
3. v <- v+u.
4. u <- (-1+i)u.
5. u <- u+v.

The resulting pair is
\[
 (u',v')=(\alpha u_{\rm old}+\beta v_{\rm old},
          \beta u_{\rm old}+\alpha v_{\rm old}).
\]
This is exactly lambda_v. There is no auxiliary scalar, no copied field, no erased owner and no original-value query after overwrite. The inverse is the reversed word with inverse scales and opposite additions. The two scale inverses are fixed Gaussian-dyadic numbers (1+i) and(-1-i)/2. Thus every translation pair uses exactly three scalar ADD/SUB operations and two in-place SCALE operations.

The coefficient catalogue is fixed before V varies. One service adds at most one factor2 to the rational denominator grid. Each elementary shear has operator norm less than2, and the two scale norms are at most1 and sqrt2 respectively; every local forward or inverse prefix has norm less than8sqrt2<12. These deliberately conservative constants suffice to show boundedness, not to replace the pinned compiler's complete constants.

For a field with D coordinates there are D/2 pairs. The scalar count is3D/2 ADD/SUB and D SCALE. If the current tape/layout does not expose the paired coordinates directly, retain one explicit ordinary pairing permutation and its inverse. Their descriptor, traversal and tape/bit work are inherited ordinary-compiler obligations; they are not removed by the scalar count. No claim that arbitrary nonlocal access is free is made.

## 2. Literal four-input source normalization

The published canonical source has four arbitrary independent inputs and physical coefficient map
\[
 X'=FQ_bX,\quad Y'=FQ_aY+FX,
\]
\[
 U'=FQ_bU-FQ_aQ_bV,\quad V'=FQ_aV.
 \tag{2}
\]
Here F is the fresh rank-seven body factor. It commutes with every head operation used below.

Before(2), apply lambda_a to X and U. After(2), apply lambda_a^{-1}lambda_b^{-1} to X and U, and lambda_a^{-1} to Y and V. The exact result is
\[
 X'=FS_bX,\quad Y'=FS_aY+FX,
\]
\[
 U'=FS_bU-FS_aS_bV,\quad V'=FS_aV.
 \tag{3}
\]
For example, the upper cross coefficient is
\[
 -\lambda_a^{-1}\lambda_b^{-1}Q_aQ_b=-S_aS_b,
\]
while the lower cross coefficient is lambda_a^{-1}lambda_a=I. All four arbitrary input columns are retained.

The checker performs this composition in the exact complex group algebra, with a common integer denominator8; it does not verify only a selected input or a point specialization.

There are eight lambda services for the full four-input control, four for each independent half. Thus, per half, the displayed implementation adds6D scalar ADD/SUB operations and4D scalar SCALE operations. A conservative separate-layout implementation uses at most eight ordinary pairing/unpairing permutations per half. The compiler must include them and the fixed coefficient/grid/prefix constants. No Gaussian-rank MOVE or owned field is added, but the ordinary work is real.

## 3. Common order-four head

Let P be the ordinary binary coordinate swap a<->b, fixing the body. It interchanges lambda_a,lambda_b and S_a,S_b. Define
\[
 A=S_bP.
\]
Then
\[
 A^2=S_bS_a,\qquad A^4=I.
 \tag{4}
\]
A is a rank-one Gaussian up explicitly ordinary operations; A^2 is a rank-two Gaussian up the ordinary lambda factors.

Apply P before(3) on Y,V and after(3) on X,U. The common source becomes
\[
 X'=FA^{-1}X,\qquad Y'=F(A^{-1}Y+X),
\]
\[
 U'=F(A^{-1}U-A^{-2}V),\qquad V'=FA^{-1}V.
 \tag{5}
\]
There are two additional ordinary swap permutations per half. The body remains positive in the literal forward service. Literal inverse and the existing ordinary F^2 correction give the opposite baseline orientation under the same accounting.

Equations(4)--(5) give a genuine reduction to commuting involutions S_a,S_b with an ordinary swap, algebraically a dihedral model. They do not produce a completed caller.

## 4. Why this simplification does not certify the old target

The lambda operators belong to C[H24]. Under both signed-permutation representations in the companion proof, every square Q_v^2 maps to I, so lambda_v maps to alpha+beta=1. Hence the ordinary normalization does not change their difference-rank bound.

The three-half/four-rank-two target with one rank-one query, and the three-half no-query(2,2,2,1) target, remain excluded when all ordinary operations stay in that collective algebra. The involution normalization does not spend a saving and does not enlarge the accepted ordinary class by itself.

It may be used in a genuinely larger ordinary source/caller, or in another query inventory, provided the actual construction and full cost are proved. The proposed one-half/three-role target in the companion proof instead uses the original cubic Z=A_cubic^3, whose difference rank is three; it must not be confused with this normalized order-four A^2, whose difference rank is two.

## 5. Compiler and verification status

The source and scalar identities are exact. The five-step butterfly has a fixed Gaussian-dyadic catalogue, a reversible in-place transcript, bounded prefixes and an explicit constant grid multiplier. These satisfy the kind of fixed-data requirement in the retained specialization/precompilation framework; they are not a new proof of that framework or a new complete precision certificate.

The checker verifies the butterfly as Gaussian-integer2 by2 matrices divided by2, its square as translation, its unitarity, all four source columns, the two-sided A inverse, A^2=S_aS_b, A^4=I and the common swap-gauged source. The exact ordinary layout/tape compilation and the updated finite supplier threshold must still be charged if this source is used in a future completed caller.

Source provenance is the same canonical control and common-cubic package as the companion proof. Credit @CubeJerry, the native/compiler authors and S012's collective lambda mechanism, which motivated this explicit two-head normalization, with S013/OpenAI assistance. No new kappa.
