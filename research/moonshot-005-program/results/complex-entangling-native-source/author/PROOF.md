# An exact order-nine native head with a non-dihedral ordinary transport

**Proved source and interface construction, pending independent review.** A single local ordinary quarter-phase on the existing three-head spectator source gives a genuine common head B of order nine, with Gaussian power ranks (0,1,2,3,3,3,3,2,1). All four original input columns and all physical phases survive. An explicit ordinary identity transports B^3 to B^4, and therefore rules out extending the preceding cyclic-double-coset dihedral shadow while preserving its cyclic covariance. This is a change of admitted source, not a profitable caller. **No new kappa.**

## 1. Source, model and exact provenance

Use the canonical all-column source as retained in `results/complex-three-head-source/author/THREE-HEAD-SOURCE-AND-ONE-QUERY-GATE.md`, sections 1–2, and its original two-head equations in `results/quadratic-sign-query-gate/author/PROOF.md`. The source has two independent callable halves, each with Gaussian MOVE ranks 1, 7, 8 and one field ADD. With seven fresh body axes F and two original heads a,b, its equations are

    X' = F C_b X,             Y' = F C_a Y + F X,
    U' = F C_b U − F C_a C_b V, V' = F C_a V.

The untouched third head c is added to every actual chart, including contacts. All rank differences and inclusions are preserved; the full source and target array volumes both acquire the same multiplier 2^V at tensor width V. That multiplier is retained throughout. No input is set to zero, copied, identified or discarded, and no owner is introduced.

Fix every integer V≥1, arbitrary independent complex input fields, and a fixed ambient dimension containing these heads and every required fresh body. The following one-column head operators are tensor-powered; field sums and the cross minus are not. Every added ordinary service and all inherited native/compiler/precision assumptions remain charged. Exact source and helper byte pins are in DEPENDENCIES.json.

Credit @CubeJerry, the native/compiler and prior caller authors, S014's pentagonal phase source and three-head spectator source, and the S015 cyclic/commuting conservation work. Worker B developed this construction with OpenAI assistance. Independent review is a distinct artifact.

## 2. A local cubic rotation transported through three heads

Order coordinates by x=u_a+2u_b+4u_c. Define the existing ordinary cycle P and the new ordinary phase D by

    P: a→c, b→a, c→b,
    P|x⟩ = |p(x)⟩,    p=(0,4,1,5,2,6,3,7),
    D|x⟩ = i^(u_b)|x⟩.

Let C_v=((1+i)I+(1−i)X_v)/2 be the actual one-column Gaussian map. Put S=DP and

    B=i C_b S,         L=i C_b D,         B=L P.

Here L acts only on coordinate b. Its literal two-by-two matrix is

    L = (1/2) [[−1+i,−1+i],[1+i,−1−i]].

Direct multiplication gives L²+L+I=0, hence L³=I and tr L=tr L²=−1. Both L and L² have two nonzero entries in every row, each of modulus 1/√2; their Gaussian ranks are one. The ordinary P cyclically moves L among the three tensor axes, so

    B³=L_a L_b L_c,         B⁹=I.

For k=0,…,8 the power B^k is an ordinary head permutation times three tensor factors whose exponents are the numbers of visits to the corresponding axes. Exponents divisible by three are ordinary identities; each other exponent has Gaussian rank one. Thus exactly

    r(B^k)=(0,1,2,3,3,3,3,2,1).

No power at k=1,…,8 is scalar; B has exact order nine. At width V, B_V=B^(tensor V), and ranks multiply by V. Independent query access to B_V^k remains a paid Gaussian query of this rank; the power identity supplies no such service for free.

## 3. Literal ordinary gauges of the real native

Because P X_b P^-1=X_a and D commutes with X_a,

    S C_b S^-1=C_a,
    R=C_a^-1 S C_b S=S².

R is implemented as the actual ordinary monomial S², not by evaluating a Gaussian inverse. Choose the boundary services

    G1=i S,       G2=−S²,       H2=−i S^-1.

