# Full-parabolic radial block operators have sublinear rank calibration

**Proved representation-interface theorem, independent review pending. No new κ.**

## 1. Arbitrary block multiplicity and value field

Let Ω be the135 Lagrangians of F2^6, Z a fixed Lagrangian, H=Stab(Z), and
ρ the permutation action of Sp(6,2) on Ω. The four H shells have indices
s=3−dim(L∩Z) and sizes1,14,56,64. Fix any coefficient field F, any integer
k≥1, and arbitrary matrices A0,A1,A2,A3 in Mat_k(F); they need not commute,
be invertible, be diagonalizable, or be involutions. On F^Ω tensor F^k put

    D = direct-sum_(L in Ω) A_(s(L)),
    R(g)=rank(D−(ρ(g) tensor I_k)D(ρ(g)^−1 tensor I_k)).

D commutes with H. Therefore R depends only on the H double-coset index
r=3−dim(Z∩gZ). Write q_r=R(w_r)/2 for the standard coordinate-swap
representatives. Then universally

    q_2≤q_1,                  4q_3≤5q_1.

If q1=0, all A_s coincide and every R(g)=0. Both displayed ratios are sharp,
simultaneously: A0=A1=0 and A2=A3=I_k give (q1,q2,q3)=(12k,12k,15k).
Thus no useful potential in this entire block-radial family, or nonnegative
sum of such potentials, has linear Gaussian-rank calibration q_r≥r q1.
This is not an obstruction to actual entangling callers.

## 2. Two exact triangle certificates

Define δ_st=rank(A_s−A_t). Rank subadditivity makes δ a pseudometric:
δ_st≤δ_su+δ_ut. The coefficient field and matrix size do not enter this fact.
The independently authenticated orbit-intersection matrices give

    q1=δ01+12δ12+32δ23,
    q2=δ02+3δ12+8δ13+24δ23,
    q3=δ03+7δ12+7δ13+28δ23.

Indeed each off-diagonal shell pair contributes twice its symmetric matrix
entry to the direct-sum rank, and q divides by two. Subtraction yields

    q1−q2=(δ01+δ12−δ02)+8(δ12+δ23−δ13),

    5q1−4q3=4(δ01+δ12+δ23−δ03)
             +28(δ12+δ23−δ13)+δ01+16δ23.

Every summand is nonnegative by one or two triangle inequalities. This proves
the claimed universal bounds without extrapolating a finite matrix experiment.
Since q1 is a positive weighted sum of the adjacent δ values, q1=0 forces
A0=A1=A2=A3. The sharp control follows by substitution.

More generally these formulas prove the same inequalities for any pseudometric
on four shell labels. In particular replacing cuts by arbitrary metric-valued
radial displacements cannot improve the rank-two calibration. Squared Hilbert
distance is not generally a metric: the separately reviewed Hilbert result has
the weaker sharp bound q2≤3q1/2. Its orbit values(7,3,1,0) yield96,144 and are
a deliberate negative control against applying the triangle proof to squares.

## 3. The63-point block-radial family and direct sums

For H acting on the63 nonzero vectors of F2^6, the orbits are Z\{0} of size7
and its complement of size56. GL3 is transitive on nonzero x, and the symmetric
shears C send z to z+Cx. For nonzero x, Cx ranges over all F2^3: take x=e1
and prescribe the first column of a symmetric C. This proves transitivity on
the complement; GL3 is also transitive on the nonzero Z vectors.

Thus every block-radial operator in this permutation representation has two
block values B0,B1. Its half commutator ranks are

    q_r=(8−2^(3−r)) rank(B0−B1),

because Z and w_rZ share2^(3−r)−1 nonzero vectors. The triple is proportional
to(4,6,7). Combining arbitrary multiplicities and nonnegative weights from
both the135- and63-point block-radial families still gives

    2q2≤3q1,                 4q3≤7q1.

A nonzero combination cannot have q1=0. These bounds exclude linear rank
calibration for this combined family. They do not cover operators with
nonzero blocks between different Ω positions, other group representations,
nonradial/covariant data, or nonlinear source/caller mechanisms.

## 4. Why general commutator ranks are legitimate candidates

For invertible group operators U,V,

    [D,UV]=[D,U]V+U[D,V],

so commutator rank is subadditive. It vanishes on ordinary H coefficients;
matrices of ordinary group-algebra coefficients likewise commute with the
rolewise D. For a common native head X and E=[D,X], the ordinary-cross native
has commutator diag(E,E). The square-cross native has commutator

    [[E,−(EX+XE)],[0,E]],

which elementary invertible block row/column operations reduce to diag(E,E).
Each therefore has twice the head commutator rank. Inverse orientation has
the same rank by [D,N^-1]=−N^-1[D,N]N^-1; this does not provide a free physical
inverse. This explains the attempted conservation proof and why endpoint
calibration matters. An actual phase-aware caller still requires its retained
faithful-algebra/ordinary-unit bridge before applying any such representation.
The failure proved here is independent of assuming that physical transfer.

## 5. Source pins, verification and status

The shell intersection matrices are read from Worker C's independent RREF
certificate TABLE.json and checked against Worker B's independently generated
135-space certificate. Those packages prove the group/orbit/double-coset facts.
`DEPENDENCIES.json` pins their exact bytes. The root checker verifies both
triangle identities symbolically in their six distance coefficients, all
claimed bounds on arbitrary noncommuting finite block controls over F2/F3,
the sharp cut and the squared-Hilbert countercontrol. These controls supplement
the written all-field proof; they are not its universal justification.

Worker C's scalar diagonal level-set corollary is a subcase: any field-valued
radial diagonal operator gives a nonnegative sum of the same cuts. The present
rank-metric proof further allows arbitrary matrix blocks and multiplicities.
Credit @CubeJerry; root's full-parabolic representation question and block
rank-metric extension; Worker B's core cut enumeration; Worker C's independent
intersection matrices and diagonal/Hilbert derivations; retained source and
phase predecessors. OpenAI assistance. No profitable caller, strict supplier,
foundational discharge or new complete κ follows.
