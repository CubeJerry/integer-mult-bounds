# A determinant deformation excludes rank-preserving path constructions

**Proved scoped obstruction, including the single nonlinear CCZ sector and its adjacent-pair clean transport extension. No new κ.** If every path with j head factors remains a rank-j Gaussian up to ordinary monomials, scaling the formal head by z exposes an exact determinant invariant. A concrete ordinary clock rewind breaks that hypothesis and specifies the next distinct interface.

## 1. Precise fixed-template hypothesis

At every positive tensor width V let `a=A^(tensor V)` on a bank of dimension `D=8^V`, and use the actual three-bank source

\[
 K(a)=\begin{pmatrix}I&0&a-I\\a&0&-a\\I&I&-I\end{pmatrix}.
\]

This is the admitted forward lower native followed by its charged ordinary bank operation, up the existing fixed role relabelling. No Gaussian query, owned zero input, discarded bank or enlarged productive bank is allowed here.

Every ordinary coefficient matrix is a finite sum of tensor lifts of fixed one-column unit-phase monomials, with exterior complex scalar coefficients. This includes arbitrary fixed Z4-phase permutation tables and finite bank ADD/SCALE words. The template and its finite list of one-column words are fixed before V varies. An unbounded width-dependent family of different tensor words is outside scope. Coefficients may depend on width for the algebraic obstruction; physical uniformity remains a separate obligation.

Let Q1,Q2,L,R be invertible ordinary matrices on three arbitrary independent banks. Expand

\[
 M(z)=K(za)Q_1K(za)Q_2K(za)=\sum_{j=0}^3z^jM_j.                    \tag{1}
\]

Assume every one-column unitary path word contributing to M_j is monomial-equivalent to a canonical rank-j Gaussian. This **rank-by-length condition** concerns individual path words, not their linear combinations. If at every sufficiently large permitted width the complete endpoint L M(1) R consists of three independent Gaussian head jobs of ranks r1,r2,r3, then

\[
 r_1+r_2+r_3=6.                                                    \tag{2}
\]

The target ranks may differ and may include zero. Exact scalar tensor phases are retained.

## 2. Proof from the actual determinant polynomial

The previously proved tensor-separation theorem makes a fixed finite set of projectively distinct one-column unitary words linearly independent after sufficiently large tensor powers. Group closure is unnecessary. Thus it applies even when A and the ordinary monomials generate an infinite group. Collect the width-dependent scalar phases of proportional words before applying the theorem. The finite family must include the ordinary endpoint encodings used in the claimed identity.

Monomial left/right multiplication preserves each Gaussian double coset and its rank: a rank-j Gaussian has exactly 2^j nonzero entries per column, and its complete monomial normal form is preserved. Therefore rank-component projection commutes with ordinary left/right multiplication. Projecting the exact endpoint identity gives

\[
 LM_jR=\operatorname{diag}(1_{r_i=j}G_i).
\]

Consequently the following is an identity of actual complex matrix polynomials in the new scalar z:

\[
 LM(z)R=\operatorname{diag}(z^{r_1}G_1,z^{r_2}G_2,z^{r_3}G_3).       \tag{3}
\]

K(za) is a constant invertible bank matrix times a two-active-bank triangular native with diagonal za,za,I. Its determinant is a nonzero constant times z^(2D). Since Q1,Q2,L,R are invertible and independent of the formal z, the determinant on the left of (3) is a nonzero constant times z^(6D). The determinant on the right is a nonzero constant times z^((r1+r2+r3)D). Their equality proves (2).

An ordinary coefficient stays its actual fixed monomial during this deformation even if its discovery formula used A and A^-1. Scaling that discovery formula instead would change the mathematical circuit. A small-width tensor alias cannot replace the stipulated asymptotic faithfulness. The determinant argument also requires all three original inputs and invertible ordinary endpoint encodings.

## 3. One nonlinear coordinate-sign sector

Take any three-bit Boolean sign source `A=C_bD_fP`, with its proved square and cube normal forms. Let H be minus one at a single one-column address and plus one at the other seven. Put

\[
 K_H=A^{-1}HA,\qquad J_H=AHA^{-1}.
\]