Preapply G1^(tensor V) to X,U and G2^(tensor V) to Y,V. Postapply H2^(tensor V) to Y,V. The individual one-column coefficient identities are

    C_b G1=B,          H2 G1=I,
    H2 C_a G2=B,       C_a C_b G2=B².

The last identity follows from C_a C_b S²=(C_b S)² and B²=−(C_b S)². Consequently the exact real source becomes

    X'=F B_V X,           Y'=F(X+B_V Y),
    U'=F(B_V U−B_V² V),   V'=F B_V V.

In particular its native halves are genuinely available as

    L0(B_V)=[[B_V,0],[I,B_V]],
    U(B_V) =[[B_V,−B_V²],[0,B_V]].

The upper ordinary-cross version L(B_V)=[[B_V,I],[0,B_V]] costs the two physical role permutations J L0 J when used. Literal inverse source words, with inverse boundary gauges, remain available at the original reversed-source cost. Their F^-1 body is not silently replaced by F: positive-body comparison additionally requires F² translations on both roles, exactly as in the pinned pentagonal source.

All scalar factors i,−1,−i above are one-column phases. Their lifted factors are i^V,(−1)^V,(−i)^V. Replacing them by width-independent field scalars would be wrong. The native upper minus stays outside the tensor: its coefficient is −(B²)^(tensor V)=−B_V².

## 4. Complete ordinary and spectator expenses

Each forward half adds exactly three fixed monomial head services, each implementable by one head-coordinate permutation and one unit-phase pass. Thus it adds three coordinate-permutation services and at most three full-array unit-phase passes, without another field ADD, Gaussian call, owner, or input erasure. The phase alphabet is {1,−1,i,−i}, and all tables and inverse tables have constant size independent of V.

The tensor phase of each service is the sum modulo four of its column phases. A fixed-alphabet odometer maintains this sum in amortized O(1) digit updates per scalar coordinate. Its total digit changes are bounded by K/(K−1) times the number of coordinates for fixed alphabet K≥8; a tape traversal along each carry path changes only a constant factor. The phase generator therefore has a uniform linear combinatorial bound and O(V) control storage. Unit phases are exact sign changes and real/imaginary swaps, with norm one and no new denominator.

This is an ordinary-instruction construction, not a proof of the compiler foundation. Retain the three actual layout/tape/permutation costs Π1(D,V)+Π2(D,V)+Π3(D,V), plus phase generation and arithmetic/tape passes. Every original MOVE, ADD, recursive Gaussian implementation, descriptor and precision charge remains. The extra spectator multiplies all source and target arrays by 2^V. Fixed larger ambient dimension and source-volume dependence must be incorporated in any eventual admission certificate.

## 5. A faithful cyclic reduction at every V≥2

For k not divisible by three, the trace of a three-factor tensor operator followed by the three-cycle is the trace of the product of those factors. This gives tr(B^k)=tr(L^k)=−1. For k=3,6, the trace is tr(L^(k/3))³=−1. Hence

    tr(B^0)=8,            tr(B^k)=−1 (1≤k≤8).

At width V, the character values are 8^V at the identity and (−1)^V elsewhere. Fourier inversion on C9 gives the trivial and each nontrivial character multiplicity

    m0(V)=(8^V+8(−1)^V)/9,
    m1(V)=(8^V−(−1)^V)/9.

Both are positive for every V≥2. Thus I,B_V,…,B_V^8 are linearly independent for every V≥2, even when scalar coefficients depend on V. A scalar cyclic caller must be checked in C[z]/(z^9−1). The width-one relation I+B+…+B^8=0 is not a uniform identity; at width two its sum is nine times a rank-eight projector.

Scalar cyclic stages and a single ordinary inversion of B still admit a contiguous-three-cut conservation proof: on the nine-cycle take a sign potential supported on three consecutive vertices. Its power difference ranks are twice (0,1,2,3,3,3,3,2,1). The standard telescoping native argument then yields H≤2m+Σ query ranks in that restricted family. The new construction priority is therefore genuinely noncommuting ordinary head transport, not scalar C9 word search.

## 6. An explicit ordinary bridge outside the previous dihedral shadow

The new ordinary phase D itself satisfies the exact identity

    B^-4 D B³ = −i S^-1,

