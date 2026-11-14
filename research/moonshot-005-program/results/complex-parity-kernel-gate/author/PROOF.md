# A parity-kernel obstruction at the one-native, two-query boundary

**Proved exact kernel theorem. It excludes the proposed one-half, one cubic-Z-query, one rank-one-query three-role target inside G192/H24. It does not exclude larger ordinary families or larger query inventories. No new kappa.**

## 1. Dependencies and the target being corrected

The signed-permutation package proves that a native half has difference-rank capacity2, a rank-one query has capacity1, and a cubic Z-type rank-two query has capacity3. Its proposed one-half/three-role target therefore passed that particular necessary inequality and had raw margin
0.9302175408765793434332220728... at t=199/200. The head circuit was explicitly unconstructed.

The present theorem closes that surviving target within the same fixed collective algebra. It leaves the earlier source identities, exact price enclosure and signed representation theorem valid. The status change is: “survives the signed-rank gate” does not imply “survives the parity-kernel gate.”

Retain G192, ordinary algebra B=C[H24], eventual tensor faithfulness and Gaussian-rank projection pi_0 from the companion packages. The character
\[
 \eta(u,\pi)=(-1)^{(u_a+u_b+u_c)/2}
\]
is trivial on H. It induces an algebra automorphism
\[
 \theta(g)=\eta(g)g.
 \tag{1}
\]
This is a linear automorphism of the collective group algebra, not an assertion that a free physical circuit applies theta. It fixes every permitted ordinary coefficient.

The original cubic A is theta-odd, and Z=A^3 is theta-odd. Rank-two nonalternating Gaussian elements are theta-even; Z-type rank-two elements are theta-odd. These are the verified group census, not a redefinition of physical rank.

Source: the admitted common cubic half package at4bf5bc1f28c87fe6120bd053d8202e40b425d6fb, from the canonical source blob8cddb0aff69b91ae648422f2cd5e77a12883ebe7. Credit @CubeJerry, the native/compiler and caller authors, the signed-rank and tensor-component investigations, and root's independent actual-prefix telescoping review. Developed by Worker B with OpenAI assistance.

## 2. A general saturated-difference lemma

Fix a faithful finite-dimensional representation of the algebra, with one bank having dimension D. Consider an invertible circuit
\[
 M=F_L F_{L-1}\cdots F_1
\]
on R independent banks, R>k. Ordinary gates are invertible matrices over B. There is exactly one principal nonordinary gate N and k query gates Q_1,...,Q_k; all other gates are ordinary. Assume:

1. N-theta(N) has rank kD and kernel equal to a designated idle coordinate subspace E of dimension(R-k)D. Both N and theta(N) act as the identity on E.
2. Each Q_j-theta(Q_j) has rank D. Each Q_j acts as the identity on the kernel of its local difference.
3. theta fixes every ordinary gate, and all displayed gates and their theta images are invertible.
4. The final circuit is theta-even: M=theta(M).

Let O_pre be the ordered product of the ordinary gates occurring before N, with every nonordinary gate omitted. Let E_0 be the standard injection of the idle coordinate subspace. Then
\[
 J=O_{\rm pre}^{-1}E_0
\]
is an ordinary injective map, and, with O the product of all ordinary gates in circuit order,
\[
 MJ=OJ.
 \tag{2}
\]
Consequently
\[
 \operatorname{rank}(\pi_0(M))\ge (R-k)D.
 \tag{3}
\]

**Proof.** Use the actual-prefix/theta-suffix telescoping identity
\[
 M-\theta(M)=\sum_{j=1}^L
 \theta(F_L)\cdots\theta(F_{j+1})
 (F_j-\theta(F_j))
 F_{j-1}\cdots F_1.
 \tag{4}
\]
Every ordinary term vanishes. Denote the principal term by T_N and the query terms by T_1,...,T_k. Invertibility of all prefixes and suffixes gives
\[
 \operatorname{rank}T_N=kD,\qquad \operatorname{rank}T_j=D.
\]
Since(4) is zero, T_N=-sum_j T_j. Equality in the rank upper bound implies that the k query images form a direct sum of total dimension kD. Therefore
\[
 K:=\ker T_N=\bigcap_{j=1}^k\ker T_j.
 \tag{5}
\]
This follows directly: a sum of vectors in independent image subspaces is zero only if every summand is zero.

For v in K, the actual input to each nonordinary gate lies in the kernel of that gate's local theta-difference, because the corresponding theta-suffix in(4) is invertible. By hypotheses1--2, that gate therefore acts as identity on that input. Chronological induction shows that every actual prefix, when restricted to K, equals the prefix formed by retaining only ordinary gates.

