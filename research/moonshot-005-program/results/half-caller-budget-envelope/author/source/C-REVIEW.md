# Independent review of actual two-stage correction support

**Accepted within the precise unitary-circuit scope below. No new κ.**
The author is the root orchestrator. Worker B independently checked the
actual affine path order, all intermediate path sums, every reported
separator and collision codimension, and the universal tensor argument.
The new checker does not import or rerun the root's screen. The two reviewed
source files and all geometric dependencies are frozen under`source/`.

The expanded root proof is also pinned as`source/ROOT-PROOF.md`. The following
paragraphs independently review its new extraction/interface argument; the
support review below is unchanged. Earlier review manifests are historical
metadata only; the v3 manifest is authoritative for this package.

## 0. Ordered extraction and the actual two-query reduction

For F1=diag(D1,D1)U(a), an intermediate diag(c,I), and
F2=diag(D2,D2)L(−b), the second output's original-y coefficient is
D2(D1−bcD1a). Its vanishing forces exactly
c=b⁻¹D1a⁻¹D1⁻¹. With this c the two outputs are
D2cD1x+D2b⁻¹D1y and−D2D1a⁻¹x. The final upper shear removes x exactly
when d=D2b⁻¹D2⁻¹, giving the claimed independent endpoints after a signed
swap. This verifies both uniqueness claims within the displayed template
without any commutation assumption. The new`check_extraction.py` confirms
all independent columns for genuinely noncommuting rational2-by2 matrices,
and rejects commuting c into the wrong order or omitting d's conjugation.
The universal statement follows from the algebra, not this finite control.

For the authentic same-minus source take a=A1⁻ and b=A2⁻. The pinned
own-stage endpoint exchange gives D1(A1⁻)⁻¹D1⁻¹=Q²R1Q, so the required
c is precisely the C_st whose paths are reviewed below. Likewise
d=Q²R2Q. Put H=Q²R2, an ordinary invertible port/coordinate operation.
Preapplying H⁻¹ to a destination, applying one Q query from its unchanged
distinct source, and postapplying H gives destination += H Q source,
while preserving the arbitrary destination baseline. Therefore d uses one
head-query bank for each pair and does not require a zero role or self-query.

The second generic endpoint D2b⁻¹D1y equals Dtot b⁻¹y only because the
other-stage D1 commutes with b⁻¹. This commutation is available from the
authentic fresh-stage routes. Applying the pinned own-stage exchange to each
endpoint gives Q²RsQ Dtot on its original input. The ordinary post-adapter
(Q²Rs)⁻¹ produces Q Dtot, a genuine rank17 job on each port. The two native
calls act on all four original banks, so there are no omitted body idles.

Both first-stage selected correction banks are independently arbitrary:
the complete first source is invertible on all four independent inputs,
and projection onto its two selected outputs is surjective. A hypothetical
modular C⊕C service must therefore handle two independent whole banks. No
free copy, clean input or unproved relation between them is available.
This proves the reduction conditional on implementing and fully paying C
at that chronology. It does not construct such a service, admit a physical
complete caller, or settle finite precision/ordinary recurrence expenses.

## 1. The actual operator and path order

With the source's112-by112 real orthogonal R, actual ordinary entry routes
M_s=X_tau P_s and exit routes O_s=X_sigma P_s, define
R_s=M_s⁻¹RM_s and R′_t=O_tRO_t⁻¹. The reviewed service is

\[
C_{st}=Q^{-1}R'_tQ^2R_sQ,\qquad s=1,\ t=2.
\]

Its h,j block is the complete sum over all intermediate ports k of

\[
R_{hk}R_{kj}\,C_{q_h}^{-\otimes V}
\bigl(O_{t,h}O_{t,k}^{-1}X_{q_k}M_{s,k}^{-1}M_{s,j}\bigr)^{\otimes V}
C_{q_j}^{\otimes V}.
\]

Here the finite port coefficient R_hk R_kj is applied **once**, not once per
tensor column. The core row-map convention is(Tf)(x)=f(g_T(x)). Therefore
the written left-to-right operator factors act in that same order on the
spatial row index. In particular, O_h acts as P_h(x+sigma_h), O_k⁻¹ as
P_kx+sigma_k, the middle Q_k² as x+q_k, M_k⁻¹ as P_kx+tau_k and M_j as
P_j(x+tau_j). This reproduces the author's sequence exactly.

The independent implementation constructs P from its complete action on
the head orthonormal basis and fresh stage basis, rather than using the
author's transvection update. It composes affine matrices and independently
checks their frequency permutation/translation phase against the reversed
operator action on every Fourier basis character. An affine permutation's
phase is linear over F2, so these basis comparisons are a complete exact
identity check, not random sampling.

All1792 authentic nonzero intermediate paths survive their full grouping
as448 nonzero h,j blocks, four distinct affine cores per block, each with
coefficient±1/4. Every output port has exactly four input blocks. All path
products, including the diagonal blocks, are retained.

## 2. The universal collision-product argument

