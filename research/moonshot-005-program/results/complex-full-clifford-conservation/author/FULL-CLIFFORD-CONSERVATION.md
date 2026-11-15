# Gaussian head-rank conservation for the full two-head monomial Clifford family

**Proved scoped obstruction, pending independent admission.** The actual canonical native half contributes at most two target head-rank units even when arbitrary finite ordinary quadratic phases and all monomial Clifford encodings on its two head coordinates are allowed. Any complete common-body caller obeys H<=2m+q1+2q2, and its Gaussian invoice fails strictly for every 0<t<1. This closes the proposed larger-ordinary-phase repair of the fixed two-head/common-body architecture. It is not a lower bound for multiplication, extra head coordinates, changed body incidence or arbitrary non-Clifford ordinary operations. **No new kappa.**

## 1. Model, source and precise statement

Take a fixed finite unitary lift G of the Clifford group on two binary head coordinates, retaining its scalar centre Z. Let H be its full subgroup of computational-coordinate monomial Clifford maps. Such ordinary maps include arbitrary fixed binary-affine coordinate permutations and quadratic coordinate phases. They stabilize the computational Pauli Lagrangian L0. The source is the actual canonical half, pinned in `DEPENDENCIES.json`, or any of its ordinary boundary gauges, inverses and signs. Its new exact gauge in `PROOF.md` supplies

    N_(sigma,epsilon,c)
      = [[B^sigma, c B^(sigma+epsilon)], [0,B^sigma]],

with sigma,epsilon,c in {+1,-1}, B a rank-one Clifford head and B^2 rank two. The original source has three MOVE ranks 1,7,8 and one ADD per half. Its original all-column proof is retained; no unpublished full120 equivalence is used.

At each tensor width V, ordinary encodings are arbitrary invertible bank matrices over the image of C[H]. They may mix roles, take finite scalar combinations, and interleave genuinely noncommuting ordinary phases. This is an algebraic enlargement of actual implemented ordinary circuits; it does not declare every algebra element a free physical service.

There are m native halves on R independent retained roles, q1 rank-one head queries and q2 rank-two head queries. A query is an invertible one-bank Gaussian Clifford call or a distinct-bank additive shear with such a coefficient; fixed nonzero scalars and inverses are included. Every endpoint role is an independent Gaussian head job, up invertible ordinary encodings. Let H_tot be the sum of their head ranks in {0,1,2}. No bank is presumed zero, discarded or omitted.

**Theorem 1.** Every all-width exact caller in this family satisfies

    H_tot <= 2m+q1+2q2.                            (1)

The native orientation and ordering, query ordering/modes and ordinary interstage encodings are arbitrary. The proof retains every scalar phase and every width residue.

## 2. Six odd quadratic refinements and fifteen matchings

Let W=F2^4 have coordinates (x1,x2,z1,z2) and symplectic form omega((x,z),(x',z'))=x dot z'+z dot x'. Computational L0 is {(0,z)}. For t in F2^4, define

    q_t(x,z)=x dot z+t dot(x,z).

The six odd refinements have, in the bit encoding with x coordinates first,

    t = 5,7,10,11,13,14.

Equivalently their x- and z-linear coefficients have dot product one. They are exactly the refinements with six zeros. A symplectic change of variables preserves the polar form and the number of zeros, so it permutes this six-element set. This gives a genuine permutation representation sigma:Sp(4,2)->S6.

For a Lagrangian plane L, pair the six refinements that agree on L. At L0, the pairs have identical z-linear parts and the matching involution is

    tau=(0 1)(2 3)(4 5)

in the displayed order of t. Equivariance gives a matching tau_L for every L. The fifteen unordered pairs of distinct odd refinements have fifteen distinct nonzero differences t+t'. Thus every nonzero linear covector labels exactly one pair. The matching for L consists of the three pair labels in the annihilator of L.

Consequently two planes L,M have exactly

    2^dim(L intersection M)-1

