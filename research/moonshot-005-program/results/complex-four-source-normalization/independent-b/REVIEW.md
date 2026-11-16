# Independent review of the four nonlinear source classes

**Accepted as an exact algebraic and source-word reduction. No caller or κ claim.** This review independently derives the root's Boolean conjugacy classification and symbolic source sign bridge. It uses a separate Gaussian-integer numerator implementation for all finite checks and does not import the source-family author's matrix helper.

## 1. Direct normalization and exact witnesses

Use `P(a,b,c)=(b,c,a)`, `A_f=C_b D_fP`, and the Boolean expansion
`f=f0+ℓ_a a+ℓ_b b+ℓ_c c+q_ab ab+q_ac ac+q_bc bc+abc`.
A diagonal sign `Z_q` with q independent of b commutes with C_b. Consequently

\[
 Z_q A_f Z_q^{-1}=A_{f+q+q\circ P^{-1}}.
\]

The choices q=a,c,ac toggle respectively (ℓ_a,ℓ_c), (ℓ_b,ℓ_c), and (q_ac,q_bc). With

\[
 q_1=\ell_a a+\ell_b c+q_{ac}ac,
\]

the resulting function is `f0+L c+A ab+B bc+abc`, where
`L=ℓ_a+ℓ_b+ℓ_c`, `A=q_ab`, and `B=q_ac+q_bc`.

The simultaneous bit complement X=X_aX_bX_c commutes with both C_b and P, so it sends f to f(x+111). For this normalized function, complement followed by the same diagonal normalization sends

\[
 (f_0,A,L,B)\mapsto(f_0+J+B+1,A+1,L+1,B),\qquad J=A+L.
\]

Apply this step precisely when A=1. The final polynomial is

\[
 f_{C,J,B}=C+Jc+Bbc+abc,
 \qquad C=f_0+A(J+B+1).
\]

This gives an explicit monomial conjugator. If A=0 take T=Z_q1. If A=1, after complement the additional normalization is q2=Bc+ac, so take `T=Z_q2 X Z_q1`. These literal sign/permutation tables satisfy

\[
 T A_f T^{-1}=(-1)^C A_{J,B},\qquad A_{J,B}=C_bD_{Jc+Bbc+abc}P.
\]

The four C=0 masks are128,64,112,176 in order (J,B)=(0,0),(0,1),(1,0),(1,1). All128 odd truth tables are covered. Each T is an actual ordinary affine/quadratic monomial, and its inverse must be paid in the direction used by the caller.

## 2. Projective and exact separation at every tensor width

The four representative pairs `(tr A,e₂(A))` are

| Mask | tr A | e₂(A) |
| --- | --- | --- |
|128|0|0|
|64|1+i|i|
|112|1+i|0|
|176|0|−i|

where `e₂(M)=((tr M)²−tr(M²))/2`. Their zero patterns distinguish projective similarity: multiplication of a matrix by a nonzero scalar scales the two quantities by λ and λ² and cannot change zero status.

For any positive integer V,

\[
 \operatorname{tr}(A^{\otimes V})=(\operatorname{tr}A)^V,
\quad
 e_2(A^{\otimes V})=
 \frac{(\operatorname{tr}A)^{2V}-(\operatorname{tr}A^2)^V}{2}.
\]

This is sufficient here without an unstated noncancellation premise. For mask64, tr(A²)=0, so both quantities remain nonzero. For mask112, tr(A²)=(tr A)², so only e₂ remains zero. For mask176, tr A=0 but tr(A²)=2i, so only the trace remains zero. Both vanish for mask128. Hence the four classes remain projectively nonsimilar at every width, even under arbitrary complex similarity, not merely monomial similarity.

The sign C tensor-lifts to `(-1)^(CV)`. At even V the two exact signs coincide. At odd V their traces of cubes have opposite nonzero values, because every odd-table source has nonzero tr(A³) by the source-family trace formula. Thus there are exactly eight exact conjugacy classes among the128 sources at odd widths and four at even widths, under the explicit ordinary monomial witnesses. There cannot be fewer classes even under arbitrary similarity by these invariants.

## 3. The native bank word sign bridge is exact

Write

\[
 K(a)=\begin{pmatrix}1&0&a-1\\a&0&-a\\1&1&-1\end{pmatrix},
\quad
 B=\begin{pmatrix}1&0&-1\\0&0&1\\1&1&-1\end{pmatrix}.
\]

Then K(a)=F(a)B for `F(a)=[[1,a,0],[a,0,0],[0,0,1]]`. For a central scalar λ with λ²=1, let `Dλ=diag(1,λ,1)`. Since `F(λa)=Dλ F(a)Dλ`,

\[
 K(\lambda a)=D_\lambda K(a)E_\lambda,
\quad
 E_\lambda=B^{-1}D_\lambda B
 =\begin{pmatrix}1&0&\lambda-1\\0&1&0\\0&0&\lambda\end{pmatrix}.
\]

This is an identity over the free one-generator polynomial algebra and holds for every operator a and every tensor width; it does not depend on a's spectrum or commutativity with anything else. Eλ is an involution. For λ=−1, a literal unit-ADD implementation applies `x←x−z` twice and then `z←−z`; Dλ changes the sign of the middle bank. Thus the conservative additional cost is two ordinary ADDs and two SCALE(−1) passes. A convention allowing one coefficient−2 shear may use that equivalent macro, but its cost must be declared. There is no Gaussian call, added owner, input overwrite or erasure.

Conjugating all three banks by T and applying this sign bridge reduces a caller built on any odd f to one of the four representatives. The actual source and target monomial wrappers, field signs, shear operations, body/idles, precision and recursive costs remain. The Gaussian profile and native count are preserved, but no complete supplier tariff or bound follows automatically.

## 4. Independent finite evidence

`check.py` constructs all128 A_f directly as Gaussian-integer matrices with common denominator2, computes T from Boolean coefficients, and checks the exact conjugacy on all64 entries. It verifies the spectral table using integer numerator products, all-width separation formulas on V=1,…,8 as finite controls, and the universal K sign identity by independent polynomial matrix multiplication. Negative controls omit the complement or a quadratic gauge, drop the odd-width global minus, and replace the required−2 shear by−1. These controls supplement the proofs above.

Prepared by @CubeJerry with substantial OpenAI assistance. Independent AI algebra review, not independent human or proof-kernel acceptance. **No new κ.**
