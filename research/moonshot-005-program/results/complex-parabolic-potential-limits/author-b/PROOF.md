# Full-parabolic Lagrangian signed cuts cannot certify Gaussian-rank conservation

**Status:** proved finite-family obstruction, with an exact exhaustive certificate and an independently implemented audit. **No new κ.** This result rejects a proposed conservation potential; it does not reject a physical caller or establish a full-ordinary supplier obstruction.

## 1. Proposition and exact scope

Let V be the six-dimensional symplectic vector space over F₂, let Ω be its 135 Lagrangian subspaces, fix a Lagrangian Z, and let H=Stab(Z) in Sp(6,2). Let ρ be the complex permutation representation on Ω. For any diagonal sign involution J in the standard Ω basis that commutes with every ρ(h), h∈H, define

    h_J(g) = rank(ρ(g) − Jρ(g)J)/2.

This quantity depends only on r(g)=3−dim(Z∩gZ). Write its values as h₀,h₁,h₂,h₃. Then

    h₂ ≤ h₁,                 4h₃ ≤ 5h₁.

The same inequalities hold for every nonnegative real combination of these potentials. If such a combination has h₁=0, it is identically zero. Consequently no useful combination satisfies h_r≥r h₁ for both r=2,3; in fact rank two already prevents this.

The statement covers **all diagonal H-invariant sign involutions in this permutation basis**, not all H-intertwining involutions or all representations of Sp(6,2). It also covers real radial L¹ displacement potentials by the coarea argument below. A separate short argument in §6 excludes exact rank-two additivity for arbitrary Hilbert-valued radial functions in this same permutation representation.

## 2. The full parabolic and its four orbits

Write a vector as (x,z) and Z={(0,z)}. Every stabilizer element has the form

    [[B,0],[CB,B^{-T}]],       B∈GL₃(F₂), C=Cᵀ.

Thus |H|=168·64=10752. Six symmetric shears (three diagonal and three off-diagonal) together with the six ordered elementary GL₃ transvections generate H. They are precisely ordinary monomial symplectic transformations; the off-diagonal shears include entangling CZ and the linear transvections include CNOT.

The H-orbits on Ω are the shells d(L)=3−dim(L∩Z), with sizes

    d:       0   1   2   3
    size:    1  14  56  64.

The exact checker authenticates the displayed generators, proves their symplectic and Z-preserving properties, and computes their four orbits. Since every element of H preserves d and this explicitly generated subgroup is already transitive within each shell, these are exactly the full H-orbits. Equivalently the orbit statement follows by extending bases of L∩Z to adapted symplectic bases.

For completeness, the permutation action is faithful as a **group action**. Each of the 63 nonzero vectors belongs to 15 Lagrangians, whose intersection is exactly its line. A linear symplectic transformation fixing every Lagrangian therefore fixes every nonzero vector. This does not assert that the 135-dimensional representation is faithful as a group-algebra representation.

A diagonal J commutes with H exactly when its signs are constant on these four orbits. Complementing every sign leaves the displacement unchanged. We may therefore require shell zero to be positive and enumerate precisely eight possibilities.

## 3. Rank is the cut displacement

Let S⊆Ω be the positive-sign set. In column L, the matrix ρ(g)−Jρ(g)J is zero if L and gL have the same sign, and otherwise is ±2 times the distinct basis vector indexed by gL. Hence

    rank(ρ(g)−Jρ(g)J) = |S Δ gS| = 2h_J(g).

The parity follows because |gS|=|S|. Since J commutes with H, this rank is constant on H double cosets. The double cosets are indexed by r=3−dim(Z∩gZ): H is transitive on the shell of gZ, and equal images of Z differ on the right by H. Representatives w_r swap x_i,z_i for i≤r and fix the other coordinates. Thus the following complete table determines the potential on every element of Sp(6,2).

| Positive shells | h₁ | h₂ | h₃ | 2h₁−h₂ | 3h₁−h₃ |
|---|---:|---:|---:|---:|---:|
| {0} | 1 | 1 | 1 | 1 | 2 |
| {0,1} | 12 | 12 | 15 | 12 | 21 |
| {0,2} | 45 | 27 | 36 | 63 | 99 |
| {0,1,2} | 32 | 32 | 36 | 32 | 60 |
| {0,3} | 33 | 33 | 35 | 33 | 64 |
| {0,1,3} | 44 | 28 | 35 | 60 | 97 |
| {0,2,3} | 13 | 11 | 14 | 15 | 25 |
| {0,1,2,3} | 0 | 0 | 0 | 0 | 0 |

Every row satisfies h₂≤h₁ and 4h₃≤5h₁. Every nonconstant row has positive h₁. Multiplication by nonnegative real weights and addition preserve these inequalities. Therefore the only combination with h₁=0 is the zero potential, and every useful combination has h₂≤h₁<2h₁. This is an exact separating certificate for the entire cone, rather than a failure of a sampled optimization.

## 4. Why the desired inequality would have mattered

