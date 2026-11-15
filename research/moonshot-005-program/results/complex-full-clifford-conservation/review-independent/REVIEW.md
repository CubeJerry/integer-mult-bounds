# Independent matching representation and full ordinary audit

Root independently reconstructed the full two-head symplectic action and its
six odd quadratic forms, using direct binary source transformations and exact
SymPy rational ranks. The checker imports no Worker B code. It exhausts all
720 symplectic matrices, identifies all 48 matrices preserving the computational
Lagrangian, and obtains difference-rank classes 0,2,4 of sizes 48,288,384.
All eight native orientations/signs have difference rank four. This is an
exhaustive finite structural check; the universal caller and invoice claims
also require the algebraic arguments below.

## Mathematical argument checked independently

Let E=F_2^4 with symplectic form omega and computational Z Lagrangian L.
For each nonzero w, exactly two of the six odd quadratic forms q vanish on w.
They differ by omega(w,-), giving a bijection from fifteen nonzero vectors to
the fifteen unordered pairs of odd forms. The three nonzero vectors of L
therefore give a perfect matching of the six forms. Its permutation involution
P commutes with every symplectic map preserving L.

The matchings for L and gL share precisely 2^d-1 edges, where
d=dim(L intersection gL). The product of their involutions has respectively
6,4,2 cycles for d=2,1,0. Hence

    rank(rho(g)-P rho(g)P)=2(2-d)=2r(g).

Here rho is the six-dimensional permutation action on the odd quadratic
forms. P is non-diagonal. A failure to express the Gaussian rank as an l1
cut metric does not obstruct this representation.

For the native block, let R and R' be the two images of B^sigma and put
A=R-R'. The cross-identity orientation has difference diag(A,A). The
cross-square orientation factors exactly as

    [[A,c(R^2-R'^2)],[0,A]]
      =[[I,cR'],[0,I]] diag(A,A) [[I,cR],[0,I]].

Consequently the difference rank is four, or 4D after the physical tensor
factor below. The verifier checks the factorization rather than only its
resulting rank. Opposite-coupling native halves give diag(B^2,B^2), establishing
sharpness of the coefficient two per native in the head-rank inequality.

## Scalar phases and faithfulness

Worker B supplied the stronger phase-safe auxiliary representation. At a
sufficiently large faithful physical tensor width V, use

    R_0(g)=rho(s(g)) tensor U_g^(tensor V),
    R_1(g)=P rho(s(g)) P tensor U_g^(tensor V).

The two auxiliary representations have the same scalar cocycle as the physical
tensor operators, since the symplectic permutation factor ignores scalar
phases. Thus they extend to homomorphisms from the same twisted finite group
algebra at every width residue. Their difference ranks are 2r(g)D, with
D=4^V, and they agree on the full computational-monomial Clifford ordinary
algebra. This avoids any change in source phases or an unjustified choice of
width residue. The inherited finite-group tensor-separation theorem is still
essential: at an unfaithful small width, a physical identity may not be an
algebra identity to which the auxiliary representation applies.

The checker includes that exact negative control. The one-column physical
pentagonal source satisfies sum_(k=0)^4 B^k=0. The same sum in the proposed
auxiliary representation has trace 20. Hence applying the auxiliary map to
the one-column operator quotient would be invalid. At sufficiently large
faithful width this accidental relation is absent. The theorem uses the
faithful algebra, not the one-column quotient.

## Caller and cost proof

Ordinary role matrices are allowed to be arbitrary invertible matrices over
the ordinary algebra. Both representations send each such inverse to the
inverse of its image, so ordinary boundary and interstage encodings do not
change the difference-rank argument. Every one-role query contributes at most
2rD, whether it acts in place or is a distinct-role additive shear. Native
blocks contribute 4D, and retained independent endpoint heads contribute
2D times their total Gaussian head rank. Telescoping therefore gives

    H_total <= 2m + sum_j r(query_j).

For the common-body model with rank-seven idles on all inactive roles,
concavity gives T<=mR[7]+d H_total, d=[8]-[7]. With x rank-one and y rank-two
queries, the full optimistic recursive price satisfies

    P-T >= (m+x)(1-d)+y([2]-2d)>0,  0<t<1, m>=1.

The positive first term and nonnegative second term follow from decreasing
increments and 2(2^t-1)<2^t. No extra cost has been dropped to obtain a saving;
additional ordinary/precision/ownership costs can only worsen this failure.

The scope is the fixed two-head Clifford algebra, retained roles, native
interfaces and common-body invoice. It does not cover non-Clifford ordinary
maps, extra head coordinates, changed body incidence, disposable input roles
or an arbitrary multiplication algorithm. No new kappa or foundation discharge.

## Reproduction

Run `check.py` in this directory; it writes `RESULT.json` beside itself.
The environment used Python 3.12 and SymPy 1.14.0. Expected status:
`PASS_INDEPENDENT_FULL_CLIFFORD_MATCHING_CONSERVATION`.

This is independent model computation and mathematical review, not independent
human or formal-kernel verification. Credit @CubeJerry, predecessor native and
tensor-algebra authors, Worker B's smaller dihedral lead and phase-safe lift,
and root's full matching extension. Substantial OpenAI assistance.
