# Tensor separation and a finite Gaussian-rank component gate

**Proved algebraic reduction, with exact finite verification for a 192-element common-head group. This is not a caller impossibility theorem or a multiplication bound. No new kappa.**

## 1. Purpose and source

The common cubic control in the S013 programme has a fixed head operator A=Q_b^{-1}P, where P cyclically permutes a,b,a+b and each Q_v is a collective tensor Gaussian. Three half calls and one rank-one head query have a positive optimistic four-role invoice, but the arbitrary-input head circuit remains open. The present result makes one necessary endpoint condition into a finite exact linear-algebra problem. It also prevents a false one-column simplification: a collective tensor Gaussian is not the same linear combination of collective ordinary maps as its one-column factor.

The source is the canonical eight-event control, Section 1 of
[the committed quadratic-sign query proof](https://github.com/CubeJerry/integer-mult-bounds/blob/83f65d544b43608eade0658083048ce0b615a933/research/moonshot-005-program/results/quadratic-sign-query-gate/author/PROOF.md), Git blob 8cddb0aff69b91ae648422f2cd5e77a12883ebe7. The common-cubic interface proof is transferred in Git blob 04bbc16a5076cb2306c3f98aa1ecf171da1d6d01; root integration supplies its permanent programme path. Neither this proof nor its checker imports a claimed full120 moving-gauge equivalence.

Credit @CubeJerry, the retained source/compiler and caller authors, and the S013 common-cubic investigation. This extension was developed by Worker B with OpenAI assistance. All statements below concern complex linear operators, prior to the separate physical precision, restoration, compilation and recursive accounting gates.

## 2. Eventual tensor independence, including scalar phases

**Theorem 1.** Let U_1,...,U_m be a fixed finite set of d by d unitary matrices, no two proportional. Define
\[
 c=\max_{i\ne j}|\operatorname{tr}(U_i^*U_j)|/d<1.
\]
For every positive integer V satisfying (m-1)c^V<1, the m operators U_j^{\otimes V} are linearly independent over C.

**Proof.** The strict inequality c<1 follows from equality in the Hilbert--Schmidt Cauchy--Schwarz inequality: two unitary matrices have inner product of modulus d only when proportional. The normalized Gram matrix of their tensor powers has diagonal entries 1 and off-diagonal entries
\[
 (\operatorname{tr}(U_i^*U_j)/d)^V.
\]
For any vector z, the absolute value of the off-diagonal part of z^*Gz is at most (m-1)c^V times the squared Euclidean norm of z, by 2|z_i z_j|<=|z_i|^2+|z_j|^2. Thus G is positive definite. This proves independence. The one-element case is immediate. QED.

This theorem allows arbitrary complex scalar coefficients at each fixed V. In particular, coefficients may depend on V; independence does not require a coefficient bound. A circuit application must nevertheless retain its own uniformity, encoding-size and physical scalar-operation contracts. The finite one-column operator family must be fixed independently of V. A family growing with V, arbitrary column-specific maps, or an unbounded number of different tensor factors is not covered by this conclusion.

Here is a phase-exact group formulation. Let G be a finite unitary group with scalar subgroup consisting of roots of unity of orders dividing L. Choose one representative U_j for each projective class. If
\[
 U_iU_j=\zeta_{ij}U_{k(i,j)},\qquad \zeta_{ij}^L=1,
\]
then for V congruent to rho modulo L, use the twisted algebra with basis e_j and multiplication
\[
 e_i e_j=\zeta_{ij}^{\,\rho}e_{k(i,j)}.
\]
The homomorphism e_j -> U_j^{\otimes V} is faithful for all sufficiently large V by Theorem 1. The scalar cocycle is not omitted: actual factors are \zeta_{ij}^V, which can differ on different width residues. A fixed uniform circuit must be checked on every permitted residue, or carry these factors symbolically. An ordinary phase correction may be used only when the corresponding physical operation is actually available and charged.

For a fixed bounded circuit, it is also enough to apply Theorem 1 to the finite list of all one-column unitary words that occur in its expansion, after collecting proportional words with their exact width-dependent scalar powers. Group closure is convenient, not necessary for tensor independence.

## 3. Gaussian-rank components and ordinary boundary encodings

Fix a finite Clifford group G on d_0 binary coordinates, retaining its exact scalar phases, and an ordinary monomial subgroup H. Here monomial means one nonzero entry in each computational-coordinate row and column. The symplectic matrix of a Clifford element g has blocks
\[
 \begin{pmatrix}A_g&B_g\\ C_g&D_g\end{pmatrix}.
\]
Use the convention in which monomial Clifford maps are exactly B_g=0, and set r(g)=rank_{\mathbf F_2}(B_g). Scalar multiples have the same r. Let E_r be the span of the projective basis elements of Gaussian rank r in the phase-exact algebra of Section 2.

**Lemma 2.** Each E_r is an H-bimodule. Thus
\[
 \mathcal A=\bigoplus_{r=0}^{d_0}E_r,\qquad
 \pi_r(LMR)=L\pi_r(M)R
 \tag{1}
\]
for matrices M over \mathcal A and matrices L,R over the ordinary subalgebra C[H], with the same exact scalar twisting convention.

**Proof.** If h is monomial, B_h=0 and A_h,D_h are invertible. Matrix multiplication gives
\[
 B_{hg}=A_hB_g,\qquad B_{gh}=B_gD_h.
\]
Their ranks equal the rank of B_g. Multiplication may contribute a nonzero scalar cocycle; that scalar does not change the projective class or its rank. Hence left and right multiplication by an ordinary basis element preserve E_r. Extend bilinearly and then entrywise to matrix multiplication. The direct-sum assertion is an assertion about distinct projective basis elements, or equivalently about their actual tensor operators for sufficiently large V by Theorem 1. QED.

**Corollary 3 (boundary cancellation gate).** Let M be a square m-bank head circuit over this fixed algebra. Suppose invertible ordinary pre- and post-encodings B and L turn it into independent rank-r_star Gaussian jobs, up ordinary monomial factors:
\[
 LMB=\operatorname{diag}(g_1,\ldots,g_m),\quad r(g_j)=r_\star.
\]
Then \pi_r(M)=0 for every r not equal to r_star.

**Proof.** Project the identity using (1). Its right side has no r-component for r different from r_star. Multiplication by the inverses of L and B gives \pi_r(M)=0. QED.

This statement requires invertible square encodings on all the displayed independent banks. It does not silently add known-zero banks, discard original inputs, or accept an identity output bank among the target jobs. Such changed interfaces need their own blockwise target statement. The claim concerns components indexed by the rank of individual Gaussian operators. It does not assign a Gaussian rank to an arbitrary linear combination, prove a MOVE lower bound, or show that a matrix supported only on rank-r_star operators is itself a collection of independent Gaussian jobs.

The inverses can either be explicitly ordinary matrices or be justified inside the same finite-dimensional ordinary algebra. Indeed, if an element of a finite-dimensional unital algebra has an invertible image in a faithful finite-dimensional representation, its inverse lies in that algebra by its minimal polynomial, whose constant term is then nonzero. A mathematical inverse does not by itself supply the required physical ordinary implementation.

Interleaved ordinary operations are not excluded: they can change which products of nonordinary gates occur and can cause genuine cancellation of unwanted components. The corollary removes only the false hope that final invertible ordinary boundary changes could hide a nonzero low-rank component. Arbitrary spatial coordinate maps outside the fixed tensor group, column-specific coefficients and other larger ordinary models are outside the stated application.

## 4. A concrete exact group for the common cubic control

Use the two-bit Walsh basis, ordered as zero frequency followed by three nonzero frequencies a,b,c=a+b. Every operator in the group below fixes the zero-frequency basis vector. Write an element as a phase vector u in (Z/4Z)^3 and a permutation pi in S_3, acting by the monomial D_u P_pi on the nonzero frequencies. Impose
\[
 u_a+u_b+u_c=0\pmod2.
\]
There are 32 phase vectors and six permutations, hence 192 elements. Multiplication is
\[
 (u,\pi)(v,\sigma)=(u+v\circ\pi^{-1},\,\pi\sigma).
\]
The Gaussian generators have phase vectors
\[
 Q_a:(1,0,1),\quad Q_b:(0,1,1),\quad Q_c:(1,1,0),
\]
and P cyclically permutes the three nonzero frequencies. Thus the common A=Q_b^{-1}P lies in the group.

The ordinary subgroup has phase vectors
\[
 (0,0,0),\ (2,0,2),\ (0,2,2),\ (2,2,0)
\]
and arbitrary permutations. It is the 24-element affine binary-coordinate group, expressed in the Walsh basis. Its tensor lift acts by the same affine coordinate permutation in every column and is physically ordinary. This 24-element subgroup is a particular allowed ordinary family, not an assertion that every physically ordinary operation belongs to it.

For u=(u_a,u_b,u_c), put
\[
 b_{11}=u_a\bmod2,\quad b_{22}=u_b\bmod2,\quad
 b_{12}=(u_c-u_a-u_b)/2\bmod2.
\]
The Gaussian rank is the binary rank of the symmetric matrix with these entries. The division by two is well defined modulo two because the phase sum is even. There are exactly 24 elements of rank zero, 72 of rank one, and 96 of rank two. The checker verifies the multiplication table and all 9,216 left/right ordinary rank-preservation incidences. The formula is also the quadratic-phase Clifford formula: the one-column phase is linear plus an even bilinear form in the Walsh coordinates, and its polar/diagonal data give the stated B block.

No nonidentity element is a scalar operator, because every group element fixes the zero-frequency vector and the representation is faithful. The exact trace is
\[
 \chi(u,\pi)=1+\sum_{\pi(j)=j}i^{u_j}.
\]
The checker finds max_{g not equal I} |\chi(g)|^2=8. Theorem 1 therefore proves tensor independence for all V>=16, since
\[
 (192-1)(1/\sqrt2)^{16}=191/256<1.
\]

There is a stronger exact finite witness. Form the 192 by 192 Gram matrix with entries \chi(g_i^{-1}g_j)^V, reduce its Gaussian-integer entries modulo 101 with i mapped to 10, and perform exact Gaussian elimination. At V=6 the rank is 192. A nonzero determinant modulo this Gaussian-integer prime quotient implies a nonzero characteristic-zero determinant. Hence the 192 tensor operators are independent at V=6. All elements fix the same zero-frequency vector, so contracting the last tensor factor against that vector sends any width-(V+1) linear relation to the identical-coefficient width-V relation. Independence propagates to every V>=6.

The checker also records modular ranks 10,37,88,155,191 at widths one through five. These are finite modular observations; no claim that they establish every corresponding characteristic-zero rank is needed.

## 5. A finite synthesis reduction

For the four-role common-cubic caller, use r_star=2. In this concrete group, every prospective endpoint must have exactly zero rank-zero and rank-one components before any invertible ordinary outer encoding. For a fixed choice of prefix B and suffix A, and an unknown interstage ordinary matrix C,
\[
 \pi_0(ACB)=0,\qquad \pi_1(ACB)=0
 \tag{2}
\]
are finite homogeneous linear equations in the coefficients of C in Mat_4(C[H]). There are 4*4*24=384 unknown scalar coefficients in this concrete ordinary family. A larger finite ordinary Clifford group can be handled by the phase-exact general theorem, with its own full group and width-residue verification.

Equation (2) is only a necessary first stage. A successful caller certificate must additionally provide:

1. An invertible C in the solution space, with an actual finite ordinary circuit or another admitted uniform physical implementation.
2. Explicit ordinary input/output encodings that turn the resulting matrix into four independent rank-two Gaussian jobs on arbitrary inputs.
3. The literal native/query chronology, correct inverse orientation, all scalar operations, restored scratch, grid/precision bounds, and paid body idles.
4. The strict complete supplier and outer compatibility conditions.

One can test algebraic invertibility in a faithful regular representation, but a finite-field nonsingularity test by itself does not construct a valid rational/complex circuit. An empty kernel for a fixed exact template rules out that template only. Failed random samples of a nontrivial kernel prove no universal impossibility.

## 6. Verification and negative controls

Run the standalone checker with Node. It has no external package or repository dependency and prints PASS_FINITE_HEAD_RANK_COMPONENTS with the exact summary.

It checks the 192-element group, the ordinary subgroup, the exact trace bound, all left/right rank contacts, six modular Gram matrices, and 48 ordinary two-bank component identities. These finite checks supplement the general proofs; they are not a substitute for their quantifiers.

Two controls expose the relevant errors:

* At width one, C_a=alpha I+beta X_a, where alpha=(1+i)/2 and beta=(1-i)/2. At width two on the spectral pair (a,a), C_a tensor C_a has eigenvalue -1, while alpha I+beta(X_a tensor X_a) has eigenvalue 1. Expanding independently in every column introduces 2^V terms and is outside the fixed collective ordinary algebra.
* Left multiplication by a nonordinary Q_a changes Q_a, a rank-one Gaussian, into Q_a^2, an ordinary rank-zero map. The ordinary-subgroup hypothesis in Lemma 2 is essential.

There is no asserted all-circuit obstruction, no new movement lower bound, and no new complete kappa. The positive contribution is a uniform, phase-exact finite algebraic gate for the next constructive caller search.
