# Independent proof review B: source/D tangent and rational local lift

**Accepted within the exact local interpolation scope.** The complete first-order D-coordinate calculation, the finite parameter-1 example, and the rank-one rational local family are distinct results. None establishes a valid complete source word, a fifth whole fibre, or a new multiplication constant.

Review date: 2026-11-22. Author files and the separate frozen physical audit remain unchanged.

## 1. Tangent interpretation

Each of the 44 systems has an independently variable protected \(6\times96\) source quotient \(F\). These maps need not arise from a common right coordinate change of a source bank. Write
\[
 X=[C_H,L],\qquad N=\text{a basis of }\ker X,\qquad FX=Y(T).
\]
The exact local interpolation criterion is \(Y(T)N=0\). It is sufficient because \(Xa\mapsto Y(T)a\) is then a well-defined map on \(\operatorname{im}X\), extendible to all 96 source coordinates.

For a retained section \(A_{jr}=T[O_r,I_j]\), the required local image is \(M_{jhr}A_{jr}^{-1}\). Over the dual numbers in characteristic two,
\[
 (A+\epsilon E)^{-1}=A^{-1}+\epsilon A^{-1}EA^{-1}.
\]
Thus the full first-order condition is
\[
 \dot Y_{jh}N_{jh}=0,\qquad
 \dot Y_{jhr}=M_{jhr}A_{jr}^{-1}
       \Delta T[O_r,I_j]A_{jr}^{-1},
\]
with zero derivative on the H-core columns.

The independent physical audit reconstructs the complete operator from its own local systems. Its rank is 88 on 561 visible coordinates. Therefore the compatible visible space has dimension 473, and the full phase-legal D-coordinate projection has dimension
\[
 921-88=833=360+473.
\]
The 360 coordinates are invisible in every retained section. The 833 is the dimension after eliminating source variations; it is not the dimension of the full joint source/D parameter space, which also contains source extensions vanishing on \(X\).

For every donor and retained receiver, the four parent maps stack to a \(24\times8\) matrix of rank 8. Therefore a nonzero visible section derivative changes some required quotient image. This justifies the interpretation of the 473 directions. The present B checker independently confirms all 44 stacked ranks using the earlier independent physical matrices.

No finite-lift conclusion follows from tangent dimension alone.

## 2. Square-zero sufficiency

Let \(T(t)=T+t\Delta T\), and let \(A_s+tE_s\) be each retained section. If
\[
 Q_s=A_s^{-1}E_s,\qquad Q_s^2=0,
\]
then
\[
 (A_s+tE_s)^{-1}
   =(I+tQ_s)A_s^{-1}
   =A_s^{-1}+tA_s^{-1}E_sA_s^{-1}
\]
for every parameter. Hence \(Y(t)=Y(0)+t\dot Y\) exactly. If \(\dot YN=0\), choose an extension \(\Delta FX=\dot Y\); then \(F(t)=F(0)+t\Delta F\) solves the local interpolation equations for all \(t\).

This condition concerns retained sections and local source equations. D phase ranks, other section ranks, source ranks, nonsaturation and physical source implementation remain separate requirements.

A structural sufficient subclass is \(T(t)=(I+tH)T\) with \(H^2=0\) and \(H[O_r,O_r^c]=0\) for every retained receiver. Support on \(A\times B\) for disjoint index sets \(A,B\) guarantees \(H^2=0\). Restrict allowed pairs by \(a\in O_r\Rightarrow b\in O_r\), and require early rows to use only early columns. This is a sufficient construction rule; no useful direction in this subclass is claimed.

## 3. Exact rational lift for the saved direction

The saved direction is the single-entry perturbation
\[
 \Delta T=E_{00}.
\]
It is rank one, so every section perturbation has rank at most one. Put \(Q=A^{-1}E\) and \(\lambda=\operatorname{tr}Q\). Then \(Q^2=\lambda Q\), and
\[
 (A+tE)^{-1}
 =A^{-1}+\frac{t}{1+\lambda t}A^{-1}EA^{-1},
 \qquad
 \det(A+tE)=\det(A)(1+\lambda t).
\]
These are exact identities for every nonpole parameter. The saved direction is not square-zero in every retained section, but this rank-one identity applies.

