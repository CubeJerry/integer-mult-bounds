# Dual pencils force a rank cost for repairing the Eisenstein form

**Status: proved finite-premise reduction and universal all-phase correction-rank theorem. No new kappa.**

The four-coordinate Eisenstein form omits required real point/facet zeros. Its correction has rank at least four for every phase section, at least six in the pinned canonical section, and exactly eight within the canonical eight-real-coordinate bilinear representation. These ranks are not numbers of MOVEs, owned records, or native calls.

## Provenance

Predecessor: research/moonshot-005-program/results/eisenstein-rank-four-contact/author/, PROOF.md Git blob 0b70dd1c1e5d4801bc8539650235e25fd0fb0346, RESULT.json Git blob 599d23ddbc300c78665d8e8079a13cb273bf868a.

Original source: research/moonshot-005-program/results/eisenstein-cycle-native/author/SYMMETRY.json, Git blob 8b0fc7779990f0a3ad15494af97f082be3592944, at programme commit 12b269a98e461ebf5e83e24cc16765540bec9626. The standalone checker pins both input byte strings by their Git blob SHA-1 values before parsing. It reconstructs A, C, all relative phase gains, the pencil partition, and the new dual-pencil property. Indices below are zero-based indices into SYMMETRY.json's cycles array.

Prepared for @CubeJerry, preserving predecessor credit, with OpenAI assistance. Classical Eisenstein/E8 and Witting-polytope references remain in the predecessor proof. The new argument is the forced correction minor and its representation consequence.

## 1. Precise correction contract

Let K = Q(theta), theta squared = -3. Statements also hold over C. A section sigma selects one of the three real root lines in each of the forty complex lines. Using the predecessor's integer eight-coordinate vectors and S=2E+I, define
\[
 A^\sigma_{ij}=p_i^Tp_j,\quad C^\sigma_{ij}=p_i^TSp_j,\quad
 H^\sigma=A^\sigma/4+\theta C^\sigma/12.
\]
The predecessor proves S transpose = -S, S squared = -3I, rank H = 4 and H_ii = 1 for every section.

For every integer V >= 1, a correction is any 40V by 40V matrix R, with V by V blocks, such that
\[
 R_{ii}=0,\qquad
 R_{ij}=-H^\sigma_{ij}I_V
 \quad(i\ne j,\ A^\sigma_{ij}=0).                       \tag{1}
\]
The base H tensor I_V is unchanged, the own blocks remain I_V, and every required real zero is restored. No Hermitian or skew-symmetric assumption is made on R. Entries at real nonorthogonal contacts are free.

There are 240 complex-orthogonal unordered pairs, for which H, A, C vanish for all sections. The other 540 pairs partition into ninety four-vertex pencils. Each pencil admits four pairwise real-orthogonal representatives. Four selected vertices have only three relative phases, so every section has a forbidden nonzero H contact in each pencil. At each bad contact, C_ij = +/-4, hence H_ij = +/-theta/3 and H_ji = -H_ij. These finite facts are reconstructed by the checker.

## 2. Dual-pencils lemma and universal theorem

**Finite lemma.** For every complex-nonorthogonal pair a,b, its four common complex-orthogonal neighbors form one of the ninety pencils.

The receipt lists the neighbors and pencil index for all 540 pairs. The checker reconstructs them from A,C and checks membership in the complete pencil list. This is an exhaustive proof of this finite premise. Its interpretation as the orthogonal complement of a nondegenerate two-plane in the four-dimensional symplectic projective geometry is not needed for the certificate.

**Theorem 1.** For every section sigma, V >= 1, and R satisfying (1),
\[
 \operatorname{rank}_K R\ge4V.
\]

**Proof.** Choose a bad pair a,b in any pencil. Its four common complex-orthogonal neighbors form another pencil L, which supplies a second bad pair c,d. The vertices are distinct. All four cross pairs between {a,b} and {c,d} are complex orthogonal. Thus the principal matrix of R on these vertices is
\[
 \begin{pmatrix}
 0&-H_{ab}I_V&0&0\\
 -H_{ba}I_V&0&0&0\\
 0&0&0&-H_{cd}I_V\\
 0&0&-H_{dc}I_V&0
 \end{pmatrix}.
\]
Each scalar two-by-two block has determinant -1/3. The scalar four-by-four determinant is 1/9; the V-block determinant is (1/9)^V. It is invertible, proving the bound. This is a proof for all 3^40 sections, not their enumeration. Square.

Only two bad pairs are used. Ninety bad contacts are not being identified with ninety independent corrections.

## 3. Stronger canonical-section minor

**Theorem 2.** For the pinned canonical section, every correction satisfying (1) has rank at least 6V.