Write one core row map as F_a(x)=A_a x+b_a. The two exterior one-column
Gaussians give its four-point support

\[
S_a(x)=F_a(x)+\operatorname{span}\{A_a q_h,q_j\}.
\]

The two directions are independent for every authentic core, so each of
these four entries has magnitude1/2 before the port coefficient. For two
different paths a,c in the same block, their supports overlap exactly when

\[
(A_a+A_c)x+b_a+b_c\in
\operatorname{span}\{A_aq_h,A_cq_h,q_j\}. \tag{1}
\]

The independent checker computes the annihilator of the right-hand space,
then solves the resulting affine binary equations. This differs from the
author's rank-modulo-subspace calculation. All2688 systems are consistent
and have the exact codimension census

| Codimension | Number of path pairs |
|---:|---:|
|3|320|
|4|480|
|7|1080|
|8|168|
|9|32|
|11|608|

For a width-V spatial row x=(x_1,...,x_V), the support of one global path is
the Cartesian product of its V four-point sets. Two such products intersect
if and only if their factors intersect in **every** column. Thus a fixed
path pair with codimension c collides on exactly a fraction2^(−cV) of all
spatial rows. No independence between different path pairs is assumed.
There are four input blocks and six pairs in each, hence24 possible
collisions at a fixed output port. The union bound gives at least

\[
f_V=\max\{0,1-24\,2^{-3V}\}
\]

of its spatial rows with all four path products disjoint in every block.
This proves the author's weaker bound max(0,1−24·2^(−V)) as well. Spectator
axes multiply both numerator and denominator equally and do not change the
fraction. The claim is universal in V; finite two-column intersection checks
are controls, not its proof.

On any such good row there are four input blocks, four paths per block and
4^V entries per path, hence exactly16·4^V nonzero entries. Their magnitudes
are(1/4)·2^(−V)=2^(−V−2); their squared magnitudes sum to1. Since supports
are disjoint, neither signs nor tensor phases can cancel them. The row's
Shannon entropy is consequently2V+4 bits. The actual112 separating rows in
the author's file also agree with the independently reconstructed supports.

The negative controls reject omission of the middle Q² translation and the
stronger false assertion that every width-one spatial row separates. The
latter has an authentic block with only twelve distinct support points.

## 3. Entropy consequence and its exact restrictions

C_st is unitary: each Q is unitary, R is real orthogonal, and its M/O
conjugations are unitary coordinate monomials. Thus all bad rows still have
nonnegative probability entropy. For b independent service banks, the
normalized full-matrix entropy is at least

\[
112b f_V(2V+4).
\]

Apply Worker C's pinned full-unitary entropy theorem. Its circuit consists
only of coordinate monomials, unitary port-mixing gates and rank-r tensor
Gaussian calls. Additional zero fields must be restored exactly; the entire
operator is unitary even on hypothetical nonzero ancillary inputs. The
ordinary port-mixing entropy allowance C_port(V) must satisfy o(V). No
productive-helper credit is subtracted. Under precisely these hypotheses,

\[
V S_V+C_{\rm port}(V)\ge112b f_V(2V+4),
\qquad \liminf_{V\to\infty}S_V\ge224b.
\]

The lower bound also covers genuine joint unitary processing of the service
banks and clean ancillas. It is not a bound only for separate implementations.
For0<t<1, the paid moment is at least S_V^t by concavity, giving a cap-free
asymptotic lower bound(224b)^t. No upper limit on child rank is needed.

At t=199/200 and b=2, independent directed integer200th-root intervals give

\[
448^t\approx434.5318593803482.
\]

Even granting four rank17 productive targets, two complete actual minimal
R0 calls and only two head-query banks, the optimistic remaining allowance is

\[
448\,17^t-448(2^t+3^t+5^t+6^t)-224
\approx169.26124907630145.
\]

Therefore this two-bank unitary/o(V)-ordinary/no-helper-credit correction
class cannot fit that optimistic allowance. Further target or query costs
only reduce this allowance. The reviewed result does **not** exclude general
nonunitary ADD circuits, new paid source histories, productive-helper
interfaces, different corrections, or the independently scheduled half-plane
caller currently under investigation. Arbitrarily large ordinary mixing
budgets are also outside the theorem, as the pinned entropy proof's boundary
control demonstrates.

## 4. Reproduction and credit

Run`python -I -B check.py --output /absolute/path/RESULT.json`.
The checker authenticates every pin, imports no root verifier, and uses its
own binary matrix/nullspace calculations and fresh directed power brackets.
Normal and optimized execution give identical receipts. The mathematical
proof above supplies all-width claims; the code checks the finite source
premises and meaningful contrary controls.

Root developed the actual two-stage correction and affine support screen.
Worker C developed the full-unitary entropy theorem. Worker B independently
checked the source and tensor-collision argument, records the stronger
codimension-three fraction, and verified the consequent scope and prices.
Prepared for @CubeJerry's programme with OpenAI assistance. **No new κ.**
