# Cubic-logarithmic arity is forced by the literal label certificate

Status: **proved scoped obstruction; independent review pending**. This is
about the retained sufficient label/endpoint invoice, not a lower bound for
the actual interchanger, scheduler or multiplication.

Predecessor: `routes/A/fixed-field-extraction-theorem.md`, Q2--Q7, at
programme head `0607d044d1d09489580da0e5828588820e1a6775`. Source:
November tape label/rectangle mechanism, OpenAI `math` at
`3344da59991ed94f9ba711217b29c1d760badfa6`, with the characteristic-two
variant credited in that predecessor.

## 1. Restricted numerical model

Let J>=1, d>=2, t>=1 be integers, q=2^t, and m>=2 real. Put x=log2 m.
The literal construction uses the rank guard

    q^(d^2) >= 2^(2d^2-2) m,                         (LB1)

and incidence majorant

    lambda=binom(2d-1,d)^(d+1) (q-1)^d t^(d(d-1)).  (LB2)

Its conservative complete gate bounds a positive constant at least one
times sqrt(m) D(1+lambda) by m^(1/2+1/(2J)), where D>=1. Every accepted
point therefore satisfies the weaker condition

    lambda <= m^(1/(2J)).                            (LB3)

The result below applies to points accepted through that sufficient invoice.
It does not claim LB3 is necessary for every implementation of these labels,
much less for another routing construction.

## 2. Necessary size theorem

**Theorem LB.** Every point satisfying LB1--LB3 obeys

    d>=2J,
    d^2<=2x/(3J),
    t>=3J/2,
    x>=4 J^3 log2(3J/2).                             (LB4)

Thus log2 m=Omega(J^3 log(J+2)) as J grows. The order matches the prior
sufficient O(J^3 log(J+2)) construction within this restricted certificate.

Proof: LB1 implies

    t>=x/d^2+2-2/d^2.                                (LB5)

The product formula binom(2d-1,d)=product_(i=1)^(d-1) (d+i)/i has every
factor at least two; hence log2 binom(2d-1,d)>=d-1. Also q-1>=2^(t-1).
Therefore

    log2 lambda >= d^2-1+d(t-1)+d(d-1)log2 t.         (LB6)

All terms are nonnegative. From LB5, d(t-1)>=x/d+d-2/d>=x/d for d>=2.
Combining LB3 with this term gives x/(2J)>=x/d, hence d>=2J.

Next d^2-1>=(3/4)d^2. Thus x/(2J)>=(3/4)d^2, giving the second inequality.
Substituting into LB5 yields t>=x/d^2>=3J/2. Finally
d(d-1)>=(1/2)d^2>=2J^2, so the last term of LB6 gives
x/(2J)>=2J^2 log2(3J/2), proving the fourth inequality. QED.

No hypothesis that d is a power of two or t is minimal was used, so the
source's extra restrictions are automatically covered. Its odd trial values
of m cannot evade the bound.

## 3. Consequence for a specified overhead certificate

Suppose a particular envelope certificate assigns each accepted parameter
point a log-overhead charge

    F_J(X)>=c log2 m_J+X/J,                           (LB7)

where c>0 is fixed and X=log2(1+log2 n). For example, explicitly charging
D_J=m_J^K with fixed K>0 has this form. This is a property of the charged
certificate. Merely knowing the upper bound D_J<=m_J^K would not imply LB7.

**Corollary.** For all sufficiently large X, uniformly over accepted J,

    F_J(X)>=c' X^(3/4)(log2(X+2))^(1/4),             (LB8)

with c'>0 depending only on c. Applicability thresholds can only restrict
the candidate set and cannot weaken the bound.

Proof: LB4 gives log2 m_J>=c0 J^3 log2(J+2) above a fixed J. Put
Y=(X/log2(X+2))^(1/4). For J<=Y, X/J>=X/Y. For J>Y,
J^3 log2(J+2)>=Y^3 log2(Y+2), which is a positive constant fraction of
the right-hand scale in LB8. The finitely many smaller J are covered by
X/J. QED.

Thus the new 3/4-power separated-cost target, when charged through this
literal polynomial-in-m profile, is optimal in scale for that accounting
model. Changing search weights or the constants of d,q,m within this
invoice cannot lower the power of X. It remains possible that a tighter
actual runtime estimate has a smaller prefactor and evades LB7.

## 4. What can evade the obstruction

The theorem leaves open a sharper complete call bound not charging LB2;
a different label family or endpoint-sharing scheme; varying-arity or
multilevel construction without one fixed m_J; or stronger runtime analysis
whose charged prefactor does not satisfy LB7. It proves neither a lower
bound on actual finite-program arity nor global optimality of the 3/4 rate.
In particular it is not an obstruction to the exact square-root endpoint.

Open next question: can the d^2 incidence loss or its log t multiplier be
removed from the *complete* shared-endpoint invoice, while retaining actual
routing and occupied reserves? This calls for a mechanism change. Optimizing
d,q within LB1--LB3 has the proved scale limit above.

Credits: Jerry Chen (@CubeJerry), source label/rectangle mathematics,
predecessor characteristic-two parameter bounds, and substantial
AI-assisted E002 analysis.
