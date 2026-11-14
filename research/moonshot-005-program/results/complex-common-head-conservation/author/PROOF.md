# Conservation of Gaussian head rank in the common-body H24 architecture

**Proved scoped no-go theorem for every0<t<1. No number of common-cubic native halves and permitted head queries can produce a positive recursive saving in the fixed G192/H24 common-body architecture. This is not a lower bound for arbitrary integer multiplication, arbitrary ordinary maps, or changed body/source interfaces. No new kappa.**

## 1. Exact model and dependencies

Use the actual common-cubic native half from
[COMPLEX-COMMON-CUBIC-HEAD](https://github.com/CubeJerry/integer-mult-bounds/tree/4bf5bc1f28c87fe6120bd053d8202e40b425d6fb/research/moonshot-005-program/results/complex-common-cubic-head):
\[
 N_{\sigma,\epsilon,c}
 =\begin{pmatrix}A^\sigma&cA^{\sigma+\epsilon}\\0&A^\sigma\end{pmatrix},
 \qquad \sigma,\epsilon,c\in\{-1,1\}.
 \tag{1}
\]
Its pinned physical source is the canonical eight-event control at83f65d544b43608eade0658083048ce0b615a933, Git blob8cddb0aff69b91ae648422f2cd5e77a12883ebe7. Each native half retains the paid profile[1]+[7]+[8].

The head algebra is the exact192-element one-column group G from the common-cubic and tensor-separation packages, acting by collective tensor lifts. The ordinary subgroup H has24 elements: ordinary binary translations and binary-linear head permutations. Ordinary bank encodings have coefficients in B=C[H], with arbitrary finite invertible matrix words. This includes finite linear combinations and conditional bank routing; it excludes ordinary quadratic point phases outside H.

Distinct projective group tensors are independent for every V>=6 by the exact Gram certificate, with independent analytic sufficiency V>=16. Width-dependent scalar phases are retained. A proof device may use the entire finite-dimensional *-closed algebra B without claiming its projector is a free implementable service.

Allowed paid head queries are invertible in-place calls or distinct-bank additive shears with a single Gaussian group coefficient. Count x rank-one queries, z rank-two queries of central-Z type, and w rank-two nonalternating queries. Inverses and nonzero fixed scalar coefficients are included. All R input banks are arbitrary and retained in a complete invertible endpoint. Known-zero or disposed-bank contracts require separate treatment.

Up invertible ordinary encodings, the endpoint consists of h_0 rank-zero heads, h_1 rank-one heads, h_N nonalternating rank-two heads and h_Z central-Z-type rank-two heads:
\[
 R=h_0+h_1+h_N+h_Z,\qquad H_{\rm tot}=h_1+2h_N+2h_Z.
 \tag{2}
\]
H_tot is an integer rank sum, not the subgroup H.

Dependencies are the tensor-separation/rank-component theorem, signed-permutation gate, parity-kernel proof and root's ordinary-kernel extension. Root and Worker C independently reviewed the two-sided argument before this proof was frozen. Credit @CubeJerry, retained source/compiler authors, S013 Workers B/C and root, with OpenAI assistance. Root supplied the clean all-t price argument.

## 2. Head-rank conservation

**Theorem1.** Every exact caller in the stated model using m native halves satisfies
\[
 \boxed{H_{\rm tot}\le2m+x+2z+2w.}
 \tag{3}
\]
The theorem allows every gate ordering, native orientation/sign, invertible ordinary interstage encoding in B, and both query modes. The right side counts two head directions per native and the physical Gaussian ranks of paid head queries. Algebraic difference rank is not charged as physical rank.

## 3. The signed representation inequality

The signed-permutation package gives3-dimensional representations rho_0,rho_1 agreeing on H and B. Their group-element difference ranks are0,1,2,3 on ordinary, rank-one, nonalternating rank-two, and Z-type rank-two elements. Every native half has difference rank exactly2 by its direct triangular reduction.

Difference-rank subadditivity and ordinary invariance imply
\[
 H_{\rm tot}+h_Z\le2m+x+2w+3z.
 \tag{4}
\]
Both in-place and distinct-bank shear queries have the indicated rank. This is an algebraic inequality, not a physical invoice.

## 4. Theta parity and telescoping

Define
\[
 \eta(u,\pi)=(-1)^{(u_a+u_b+u_c)/2},\qquad\theta(g)=\eta(g)g.
\]
Theta fixes B; rank-one and Z-type coefficients are odd, while ordinary and nonalternating rank-two coefficients are even.

At any sufficiently large faithful tensor width let one bank have dimension D. Write the complete invertible head word M=F_L...F_1. Use the actual-prefix/theta-suffix identity
\[
 \Delta M:=M-\theta(M)=\sum_j T_j,
\quad
 T_j=\theta(F_L)\cdots\theta(F_{j+1})
       (F_j-\theta(F_j))F_{j-1}\cdots F_1.
 \tag{5}
\]
Ordinary gates and the w even queries contribute zero terms. Nonzero term ranks are2D per native and D per odd query, so
\[
 s:=\sum_{T_j\ne0}\operatorname{rank}T_j=(2m+x+z)D.
 \tag{6}
\]
The Gaussian endpoint, including its ordinary boundary encodings, gives
\[
 \operatorname{rank}\Delta M=(h_1+h_Z)D.
 \tag{7}
\]

A native acts as identity on both kernels of its local difference: precisely its idle banks. An odd in-place query acts as identity outside its affected bank. An odd shear acts as identity on its right difference kernel when the source bank is zero, and on its left difference kernel when the destination bank is zero.

For each even query impose one extra right coordinate condition: zero affected bank for an in-place query, or zero source bank for a shear. Impose an extra left condition using the affected/destination bank. Each has rank at most D and ensures that the query acts as identity. These are deliberately stronger conditions than the kernel of its zero theta difference.

## 5. Ordinary structure of the common right kernel

Let K_r be the intersection of right kernels of all nonzero T_j. Add the w right coordinate conditions at the actual inputs of even queries, obtaining K_r^+.

For v in K_r^+, the invertible theta-suffix in(5) puts each actual odd-gate input in its local difference kernel. Every nonordinary gate therefore acts identically on that trajectory; even queries do so by their added condition. Chronological induction replaces the actual prefix by its ordinary-only prefix. Conversely, satisfying the corresponding coordinate constraints with ordinary-only prefixes implies the actual constraints by the same induction. Thus K_r^+ is exactly the kernel of a stacked matrix with entries in B.

Since B is *-closed, its orthogonal kernel projector P_r belongs to the matrix algebra over B. For example, if F is the stacked ordinary constraint matrix, the spectral projector of F^*F at zero is a polynomial in F^*F. This proves algebra membership; it does not assert a free physical projection or bounded implementation coefficients.

Let O be the product of all ordinary gates in circuit order. We have MP_r=OP_r. The right side is ordinary and has rank dim K_r^+. The rank-zero projection pi_0 is a B-bimodule map, hence
\[
 \pi_0(M)P_r=MP_r.
\]
Since rank(pi_0(M))=h_0D,
\[
 \dim K_r^+\le h_0D.
\]
Adding w constraints of rank at most D reduces dimension by at most wD. Therefore
\[
 \operatorname{codim}K_r\ge(R-h_0-w)D.
 \tag{8}
\]

## 6. The common left kernel

Let K_l be the common left kernel of the nonzero T_j. Add the w left coordinate conditions at the theta-suffix states of even queries, producing K_l^+.

If u^*T_j=0, invertibility of the actual prefix gives
\[
 u^*\theta(F_L)\cdots\theta(F_{j+1})(F_j-\theta(F_j))=0.
\]
The local left-kernel facts imply that both F_j and theta(F_j) act identically on this row state. For even queries the added destination/affected-bank condition gives the same result. Reverse chronological induction replaces the theta-suffix by its ordinary-only suffix.

Thus K_l^+ is defined by ordinary linear constraints. Its orthogonal projector P_l belongs to the same *-closed ordinary matrix algebra, and
\[
 P_l\theta(M)=P_lO.
\]
Theta fixes pi_0, so rank(pi_0(M))>=dim K_l^+. Consequently
\[
 \operatorname{codim}K_l\ge(R-h_0-w)D.
 \tag{9}
\]

For a shear the left constraint is on its destination, not its source. This reverse-time argument uses the theta-suffixes in(5), not an unmatched actual-suffix convention.

## 7. Sylvester's inequality proves conservation

Choose minimal rank factorizations T_j=X_jY_j. Concatenate the X_j horizontally and stack the Y_j vertically to obtain X,Y with XY=Delta M and inner dimension s. The rank of X is the codimension of the common left kernel; the rank of Y is the codimension of the common right kernel. Sylvester's inequality and(6)--(9) give
\[
 (h_1+h_Z)D\ge2(R-h_0-w)D-(2m+x+z)D.
\]
Because2R-2h_0-h_1=H_tot, this becomes
\[
 H_{\rm tot}-h_Z\le2m+x+2w+z.
 \tag{10}
\]
Adding(4) and(10) proves(3). QED.

The proof uses no failed finite search. It handles arbitrary counts and mixed Gaussian endpoint ranks simultaneously.

## 8. Strict failure of the complete common-body invoice

Assume m>=1 and R>=2, with the admitted common-body construction: every native stage contributes seven fresh body directions, every role receives that body operator, and all head operations commute with it. Thus m native halves and m(R-2) paid rank-seven idles make a common body of rank7m. No unpaid body sharing or interleaved noncommon recharting is assumed.

The Gaussian targets have ranks7m+r_i, with r_i in{0,1,2} and sum r_i=H_tot. For0<t<1 set[r]=r^t and d=[8]-[7], so0<d<1. Concavity gives
\[
 [7m+r_i]\le[7m]+r_i d\le m[7]+r_i d.
\]
Therefore
\[
 T_{\rm target}\le mR[7]+dH_{\rm tot}.
 \tag{11}
\]
The complete optimistic recursive price is
\[
 P=m([1]+[7]+[8])+m(R-2)[7]+x[1]+(z+w)[2]
\]
\[
 =mR[7]+(m+x)[1]+m d+(z+w)[2].
 \tag{12}
\]
Apply(3) in(11), subtract, and obtain
\[
 P-T_{\rm target}\ge(m+x)(1-d)+(z+w)([2]-2d).
 \tag{13}
\]
The first term is strictly positive because m>=1 and d<1. The second is nonnegative: decreasing increments give d<=[2]-[1]=2^t-1, and2(2^t-1)<2^t for0<t<1. Hence
\[
 \boxed{P>T_{\rm target}\quad\text{for every }0<t<1.}
\]

The failure occurs before additional ordinary work, precision, ownership, compiler constants or recursion overhead. Those costs cannot repair the invoice. The result covers mixed rank-zero/one/two heads as well as all-rank-two targets, and retains the actual native and idle prices.

## 9. Second representation control and superseded candidates

For an additional exact control, rho_2=eta*rho_1 also agrees with rho_0 on H. Its difference ranks against rho_0 are0,2,2,0 on ordinary, rank-one, nonalternating rank-two and Z-type elements. A native has difference rank4 by the same triangular calculation. Thus
\[
 2h_1+2h_N\le4m+2x+2w.
\]
This earlier necessary inequality remains valid but is not needed in the proof of(3).

The favourable hypothetical invoices for the three-half/one-query target, the mixed no-query target, the one-half/Z-plus-rank-one target and the two-half/four-role/Z-plus-rank-one target remain correct arithmetic. Conservation now shows that no exact caller within this family achieves those endpoints. Historical source proofs and price records should be preserved and linked to this scoped supersession.

The full native source is not disproved. The next constructive step must use a genuinely larger ordinary family, especially ordinary quadratic coordinate phases, a changed body-incidence pattern, a different supplier/source, or another explicit interface. The two representations do not agree on arbitrary ordinary Clifford phases. The price proof does not cover noncommon body transport.

This is not an unconditional multiplication lower bound and does not refute kappa=0.005.

## 10. Verification scope

The checker retains the exact source/group pins, verifies the second representation pair, and tests right/left ordinary-kernel constraint equivalence using the matched actual-prefix/theta-suffix convention on finite words with odd and even queries. These finite matrix controls are separated from the universal faithful-algebra, projector and concavity arguments.

Two native halves on the same pair with opposite coupling signs give diag(A^2,A^2), attaining H_tot=2m=4. This is a sharp head-conservation control; its common-body invoice still fails strictly for0<t<1. The incorrect left-source shear constraint, extra even queries, ordinary-projector scope and merely favourable arithmetic receive explicit negative controls.

No complete supplier, multiplier or new kappa is claimed.