The proposed method sought a potential that was unchanged by every full ordinary parabolic stage and detected Gaussian endpoint rank at least linearly. Its native accounting uses an exact noncommutative identity. Set X=ρ(a), Y=JXJ, E=X−Y for a native rank-one head. For the ordinary-cross native, the difference is block diagonal with two copies of E. For the square-cross native, its difference is

    [[E, −(X²−Y²)], [0,E]],   X²−Y²=XE+EY.

Add X times the second block row to the first, then add the first block column times Y to the second. The result is diag(E,E). Both operations are invertible. Thus either native orientation has difference rank 2rank(E)=4h₁. Inverting a native preserves its difference rank by multiplication with invertible matrices; this statement does not supply a free physical inverse.

Rank subadditivity under composition would give Σ h_{r_j}≤2m h₁ for m native calls and independent Gaussian endpoints, after a legitimate transfer from the actual phase-aware source algebra to this representation. If h_r≥r h₁ and h₁>0, it would follow that Σr_j≤2m, closing the full entangling-ordinary family by the earlier invoice argument. The table proves that this particular attempted transfer potential cannot supply that implication. It leaves the physical entangling caller open.

No physical scalar phase has been discarded in an admitted construction here. Applying any representation to an actual all-width caller still requires the separately retained faithful phase-algebra reduction and ordinary-unit transfer. The finite-family failure in §§1–3 does not depend on asserting that reduction or on any of the five multiplication foundations.

## 5. Two useful finite-family extensions

For a real H-radial scalar function f on Ω, the L¹ displacement Σ_L|f(L)−f(gL)| is a nonnegative linear combination (or threshold integral) of the cut displacements: sort its four orbit values and use the layer-cake decomposition of absolute differences. Every threshold set is a union of the four shells. Thus it too has h₂≤h₁ and cannot provide linear Gaussian-rank detection.

The previously considered cut on the 63 nonzero Pauli labels has positive set Z\{0}. Its half symmetric differences are (h₁,h₂,h₃)=(4,6,7), because Z and w_rZ intersect in 2^{3−r}−1 nonzero vectors. Including this specified cut along with all eight Lagrangian cuts still gives the exact cone bounds

    2h₂≤3h₁,                 4h₃≤7h₁.

Thus nonnegative mixing of these two finite representation families also fails. This statement concerns that specified 63-point cut, not every possible sign function in every other representation.

## 6. Radial Hilbert additivity: a three-space proof

The following strengthening was independently supplied by Worker C during review. Let f:Ω→K be H-radial, where K is a real or complex Hilbert space, and define D_r=Σ_L||f(L)−f(w_rL)||². Let s₁,s₂ be the individual first and second coordinate swaps, so w₁=s₁ and w₂=s₁s₂. Let U₁,U₂ be their commuting permutation involutions. H symmetry makes their displacements equal. Decomposing the function f into their four joint eigenspaces gives

    D₂ = 2D₁ − 8||P_{--}f||².

Therefore D₂≥2D₁ would force (I−U₁)(I−U₂)f=0. Write v_d for the value of f on shell d. Choose symplectic pairs e_i,f_i with Z=span(e₁,e₂,e₃). Three Lagrangians have distance tuples under (I,s₁,s₂,s₁s₂) as follows:

- span(e₁,e₂,e₃): (0,1,1,2);
- span(e₁,e₂,f₃): (1,2,2,3);
- span(e₁+e₂,e₃,f₁+f₂): (1,2,2,1).

The mixed-difference equation then gives

    v₀−2v₁+v₂=0,   v₁−2v₂+v₃=0,   2(v₁−v₂)=0.

Over a real or complex Hilbert space these force all four values equal. Hence every nonconstant radial f has D₂<2D₁. The checker verifies the three actual Lagrangians and all distance tuples. Squared Hilbert displacements are not asserted to be subadditive native-cost invariants; this section only rules out another proposed endpoint-detection family.

## 7. Exact verification, provenance, and open direction

Run, from this package directory:

    python check.py --out RESULT.json --spaces-out LAGRANGIANS.json

The checker uses only the Python standard library. It enumerates all unordered triples of the 63 nonzero vectors, rejects dependent or nonisotropic triples, and takes their spans. Every Lagrangian contains an independent triple, so the enumeration is exhaustive. It finds 3780 unordered isotropic bases and 135 distinct Lagrangians, consistently with 28 unordered bases per three-space. The complete finite certificate stores every space, generator, and representative. Controls cover the constant cut, complements, a nonradial singleton that fails H invariance, symplecticity, orbit completeness, line recovery, and the three-space analytic certificate.

Worker C independently enumerated all 1395 three-dimensional subspaces by a fresh RREF method, retained the 135 isotropic ones, authenticated full H orbits, and obtained the same table without importing this checker. Its separate review package records exact pins and additional optional derivations.

Credit: @CubeJerry's persistent programme; root proposed the full-parabolic Lagrangian representation; Worker B developed the finite-family certificate and native-method interpretation; Worker C independently checked it and contributed §6. AI-assisted research. Previous source, phase, and invoice results retain their existing attribution.

The next mathematical direction remains an actual caller using noncommuting entangling ordinary interstages, or a different proven representation invariant. A non-diagonal H-intertwiner, another representation, or a genuinely different structural potential remains outside this obstruction. No complete supplier or multiplication bound follows from the present result.