common matching edges. In particular the map from the fifteen Lagrangian planes to the fifteen matchings is injective and equivariant. The stabilizer of L0 therefore centralizes tau on the six odd forms. Let P be the six-by-six permutation matrix of tau. Every ordinary h in H has symplectic image fixing L0, hence its six-point permutation matrix commutes with P.

## 3. Exact auxiliary rank potential

Let s(g) be the six-point permutation matrix of the symplectic image of g. Put r(g)=rank_F2(B_g), using the convention in which monomial Clifford maps have symplectic B block zero. Then

    r(g)=2-dim(L0 intersection gL0).

Write tau'=s(g)^(-1) tau s(g). The rank of s(g)-P s(g)P is the rank of I-tau'tau as a complex permutation-matrix difference. For a permutation on six points that rank equals six minus its number of cycles.

If the matchings share all three edges, tau'tau is identity and the rank is zero. If they share one edge, the two shared vertices are fixed and the other four form two transpositions, giving rank two. If they share no edge, their union is one alternating six-cycle and tau'tau has two three-cycles, giving rank four. Therefore for every two-head Clifford g,

    rank_C(s(g)-P s(g)P)=2r(g).                   (2)

This is exact for all 720 symplectic images. P is a **non-diagonal** matching involution; it is not a diagonal sign cut. A limitation on weighted diagonal cuts therefore does not exclude this representation.

## 4. Phase-exact passage from physical tensors to auxiliary representations

This step prevents an incorrect quotient of scalar phases. Let phi_V(g)=g^(tensor V), of head-bank dimension D=4^V. The applicable finite algebra is

    A_V = C[G] / <z-zeta_z^V I : z=zeta_z I in Z>.

Distinct projective Clifford representatives are unitary and not proportional. The programme's tensor-separation theorem therefore makes phi_V faithful on A_V for every sufficiently large V. This follows from its positive-definite tensor Gram matrix; it does not require a finite numerical check or one special width residue. An all-width physical caller must hold at such a faithful width.

Define two auxiliary representations at that same V by

    Psi_0(g)=s(g) tensor phi_V(g),
    Psi_1(g)=(P s(g)P) tensor phi_V(g).            (3)

These are multiplicative. A central scalar z acts as zeta_z^V in both, exactly as in phi_V. Hence both descend to the SAME phase-exact algebra A_V, for every width residue. Applying them to a lifted physical identity is legitimate. No scalar centre has been set to one, and no extra physical service is performed.

For ordinary h, s(h) commutes with P, so Psi_0(h)=Psi_1(h); they consequently agree on every ordinary bank encoding. By (2) and invertibility of phi_V(g),

    rank(Psi_0(g)-Psi_1(g))=2r(g)D.               (4)

An ordinary matrix invertible in the faithful physical representation has its inverse in the same finite-dimensional algebra, by its minimal polynomial. Its common auxiliary image is therefore invertible. This is algebraic invertibility, not a new ordinary compilation theorem.

## 5. The exact native difference rank

Put U=Psi_0(B^sigma), V'=Psi_1(B^sigma), E=U-V'. Equation (4) gives rank(E)=2D. For epsilon=-sigma the native cross coefficient is ordinary, so its difference is diag(E,E), rank 4D.

