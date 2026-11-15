# Two full ordinary interstages admit a dihedral shadow

**Status: proved in the stated group-algebra model; independent review
pending. No new κ.** The theorem closes the entire three-native attempt with
two arbitrary full ordinary interstages and scalar/cyclic endpoint gauges.
It does not close arbitrary head-dependent ordinary endpoint encodings.

## 1. The precise source-bound consequence

Use the actual three-head source at programme baseline
`eefa411ebab86271d50b56b6953af3a157366bdb`. Its head is `A=C_b S₃`, and

\[
A^3=C_aC_bC_c,\quad A^6=X_aX_bX_c,\quad A^{12}=I.
\]

The Gaussian ranks of its powers modulo six are `(0,1,2,3,2,1)`. The actual
native halves in their authenticated ordinary gauges are

\[
L(a)=\begin{pmatrix}a&I\\0&a\end{pmatrix},\qquad
U(a)=\begin{pmatrix}a&-a^2\\0&a\end{pmatrix},\qquad a=A^{\otimes V}.
\]

Inactive retained roles carry identity head action. The native field-level
minus is a complex coefficient outside the tensor power. Literal inverses
are permitted in the algebraic statement; a physical use requires its actual
source service and paid costs.

At each tensor width, allow arbitrary invertible role matrices over the full
ordinary monomial Clifford algebra on these three head coordinates. There
are exactly two such unrestricted interstages, so the word is

\[
N_3 Q N_2 P N_1
  = E\operatorname{diag}(a^{k_1},\ldots,a^{k_R})F.             \tag{1}
\]

Each `N_j` is one native half on any pair of the R retained roles, possibly
with scalar role gauges or literal inversion. The endpoint matrices E,F
have entries in `C[a⁶]` and are invertible. Their coefficients may depend on
the width. Every role remains an independent arbitrary-input Gaussian job.
No role is granted clean, discarded, or omitted. The native's fixed internal
authentication gauges are included in its actual interface; they are not
additional unrestricted endpoint gauges.

**Theorem 1.** Every exact all-width caller (1) satisfies

\[
H=\sum_i\min(k_i\bmod6,6-k_i\bmod6)\le6.                  \tag{2}
\]

Thus (3,2,2) on three retained roles and (3,3,1,1) on four retained roles are
both excluded in this scope, with every mix of L/U orientations and arbitrary
full ordinary interstages. Arbitrary head-dependent ordinary E,F remain
outside the theorem. This distinction cannot be removed by saying that
Gaussian rank is an ordinary double-coset invariant.

The proof first establishes a general algebraic reduction. It uses an
ordinary character only as a necessary consequence of an actual unit; it
does not mistake a character-level solution for a physical caller.

## 2. A partial-isometry lemma for an even cycle

Let `C_{2d}` have vertices `j mod 2d` and circular distance
`δ(i,j)=min(|i-j|,2d-|i-j|)`.

**Lemma 2.** Every distance-preserving injection from a subset of the cycle
containing 0 into the cycle, fixing 0, is the restriction either of `j↦j`
or of `j↦−j`.

**Proof.** A vertex j must map to j or −j because its distance from 0 is
preserved. Vertices 0 and d are fixed by both possibilities. For two
nonfixed vertices, their orientation choices must agree: after choosing
representatives `0<i,j<d`, the two possible distances between them are
`|i-j|` and `min(i+j,2d-i-j)`. These are unequal, since equality would force
one representative to be 0 or d. This also handles two distinct vertices
at the same distance from 0; injectivity forces their opposite positions.
Consequently all nonfixed vertices have one common orientation. If the
domain contains only 0,d, either orientation extends the map. ∎

## 3. The ordinary subgroup sees an isometric six-cycle

Pass temporarily to the symplectic quotient `G=Sp(6,2)`. Write `a` for the
image of A and let `H₀` be the stabilizer of the computational Lagrangian
`Λ₀`. This is the image of the full ordinary monomial Clifford subgroup.
The element a has order six. Its six Lagrangians `Λ_j=a^jΛ₀` satisfy

\[
d(\Lambda_i,\Lambda_j)
 =3-\dim(\Lambda_i\cap\Lambda_j)
 =\min((j-i)\bmod6,6-(j-i)\bmod6).                         \tag{3}
\]

The equality follows from the actual source's six Gaussian ranks and
symplectic invariance. In particular the six Lagrangians are distinct.

For any `h∈H₀`, consider those indices v for which `hΛ_v` is again on this
cycle. The induced partial map fixes 0 and preserves (3). Lemma 2 supplies
an orientation `ε_h∈{+1,−1}` such that

\[
h\Lambda_v=\Lambda_{\epsilon_h v}
\quad\hbox{whenever }h\Lambda_v\hbox{ is on the cycle}.    \tag{4}
\]