Both are ordinary unit-phase monomial involutions: A and A^-1 send any basis vector to two coordinates of equal magnitude, so conjugating a coordinate sign reflection gives zero diagonal and unit off-diagonal phases on that two-point block, fixing the other six coordinates.

At width V let h=H^(tensor V), k=K_H^(tensor V), and

\[
 C_h=\begin{pmatrix}(I+h)/2&0&(I-h)/2\\0&I&0\\(I-h)/2&0&(I+h)/2\end{pmatrix}.
\]

This actual conditional bank permutation already has a four-ADD, two-dyadic-SCALE, one-phase implementation. The halves are exterior field coefficients. Let Q be any invertible matrix with entries in span{I,k}. Then

\[
 W=K(a)C_hK(a)QK(a)                                                \tag{4}
\]

satisfies the rank-by-length condition, so every independent Gaussian endpoint under arbitrary permitted ordinary encodings has total head rank exactly six.

Indeed its individual path words are `A^e1 H^u A^e2 K_H^v A^e3`, with all exponents zero or one. Zero/one A factors give rank zero/one. Two A factors reduce to ordinary factors around A² using `HA=A K_H`, `A K_H A^-1=H` and `AHA^-1=J_H`. Three A factors reduce to `A H^w A²`. Expanding the cyclic source gives three distinct Gaussian bits, each crossed once, with arbitrary fixed sign diagonals between them. The Boolean family's unique-path/Hadamard-eight proof gives rank three; it never required the three sign diagonals to coincide. All32 patterns are thereby covered with their actual phases.

This proves the complete profitable-endpoint exclusion for the declared one-sector family, including the unbalanced prospective profile (3,3,1). It is stronger than a failed search or a single deficient mixed endpoint.

## 4. Adjacent nonlinear sectors and their clean transport algebra

For a concrete extension let H7,H6 be signs at addresses111 and110, respectively. Their product is CZ_bc. Set

\[
 K_7=A^{-1}H_7A,\quad K_6=A^{-1}H_6A,\quad
 Z=A^{-2}(H_7H_6)A^2.                                               \tag{5}
\]

Each individual `A^-2 H_i A²` is nonmonomial. From `A²=C_aC_bR_f` it is a reflection `I−2vv*` whose v has four nonzero entries of magnitude1/2. It has four columns with four nonzero entries and four columns with one. Its tensor power has a column of support4^V and cannot be a linear combination of only two monomial tensor operators.

Nevertheless Z in (5) is ordinary, exactly:

\[
 Z=R_f^{-1}(C_b^{-1}CZ_{bc}C_b)R_f.                                \tag{6}
\]

The middle operator is conditional Pauli Y on bit b, controlled by c: it flips b when c=1 and applies the input phase `i^{c(1+2b)}`. Formula (6) is a literal fixed monomial recipe with R_f and its inverse charged. This is a real transport improvement over either individual sector. Pairing111 with011 instead gives CZ_ab, which is crossed by both Gaussians and is not ordinary after this conjugation.

Let H0 be the four-element diagonal group generated by H7,H6, and let G be the finite monomial group generated by K7,K6,Z. For the canonical CCZ source its exact order is16, with the displayed generators realizing D8×C2; the obstruction below only needs the stated monomial generators, not that census. Every element of G and both of its first two forward conjugates by A are ordinary. It suffices to check generators:

\[
 AK_iA^{-1}=H_i,\quad A^2K_iA^{-2}=AH_iA^{-1},
\]

\[
 AZA^{-1}=K_7K_6,\quad A^2ZA^{-2}=H_7H_6.
\]

All right sides are monomial, and conjugation respects multiplication. Thus the new construction changes the available ordinary transport but preserves two steps of clean forward transport.

Now allow **any** invertible Q1 with entries in the tensor group algebra of H0, and **any** invertible Q2 with entries in the tensor group algebra of G. This includes arbitrary joint four-sector bank routing, dyadic sector projectors and nonlinear ordinary mixtures, not merely a pair of bank swaps. Every path still has Gaussian rank equal to its number of A factors.

For a proof write a one-column path as `A^e1 H A^e2 G0 A^e3`, H in H0 and G0 in G, and put K_H=A^-1 H A in G. The three two-factor patterns reduce respectively to `A² K_H G0`, `H(AG0A^-1)A²`, and `(AHA^-1)(AG0A^-1)A²`. The three-factor pattern is

