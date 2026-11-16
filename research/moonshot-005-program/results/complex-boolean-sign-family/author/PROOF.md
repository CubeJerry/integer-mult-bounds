# Boolean-signed native heads with constructive Gaussian cubes

**Proved operator family; physical admission uses the separately reviewed fixed-monomial service. No profitable caller and no new κ.** This extends the single CCZ source without changing its source equations or Gaussian price convention. For every fixed head dimension, an arbitrary Boolean sign table can be inserted into a cyclic native head while its square and cube retain complete Gaussian normal forms. In exactly three heads, table parity decides finite versus infinite projective order.

## 1. Exact theorem and computational interface

Fix `d≥3`, put `N=2^d`, and label address bits `0,…,d−1`. Let `P` shift each old bit `j` to `j−1 mod d`, and put `a=0,b=1,c=d−1`. For any fixed Boolean function `f:F₂^d→F₂`, define

\[
 D_f|x\rangle=(-1)^{f(x)}|x\rangle,\quad S_f=D_fP,\quad
 A_f=C_bS_f,\qquad C_j=\frac{(1+i)I+(1-i)X_j}{2}.                    \tag{1}
\]

There are fixed unit-phase monomials `R_f,L_f,Q_f`, constructively determined from the truth table, satisfying

\[
 C_bS_f=A_f,\quad S_f^{-1}C_aR_f=A_f,\quad
 A_f^2=C_aC_bR_f,\quad A_f^3=L_f C_0C_1C_2 Q_f.                     \tag{2}
\]

The last canonical rank-three transform uses a paid fixed coordinate matcher when `c≠2`. All identities are exact over Gaussian dyadic rationals, and all monomial phases belong to `{1,i,−1,−i}`. They tensor-lift at every positive width `V`; source field scalars remain exterior. Every member supplies the same lower/upper native head source conditional on its charged monomial services.

For `d=3`, exactly half the 256 sign tables have infinite projective order:

\[
 A_f\text{ has finite projective order}
 \iff \sum_{x\in F_2^3}f(x)=0\pmod2.                                \tag{3}
\]

Every odd-parity member has no full stable lattice at a prime over two. The dichotomy (3) is specific to eight addresses; it is not asserted for larger `d`.

## 2. The source square is explicit for every Boolean table

Set `g(x)=f(x)⊕f(x+e_a)`. Then `g` is independent of bit `a` and

\[
 S_fX_bS_f^{-1}=X_a\operatorname{diag}((-1)^{g(x)}).
\]

The generalized monomial-admission proof in the single CCZ package gives

\[
 J_g|x\rangle=i^{g(x)}|x+g(x)e_a\rangle,\qquad R_f=J_gS_f^2.          \tag{4}
\]

This is an actual conditional permutation and phase table with a table inverse, not an executed Gaussian inverse. Equation (4) and commuting `C_a,C_b` prove the first three identities in (2). Every inactive head bit remains a complete spectator on every source and target field.

## 3. The cube reduces to real Hadamard blocks of order eight

Expand the three powers, without tensor-distributing any sum:

\[
 A_f^3=C_bD_f\ C_a(PD_fP^{-1})\ C_c(P^2D_fP^{-2})\ P^3.              \tag{5}
\]

Temporarily omit the last paid permutation `P³`. Three distinct bits each encounter exactly one Gaussian. At fixed values of all remaining bits, every input-to-output path between the eight active addresses is unique. Its Gaussian coefficient is `α³(-i)^{dist(x,y)}`, with `α=(1+i)/2`; all three sign factors contribute only `±1`. There are no zero entries. Multiplying rows and columns by `i^{|x|}` and `i^{|y|}`, and dividing by the common `α³`, leaves only signs because

\[
 (-i)^{\operatorname{dist}(x,y)}
 =(-i)^{|x|+|y|}(-1)^{x\cdot y}.
\]

Unitarity gives `HHᵀ=8I` for the resulting sign matrix `H`. The spectator blocks may have different signs and different normalizers; equality of their tables is not assumed.

### Constructive normalization lemma

Every real Hadamard matrix of order eight is equivalent to the Sylvester character table of `F₂³` by row/column permutations and sign changes.

**Proof.** Normalize one row and one column to all plus. Each other row has four minus signs among seven remaining columns. Two such four-subsets meet in two points. Their complementary triples meet in one point. No pair of points occurs in two triples; the seven triples contain `7·3=21=binom(7,2)` distinct pairs, so every pair occurs once.

Label one triple by `u,v,u+v`, and choose a point `w` outside it. The unique triples through `w` and each of these points label the other three points `u+w,v+w,u+v+w`. Pair uniqueness forces the three remaining triples: each triple is a zero-sum line of the seven nonzero vectors in `F₂³`. The triples are therefore the nonzero parts of the seven nonzero linear kernels. Their complementary four-subsets are the supports of the seven nonzero linear forms. Adjoin the initial zero column and constant row to obtain the Sylvester character table. ∎

