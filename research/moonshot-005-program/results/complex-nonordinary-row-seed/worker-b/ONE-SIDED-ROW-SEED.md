# A nonordinary-input rank-two row and its first completion obstruction

**Exact algebraic seed and scoped obstruction, author proof pending review. No new kappa.** This is a final structural attempt on the surviving three-query placement, not a completed caller. It uses the F1 proof representation of the native; no free physical inverse source is asserted.

Let A=C_b S be the proved three-head cycle head. Let P multiply a computational basis vector by i to the c-th coordinate bit. P is an ordinary monomial phase. Define

    L=[[A^-1,I],[0,A^-1]],  D=[[I,P],[0,I]],
    Q1=diag(A^-1,I),       G=A^-2, H=A^-1 P A^-1.

The exact first-query word is

    Q1 D L = [[G,A^-1+H],[0,A^-1]].

The rank pattern is r(G)=r(H)=2, while K=G^-1 H=A P A^-1 has rank one. These are multiplicative Clifford identities and tensor to all widths. Thus the degree-two row is R=(G,H), full row rank, and it cannot factor R=J(v1,v2) with J invertible and v1,v2 ordinary. Indeed G=Jv1 forces v1 invertible and then G^-1 H=v1^-1v2 ordinary, contradicting r(K)=1 in the faithful bulk algebra. This explicitly realizes the nonordinary-input condition as an initial row; it does not yet provide the required two-query invertible high-rank intermediate.

A natural second step subtracts the low row and re-adds an arbitrary ordinary multiple lambda of R. The invertible ordinary bank matrix

    O_lambda=[[I,-I],[lambda,I-lambda]]

gives rows R and lambda R+(0,A^-1). Apply the second in-place query q=A^-1 to the second row. For the result to have only ranks two and three and its rank-two part to have physical rank d, its lower rank-two row must be C R for an ordinary C; this is forced whenever the final third query admits the required ordinary rank-component output separation. The necessary equations are

    X=(q lambda-C)G in E3,
    (q lambda-C)H+G = X K+G in E3.              (1)

However G K^-1=G H^-1 G=A^-1 P^-1 A^-1 has rank two. In the faithful group-coefficient algebra, right multiplication by K permutes group basis elements. An E3 element X therefore cannot contribute the group coefficient G to pi2(XK), because its unique preimage G K^-1 lies in E2. Equation (1) would require that coefficient to be -1. This is impossible.

Thus this particular seed with second query A^-1 and ordinary O_lambda cannot complete the needed intermediate, even when lambda has arbitrary ordinary zero divisors. The obstruction is more precise than a failed finite search. A repair must change the second query or the seed so that the required rank-two residual has a rank-three preimage under the relative transport K. The general three-query same-side caller remains open.

For a sum of tensor coefficients, native additions and minus signs remain field-level scalars. This argument assumes the independently justified faithful group basis, not only one-column matrix equality. Fixed marked-column admission remains subject to the bulk model; the coefficient-preimage statement above is stated in the fixed collective algebra.
