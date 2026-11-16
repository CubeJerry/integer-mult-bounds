# Four distinct nonlinear source types at every width

**Proved classification and caller-interface reduction. Physical costs use
the retained fixed-monomial bridge. No profitable caller or new kappa.**

Fix bits x0,x1,x2, P(x0,x1,x2)=(x1,x2,x0), C1=((1+i)I+(1-i)X1)/2,
and A_f=C1 D_f P. Assume odd truth-table parity. Write the Boolean ANF

    f=c+l0*x0+l1*x1+l2*x2+q01*x0*x1+q02*x0*x2+q12*x1*x2+x0*x1*x2.

All coefficient arithmetic below is in F2. Put

    u=l0+l1+l2, v=q01, w=q02+q12,
    j=u+v, epsilon=c+v*(j+w+1).

## 1. Explicit monomial normal form

For f_(j,w)=j*x2+w*x1*x2+x0*x1*x2, there is a sign monomial T_f with

    T_f A_f T_f^-1 = (-1)^epsilon A_(j,w).                 (1)

Every diagonal Z_q with q independent of x1 commutes with C1. Its conjugation
adds q(x)+q(P^-1 x) to f. For q=x0,x2,x0*x2 these additions are x0+x2,
x1+x2, x0*x2+x1*x2. First choose q0=l0*x0+l1*x2+q02*x0*x2.
The table becomes c+u*x2+v*x0*x1+w*x1*x2+x0*x1*x2.

Simultaneous complement X=X0 X1 X2 commutes with C1 and P. It flips(v,u),
keeps w and changes the constant by u+v+w+1. If v=1, apply this complement
and then Z_q1, where q1=w*x2+x0*x2. This proves(1) with
T_f=Z_q0 if v=0 and T_f=Z_q1 X Z_q0 otherwise. These are literal monomials
with actual inverses; no search or Gaussian inverse is assumed.

For every positive width V, the exact consequence is

    T_f^tensor(V) A_f^tensor(V) (T_f^-1)^tensor(V)
       = (-1)^(epsilon*V) A_(j,w)^tensor(V).              (2)

The absolute sign is width-dependent and must be retained. Each T_f compresses
to at most three columnwise NOTs and one sign-phase pass, all paid. The inverse
has the same bounds with its correctly reindexed phase.

## 2. Exactly four projective classes at every positive width

The canonical truth-table masks, using bit x0+2*x1+4*x2, are128,64,112,176.
For an operator M define e2(M)=((tr M)^2-tr(M²))/2. Direct exact matrices give:

| j,w | Mask | tr A | e2(A) | tr(A²) | tr(A³) |
| --- | --- | --- | --- | --- | --- |
| 0,0 |128|0|0|0|(-3+3i)/2|
| 0,1 |64|1+i|i|0|(-1+i)/2|
| 1,0 |112|1+i|0|2i|(-1+i)/2|
| 1,1 |176|0|-i|2i|(3-3i)/2|

All entries can be verified by Gaussian-integer multiplication after scaling
A by2. For A^tensor(V), the first two trace powers are (tr A)^V and
(tr A²)^V. Thus the zero-pattern of(tr,e2) is respectively

    (zero,zero), (nonzero,nonzero), (nonzero,zero), (zero,nonzero)

for every V>=1. In the nonzero e2 cases it equals ±(2i)^V/2, so there is no
exceptional width cancellation. These patterns are preserved under arbitrary
invertible similarity and multiplication by any nonzero scalar. Therefore the
four canonical operators are pairwise projectively nonconjugate at every width.
Together with(2), this proves EXACTLY four projective similarity classes among
all128 odd tables, rather than merely four representatives for a chosen group.

At even widths the sign in(2) disappears, so there are exactly four ordinary
similarity classes. At odd widths, each canonical operator and its negative
are distinct: their cubic traces are opposite and nonzero. Hence there are
exactly eight ordinary similarity classes at every odd width. All signs occur
because toggling the constant Boolean coefficient negates the one-column source.
These are algebraic classifications of the declared family, not a claim that
arbitrary nonlinear monomial heads fall into the same four classes.

## 3. Literal sign transport through the three-bank native

Head similarity alone is not a cost-free native-caller equivalence. Write

    K(a)=[[I,0,a-I],[a,0,-a],[I,I,-I]],
    B=[[I,0,-I],[0,0,I],[I,I,-I]].

For every invertible a in any unital algebra,

    K(a)=[[I,a,0],[a,0,0],[0,0,I]] B.

For a central scalar lambda in{+1,-1}, put

    D_lambda=diag(I,lambda*I,I),
    E_lambda=[[I,0,(lambda-1)*I],[0,I,0],[0,0,lambda*I]].

Then E_lambda=B^-1 D_lambda B, and multiplication proves

    K(lambda*a)=D_lambda K(a) E_lambda.                   (3)

For lambda=-1, E performs x<-x-2z and z<- -z, preserving y. The strict
unit-coefficient ADD grammar implements this as TWO subtractions x<-x-z
before the z sign. D adds the y sign. Thus the literal invoice is two unit
ADDs and two SCALE(-1) passes. A coefficient-2 shear may be used only if
separately admitted and priced. All banks and spectators are charged; there
is no Gaussian query, helper or erased input.

If a_f=lambda*T^-1 a_r T and T_B=diag(T,T,T), equations(2)-(3) give

    K(a_f)=T_B^-1 D_lambda K(a_r) E_lambda T_B.            (4)

Use lambda=(-1)^(epsilon*V), determined by declared width. At even width or
epsilon=0 the sign bridge is identity. Every T service, inverse, bank sign
and ADD is paid. Core native count and Gaussian profile are unchanged.
Caller interstages transform by the same actual frame conjugation; their
fixed monomial recipes are lowered by the retained bridge. Endpoints retain
two-sided gauges, phases and full volumes. This reduces source choice to four
types while preserving every additional ordinary expense.

Extra constants must enter any completed supplier invoice. This reduction
does not establish a caller budget, a strict complex supplier, BIT compatibility,
complete recursion or any foundational discharge. No new kappa.

## 4. Verification and provenance

The separate independent review reconstructs all128 conjugators, canonical
matrices, spectral invariants and the free-polynomial K sign identity. It
imports neither the family author's arithmetic nor root's family checker.
It rejects omitted complements/quadratic gauges, dropped global signs and
replacing the two subtractions by one. Finite width controls corroborate the
uniform trace argument above; they do not replace it.

Dependencies are the Boolean-sign family, the actual three-bank K source,
and the fixed-monomial physical bridge. The author-family source and root
classification are separately credited and reviewed. Credit @CubeJerry,
complex_discovery, root and all pinned predecessors; OpenAI assistance.
This package is an exact source reduction inside the continuing programme.