Apply this construction separately to every spectator block in (5). Undo the `i^{|x|}` phases and insert the fixed phases of `C_0C_1C_2`. This gives `L_f,Q_f` with fourth-root phases. The separate block tables combine into global fixed monomials on all `2^d` addresses. This proves the cube identity in (2). It assumes no classification of larger-order Hadamard matrices.

An explicit implementation normalizes a block's first row/column, converts the remaining sign rows to binary words, labels the Fano triples, then undoes the row/column phase changes. The checker uses the equivalent character-span procedure and multiplies each complete normalizer back to the original cube.

### Closed three-bit normalizer with at most two Toffoli gates

For `d=3`, write the Boolean algebraic normal form as

\[
 f(a,b,c)=f_0+\ell_a a+\ell_b b+\ell_c c
 +q_{ab}ab+q_{ac}ac+q_{bc}bc+\eta abc\pmod2.
\]

Define the two triangular bijections

\[
 F(u,v,w)=(u,\ v\oplus q_{ab}u\oplus\eta uw,\ w),
\quad
 G(a,b,c)=(a,b,\ c\oplus q_{ab}a\oplus(q_{bc}\oplus q_{ac})b\oplus\eta ab).
                                                                    \tag{5a}
\]

Both are involutions. Set

\[
 R_0(u,v,w)=\ell_a u+(\ell_a+\ell_c)w+q_{ac}uw\pmod2,
\]

\[
 C_0(a,b,c)=f_0+(\ell_b+\ell_c)a+(\ell_a+\ell_b+\ell_c)b+\ell_b c
 +(q_{bc}+q_{ac})ab+q_{ab}bc+q_{bc}ac+\eta abc\pmod2.
\]

The literal endpoint adapters are

\[
 L_f|z\rangle=i^{|z|-|F(z)|+2R_0(F(z))}|F(z)\rangle,
\quad
 Q_f|x\rangle=i^{|G(x)|-|x|+2C_0(x)}|G(x)\rangle.                   \tag{5b}
\]

All phase exponents are reduced modulo four. To verify these formulas, the unique path in (5) has sign exponent
`f(u,b,w)+f(w,a,b)+f(b,c,a)`. Expanding its eight ANF terms gives

\[
 (u,v,w)\cdot(a,b,c)+f(u,b,w)+f(w,a,b)+f(b,c,a)
 =F(u,v,w)\cdot G(a,b,c)+R_0(u,v,w)+C_0(a,b,c)\pmod2.
\]

The Hamming-weight phase difference between the original Gaussian factors and `C_0C_1C_2` is exactly (5b). This is a direct Boolean-polynomial proof of the complete three-bit endpoint, independent of the general Hadamard normalization argument.

Permutation `F` uses at most one CNOT and one Toffoli. Permutation `G` uses at most two CNOTs and one Toffoli. Thus the cube's two adapters together require at most **two Toffolis, three CNOTs and two unit-phase passes**. The source derivative is `g=ℓ_a+q_ab b+q_ac c+ηbc`; its conditional permutation `J_g` needs at most one NOT, two CNOTs and one Toffoli. These are literal fixed gate lists, not arbitrary-permutation tariffs.

## 4. Complete finite/infinite classification in three heads

Assume `d=3`. Write `δ_x=(-1)^{f(x)}`. The cyclic bit permutation has fixed addresses `0,7` and two three-element orbits `O₁,O₂`. Set `ε_j=prod_{x∈O_j}δ_x`. A diagonal entry of `A_f³` comes from the unique path selecting the identity term in all three Gaussians. Therefore

\[
 \operatorname{tr}(A_f^3)=\alpha^3 T_f,
 \qquad T_f=\delta_0+\delta_7+3\varepsilon_1+3\varepsilon_2,
 \qquad\alpha^3=(-1+i)/4.                                           \tag{6}
\]

Also

\[
 \det A_f=\det D_f=\delta_0\delta_7\varepsilon_1\varepsilon_2
            =(-1)^{\sum_x f(x)},                                    \tag{7}
\]

because `det C_b=i⁴=1` and the address permutation of `P` is even.

If (7) is minus one, exactly an odd number of the four signs in (6) is negative. Modulo four the coefficient three is minus one, so `T_f≡2 mod4`; explicitly `T_f∈{−6,−2,2,6}`. Equation (6) is then not a Gaussian integer. Finite-order matrices have algebraic-integer traces on all powers, so `A_f` has infinite order. If a projective power `A_f^m=ζI` existed, (7) would imply `ζ⁸=(det A_f)^m`, making `ζ` a root of unity and forcing a finite ordinary power. Hence projective order is also infinite.

At `(1+i)`, the valuation of `α³T_f` is `−3+2=−1`, because `T_f` is twice an odd integer. A full stable lattice would make `A_f³` integral in a lattice basis and its trace integral. This contradiction survives every finite number-field extension at a prime over two. Thus every odd table fails the invariant-lattice premise, independently of the caller question.

