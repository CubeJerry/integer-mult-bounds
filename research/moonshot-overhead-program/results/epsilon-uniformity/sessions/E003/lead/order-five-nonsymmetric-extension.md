# Order five is forced without assuming a symmetric gate

Status: **proved extension of the exact converter-word classification;
independent review pending**. This removes the initial symmetry restriction
from `order-five-word-classification.md`. The swap word, diagonal conversions,
two-dimensional gate, determinant normalization and split distinct spectrum
remain fixed. There is no new asymptotic multiplication bound.

## 1. Statement

Let K have characteristic two. Let lambda,mu be distinct nonzero elements
of K with lambda mu=1, and tau=lambda+mu. Let

    C=[[a,b],[c,d]],   det(C)=ad+bc=1,   a+d=tau.

Let S be any ordered eigenbasis satisfying
`C S=S diag(lambda,mu)`. Column scaling of S is immaterial. Put
`Q=[[0,1],[1,0]]`.

**Theorem UN.** Invertible diagonal matrices A,B,E,D with

    S=A C B,                Q=E C D C^2                 (UN1)

exist if and only if

    order(lambda)=5,
    a=mu^2/tau,  d=lambda^2/tau,  bc=tau^2.             (UN2)

In particular b,c are nonzero. Every admitted gate is diagonally conjugate
to the symmetric order-five gate of the earlier theorem. Dropping symmetry
does not admit a new eigenvalue order for this particular word pair.

## 2. Triangular gates cannot implement the swap word

If b=0, C and every product of it with diagonal matrices are lower
triangular. If c=0 they are upper triangular. Their invertible diagonal
entries cannot become zero. Thus neither case can equal Q in UN1.
This rules out triangular gates from the **joint** theorem.

It does not rule them out from the one-converter condition alone. For
example an invertible diagonal C is diagonally equivalent to its ordered
identity eigenbasis. The proof below therefore only invokes the nonzero
entry cross-ratio test after the swap condition has forced bc!=0.

## 3. Exact one-converter condition for bc nonzero

For bc!=0, choose the normalized eigenbasis

    S=[[1,1],[(lambda+a)/b,(mu+a)/b]].

Both lower entries are nonzero: if a were an eigenvalue, its characteristic
equation would force bc=0. If S=A C B, its zero pattern forces a,d!=0.
The diagonal-equivalence criterion consequently reads

    ad/(bc)=(mu+a)/(lambda+a).

Put z=bc. Using ad=1+z gives a=lambda+tau z. Substituting this in
`a(tau+a)+z=1`, expanding in characteristic two, and using lambda mu=1
gives

    z[1+tau^2+tau^2 z]=0.

Since z!=0 and tau!=0, this is equivalent to

    bc=(tau^2+1)/tau^2,
    a=mu^2/tau,          d=lambda^2/tau.                (UN3)

Conversely UN3 gives the correct trace, determinant and nonzero cross
ratio, hence a one-transform converter. Its only excluded trace is tau=1,
which would force bc=0. Define

    beta=(tau+1)/tau,    g=beta/b,    G=diag(g,1).

Then beta is in K and beta^2=bc. No perfect-field or square-root-existence
assumption is needed. Direct multiplication gives

    G C G^(-1)=[[a,beta],[beta,d]].                     (UN4)

The one-converter condition itself has forced diagonal symmetrizability.

## 4. The swap condition depends only on bc

Cayley-Hamilton gives C^2=tau C+I. For D=diag(s,t), the two diagonal
entries of C D C^2 vanish precisely when

    [[a(tau a+1), tau bc],
     [tau bc, d(tau d+1)]] [s,t]^T=0.                  (UN5)

The off-diagonal coefficients are nonzero, so this matrix is singular
exactly when it has a kernel vector with s,t both nonzero. The resulting
word is invertible with zero diagonal, and an invertible left diagonal E
scales its two off-diagonal entries to one. Its determinant simplifies to

    1+bc(tau^2+1).

Combining this with UN3 gives `(tau^2+tau+1)^2=0`. Since K is a field,
tau^2+tau+1=0. Substituting tau=lambda+lambda^(-1) yields
`lambda^4+lambda^3+lambda^2+lambda+1=0`, which is equivalent here to
lambda having order five. Conversely order five makes UN5 singular and
UN3 says bc=tau^2. This proves both directions of UN.

At order five beta=tau, so UN4 is exactly the earlier symmetric gate.
Conjugating a zero-diagonal invertible word by G changes only its two
nonzero entries, which E can rescale. Thus diagonal conjugation preserves
the required swap-word existence; it does not change the word's powers.

## 5. Finite verification and limits

The separate verifier enumerates all determinant-one gates with an ordered
split distinct spectrum over F4, F8 and F16, including zero entries. It
checks actual diagonal equivalence of eigenbases, separately classifies
the bc!=0 converters, enumerates invertible D for every converter, and
tests the field-universal conclusion. The predicted nontriangular F16
counts are 180 ordered converters and 60 joint gates; these predictions
are checked rather than used to define the enumeration.

The extension still says nothing about another word `C^r D C^s`, a
larger block, a repeated/nonsplit spectrum, a different determinant
normalization, or non-diagonal row conversions. It does not price a whole
finite repair or improve the global profile. Those require their own
complete identities and physical invoice.

Credits: @CubeJerry; E003 C's order-five gate; the earlier lead cross-ratio
and word classification; substantial AI-assisted derivation. No literature
priority, formal-machine or human-refereeing claim.