\[
 AHAG_0A=A^2K_HG_0A=(A^2K_HG_0A^{-2})A^3.
\]

Every displayed adapter is ordinary. The determinant theorem therefore again gives total independent endpoint head rank exactly six. The paired sector fixes the missing one-sector transport but does **not** by itself escape the complete source obstruction. The result identifies which extra feature a successful caller must add.

## 5. Complete common-body Gaussian consequence and a sharp control

Give each of the three native occurrences its complete fresh seven-axis body and deliver all three bodies to all three productive banks, paying one inactive-role seven-axis idle per native. The exact Gaussian price remains

\[
 P_t=3[1]+6[7]+3[8],\qquad[r]=r^t,
\]

and an independent endpoint with heads r_i has target moment `T_t=sum_i[21+r_i]`. The theorem forces `sum_i r_i=6`. For every `0<t<1`, put `Δ=8^t−7^t`, so `0<Δ<1`. Concavity and subadditivity give

\[
 T_t\le3\,21^t+\Delta\sum_i r_i\le9\,7^t+6\Delta,
\]

\[
 P_t-T_t\ge3(1-\Delta)>0.                                         \tag{7}
\]

Every real ordinary, physical, tape, precision, storage and recursive cost is additional. Thus neither declared family can be a profitable complete supplier under this body accounting, including at t=199/200. The argument does not change the Gaussian credit convention.

The bound on head rank is sharp: Q1=Q2=I is allowed and the exact baseline `K(a)³=diag(a²,a²,a²)` delivers total six. Its already pinned Gaussian margin at t=199/200 is negative. The obstruction concerns this fixed forward-native, retained-three-bank, common-body architecture. It does not cover queries, extra banks, changed body incidence, different native orientations or transport coefficients that break the path-rank hypothesis.

## 6. A concrete ordinary clock rewind breaks the hypothesis

Let **D_b=diag(1,i) on bit b**, with the identity on the other bits. This is not the sign Z_b. For the normalization `C_b=((1+i)I+(1-i)X_b)/2`, exact two-by-two multiplication proves

\[
 C_bD_bC_b=D_bC_bD_b.                                               \tag{8}
\]

Set `H_clock=S_f^-1 D_b`, an actual ordinary monomial with its charged inverse. Then

\[
 A H_{clock} A
 =C_bD_bC_bS_f
 =D_b A(S_f^{-1}D_bS_f).                                           \tag{9}
\]

The left side contains two native head factors, but the right side is a rank-one Gaussian between actual ordinary monomials. All phases in (8)-(9) are literal, and tensor powers preserve the equality at every width. This is an explicit rank collision across path lengths, so a caller using the clock rewind can fall outside the determinant-grading theorem. Replacing D_b by the sign Z_b would yield a monomial product instead and is a meaningful wrong-gate control.

Implement H_clock through its one fixed permutation and phase table or through the separate charged S_f^-1 and D_b services. Its inverse is D_b^-1 S_f with correct phase indexing. An ADD using a transported source must restore the source or pay for a separate owned implementation; the displayed equality is not a free nonordinary update. No new Gaussian query is introduced by the clock service itself.

The next concrete candidate is a role-dependent clock rewind combined with nonlinear sector routing between the three native calls. It retains the optimistic (3,2,2) Gaussian target margin `0.56100733960089153867…` only if the complete independent endpoint is constructed without an extra query. Every added monomial, ADD/SCALE, phase, body, precision and recursive expense remains. A rank collision is a necessary way to leave the proved graded family, **not** a profitable caller or a new κ theorem.

## 7. Verification and provenance

The author checker verifies exact single-sector path factorizations, the adjacent transport group and its monomial conjugates, every relevant path normal form, the literal braid/clock word and its phases, the sharp K³ baseline, the native determinant exponent and negative controls. Finite computations corroborate the algebraic proof, not an asymptotic search claim. Sufficiently large tensor faithfulness is inherited from the pinned finite-word theorem, with the actual finite endpoint support included.

The source-family tables and compiler costs remain separately pinned. Credit @CubeJerry, the actual source/compiler authors, prior tensor-separation and mixed-sector contributors, and the continuing programme. Prepared with substantial OpenAI assistance. **No new κ.**