Only the existence of this orientation is needed; it need not define a
homomorphism on H₀.

## 4. A linear bimodule map to the dihedral algebra

Let `C=⟨a⟩`. Decompose the group basis of `C[G]` into double cosets `CgC`.
For each double coset meeting H₀, choose a representative `h∈H₀` and one
orientation ε supplied by (4). Let `D₁₂=⟨x,τ:x⁶=τ²=1,τxτ=x⁻¹⟩`.
Put `e=0` for ε=+1 and `e=1` for ε=−1. Define on this double coset

\[
\mathcal T(a^u h a^v)=x^{u+\epsilon v}\tau^e.              \tag{5}
\]

On double cosets disjoint from H₀, set T to zero. On the identity double
coset choose ε=+1, so `T(a^j)=x^j`.

**Lemma 3.** Formula (5) is well-defined and extends to a complex-linear
map satisfying

\[
\mathcal T(a^r Z a^s)=x^r\mathcal T(Z)x^s,
\qquad
\mathcal T(\mathbb C[H_0])\subseteq\mathbb C[\langle\tau\rangle].
                                                               \tag{6}
\]

Every ordinary group element is sent to either I or τ. Consequently
evaluation at `τ=+1` after T is the ordinary augmentation character.

**Proof.** If `a^u h a^v=a^{u'} h a^{v'}`, then
`a^{u-u'} h a^{v-v'}=h∈H₀`. Applying this to Λ₀ gives
`hΛ_{v-v'}=Λ_{-(u-u')}`. Equation (4) implies
`(u-u')+ε(v-v')=0 mod6`, proving well-definedness.

If `a^u h a^v∈H₀`, then `hΛ_v=Λ_{−u}`, so `u+εv=0` and its image is τᵉ.
The left/right covariance follows from `τᵉx^s=x^{εs}τᵉ`.
Summing the ordinary coefficients gives the augmentation claim. ∎

T is generally not multiplicative. The next argument uses exactly the
linear two-interstage reduction; it never applies T to an arbitrary product
of ordinary factors.

## 5. A unit in the original linear space forces a dihedral unit

The following statement permits any retained-role count R. Let
`N₁,N₂,N₃,D` be invertible matrices over `C[C]`, and suppose ordinary units
`P,Q∈GL_R(C[H₀])` satisfy `N₃ Q N₂ P N₁=D`. Set

\[
R_0=P^{-1},\quad B=N_3^{-1}DN_1^{-1},\quad
Q=BR_0N_2^{-1}.                                           \tag{7}
\]

The right side is linear in R₀. Apply T entrywise and use (6). Write

\[
\mathcal T(R_0)=R_++R_-\tau,\qquad
\mathcal T(Q)=Q_++Q_-\tau,
\]

where the four coefficient matrices have complex scalar entries. The even
and odd dihedral components in (7) are independent. Therefore, for every
complex scalar λ,

\[
Q_++\lambda Q_-\tau
 =B(x)(R_++\lambda R_-\tau)N_2(x)^{-1}.                   \tag{8}
\]

Since R₀ is an ordinary unit, its augmentation is invertible. By Lemma 3,
that augmentation is `R_++R_-`. Hence

\[
p(\lambda)=\det(R_++\lambda R_-)
\]

is not the zero polynomial (`p(1)≠0`). Choose λ avoiding the finite zeros of
`p(λ)p(−λ)`. Then both `R_++λR_-` and `R_+−λR_-` are invertible. These are
the two character evaluations of `R_++λR_-τ`, so this matrix is a unit over
`C[⟨τ⟩]≅C×C`. Equation (8) makes `Q_++λQ_-τ` a unit as well, because B
and N₂ are units in the dihedral algebra. Its inverse remains ordinary by
finite-dimensional inverse closure.

Thus (8) reconstructs an exact dihedral caller with the same three cyclic
blocks and same endpoint, whose two interstages are ordinary units over
`C[⟨τ⟩]`. This is an auxiliary algebraic consequence, not a proposed free
physical implementation. The generic λ step is justified by a nonzero
polynomial; no random search or guessed nonsingularity is used.

## 6. Dihedral conservation

On six basis vectors `e_j`, represent `x e_j=e_{j+1}` and
`τe_j=e_{2−j}`. Let P₀ be diagonal with signs `(+,+,+,−,−,−)`. This auxiliary
reflection differs from the geometric reflection fixing 0; both satisfy
the same dihedral relation. The auxiliary τ preserves the two sign arcs,
so its permutation matrix commutes with P₀. For every integer k,

\[
\operatorname{rank}\bigl(\rho(x^k)-P_0\rho(x^k)P_0\bigr)
 =2\min(k\bmod6,6-k\bmod6).                               \tag{9}
\]