The six cycle indices I=(3,8,14,18,20,25), with canonical binary normals (19,38,74,84,97,127), are pairwise real orthogonal. Their exact C principal matrix is four times
\[
 N=\begin{pmatrix}
 0&0&1&0&-1&0\\
 0&0&1&-1&0&0\\
 -1&-1&0&0&0&-1\\
 0&1&0&0&0&-1\\
 1&0&0&0&0&-1\\
 0&0&1&1&1&0
 \end{pmatrix}.
\]
Fraction-free integer elimination gives det N = 9, and det C[I,I] = 4^6 times 9 = 36864. All entries of this correction minor, including its diagonal, are forced. Consequently
\[
 R[I,I]=-\theta C[I,I]/12,\qquad
 \det R[I,I]=(-\theta/12)^6\,36864=-1/3.
\]
For V-blocks the determinant is (-1/3)^V. This proves rank R >= 6V. Square.

This is a canonical-section statement. A rank-six minor in every section is not established.

## 4. Rigidity inside the canonical eight-coordinate representation

Let T_ab, for 1 <= a,b <= 8, be arbitrary V by V matrices, and impose the additional representation
\[
 R_{ij}=\sum_{a,b=1}^8 p_{ia}\,T_{ab}\,p_{jb}.           \tag{2}
\]
This allows arbitrary mixing within and between the eight coordinate blocks. No alternating assumption on T is needed.

**Theorem 3.** In the canonical section, (1) and (2) force
\[
 T_{ab}=-(\theta/12)S_{ab}I_V,\qquad
 R=-(\theta/12)C\otimes I_V,
\]
and therefore rank R = 8V.

**Proof.** The forty zero diagonal blocks and 480 directed complex-orthogonal contact blocks give homogeneous constraints. For a single matrix entry of the T_ab these are 520 equations in 64 unknowns, with integer coefficient row p_i tensor p_j.

The checker obtains rank 63 modulo 101. Thus the characteristic-zero rank is at least 63. The nonzero vector of S entries is an exact kernel vector, verified in integers, so the rank is at most 63. The kernel over K is exactly span(S).

Apply this scalar equation system separately to each of the V squared matrix entries. There is one V by V matrix B such that T_ab = S_ab B, and hence R_ij = C_ij B. Any bad pair has C_ij nonzero; (1) forces B=-(theta/12)I_V.

The factorization C=P transpose S P gives rank C <= 8. Its rank modulo 101 is eight, proving characteristic-zero rank eight. Tensoring with I_V gives the asserted 8V. Square.

The rank-63 premise is canonical. It is not asserted for every section. This is not a lower bound on arbitrary corrections: (2) restricts both the input and output coefficient spaces to the original eight real coordinate spaces.

## 5. Explicit shared corrections and the escape left open

Write G=A/4. The exact identities
\[
 G-H=(\bar H-H)/2=-\theta C/12,\qquad
 G=H/2+\bar H/2
\]
supply controls against overreading these results.

The first is an unchanged-base correction of canonical rank eight. The second is an explicit decomposition into two rank-four forms; its added component has diagonal 1/2 and accompanies a rescaled base H/2. It therefore does not satisfy the unchanged-base, zero-diagonal contract (1).

The rank-four component bar H/2 repairs all contacts at once in that rescaled decomposition. Many bad contacts can share correction work. The resulting canonical operator is the old rank-eight Gram matrix, so this identity alone gives no rank saving.

If an interface separately computes unchanged H through a 4V-wide bank and factors R through an additional independent bank, Theorem 1 forces the additional bank to have width at least 4V: a factorization cannot have internal width below its matrix rank. Under that specific additive-bank accounting the total reaches the original eight-coordinate count.

Physical programmes need not obey that restricted accounting. Shared histories, a changed base, different moment spaces, or local repairs remain possible. Their costs are not supplied by this theorem. The exact surviving obligation is to construct and pay for such a mechanism within the complete complex supplier and recursive interface.

## 6. Verification and classification

Run:
\[
 \texttt{node check.mjs /absolute/path/to/SYMMETRY.json /absolute/path/to/eisenstein-rank-four-contact/author/RESULT.json > RESULT.reproduced.json}.
\]
Expected status: PASS_DUAL_PENCIL_CORRECTION_RANK.

The exported checkCorrection function and the three negative controls were actually run in the available pure-JavaScript tool after the local executor became unavailable. The Node CLI is provided for reproduction; local execution of that CLI is not claimed.

The receipt contains all 540 dual-pencil witnesses, canonical four-block witnesses, the six-block determinant, the canonical homogeneous rank result, and negative controls rejecting a missing pencil, a changed relative phase gain, and an altered E entry. Bounded integer and modular calculations stay exactly representable in binary64. Determinants use BigInt and check every fraction-free division.

The infinite all-V and all-section conclusions are proved linear-algebraic consequences of the fully checked finite premises. Author execution is not independent verification; the integrator records that review separately.

**No new kappa.** No native movement implementation, completed caller, or movement lower bound is claimed. The full complex/BIT compatibility, ownership and erasure, precision, compiler, recursion, and retained foundational assumptions remain. The next positive step is a shared or changed-source construction that pays for these contacts without reintroducing the full old source cost.
