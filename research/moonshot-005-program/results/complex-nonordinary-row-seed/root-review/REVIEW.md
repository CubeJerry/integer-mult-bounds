# Independent audit of the initial nonordinary row and completion gate

**Accepted as an exact algebraic seed and a scoped obstruction. No caller, supplier or new kappa.** Root independently derives the identities below and checks them with SymPy matrices, without importing the author's integer Gaussian-dyadic implementation. The author's original pending-review label is superseded by this explicit admission only within the stated scope.

Let A=C_b S be the pinned three-head Clifford source and P the ordinary phase i raised to the c-bit. The first-query identity follows by block multiplication:

    diag(A^-1,I) [[I,P],[0,I]] [[A^-1,I],[0,A^-1]]
      = [[G,A^-1+H],[0,A^-1]],
    G=A^-2, H=A^-1 P A^-1.

The Clifford products G,H have Gaussian rank2, K=G^-1 H=A P A^-1 has rank1, and J=G K^-1=A^-1 P^-1 A^-1 has rank2. The independent exact checker verifies all column supports4,4,2,4 and the source identity at widths1,2. For Clifford operators, support per column is2^r by the admitted ordinary/Fourier/ordinary factorization; the identities are exact products and tensor to arbitrary widths. Universal use of the rank projections still requires the separately proved sufficiently-large faithful phase sector.

The pure E2 row R=(G,H) has full physical row rank d. If R=J0(v1,v2) with J0 invertible and v1,v2 ordinary, G=J0 v1 forces v1 invertible. The ordinary finite matrix algebra is inverse closed, so K=v1^-1 v2 would be ordinary. This contradicts the faithful direct E0/E1 decomposition. Thus the necessary nonordinary-input property has a concrete initial row. It is not yet the required two-query intermediate.

For the proposed next stage O_lambda=[[I,-I],[lambda,I-lambda]], the two rows become R and lambda R+(0,A^-1). O_lambda is invertible for every ordinary lambda: its Schur complement is I. Applying q=A^-1 to the second row gives lower row (q lambda G,q lambda H+G).

Suppose this particular second stage could be completed by a final rank-one query and ordinary mixing to an invertible pure E3 endpoint. Removing the last query gives support only in E2+E3. Its E2 image is an ordinary one-role submodule, since an unaffected row of the last query annihilates it after an invertible ordinary change. The top row is R of full rank d, so the E2 component has rank d and its top projection is an isomorphism. An ordinary basis column for its image therefore has invertible ordinary top block. It follows that the lower E2 row is C R for an ordinary C. This supplies the necessity that might otherwise be mistaken for an assumption.

Subtracting C R leaves

    X=(q lambda-C)G in E3,
    X K+G in E3.

Right multiplication by the group element K permutes the faithful projective group basis, retaining its exact central phase. The only preimage of the coefficient class G is G K^-1=J, which lies in E2. An X in E3 therefore contributes zero to that coefficient in X K. Adding G contributes a nonzero unit coefficient in E2, contradicting the second equation. This works for every ordinary lambda, including zero divisors; it is not a finite-search exclusion. The projective-basis phase can multiply a coefficient by a nonzero scalar but cannot turn an absent coefficient into a present one.

All additions and minus signs are at field level. The universal preimage statement is admitted for the fixed collective faithful algebra; no unrestricted width-growing exceptional algebra is assumed. The source L is the inverse-native **proof representation**. No free physical inverse primitive or cost-free ordinary mixing is asserted. A completed identity would still need the actual source direction, physical volumes, ordinary implementation, all recursive costs and the five foundations.

The phase-free control P=I has K=I and R=G(I,I), so the ordinary-factorization obstruction disappears. Changing the second query or seed remains open; any repair of this particular coefficient mechanism must place the needed residual's preimage in the allowed rank-three support. The general same-side three-query caller is unresolved.

Credit @CubeJerry, source/rank-bimodule predecessors, Worker B's seed and coefficient argument, and Root's independent derivation and exact implementation. OpenAI-assisted research.