Use the two representations `ρ` and `P₀ρP₀`. They agree on the entire
ordinary algebra `C[⟨τ⟩]`, including the constructed unit interstages.
Each L native has difference rank four. Each U native also has difference
rank four: if X,Y are the two images of x and `E=X−Y`, its difference is

\[
\begin{pmatrix}E&-(X^2-Y^2)\\0&E\end{pmatrix},
\quad X^2-Y^2=XE+EY,
\]

which reduces to `diag(E,E)` by invertible triangular row and column
operations. Inversion and scalar role gauges preserve this rank. Inactive
roles contribute zero.

Telescoping the product difference of the shadow caller gives endpoint
difference rank at most twelve. Independent endpoint powers contribute
exactly `2H` by (9); invertible ordinary endpoint gauges preserve it. Hence
`2H≤12`, proving (2) in the symplectic quotient.

The same argument applies to three cyclic blocks containing more natives
or cyclic-power queries, provided only two unrestricted ordinary interstages
separate them. Its bound is `H≤2m+Σ rank(query)`. It does not cover three
or more unrestricted interstages separated by nonordinary blocks.

## 7. Why the quotient is legitimate for an all-width obstruction

Retain the actual finite scalar lift of the Clifford group and its full
centre. At arbitrarily large widths divisible by the centre's exponent, all
central tensor characters are trivial. The credited tensor Gram-separation
argument makes the physical representation faithful on the corresponding
phase-exact projective group algebra at every sufficiently large such width.
The exact retained statement is Theorem 1 and the phase-exact group paragraph
in `results/complex-tensor-rank-components/author/PROOF.md`, Section 2;
its file hash and the actual source-cycle proof hash are pinned in
`DEPENDENCIES.json`. The centre-divisible subsequence sets its cocycle
`ζᵢⱼ^ρ` to one with `ρ=0`; faithfulness follows from `(m−1)c^V<1`.
An asserted all-width identity therefore lifts to that finite group algebra.
Every ordinary inverse also lifts by finite-dimensional inverse closure.

The projective Clifford group has the Pauli normal subgroup, and quotienting
it yields Sp(6,2). This is a unital algebra homomorphism, so actual units
remain units. The actual source maps to the order-six a used above; ordinary
monomial maps land in H₀. The endpoint `C[a⁶]` gauges map to invertible
scalar role matrices. Thus the quotient identity obeys the hypotheses of
Sections 3–6.

This does not delete the physical eigenspace on which `a⁶` acts as `−I`, or
declare `a⁶=I` in the physical caller. Globally `a⁶=(X_aX_bX_c)^{⊗V}` is
an ordinary translation. The proof uses a necessary quotient of an exact faithful lift on
one infinite admissible width subsequence. A caller required at all widths
must survive that subsequence. Field-level signs and scalar coefficients
remain ordinary complex numbers; in particular `−a²` maps to `−x²`.

## 8. Complete invoice and precise remaining construction

With three fresh rank-seven bodies and R retained roles, including all
`3(R−2)` inactive-role body calls, the Gaussian price is

\[
P_t=3R[7]+3[1]+3([8]-[7]),\qquad [r]=r^t,\quad0<t<1.
\]

Set `d_t=8^t−7^t`. Concavity gives
`Σ_i[21+r_i]≤3R[7]+d_t H`. With H≤6,

\[
P_t-T_t\ge3(1-d_t)>0.                                    \tag{10}
\]

Thus no complete saving is possible in this source/common-body family with
the stated two full interstages and cyclic endpoint gauges, even before
adding all ordinary, compiler, precision, ownership and recursive costs.
The actual spectator volume multiplier `2^V` is common and has not vanished.
All five foundational assumptions remain.

The next construction must change a premise not removed by the proof:
genuinely head-dependent ordinary endpoint encodings; a fourth nonordinary
block giving a third unrestricted interstage; a different authenticated
head/source or body geometry; or another expressly priced representation.
Enlarging the two internal ordinary coefficient catalogues is insufficient.

## 9. Verification and provenance

`check.py` reconstructs the isometric six-cycle, enumerates all 10,752
ordinary symplectic stabilizers and every resulting cyclic double coset,
checks the partial-isometry and well-definedness statements, and verifies
the dihedral source-difference ranks and sign controls. These are exact
finite diagnostics of the stated finite geometry. The universal group-
algebra/unit argument is the written proof above.

Dependencies are the admitted actual three-head source, the finite-group
tensor-separation theorem, and the independently rederived two-interstage
linear reduction. The earlier cyclic conservation package supplies the
source model and invoice; its ordinary algebra was smaller, so it did not
already establish the present two-full-interstage theorem.

Credit @CubeJerry, the credited source/tensor-separation authors, and the
lead/Worker B's independent linear reduction. The new dihedral shadow and
unit deformation were developed by Worker B with OpenAI assistance.
