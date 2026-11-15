# An exact quadratic-phase pentagonal native head

**Proved source/interface theorem.** An explicit ordinary quadratic coordinate phase gauges the actual canonical complex native into a common head of order five. The gauge is uniform at every tensor width, preserves all four independent input columns, and adds exactly three ordinary coordinate-permutation services and three unit-phase passes per native half. The cyclic algebra is faithful at every width at least two. The old parity involution cannot extend while fixing this enlarged ordinary family. **This is not a completed caller or supplier. No new kappa.**

## 1. Source, quantifiers and provenance

The pinned input is `results/quadratic-sign-query-gate/author/PROOF.md`, Git blob `8cddb0aff69b91ae648422f2cd5e77a12883ebe7`, SHA-256 `1bc214b889a5d9ecee6fa887966dd828a4aeee95b5584379e5d249d9ceddea01`, present at programme baseline `9fb0a34adad2f5903d3169fee7f7a7fcb6f03e3a`. Its literal eight-event native has no owners and two independent halves, each with MOVE ranks 1, 7 and 8, one ADD, and exact equations

\[
 X'=FQ_bX,\quad Y'=FQ_aY+FX,\quad
 U'=FQ_bU-FQ_aQ_bV,\quad V'=FQ_aV.                 \tag{1}
\]

Here the heads are independent binary axes a,b, F is the fresh seven-axis body, and Q_w=C_w^(tensor V), where C_w=((1+i)I+(1-i)X_w)/2. The inverse is the literal reversed source. The published common-cubic source, tensor-component lemma and common-head conservation theorem remain valid predecessors in their stated classes.

Fix any integer V>=1, any permitted finite ambient dimension containing the heads and fresh body, and arbitrary independent complex input fields. Every new operator acts on the two head coordinates in every column and fixes every body coordinate. Field-level sums in (1) remain field-level sums; they are never tensor-powered.

Credit @CubeJerry, the native/compiler and caller authors, and the S013 source, phase and obstruction investigations. Worker B developed this S014 source with substantial OpenAI assistance. Independent reviews are separate artifacts. No original full120-to-control equivalence is assumed.

## 2. Three explicit ordinary monomials

Order one-column head coordinates by j=u+2v, for u,v in F2. Write C_a,C_b for the one-column Gaussian matrices. Let

\[
 P|u,v\rangle=|u+v,u\rangle,\quad
 D_{CZ}|u,v\rangle=(-1)^{uv}|u,v\rangle,\quad S=D_{CZ}P.
\]

P is a binary-linear coordinate permutation and D_CZ is a pointwise sign, so both are ordinary. In input-coordinate notation, S|u,v>=(-1)^(u+uv)|u+v,u>. A direct four-coordinate calculation gives

\[
 R:=C_a^{-1}SC_bS,\qquad
 R|u,v\rangle=(-i)^{u+v}|u,u+v\rangle,            \tag{2}
\]

where u+v in the exponent is the binary sum represented by 0 or 1. Thus R is an explicit ordinary monomial; its implementation does not evaluate the Gaussian expression on the left.

Use the actual boundary operators

\[
 G_1=iS,\qquad G_2=-R,\qquad H_2=-iS^{-1}.        \tag{3}
\]

Each table row means M e_j=i^(q_j) e_(p(j)).

| Boundary service | p(0),p(1),p(2),p(3) | q_0,q_1,q_2,q_3 modulo 4 |
|---|---|---|
| G_1, before first role | 0, 3, 1, 2 | 1, 3, 1, 1 |
| G_2, before second role | 0, 3, 2, 1 | 2, 1, 1, 2 |
| H_2, after second role | 0, 2, 3, 1 | 3, 3, 3, 1 |

The constants i,-1,-i in (3) are **one-column** factors. At width V they become i^V,(-1)^V,(-i)^V. The tensor lift of these tables includes them automatically. Substituting a width-independent scalar is incorrect.

## 3. The order-five head

Define B=i C_b S and B_V=B^(tensor V). Its exact one-column matrix is

\[
 2B=\begin{pmatrix}
 -1+i&0&0&1+i\\
 0&-1-i&-1+i&0\\
 1+i&0&0&-1+i\\
 0&1-i&1+i&0
 \end{pmatrix}.                                  \tag{4}
\]

Direct multiplication proves

\[
 B^5=I,\quad B^*=B^4,\quad
 \operatorname{tr}(B^k)=-1\ (1\le k\le4).         \tag{5}
\]

A short rank witness is

