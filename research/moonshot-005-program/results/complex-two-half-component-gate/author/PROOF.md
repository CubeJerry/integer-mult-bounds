# A two-half rank-component obstruction and the remaining mixed-head target

**Proved within the fixed tensor/ordinary algebra. Exact favourable and unfavourable invoices are separated from source construction. No new kappa.**

## 1. Source and hypotheses

Use the actual common cubic half-source from
[COMPLEX-COMMON-CUBIC-HEAD](https://github.com/CubeJerry/integer-mult-bounds/tree/4bf5bc1f28c87fe6120bd053d8202e40b425d6fb/research/moonshot-005-program/results/complex-common-cubic-head).
Its source is the canonical eight-event control pinned at commit 83f65d544b43608eade0658083048ce0b615a933, Git blob 8cddb0aff69b91ae648422f2cd5e77a12883ebe7. After the admitted ordinary boundary permutations, a native half on two ordered independent roles has head matrix
\[
 N_{\sigma,\epsilon,c}=
 \begin{pmatrix}A^\sigma&cA^{\sigma+\epsilon}\\0&A^\sigma\end{pmatrix},
 \qquad \sigma,\epsilon\in\{-1,1\},\quad c\in\{-1,1\}.
 \tag{1}
\]
Its fresh seven-dimensional body factor multiplies both active roles. Literal inverse and sign conventions are those of the pinned source proof. Each A^{+1} or A^{-1} has Gaussian rank one; the off-diagonal coefficient has Gaussian rank zero or two.

Fix a finite phase-exact tensor Clifford algebra and an ordinary monomial subgroup H, as in the tensor-separation/rank-component theorem. Width is sufficiently large that its distinct projective tensor operators are independent, with exact scalar width phases retained. The concrete 192-element common-A group is faithful for every V>=6. Let E_r be the Gaussian-rank components, and pi_r their projections. We use only the proved ordinary-bimodule identity
\[
 \pi_r(LMR)=L\pi_r(M)R
 \tag{2}
\]
for ordinary matrices L,R. Every input bank is arbitrary and independent. Encodings are square invertible ordinary operators; no zero input, discarded bank, unpaid nonordinary coefficient, column-specific enlargement, or unrecorded owner is allowed.

For the obstruction the common body can be factored out, as in the all-body construction. The proof itself is an exact head-interface statement and does not assert that a different body-incidence scheme factors in the same way.

Credit @CubeJerry, the source/compiler authors, the retained native/caller lineage, and the S013 common-cubic and tensor-component investigations. This extension was developed by Worker B with OpenAI assistance.

## 2. Two halves with idle roles

**Theorem.** Consider two native halves, on m=2+p independent roles, with p>=1. Allow arbitrary invertible ordinary encodings before, between and after them, and allow either orientation and either sign in (1). If their endpoint is a collection of independent Gaussian head jobs with no rank-zero job, then p<=2 and at least 2p of the endpoint jobs have Gaussian rank one.

In particular, two halves on three roles cannot produce head ranks (2,2,1) without an additional nonordinary operation. Two halves on four roles cannot produce a no-rank-zero endpoint containing even one rank-two job. With more than four roles they cannot produce a no-rank-zero endpoint at all.

**Proof.** Relabel each native active pair to the first two coordinates. The relabelings are ordinary and are absorbed into the adjacent encodings. It suffices to consider
\[
 M=N_2 C N_1,\qquad
 N_j=\operatorname{diag}(N_{\sigma_j,\epsilon_j,c_j},I_p),
 \tag{3}
\]
where C is invertible ordinary. Partition into an active block of two banks and an idle block of p banks:
\[
 C=\begin{pmatrix}C_{aa}&C_{ai}\\C_{ia}&C_{ii}\end{pmatrix}.
\]
The idle-idle block of M is exactly C_{ii}. Since the assumed Gaussian target has no rank-zero component, (2) and invertibility of the outer encodings imply pi_0(M)=0. The block C_{ii} is ordinary, so C_{ii}=0.

Let D be the physical dimension of one bank at the selected permitted width. Invertibility of C now implies that C_{ai}:C^{pD}->C^{2D} is injective and C_{ia}:C^{2D}->C^{pD} is surjective. For example, a kernel vector of C_{ai}, inserted entirely in the idle input block, would lie in the kernel of C; the row assertion follows dually. Thus p<=2.

The active-idle and idle-active blocks of the rank-one component of M are
\[
 X=\operatorname{diag}(A^{\sigma_2},A^{\sigma_2})C_{ai},\qquad
 Y=C_{ia}\operatorname{diag}(A^{\sigma_1},A^{\sigma_1}).
 \tag{4}
\]
Indeed, the diagonal native coefficients lie in E_1, while their off-diagonal coefficients lie in E_0 or E_2. Ordinary multiplication preserves these components. Hence
\[
 \pi_1(M)=\begin{pmatrix}T&X\\Y&0\end{pmatrix},
 \tag{5}
\]
where X has rank pD and Y has rank pD. Its image contains the pD-dimensional subspace X(C^{pD}) in the active output block, and its projection onto the idle output block is the entire pD-dimensional idle space. Consequently rank(pi_1(M))>=2pD.

For independent Gaussian target jobs, each rank-one job contributes exactly D to the rank of its E_1 component; the other Gaussian ranks contribute zero. Ordinary invertible outer encodings preserve this matrix rank by (2). Therefore there must be at least 2p rank-one jobs. QED.

The proof allows arbitrary complex ordinary coefficients, even coefficients depending on width, as an algebraic statement. Any actual caller still owes the boundedness, uniformity and precision contracts. Enlarging the coefficient range does not evade this particular exact obstruction as long as the finite tensor algebra and ordinary subgroup assumptions remain true.

This is not a theorem about every physical ordinary map. It does not cover arbitrary non-tensor spatial encodings, unknown-zero ancillary blocks, arbitrary changes of body incidence, or approximate singular degenerations.

## 3. The paid nonordinary operation is essential

Take the two halves on the same two roles with sigma=epsilon=1 and opposite coupling signs:
\[
 N_+=\begin{pmatrix}A&A^2\\0&A\end{pmatrix},\qquad
 N_-=\begin{pmatrix}A&-A^2\\0&A\end{pmatrix}.
\]
They satisfy N_-N_+=diag(A^2,A^2). On a third role, insert one paid rank-one query Q_a between them. The exact endpoint is
\[
 \operatorname{diag}(A^2,A^2,Q_a),
 \tag{6}
\]
with ranks (2,2,1). Thus dropping the ordinary-interstage hypothesis produces an immediate counterexample to the component obstruction. The extra query is a real service and must be charged.

With common body dimension14, two native halves and two rank-seven idles cost
\[
 2[1]+4[7]+2[8],
\]
where [r]=r^{199/200}. The target (16,16,15) would have raw margin
\[
 2[16]+[15]-2[1]-4[7]-2[8]
 =0.79431153928347749126082819899\ldots>0.
 \tag{7}
\]
The theorem excludes this no-query interface. The explicit paid construction (6) costs an additional [1], changing the margin to
\[
 -0.20568846071652250873917180100\ldots<0.
 \tag{8}
\]
This cleanly separates favourable target arithmetic from an actually paid construction.

## 4. A surviving no-query four-role alternative

The two-half theorem does not settle three halves. The common-cubic caller should retain two distinct sufficient synthesis obligations.

* Three native halves, six rank-seven idles, and at most one rank-one query: seek four independent rank-two heads. The pinned common-cubic package proves the raw margin 0.4271495002708613478483948993... after the query.
* Three native halves, six rank-seven idles, and no additional query: seek three independent rank-two heads and one independent rank-one head.

The second target has full job ranks (23,23,23,22). Its exact raw margin is
\[
 3[23]+[22]-3[1]-9[7]-3[8]
 =0.44751888809952558739966322971\ldots>0.
 \tag{9}
\]
It is a legitimate remaining construction target. Neither (9) nor the preceding one-query margin constructs its head circuit or discharges the complete supplier/outer dependencies.

For this heterogeneous target, the algebraic necessary conditions are pi_0(M)=0, rank(pi_1(M)) equal to one bank dimension, and rank(pi_2(M)) equal to three bank dimensions, together with actual ordinary Gaussian endpoint factorization. The stronger condition pi_1(M)=0 belongs only to the four-rank-two target. Component ranks alone are not sufficient.

## 5. Why a missing fourth head cannot be repaired inside the one-query invoice

For the all-common-body construction, paying one rank-one query while targeting (23,23,23,22) gives the negative margin
\[
 -0.55248111190047441260033677028\ldots.
\]
There is also a limited optimistic body-allocation check. Assume precisely three native half calls, i additional rank-seven idles, three rank-two heads and one rank-one head, and final body ranks 7b_j with 0<=b_j<=3 and sum b_j=6+i. Give the mechanism any such body allocation, even one not physically realized by a caller. Its invoice is
\[
 \sum_{j=1}^{3}[7b_j+2]+[7b_4+1]
 -3([1]+[7]+[8])-i[7]-[1].
 \tag{10}
\]
Every one of these finitely many optimistic allocations is negative for every integer 0<=i<=6. The largest margin, at i=0, is attained by job ranks (9,9,16,15) and is
\[
 -0.16710951143553206112048726900\ldots.
\]
The checker encloses all150 allocations with exact integer arithmetic. This bounds only the stated incidence/counting class. A changed body-sharing mechanism or a target not of this tensor-product profile is outside (10), and needs its own full accounting.

## 6. Verification

The standalone JavaScript checker executes 128 exact group-ring controls, covering every pair of the four sigma/epsilon choices and eight independently invertible ordinary middle examples. It verifies (4) exactly and exhibits left/right inverse witnesses for both cross blocks. It also checks (6), rejection of a nonzero ordinary idle corner, and a singular-middle negative control showing why invertibility is essential.

The universal obstruction is the block-rank proof, not the finite sample. All price inequalities are rigorous enclosures: for r in the used finite set, the checker brackets r^{199/200} by integers at scale10^30 using the equivalent 200th-power comparison. Receipt intervals give both endpoints. No binary floating-point comparison decides a claimed price sign.

Status: two-half obstruction proved within its explicit algebra; three-half mixed-head and all-full-head circuits unresolved; all complete supplier, precision, compiler and foundational obligations retained; no new kappa.