For epsilon=sigma the difference is

    [[E,c(U^2-V'^2)],[0,E]].

Since U^2-V'^2=U E+E V', invertible block triangular row and column operations reduce this matrix to diag(E,E), exactly as in the dihedral proof. Its rank is therefore 4D. Every inactive role contributes zero difference.

Ordinary boundary gauges preserve difference rank because both auxiliary representations agree on their invertible images. Literal inversion also preserves rank, using U^-1-V'^-1=U^-1(V'-U)V'^-1. Thus this rank is attached to the actual canonical source, not only to a convenient formal common head. The same calculation permits different ordinary gauges at different stages.

An in-place rank-r query has difference rank 2rD by (4). A distinct-bank shear has only its one offdiagonal coefficient changed and has the same difference rank. Nonzero fixed scalar multiples do not affect the rank.

## 6. Proof of conservation

Apply both auxiliary representations to the whole source word and telescope the difference of the products. Each ordinary factor has zero difference; each native contributes 4D and each rank-r query contributes 2rD. Rank subadditivity yields

    rank(Psi_0(endpoint)-Psi_1(endpoint))
       <= 4mD+2q1D+4q2D.

The complete independent Gaussian endpoint has difference rank 2H_tot D by (4). Invertible ordinary outer encodings preserve it. Cancel 2D to obtain (1). The proof is valid at every sufficiently large faithful width and hence for every claimed all-width caller in the stated family. QED.

## 7. Complete common-body consequence

Assume each native stage introduces seven fresh independent body axes, all head services fix them, and every role receives the stage body. The m(R-2) rank-seven idles are paid. Write [r]=r^t, 0<t<1, and d=[8]-[7]. The Gaussian price is

    P_t=mR[7]+(m+q1)[1]+m d+q2[2].

Targets have ranks 7m+r_i with r_i in {0,1,2}, and sum r_i=H_tot. By concavity,

    T_t <= mR[7]+d H_tot.

Using (1),

    P_t-T_t >= (m+q1)(1-d)+q2([2]-2d)>0          (m>=1).

Indeed 0<d<1, d<=2^t-1, and 2(2^t-1)<2^t. This strict obstruction holds for every 0<t<1 before ordinary, precision, layout, ownership and compilation expenses. Those expenses cannot improve the invoice.

It rules out every proposed common-body repair using more ordinary quadratic phases on the same two head coordinates, not merely H24 or the single-inverter subalgebra. It does not rule out more head coordinates, head/body mixing or changed body incidence, another native/source, a changed endpoint contract, arbitrary non-Clifford ordinary operators, approximation or a width-growing family. It is not an unconditional multiplication lower bound.

## 8. Verification, novelty and next obligation

`check_full_clifford.py` independently reconstructs the actual Gaussian-dyadic B from the new source and computes its symplectic columns by conjugating all Pauli basis operators. It obtains columns (13,11,10,14), then builds the six-odd-form action directly, without importing root's separate construction. It enumerates all 720 symplectic elements and 48 ordinary stabilizers and checks the exact rank-difference census:

| Gaussian rank | Difference rank before tensor factor D | Number of symplectic elements |
|---|---:|---:|
| 0 | 0 | 48 |
| 1 | 2 | 288 |
| 2 | 4 | 384 |

It checks 4,320 generator multiplication incidences, the actual ordinary source gauges, all eight native signs/orientations, and a negative control showing that replacing the matching involution by an unrelated diagonal sign cut breaks ordinary agreement. All arithmetic is integer, Gaussian-dyadic or exact Fraction elimination. The all-width scalar-centre argument is the mathematical construction (3), not an inference from the finite catalogue.

Root independently derived the same six-point matching representation, its all-720 census and native difference ranks before reading this verifier. Its distinct proof/replay artifact provides independent mathematical corroboration. Author and root source-phase controls both explicitly retain the native cross minus outside tensor products.

The contribution is a complete mathematical closure of the primary two-head enlarged-phase repair, with a positive exact order-five source retained as a reusable interface. A next productive complex construction must change a substantive source/body/head premise. The immediate suggested investigation is graph-local fresh-body delivery without full-role idles, with all chronological equal-body requirements derived explicitly. An additional head coordinate is another possible escape, but requires an actual source and optimistic complete budget before synthesis.

Dependencies are the pinned canonical source, the newly verified gauge in `PROOF.md`, and the programme's general tensor-separation/rank-component result. No current selected certificate changes. All five foundational assumptions remain retained.

Credit @CubeJerry; the retained native/compiler, tensor-separation and common-body price authors; S013's representation methodology; and the independent S014 root/Worker B matching construction, with substantial OpenAI assistance. The cumulative programme remains ongoing. No new complete kappa.