\[
 2B^2=\begin{pmatrix}
 -i&1&i&-1\\
 -1&i&1&-i\\
 -1&i&-1&i\\
 i&-1&i&-1
 \end{pmatrix}.                                  \tag{6}
\]

Every row of B has two entries of magnitude 2^(-1/2); every row of B^2 has four entries of magnitude 1/2. B is a product of a Gaussian Clifford map and ordinary monomial Clifford maps, so these are Gaussian ranks one and two in the retained Gaussian contract. Inverses have the same ranks. Therefore

\[
 r(B^k)=(0,1,2,2,1)\ (k=0,1,2,3,4),\qquad
 r(B_V^k)=V r(B^k).                              \tag{7}
\]

Actual monomial adapters remain owed when a power is supplied as an independent query; (7) does not provide those queries for free. The unnormalized A=C_bS has A^5=-iI. The factor i in B removes that central phase exactly, since i^5(-i)=1.

## 4. Exact gauge of every native input column

Before (1), apply G_1^(tensor V) to X,U and G_2^(tensor V) to Y,V. After (1), apply H_2^(tensor V) to Y,V. No boundary operator follows the first role of either half. The exact full result is

\[
 \boxed{\begin{aligned}
 X'&=FB_VX,&Y'&=F(X+B_VY),\\
 U'&=F(B_VU-B_V^2V),&V'&=FB_VV.
 \end{aligned}}                                  \tag{8}
\]

**Proof.** Put A=C_bS. The individual one-column coefficient identities are

\[
 C_bG_1=iA=B,\quad H_2G_1=I,\quad
 H_2C_aG_2=iS^{-1}C_aR=iA=B.
\]

For the upper cross coefficient, commuting C_a,C_b and using (2) gives

\[
 C_aC_bG_2=-C_aC_bR=-(C_bS)^2=-A^2=B^2.
\]

Tensor products preserve these multiplicative coefficient products. The upper native minus remains a field-level scalar outside the tensor: its coefficient is -(C_a C_b G_2)^(tensor V)=-B_V^2, not (-B^2)^(tensor V). All head maps commute with the fresh disjoint F. Every input remains arbitrary and independent; no column is set to zero or discarded. QED.

Each half is a literal independently callable half of the real source with its own boundary services. This is an actual source construction, beyond declaring a larger allowed algebra.

## 5. Inverses and the complete half inventory

Write the head-only halves as

\[
 L_B=\begin{pmatrix}B&0\\I&B\end{pmatrix},\qquad
 U_B=\begin{pmatrix}B&-B^2\\0&B\end{pmatrix}.
\]

Their exact inverses are

\[
 L_B^{-1}=\begin{pmatrix}B^{-1}&0\\-B^{-2}&B^{-1}\end{pmatrix},\qquad
 U_B^{-1}=\begin{pmatrix}B^{-1}&I\\0&B^{-1}\end{pmatrix}. \tag{9}
\]

Literal inversion has body F^-1. Applying ordinary translation F^2 to **both** roles restores positive body F, costing two ordinary body translations. Rebinding the ordered pair and conjugating one role by a sign supplies

\[
 N_{\sigma,\epsilon,c}
 =\begin{pmatrix}B_V^\sigma&cB_V^{\sigma+\epsilon}\\0&B_V^\sigma\end{pmatrix},
 \quad\sigma,\epsilon,c\in\{-1,1\}.              \tag{10}
\]

The lower forward source gives (sigma,epsilon)=(1,-1) after exchanging role names; the upper forward source gives (1,1). The inverse upper and lower give (-1,1) and (-1,-1). Sign conjugations and physical bank swaps remain ordinary services. Equation (10) has the useful formal shape of the old common cubic, now with B_V^5=I and rank pattern (7).

## 6. Uniform ordinary implementation and all added expenses

Let D be the number of scalar coordinates of a field. Implement each monomial in (3) by one pointwise unit-phase pass followed by its tensor coordinate permutation. A forward half adds exactly three ordinary coordinate-permutation services and three phase passes, with at most 3D applications of a scalar in {1,-1,i,-i}. It adds no field ADD, owned or copied field, erasure or Gaussian call. The original one ADD and MOVE ranks 1,7,8 remain.

Inverse gauges have the same three-service cost; positive-body inversion additionally needs the two F^2 translations above. A destination sign conjugation uses two sign passes if separate. Sign and swap costs are not silently credited to the Gaussian invoice.