For each local system, group its receiver derivative blocks by \(\lambda\). Let \(D_\lambda\) be the full target derivative containing that group's receiver blocks and zero H columns. The B checker independently verifies
\[
 D_\lambda N=0
\]
for every group in all 44 systems. Therefore each group has an extension \(E_\lambda X=D_\lambda\), and
\[
 F(t)=F(0)+\sum_\lambda \frac{t}{1+\lambda t}E_\lambda
\]
solves the exact local source equations wherever the relevant denominators are nonzero.

The grouped test matters: tangency only says that the sum of the group residuals vanishes. Cancellation between different denominators would not justify an exact line.

The six nonzero retained-section slopes are:

| Donor | Receiver | GF64 slope |
| --- | --- | ---: |
| 0 | 9 | 29 |
| 0 | 48 | 42 |
| 32 | 9 | 55 |
| 32 | 48 | 30 |
| 35 | 9 | 9 |
| 35 | 48 | 35 |

All other retained section perturbations have slope zero.

## 4. Independent geometric and phase pole census

The B checker reconstructs the 35 D owners from the raw paid routes. It reconstructs geometric donors, receivers and section indices from the pinned root table, planes and charts, rather than accepting the author's pole list. It uses an independently written GF64 multiplication table from polynomial reduction modulo \(x^6+x+1\), fresh matrix inversion, and independent elimination.

For all 144 geometric sections it checks old rank 8, perturbation rank at most one, the identity \(Q^2=\lambda Q\), and the exact pole \(\lambda^{-1}\) when nonzero. It independently obtains the nine geometric section poles
\[
 \{2,7,21,36,37,45,48,53,60\}.
\]
At each of the nine affected section poles, direct elimination gives rank 7. These are genuine singularity controls, not just a recomputation of a list.

The early/late phase blocks have dimensions 19 and 16. The only additional phase pole is 46; the early block has rank 18 there. The upper-right phase block remains zero for the entire line. Consequently exactly
\[
 63-9-1=\boxed{53}
\]
nonzero GF64 parameters preserve every geometric D section and both phase ranks. The determinant identities prove validity at all remaining parameters without testing a candidate search list.

Every retained pole is among the geometric poles, so these same 53 parameters admit the exact local quotient interpolation proved in Section 3. This statement combines exact local source equations with valid D phases and sections. It does not assert a complete valid source word.

The checker also directly rechecks all 44 finite source equations at \(t=1\). Twelve quotient maps change, at donors 0, 32 and 35; the other 32 saved local deltas vanish.

## 5. Remaining obstruction and review coverage

The separate frozen physical audit already establishes the complete tangent operator, all 44 finite interpolation equations, all 144 section ranks at \(t=1\), and the unchanged common-response rank
\[
 32-30=2
\]
on the fixed forced four-space. The present B audit adds the independently reproduced grouped rational identities and the complete nine-plus-one pole census. It imports no executable from the new author packages.

Neither audit proves full protected source-view ranks, source nonsaturation, an executable changed source phase word, chronology, a source compiler invoice or a common fifth whole fibre. The rational family does not establish a rank-4 common response; the checked parameter-1 response still has rank 2. No response-rank claim is made for the other parameters.

The reproducible B check is:

~~~sh
python3 -I -B research/moonshot-005-program/results/bit-source-d-tangent-s032/independent-line-check-b.py --out /tmp/s032-independent-b-line
~~~

Expected status: PASS_INDEPENDENT_B_EXACT_LOCAL_RATIONAL_LINE.

Exact consumed files are bound by independent-line-review-b-pins.json. The saved receipt and section/group certificate are in independent-line-review-b-output/RESULT.json and independent-line-review-b-output/CERTIFICATE.json. The independent-review-b-manifest.json binds this review, its checker, pins and outputs. The B check reuses the earlier independently reconstructed local physical matrices; it does not claim to reconstruct those source/H matrices again.

This deterministic review performed no new direction or parameter search. The bounded follow-up stops with these explicitly scoped results.

Credit the author construction and the independent physical/compiler reviewer, with predecessor attribution unchanged. Substantial OpenAI assistance. Apache-2.0.
