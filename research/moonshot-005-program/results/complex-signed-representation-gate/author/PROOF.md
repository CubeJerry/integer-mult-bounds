# A signed-permutation rank gate for common-head callers

**Proved scoped obstruction. The three-half, one-rank-one-query and no-query mixed-head targets are impossible in the fixed collective G192/H24 algebra. A different query inventory and a larger ordinary algebra remain open. No new kappa.**

## 1. Exact source and algebraic scope

The source is [COMPLEX-COMMON-CUBIC-HEAD](https://github.com/CubeJerry/integer-mult-bounds/tree/4bf5bc1f28c87fe6120bd053d8202e40b425d6fb/research/moonshot-005-program/results/complex-common-cubic-head), starting from the canonical control at commit83f65d544b43608eade0658083048ce0b615a933, Git blob8cddb0aff69b91ae648422f2cd5e77a12883ebe7. Its common A has powers of Gaussian ranks0,1,2,2,2,1 and A^6=I. The actual half head matrix, on its two active roles, is
\[
 N_{\sigma,\epsilon,c}=
 \begin{pmatrix}A^\sigma&c A^{\sigma+\epsilon}\\0&A^\sigma\end{pmatrix},
 \quad \sigma,\epsilon,c\in\{-1,1\}.
 \tag{1}
\]
Other roles are unchanged. Fresh body factors and all required rank-seven idles remain paid as in the admitted reduction.

Use the exact192-element one-column group G=D_u P_pi from the tensor-separation package: u in(Z/4Z)^3 has even coordinate sum and pi in S3 permutes the three nonzero Walsh frequencies. Its24-element ordinary subgroup H consists of the four translation phase vectors, followed by arbitrary pi. Every group element fixes the zero-frequency vector, so there are no nontrivial scalar operators in G.

Ordinary matrices in this theorem have entries in the collective algebra C[H], with a fixed finite family of tensor operators and exact width phases. They may contain arbitrary bounded finite scalar circuits and invertible ordinary matrix encodings. The tensor-separation theorem makes the group algebra faithful for every V>=6; alternatively its independent analytic bound V>=16 suffices. Thus a claimed uniform actual-operator identity in this class implies the corresponding algebra identity. Explicit inverses, or invertibility in the faithful finite-dimensional ordinary algebra, ensure that ordinary encodings evaluate to invertible matrices below.

This scope includes finite linear combinations of the permitted ordinary translations and binary-linear head permutations, not merely one monomial per coefficient. It excludes ordinary quadratic coordinate phases outside H, arbitrary column-specific encodings, unbounded operator families, approximate endpoint limits and changed source/body interfaces. These exclusions are mathematical scope, not statements of physical impossibility.

Credit @CubeJerry, the native/compiler and caller authors, the S013 common-cubic and tensor-separation work, and root's direct triangular native-difference verification. Worker B developed this representation reduction and checker with OpenAI assistance.

## 2. Two representations agreeing on every permitted ordinary coefficient

Let T be the normal four-element subgroup of ordinary translations. The quotient is
\[
 G/T \cong (\mathbf F_2)^3\rtimes S_3.
\]
The three standard sign coordinates correspond to Q_a,Q_b,Q_c. For an explicit formula in the stored phase convention, put
\[
 e=(u_a+u_b+u_c)/2\bmod2,
\]
\[
 x=(e+u_b,\ e+u_a,\ e+u_a+u_b)\bmod2.
 \tag{2}
\]
The first two coordinates u_a,u_b in (2) are reduced modulo2. This additive map on the phase group has kernel exactly T; it sends Q_a,Q_b,Q_c to the three coordinate vectors. If z is the transposition exchanging the first two labels, the induced permutation of the sign coordinates is tau=z pi z^{-1}. This reflects that the displayed phase vector for Q_a has its zero in the second Walsh position.

Define3-dimensional representations
\[
 \rho_0(u,\pi)=P_\tau,\qquad
 \rho_1(u,\pi)=D_{(-1)^x}P_\tau.
 \tag{3}
\]
These are respectively the unsigned and signed permutation representations of the quotient. Equation(2) is compatible with the S3 action, so both are group homomorphisms. Every h in H has x=0, hence rho_0(h)=rho_1(h). They consequently agree on the whole ordinary algebra C[H].

For a group element g, define
\[
 d(g)=\operatorname{rank}_{\mathbf C}(\rho_1(g)-\rho_0(g)).
\]
The common permutation factor is invertible and the diagonal difference has one nonzero entry for each set sign bit. Therefore
\[
 d(g)=\operatorname{wt}(x).
 \tag{4}
\]
The exact census is:

| Gaussian rank | Difference rank d | Number of elements |
| --- | --- | --- |
|0|0|24|
|1|1|72|
|2, nonalternating type|2|72|
|2, central-Z type|3|24|

Here Z=A^3 has all three sign bits set. “Z type” means the double coset ZH, not that every element literally equals Z. The remaining rank-two elements form the nonalternating double coset. Their physical Gaussian rank is still two. Difference rank is a separate algebraic potential and is never charged as physical rank.

## 3. Difference rank is a caller invariant

Extend each rho_j entrywise to matrices over C[G], and put
\[
 D(M)=\operatorname{rank}(\rho_1(M)-\rho_0(M)).
\]
For compatible matrices M,N,
\[
 \rho_1(MN)-\rho_0(MN)
 =\rho_1(M)(\rho_1(N)-\rho_0(N))
  +(\rho_1(M)-\rho_0(M))\rho_0(N),
\]
so
\[
 D(MN)\le D(M)+D(N).
 \tag{5}
\]
Every ordinary matrix has D=0. Moreover, if L,R are invertible ordinary matrices, then
\[
 D(LMR)=D(M),
 \tag{6}
\]
because the two representation images of L and R are equal and invertible.

An in-place Gaussian query g on one bank has D=d(g). A distinct-bank shear query I+c g E_ij, i not equal j and c nonzero, also has D=d(g): its difference consists of one off-diagonal block c(rho_1(g)-rho_0(g)). Thus the present rank gate treats both query modes correctly. This differs from a determinant character, for which a shear has determinant one.

For independent Gaussian target jobs g_1,...,g_R, the endpoint is block diagonal up ordinary encodings and
\[
 D(\operatorname{diag}(g_1,\ldots,g_R))=\sum_j d(g_j).
 \tag{7}
\]
No original bank is silently discarded in (7).

## 4. Every native half has difference rank exactly two

Write B_j=rho_j(A^\sigma) and X=B_1-B_0. Equation(4) gives rank(X)=1.

If epsilon=-sigma, the off-diagonal coefficient in(1) is cI and its difference is zero. The native difference is diag(X,X), of rank two.

If epsilon=sigma, its difference is
\[
 K=\begin{pmatrix}
 X&c(B_1^2-B_0^2)\\0&X
 \end{pmatrix}
 =
 \begin{pmatrix}
 X&c(B_0X+XB_1)\\0&X
 \end{pmatrix}.
\]
Multiply on the left by
\[
 \begin{pmatrix}I&-cB_0\\0&I\end{pmatrix}
\]
and on the right by
\[
 \begin{pmatrix}I&-cB_1\\0&I\end{pmatrix}.
\]
The result is diag(X,X). Both multipliers are invertible, so again the native difference rank is exactly two. Idle banks add only zero difference blocks.

This direct proof covers both orientations and signs; it does not require an unproved source factorization of the off-diagonal-I half.

## 5. The universal necessary inequality and closed targets

Let a caller in the stated algebra use m native halves, q_1 rank-one Gaussian queries, q_{2,N} nonalternating rank-two queries and q_{2,Z} Z-type rank-two queries. Let its Gaussian endpoint contain h_1 rank-one jobs, h_{2,N} nonalternating rank-two jobs and h_{2,Z} Z-type rank-two jobs. Equations(5)--(7) imply
\[
 h_1+2h_{2,N}+3h_{2,Z}
 \le 2m+q_1+2q_{2,N}+3q_{2,Z}.
 \tag{8}
\]
Arbitrarily many invertible ordinary operations in C[H] do not change this inequality. Ancillary independent banks retained in the interface must be included in the endpoint; zero inputs or discarded outputs are outside the statement.

Consequences:

* Three halves and at most one rank-one query have available difference rank at most7. Four rank-two Gaussian target jobs require at least8. Thus the positive raw invoice in the common-cubic package cannot be realized within this ordinary family.
* Three halves and no query have available difference rank at most6. The mixed target(2,2,2,1) requires at least7. Its positive raw invoice is likewise excluded within this family.
* The same arithmetic excludes the corresponding m-half, m+1-role all-rank-two target with at most one rank-one query, and the no-query target with one rank-one head and all remaining heads rank two.

This is stronger than an unsuccessful finite circuit search and stronger than the determinant-character filter. It does not close the physical problem once a genuinely larger ordinary family or a different source/interface is allowed.

## 6. A changed query inventory that survives the gate

The cubic Z type has physical Gaussian rank2 but difference rank3. This discrepancy suggests a concrete different sufficient obligation rather than continuing the closed one-query design.

Use one actual native half on two of three independent roles, one rank-seven idle on the third, one rank-two query Z=A^3 and one rank-one query. Seek three nonalternating rank-two head targets. Equation(8) is then exactly saturated:
\[
 3\cdot2=2+3+1.
\]
The common body rank is7 on every role, so the three completed Gaussian target ranks would be9,9,9. Its full optimistic recursive invoice is
\[
 3[9]-\bigl(2[1]+2[7]+[8]+[2]\bigr),
 \qquad [r]=r^{199/200},
\]
and rigorous integer-root enclosure gives
\[
 0.93021754087657934343322207280\ldots>0.
 \tag{9}
\]
Both paid queries and the idle are retained in(9). All ordinary normalization, grid, finite compiler constants, strict supplier and outer assumptions remain. No head circuit achieving this interface has been constructed. The rank gate merely leaves it possible.

Alternatively, an ordinary quadratic coordinate-phase operation outside H enlarges the head algebra and invalidates the specific agreement of the two representations. Such an operation must be used in an actual uniform circuit; invoking the larger algebra alone does not prove a caller.

## 7. Verification

The standalone checker verifies both representation multiplication tables on all192 squared group pairs:73,728 exact homomorphism identities. It checks agreement on all24 ordinary elements, the complete rank/difference census, all eight native orientation/sign cases by exact triangular reduction, and all72 rank-one query types. It also verifies that the ordinary translation factors used in lambda normalization collapse identically under both representations. The mathematical rank arguments are universal; these finite checks certify the concrete group and source interface.

The changed-query price is bracketed at scale10^30 using exact200th-power comparisons. The separate LAMBDA-NORMALIZATION.md gives the actual five-operation in-place ordinary butterfly, all four source input columns, and the limitations of its compiler claim.

Status: exact fixed-algebra obstruction proved; changed-query and enlarged-ordinary constructions unresolved; no complete supplier and no new kappa.