The phase schedule is uniform. The tensor phase is the sum modulo four of the displayed column phases. Enumerate the array's fixed finite column alphabet with an odometer, maintaining that two-bit sum. Each digit update changes it by a fixed table difference. Across K^V coordinates for fixed K>=4, fewer than K/(K-1) K^V <= 4K^V/3 digit updates occur. A tape odometer returning along its carry path still uses a constant multiple of this count. The description uses three fixed tables and O(V) control storage. Unused body symbols have phase zero. Thus phase **generation** has linear combinatorial cost, without an uncharged V-step dot product per scalar coordinate.

The unit phases are exact sign changes or real/imaginary swaps on a Gaussian fixed-point grid. They add no denominator factor, have norm one and add no local numerical amplification. The permutations also have norm one. The fixed coefficient catalogue and inverses are independent of V.

**Accounting boundary.** All three coordinate permutations require the retained ordinary compiler's descriptor, traversal, tape/layout and bit work. Keep their charges Pi_1(D,V)+Pi_2(D,V)+Pi_3(D,V) explicitly, together with the phase passes/control work. This theorem supplies uniform finite monomial instructions; it does not discharge the compiler foundation, waive nonlocal tape movement, or supply a new complete precision certificate. A completed caller must instantiate these costs in its full supplier threshold.

The Gaussian half tariff remains h_t=1+7^t+8^t. With m stages on R roles, making bodies common still costs m(R-2) rank-seven idles. Every independent rank-one/rank-two query and every ordinary boundary/interstage service must be charged. The gauge itself has not added a target job or proved a positive saving.

## 7. The cyclic algebra is faithful at every V >= 2

At one column, the character (4,-1,-1,-1,-1) in (5) gives precisely the four nontrivial fifth roots as eigenvalues, once each. At width V, traces are 4^V at the identity and (-1)^V at each other power. Fourier inversion gives multiplicities

\[
 m_0(V)=\frac{4^V+4(-1)^V}{5},\qquad
 m_1(V)=\frac{4^V-(-1)^V}{5}                      \tag{11}
\]

for the trivial character and each nontrivial character, respectively. Both are positive for all V>=2. Hence the minimal polynomial is exactly z^5-1, and I,B_V,B_V^2,B_V^3,B_V^4 are linearly independent, even with arbitrary width-dependent scalar coefficients. A fixed caller using only scalar ordinary role matrices and powers of B_V must therefore be checked in C[z]/(z^5-1). This is an exact all-width reduction for V>=2.

The tempting one-column identity I+B+B^2+B^3+B^4=0 **does not tensor**. At V=2, that sum is five times a rank-four projector. The verifier checks trace 20 and S^2=5S. A caller using the one-column cyclotomic relation fails uniformity.

## 8. Why the old parity proof cannot extend unchanged

G192 has no projective element of order five, since five does not divide 192. The new head genuinely lies outside that group, including up to scalar. D_CZ is also outside the old ordinary algebra C[H24]: every H24 permutation preserves the constant vector, every linear combination maps it to a scalar constant vector, and D_CZ maps it to a nonconstant sign vector. This holds at every tensor width.

More strongly, there is no complex-algebra automorphism extending the old parity, fixing the enlarged ordinary maps and sending Q_b to -Q_b. Such an automorphism would send B_V=i^V Q_b S^(tensor V) to -B_V. But theta(B_V^5)=I while theta(B_V)^5=(-B_V)^5=-I, a contradiction. The specific parity mechanism in the old conservation proof is therefore unavailable here. This does not disprove conservation by a different argument, prove a profitable caller, or invalidate the old theorem within H24.

## 9. Open next questions

The next requirement is an exact caller retaining all original inputs. Candidate common-body inventories include three native halves and at most one rank-one query on four roles, and one native half with one rank-one and one rank-two query on three roles. These inventories are only proposals; their endpoints need actual construction before their arithmetic matters.

The faithful C5 reduction supplies a small exact screen for scalar ordinary interstage matrices. A broader construction may use genuinely noncommuting monomial phase services; a scalar C5 obstruction must not be overextended to them. Exact caller synthesis, ordinary/precision/layout costs, strict uniform complex admission and BIT/outer compatibility remain open. All five foundational assumptions remain retained.

## 10. Reproduction and classification

Run from the repository root:

```sh
python3 research/moonshot-005-program/work-in-progress/2026-11-15-S014/worker-b/check.py --repo .
```

The author verifier uses Python integer Gaussian-dyadic arithmetic only. It pins the source bytes and checks the monomials, both halves and all four independent input columns at widths 1,2,3, inverses, orders, rank pattern and phase/projector controls. The all-width conclusion follows from the written tensor and character proofs, not those three tests. Negative controls remove the quadratic phase, width scalar, output gauge or second input gauge, and reject tensoring the one-column cyclotomic relation. Independent admission remains a separate gate. No new complete kappa.
