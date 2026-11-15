# A modular parabolic filtration forces essential dyadic ordinary coefficients

**Status: proved scoped algebraic obstruction, awaiting independent review. No new κ.**

The full entangling monomial subgroup admits an exact Gaussian-rank filtration
in residue characteristic two. This differs from the previously exhausted
characteristic-zero radial commutator potentials. It applies to every fixed
number of head coordinates and every call count, but only to callers whose
ordinary group-algebra coefficients admit the stated characteristic-two
specialization. Half-integral ordinary algebra can escape this hypothesis.
No claim is made that a profitable caller in that larger algebra exists.

## 1. Formal source model and the coefficient hypothesis

Fix a finite unitary Clifford group G on d binary head coordinates, d >= 2,
including its scalar centre Z. Let H be the computational monomial subgroup.
Its symplectic image stabilizes the computational Lagrangian L in F2^(2d).
The actual native source and monomial boundary admission are the pinned
`complex-entangling-native-source` construction. Each native has rank-one
head a and one of the two forms

    N0(a) = [[a,1],[0,a]],
    N2(a) = [[a,-a^2],[0,a]].

Role permutations, signs, literal inverses, and independently chosen admitted
monomial gauges are allowed. Inactive roles carry the identity on the heads.
The seven-axis body and every Gaussian and ordinary cost remain physical.

At tensor width V, write phi_V(g)=g^(tensor V). For sufficiently large V the
finite phase-exact algebra

    A_V = C[G] / (z - chi_V(z)1 : z in Z)

embeds faithfully in the physical operators, by the programme's proved tensor
separation theorem. Ordinary stages are role matrices over the image of C[H].
All endpoint roles are independent Gaussian Clifford jobs, up to invertible
ordinary outer encodings, and no input is zeroed, identified or discarded.

Here is the extra hypothesis, which is not a condition of the general model:
there is a number field K containing the entries of G and all scalar
coefficients at a faithful width, a prime p of its ring of integers above 2,
and every scalar coefficient of the ordinary matrices AND their actual
inverse/outer encodings belongs to the local DVR O=O_(K,p). Equivalently, the
ordinary stages are units over O[H] in this phase-exact description. It is
enough to give actual elementary ordinary circuits with O coefficients and
O-unit scalar multipliers. Coefficients may depend on V; the hypothesis is
required at any one sufficiently large faithful width used below.

For rational scalar coefficients, the usual sufficient condition is that no
reduced denominator is even. Unit phases remain group elements, rather than
being silently erased. A larger class is permitted whenever the ordinary
coefficient ring and chosen finite integral representation have a compatible
nonzero characteristic-two specialization.

The conclusion is a restriction on **ordinary group-algebra coefficients**.
It does not say that a real implementation must execute arithmetic division
by two. For example, a conditional bank permutation may have a half-integral
expansion in a collective monomial basis even if its physical table contains
only zeros and ones. That distinction is essential.

## 2. Main theorem

Let m be the number of paid native halves, and let q_j be the Gaussian rank of
each additional paid query. A query may be an in-place invertible head job or
a distinct-bank additive shear with that head coefficient. Assume every
nonzero scalar multiplying a query has nonzero residue; dropping this premise
only lowers its contribution and leaves the upper bound valid. Let r_i be the
Gaussian ranks of the independent endpoint jobs. Under Section 1's coefficient
hypothesis,

    sum_i r_i <= 2m + sum_j q_j.                         (1)

There is no bound on d, m, the number of roles, the number of ordinary
interstages, or the finite support of their coefficients, except that each is
fixed independently of V. Arbitrary entangling CNOT/CZ monomial interstages
are included. The theorem is conditional on this stated algebraic interface;
it is not an unconditional multiplication lower bound.

## 3. The crossing-block rank

Let F be any field of characteristic two. On F^(2d) use the basis (x,z), so
L is the z subspace. For a matrix T acting on R copies of this space define
b(T) to be the rank of its block from all input z coordinates to all output x
coordinates. Blocks are grouped globally by the filtration, not by role.
For arbitrary compatible matrices T,U,

    B(TU) = A(T)B(U) + B(T)D(U),
    b(TU) <= b(T)+b(U).                                (2)