For the converse, use the unique algebraic-normal-form expansion of a three-bit Boolean function. Its cubic coefficient is the XOR of all eight truth values: each proper monomial is nonzero on an even number of inputs, whereas `abc` is nonzero once. If the table parity is even, `f` has degree at most two. Its sign operator is a product of constant signs, single-bit Z phases and pairwise CZ phases. These and `C_b,P` normalize the finite Pauli group. Their projective normalizer is finite: conjugation gives an automorphism of that finite group, and the kernel consists of scalars because the Pauli representation is irreducible (commuting with all diagonal Z and bit flips forces a matrix to be scalar). Therefore `A_f` has finite projective order. Its root-of-unity determinant also makes its ordinary order finite. This proves both directions of (3), with exactly128 tables in each class.

No claim is made that all odd tables have the same spectrum or can use the same eventual caller. They have the same source/endpoint type and the same rigorous escape from the finite-group lattice premise.

## 5. All-width physical and cost contract

All table sizes are fixed before `V` or the integer input length varies. At width `V`, each address column follows the same fixed table and its unit phase is summed over columns modulo four. The source maps retain three actual services `S_f,R_f,S_f⁻¹`; a square target needs its actual `R_f` wrapper, while a cube needs both `L_f,Q_f` wrappers. No normalizer is free because its truth table is finite. Constants can grow exponentially with fixed `d` and are all retained in the ordinary movement/phase count.

The explicit fixed-monomial compact-control bridge, if admitted independently, implements these tables with restored dirty compact fields and full repaired fixed-tape/descriptor costs. The algebra theorem does not independently prove that physical bridge or the foundational assumptions behind its tariff. Every native Gaussian `[1]+[7]+[8]`, original ADD, body, idle, source/target volume, precision and recursive charge stays unchanged. All adapters are norm-one permutations with unit phases. Scalar bank words still require their own bounded coefficient and intermediate-norm accounting.

For three-bit sources, the three native boundary permutations together need at most six logical coordinate SWAPs, one NOT, two CNOTs and one Toffoli, with three phase passes: `S_f,S_f⁻¹` each have one three-cycle, and `R_f=J_gS_f²` has one inverse three-cycle followed by the explicit `J_g`. A square endpoint wrapper has at most two SWAPs, one NOT, two CNOTs, one Toffoli and one phase pass. Inverse wrappers have the same gate counts and the correctly inverted phase table. Consequently the nine source plus four target services for a hypothetical three-native `(3,2,2)` caller are bounded in total by **22 SWAPs, five NOTs, 13 CNOTs, seven Toffolis and 13 phase passes**. Lowering every logical SWAP to three CNOTs gives the alternative bound **79 CNOTs, five NOTs, seven Toffolis and 13 phase passes**. These are ordinary gate counts; each receives its retained physical tariff, temporary reservations and repair. The caller's own bank ADD/SCALE/permutations are additional.

For general fixed `d`, the generic fixed-monomial bridge supplies the conservative per-service bound `(2^d−1)(2d−1)` multiple-control NOTs, each with at most `2(d−1)` surrounding affine translations, plus one fixed phase pass. The source uses three such services, a square endpoint one, and a cube endpoint two. Their constants, highest-bit handling and repair remain charged.

For a three-native, three-role `(3,2,2)` target with all three fresh seven-axis bodies, the unchanged optimistic Gaussian invoice is

\[
 P=3[1]+6[7]+3[8],\qquad T=[24]+2[23],\qquad[r]=r^{199/200}.
\]

Its prior certified positive movement margin is `0.56100733960089153867…`. The actual ambient cap is now `d+21`, not automatically24. For `d>3`, use the previously proved compiler extension with independent ambient cap, fresh constants and real source volume; spectators are not omitted. The nine native adapters, four endpoint adapters, caller operations and nonlinear movement services remain. An actual endpoint circuit, complete ordinary/precision/recursive accounting and compatible supplier theorem are still missing. The family supplies additional exact source choices, not the target circuit itself.

## 6. Verification and provenance

The author checker exhausts all256 three-bit sign tables, builds the literal `R_f`, derives cube normalizers, and checks every source/endpoint entry. It checks the trace formula, all128 negative-valuation cases and all128 degree-at-most-two cases. Width-two controls include both finite- and infinite-order examples and verify tensor phase/sign conventions. Larger fixed dimensions receive explicitly finite checks of the general constructive cube theorem; no finite sample substitutes for the proof of arbitrary `d` or `V`.

The checker also verifies the Hadamard normalization on a deliberately nontrivial row/column scramble and rejects missing cubic phases, incorrect derivative controls, missing endpoint permutations, and tensoring of exterior native signs. It reuses the pinned exact Gaussian-dyadic helper and is author verification, not independent review.

Dependency/source credit follows the pinned common-head admission, exact tensor, source and physical packages. Retain @CubeJerry attribution, the original native/compiler contributors, and prior programme evidence. Prepared by @CubeJerry with substantial OpenAI assistance. **No new κ.**
