# An explicit ordinary inverter and faithful dihedral head algebra

**Proved structural extension, pending independent admission.** The new pentagonal head has an explicit ordinary monomial involution T with TBT=B^-1. Its ten-element dihedral algebra is faithful at every width V>=2 and gives a concrete noncommuting next caller model. This is an enabling source/interface lemma, not a synthesized caller or new kappa.

## 1. Exact operator and service

Use B from `PROOF.md`, with one-column coordinate index j=u+2v. Define

    T e_0=e_1, T e_1=e_0, T e_2=-e_2, T e_3=e_3.

Equivalently its permutation is (1,0,2,3), with input phase exponents (0,0,2,0) modulo four. The permutation is the affine binary map (u,v)->(u+v+1,v), and the phase is (-1)^(v(1+u)). T is therefore an actual ordinary coordinate permutation plus an ordinary quadratic sign pass.

Exact multiplication gives T^2=I and TBT=B^4=B^-1. Every identity is multiplicative, so T_V=T^(tensor V) is an ordinary involution satisfying T_V B_V T_V=B_V^-1 at every width. One service costs one actual coordinate permutation and one sign pass, with at most D scalar sign applications. It creates no owner, added denominator or Gaussian call. Its ordinary layout/tape costs remain charged.

## 2. The exact dihedral algebra

The ten operators B^k T^e, k=0,...,4 and e=0,1, obey the dihedral multiplication law. They are distinct: rotations have order five, T has order two, and no T can be a power of B. No extra scalar cocycle occurs in these displayed generators. Multiplication by ordinary T preserves Gaussian rank, so their rank sequence is (0,1,2,2,1) in either e column.

The one-column representation has trace 4 at identity, -1 at a nonidentity rotation and 0 at every reflection. For reflection trace, T maps the eigenspace of a nontrivial fifth root lambda to that of lambda^-1; these are distinct, so B^kT has zero trace. Thus the representation is exactly the sum of the two inequivalent two-dimensional dihedral irreducibles.

At tensor width V, the character is 4^V at identity, (-1)^V on each nonidentity rotation and 0 on every reflection. Character orthogonality gives multiplicities

    a(V)=(4^V+4(-1)^V)/10

for each one-dimensional representation, and

    b(V)=(4^V-(-1)^V)/5

for each two-dimensional representation. These are positive for every V>=2. Hence the group-algebra representation is faithful for every such V: every simple matrix block occurs. A fixed head circuit over C[D10] can therefore be verified in this exact ten-element algebra, with no tensor-width extrapolation.

At V=1 the two one-dimensional blocks are absent. This is a genuine uniformity distinction, and a four-coordinate operator identity may use absent blocks incorrectly. Both one-dimensional blocks must be checked in a proposed uniform caller, even if the two physical two-dimensional blocks already agree at one column.

## 3. A concrete ordinary interstage class

The next exact caller class uses ordinary matrices with entries alpha I+beta T_V, where alpha,beta are fixed Gaussian-rational scalars. These can act differently on the T_V=+1 and T_V=-1 subspaces, so this class genuinely exceeds scalar C5 role mixing. It remains a small explicitly implemented algebra.

For distinct fields X,Y, an elementary shear

    X <- X + (alpha I + beta T_V)Y

has an actual ordinary implementation: X+=alpha Y; apply T_V to Y; X+=beta Y; apply T_V again to Y. Y is restored and no copied field is retained. A nonzero scalar-weighted ADD can itself be implemented by SCALE(source), ADD, inverse SCALE(source). Thus a conservative count is two ADDs, four fixed scalar SCALEs and two T_V services per shear. Zero coefficients simply remove their service. All constants and inverses must be included in the fixed compiler catalogue.

A diagonal unit a I+b T_V is invertible exactly when a+b and a-b are both nonzero. On a fixed point of the signed monomial T_V with sign tau, it is the scalar a+b tau. On a two-cycle with sign s in {+1,-1}, it is the two-coordinate matrix [[a,bs],[bs,a]]. If a is nonzero, its explicit LDU factorization is

    [[1,0],[bs/a,1]] diag(a,(a^2-b^2)/a) [[1,bs/a],[0,1]].

This is an in-place finite scalar circuit, with no stored copy. If a=0, the unit is simply b T_V. The inverse is (a I-b T_V)/(a^2-b^2). Pair enumeration, pairing/unpairing and tape/layout access are explicit ordinary work; this identity does not make nonlocal pair access free. The displayed constants are Gaussian-rational when a,b are, and their bounds are fixed before V varies.

Since C[T_V] is the direct product of its two eigenspace scalar algebras, a fixed matrix A_0+A_1 T_V is invertible exactly when A_0+A_1 and A_0-A_1 are invertible. Separate Gaussian elimination on those two fixed matrices expresses it as finitely many such controlled shears, units and swaps. This supplies a concrete compilation route for a successful exact rational caller certificate; its resulting number of services, constants, coefficient growth, pair layout and precision invoice must be recorded. An arbitrary numerical solution is not such a certificate.

## 4. Synthesis problem and its subsequent closure

**Same-session update:** `PENTAGONAL-DIHEDRAL-GATE.md` now proves that every common-body caller in this C[T_V] family has a strictly failing Gaussian invoice, including the proposed inventory below. The source and ordinary implementation lemmas remain valid. The proposal is retained to explain the investigation; it is no longer an open caller task in C[T_V]. Full monomial Clifford interleavings outside this subalgebra remain open.

The one-native query gate excludes three rank-two jobs with only two one-bank queries even in this larger ordinary family. The next small test is one native plus three rank-one queries on three arbitrary roles, with all ordinary interstage encodings explicitly in Mat_3(Q(i)[T_V]). The full ten-element algebra, including both one-dimensional blocks absent at width one, must be checked.

Its optimistic common-body Gaussian invoice is target 3[9] against price 4[1]+2[7]+[8], before all ordinary and supplier costs. At t=199/200 a numerical planning estimate of the margin is 0.923298066532315..., not a rigorous admission certificate. A successful caller, exact rational or certified algebraic constants, complete ordinary compilation, and strict uniform supplier admission are still missing. The three-native/four-role route remains another open option.

Finite numerical synthesis is exploratory only. Failure of a finite template or numerical optimizer proves no all-circuit obstruction. The larger full monomial Clifford family remains outside any restriction to C[T_V]. No new kappa or foundation discharge is claimed.