Every ordinary symplectic h has B(h)=0. Any matrix over the group span of H
therefore also has B=0. If it is invertible and its inverse is ordinary, both
its x and z diagonal filtration blocks are invertible; hence multiplying on
either side preserves b. A symplectic head g has

    b(g)=rank_F2 B(g)=r(g),

and the rank remains r(g) after extension from F2 to F.

For N0(g), the crossing block is diag(B(g),B(g)), so b(N0)=2r(g).
For N2(g), it is

    [[B(g), -(A(g)B(g)+B(g)D(g))], [0,B(g)]].

Adding A(g) times the second block row to the first, and then adding the first
block column times D(g) to the second, reduces it to diag(B(g),B(g)). Thus
b(N2)=2r(g) as well. These are invertible row/column operations on the crossing
block; no physical primitive has been introduced. Native inversion has the
same crossing rank: for an invertible full matrix T,

    b(T)=dim(L_R)-dim(L_R intersect T L_R)=b(T^-1).

The middle equality follows from the kernel of pi_x T|L_R; applying T^-1 to
the intersection gives the last equality. Ordinary gauges preserve b. Each
query of rank q has crossing rank at most q, with equality for a nonzero
residue scalar. Independent diagonal endpoints have crossing rank sum_i r_i.
Applying (2) to the whole word proves (1) in a genuine residue-field model.
The remaining issue is constructing that model from the physical phase algebra.

## 4. Phase-safe transfer through an invariant lattice

This step is required: replacing physical Clifford phases by a binary
symplectic matrix without a faithful algebra transfer would be invalid.

Choose a faithful width V and use the actual physical representation phi=phi_V
on a D-dimensional K space. There exists a full O-lattice Lambda invariant
under every g in G. Indeed start with any full free O-lattice Lambda0 and set

    Lambda = sum_(g in G) phi(g)Lambda0.

The sum is finite and spans K^D. Over the DVR O it is a free rank-D lattice.
The finite group permutes its summands, so phi(g)Lambda=Lambda. Thus, in a
basis of Lambda, every phi(g) and its inverse have O entries. Reduction
modulo p gives an invertible representation phibar:G->GL_D(F), where
F=O/p. A central scalar z acts by the residue of its ACTUAL phase chi_V(z).
No assumption that a one-column Gaussian matrix is entrywise integral in the
standard computational basis is made; Lambda is an auxiliary proof object.

Let s:G->Sp(2d,F2) be the symplectic quotient and define

    Psi(g)=s(g) tensor phibar(g).                       (3)

This is multiplicative. For every z in Z, s(z)=I and
Psi(z)=residue(chi_V(z))I. Consequently (3) respects precisely the reduced
central relations of A_V. Start from the physical identity, lift it to A_V
using faithfulness, express it in distinct projective group representatives,
and reduce its O coefficients. The lifted coefficients vanish before
reduction, so the reduced identity is valid. Apply (3) to that identity.

In this model the crossing block of Psi(g) is B(s(g)) tensor phibar(g).
Invertibility of phibar(g) gives its rank exactly r(g)D. Every ordinary
coefficient preserves the filtration. Each native has crossing rank 2D by
the same square identity as in Section 3, and query rank is at most qD.
The endpoint has rank D sum_i r_i. Ordinary unit images remain invertible
because their inverses are included over O. Cancel D to prove (1) for the
physical caller. The actual central phase character is retained throughout
lifting and only reduced by a legitimate ring homomorphism afterward.

For a finite 2-power scalar centre, all its residues happen to be one, but
that is a consequence of (3), not an unsupported identification in C. The
argument does not rely on choosing a special width residue. It also permits
larger finite scalar centres as long as the corresponding actual residues
are used.

## 5. Full common-body price consequence