At N this gives K contained in O_pre^{-1}E. Both spaces have dimension(R-k)D, so they are equal. Hence J maps exactly onto K, and the same chronological induction through the full circuit yields(2).

The right side of(2) is ordinary and has full column rank(R-k)D. The ordinary-bimodule identity implies
\[
 \pi_0(M)J=\pi_0(MJ)=MJ.
\]
This proves(3). QED.

The argument is independent of gate ordering. Query gates may precede, follow or surround N. It uses the exact actual prefixes in(4); switching prefix conventions without changing the induction would leave a gap.

## 3. Application to one native half and two theta-odd queries

For the common cubic native half
\[
 N_{\sigma,\epsilon,c}
 =\begin{pmatrix}A^\sigma&cA^{\sigma+\epsilon}\\0&A^\sigma\end{pmatrix}
\]
on two active banks, theta negates both diagonal coefficients and fixes the off-diagonal coefficient. Thus N-theta(N) is2diag(A^\sigma,A^\sigma) on the active banks and zero on the idle banks. It has rank2D, its kernel is exactly the idle coordinate space, and N is identity there.

For an in-place query with theta-odd invertible coefficient g, the local difference is2g on its one affected bank and zero elsewhere. Its kernel consists of states whose affected bank is zero, and the query is identity on that kernel.

For a distinct-bank shear I+c g E_ij with theta-odd invertible g, the difference is2c g E_ij, of rank D. Its kernel consists of states whose source bank is zero; the shear is again identity there. A nonzero scalar c is fixed by theta.

Therefore the general lemma applies with k=2 to one native half and any two such paid queries, including one original cubic-Z rank-two query and one rank-one query. If its endpoint is theta-even,
\[
 \operatorname{rank}(\pi_0(M))\ge(R-2)D.
 \tag{6}
\]
For a complete diagonal Gaussian endpoint up invertible ordinary encodings, this means at least R-2 of the Gaussian jobs must have rank zero. A theta-even endpoint with no ordinary component is impossible whenever R>2.

## 4. Composition with the signed-rank gate

For the proposed three-role target, the signed-rank capacity is2+3+1=6. Three rank-two Gaussian jobs require at least6, and any Z-type target would increase the requirement to at least7. Thus all three target heads would have to be nonalternating rank-two jobs, which are theta-even.

Outer invertible ordinary encodings preserve theta-evenness and preserve the absence of the ordinary rank component. Consequently the target would satisfy M=theta(M) and pi_0(M)=0. Equation(6) instead forces rank(pi_0(M))>=D. This is a contradiction.

The entire one-half, one-Z-query, one-rank-one-query three-role head target is therefore disproved in the fixed G192/H24 model, for every ordering, both query modes, either native orientation/sign and arbitrary invertible ordinary interstage encodings. The favourable invoice is retained as an accounting fact but cannot certify a source in this class.

## 5. Sharpness and essential hypotheses

The lower bound on the ordinary component is attained. For example, take
\[
 N=\begin{pmatrix}A&A^2\\0&A\end{pmatrix}
\]
on the first two of three roles, put a Z query on the source role before N and a Z query on the destination role after N. Since Z is central and Z^2=I, the active endpoint is
\[
 \begin{pmatrix}AZ&A^2\\0&AZ\end{pmatrix},
\]
which is theta-even and supported on nonalternating rank-two coefficients; the third role is exactly ordinary identity. Thus pi_0 has rank exactly D. This is a component sharpness example, not an assertion that the active block is already two independent Gaussian jobs.

If one additionally applies a theta-even nonordinary Gaussian AZ on the idle role, the ordinary component can disappear. That additional operation does not act as identity on the kernel of its zero local theta-difference. This is a negative control showing why uncounted theta-even nonordinary services are excluded from hypothesis2.

Singular ordinary encodings, omitted original inputs, a growing/nonfaithful operator family, approximate singular degenerations and an ordinary subgroup not fixed by theta also invalidate specific hypotheses. They are not covertly covered.

All boundary maps, scratch and input domains must be included in an actual larger construction. An independent helper bank that must be restored is not automatically a loophole: equation(3) gives an explicit dimensional requirement on the complete ordinary endpoint component. A changed zero-input or disposal contract requires a separate analysis.

## 6. Next constructive interface

The current exact positive-price targets are now closed within H24. A substantive continuation must change a premise, for example by using explicitly implemented ordinary quadratic coordinate phases that enlarge the Clifford head algebra, by changing the source/body interface, or by constructing a larger paid query architecture with a genuinely different complete budget.

The theorem does not claim every larger query architecture is impossible. It only settles the saturated one-principal-gate/two-query configuration and its stated application.

No complete multiplier, strict supplier or new kappa has been established.