equivalently

    B⁴ = i D B³ S.

For a direct derivation, the displayed two-by-two matrix gives L²=iDLD. Since B³=L_a L_b L_c and the three local factors commute, B⁴=L_a L_b² L_c P=iD B³ DP=iD B³ S. The equivalent inverse-form identity above follows by multiplying units. The accompanying exact matrix verifier checks the literal one-column equality. It tensors to

    B_V^-4 D_V B_V³ = (−i)^V S_V^-1.

Both D_V and the right side are actual ordinary monomials. This is a transport between two rank-three powers, not a way to raise rank for free.

It also proves a precise obstruction to reusing the preceding dihedral *bimodule shadow*. Such a shadow would preserve left/right B multiplication as left/right multiplication by a nine-cycle x and send each ordinary group element h to a reflection/orientation basis value (1 or t), as in the prior partial-cycle extension construction. For D, the relation above demands x^-4 φ(D) x³ be ordinary. If φ(D)=1, its rotation exponent is −1 mod9; if φ(D)=t, it is −7 mod9. Neither is zero, so neither lies in the designated ordinary span {1,t}. Thus that specific construction cannot extend to all current ordinary monomials with its stated covariance. This does not disprove any other conservation theorem, nor supply a caller.

Equivalently, the ordinary stabilizer has a partial action on the nine Lagrangians sending the index 3 to 4 while fixing 0. Neither orientation j↦j nor j↦−j of the cycle does so. The old even-cycle metric extension lemma has an explicitly failed hypothesis here: ranks at distances 3 and 4 both equal three.

## 7. A complete optimistic caller budget and the next exact obligation

The prior one-query compression and source-independent two-native/rank-component obstructions still apply where their explicit premises hold; B and B² have pure ranks one and two. They are not bypassed by a new source name.

A concrete next construction target is three real natives on three retained roles, with two full ordinary interstages and genuine ordinary boundary encoders, giving independent head ranks (3,2,2) or stronger. The twenty-one fresh body axes must reach all three roles; all three rank-seven idles are paid. At t=199/200 the complete Gaussian invoice is

    P=3[1]+6[7]+3[8],
    T_(3,2,2)=[24]+2[23],       [r]=r^t.

The exact rational interval for T−P is

    [561007339600891538672434298712,
     561007339600891538672434298724] / 10^30.

For the stronger (3,3,3) endpoint T=3[24], the movement surplus is larger. Neither margin includes a free extra query: any added Gaussian service must be invoiced, and all ordinary/compiler/precision/recursive costs must fit the retained strict supplier contract. A complete caller would also require uniform scheduling and code growth, ordinary source access, fixed precision, and complex/BIT/outer compatibility. This source theorem does not complete any of those obligations.

For an exact synthesis route, retain the real ordinary-cross stage K=L(B)T from the reviewed three-role base, where

    T=[[0,0,I],[I,0,−I],[I,I,−I]],
    K=[[I,0,B−I],[B,0,−B],[I,I,−I]].

K³=diag(B²,B²,B²) remains a valid control and has no positive invoice. The previous literal-gauge coset obstruction for target diag(B³,B²,B²) uses source-specific cyclic-double-coset separation and must be checked afresh; it must not be presumed false. A target with genuine ordinary endpoint encoders or another orientation can instead be reduced to a linear ordinary-intersection problem using the reviewed two-interstage bridge. D and S provide a concrete noncommuting starting family, with all phases and inverses retained.

## 8. Verification and classification

Run `python check.py --repo /path/to/programme --out RESULT.json` from this package. The verifier pins the real source and exact arithmetic helper, checks local L identities, every power/rank/trace, all native input columns at widths one and two, inverse/source identities, the ordinary bridge, rigorous invoice enclosures, and meaningful phase and width-one negative controls. The all-width source statement follows from the displayed tensor identities and character proof; finite tests alone are not that theorem.

Classification: **proved source/interface and exact scoped shadow nonextension**, pending independent admission. No profitable caller, uniform complex supplier, completed BIT supplier, complete conditional target theorem, unconditional theorem or new complete kappa has been established. All five foundational assumptions remain visible and retained.