Assume the retained common-body architecture: each of m native stages adds
seven fresh axes to all R retained roles, paying m(R-2) rank-seven idle jobs.
Head operations leave those body axes fixed. Write [u]=u^t with 0<t<1, and
Delta=[8]-[7]. Its paid Gaussian profile is

    P = mR[7] + m[1] + m Delta + sum_j [q_j].

Endpoint ranks are 7m+r_i. Since (7m)^t <= m 7^t for m>=1, and decreasing
unit increments above 7 give

    T = sum_i [7m+r_i] <= mR[7]+Delta sum_i r_i,

(1) yields

    P-T >= m(1-Delta) + sum_j ([q_j]-q_j Delta).          (4)

The last summands need not all be positive for arbitrarily large q_j. A
correct statement must retain each actual query rank. For q_j<=7, concavity
gives [q_j]/q_j >= [7]/7 > Delta, so every summand is positive. More generally
(4) is useful exactly when its right side is positive. In particular the
native-only family and the existing three-head family (query ranks at most
three) fail strictly whenever m>=1. There is no unsupported claim that the
same loose increment bound excludes unbounded query ranks.

Thus every native-only profitable common-body caller, and every such caller
with the admitted three-head query inventory, must violate the integral
coefficient hypothesis. It must use essential dyadic ordinary group-algebra
coefficients, a changed body/input/source interface, or another excluded
premise. Adding ordinary, compiler, tape and precision expenses cannot repair
a negative Gaussian margin.

## 6. Constructive interpretation and an exact scope control

For an ordinary involution h, the two-role unit

    J_h = (1/2) [[1+h,1-h],[1-h,1+h]],       J_h^2=I,     (5)

routes the +1 eigenspace without exchange and the -1 eigenspace with a role
exchange. It is synthesized by a two-role sum/difference transform, applying
h to one transformed role, and the inverse sum/difference transform. This is
an exact ordinary circuit with an essential coefficient 1/2 in its collective
basis unless h=1 after the relevant specialization.

If h is a diagonal CZ phase, (5) is instead a literal conditional role
permutation based on its quadratic parity. Its physical realization is a
uniform coordinate/role permutation with a tracked parity counter; the cost
of that permutation and tape traversal must be charged. It has no Gaussian
query and uses neither a zero input nor erasure. This example explains why
(1) is not a theorem for arbitrary ordinary circuits.

This package does NOT claim (5) achieves a profitable caller, or that the
construction itself is new: projector routing exists in earlier programme
controls. The new conclusion identifies why an integral search cannot find
a profitable full-parabolic common-body caller, and directs synthesis toward
nontrivial quadratic-sector coupling rather than merely adding entangling
monomial generators. Pauli-only routing can be weaker: in the centre-trivial
projective quotient its augmentation may make (5) integral again.

A future extension should either construct a complete denominator-bearing
caller or establish a quantitative obstruction for those sector couplings.
Fixed marked factors and arbitrary per-column gates are NOT silently included
by the current transfer; their exact coefficient and faithful-algebra models
need a separate admission argument.

## 7. Exact checks, provenance and remaining obligations

`check.py` independently builds binary symplectic and parabolic matrices,
checks the block identities for fixed head dimensions 2 through 5, tests
arbitrary entangling ordinary role circuits, native signs/inverses and query
modes, and authenticates the real order-fifteen head's rank-one/rank-two
source data. It gives a sharp two-native independent-endpoint control and
rejects changing an ordinary stage to a Gaussian stage without charging it.
A one-qubit invariant-lattice example is checked exactly, including actual i
phases; naive entrywise reduction in the computational basis is rejected.
Projector routing and its factor 1/2 are separately authenticated. These
finite controls supplement the written universal proof; they are not that
proof and are not a full physical caller replay.

All source references and SHA256 pins appear in DEPENDENCIES.json. Existing
source, tensor-separation and accounting authors retain their credit. Prepared
for @CubeJerry's permanent programme by Worker B with OpenAI assistance.
No complete supplier, foundational discharge, accepted certificate change or
new complete κ has been established. Independent proof review is pending.
