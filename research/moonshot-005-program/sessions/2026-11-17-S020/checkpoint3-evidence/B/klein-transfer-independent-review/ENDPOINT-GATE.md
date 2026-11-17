# The transferred column passes the coset test but cannot have independent endpoints

**Scoped universal obstruction for the original Klein first interface and
every ordinary Q with the specified last column. The positive dyadic transfer
and its inverse remain valid. A changed last column or first interface is
not excluded. No complete supplier or new kappa.**

## 1. Source, endpoints, and exact quantifiers

Retain the literal four-bit source a=A^(tensor V), the collective involutions
s=SWAP_cd and t=X_c X_d, and the reviewed first interface

    C=[[Ps,-E,-F],[Pt,I-E,0],[Pst,0,I-F]],
    E=(I-s)(I+t)/4, F=(I-s)(I-t)/4.

Use the native word Efull=L C U_native Q L, with L and U_native as in the
Klein package. All entries of C,Q and both endpoint units and their actual
inverses lie in a fixed finite ordinary root-four collective catalogue.
Coefficient sums are formed after lifting. The conclusions below hold at
all sufficiently large faithful widths divisible by four for the complete
catalogue. Width-dependent exterior coefficients do not change the argument;
the complete catalogue is fixed.

Write sj=a^-j s a^j, tj=a^-j t a^j. Put

    U=a^2, P'=(I+a t a^-1)/2, M'=I-P',
    e=(I+s1)(I-t1)/4.

The actual transports are ordinary for j=1,2; a t a^-1 is ordinary as well.
In contrast, U s1 U^-1=A^2 s1 A^-2 lifted collectively is nonordinary.
Its one-column matrix has exact Gaussian rank two. Also

    U t1 U^-1=a t a^-1,    [s1,t1]=0.               (1)

The sector e has rank D/4 at every positive width, D=16^V. This follows from
the literal traces tr(s1)=8, tr(t1)=0, tr(s1t1)=8 before lifting.

Independent (4,2,1) endpoints mean an actual factorization

    Efull=O diag(F4,F2,F1) Iin,                     (2)

where O,Iin are ordinary invertible three-bank operators and each Fr is an
invertible exact Gaussian-r job on one whole bank. This definition includes
both endpoint encoders and decoders. No numerical class rank or analytical
component projection is substituted for (2).

## 2. A partial-column condition that is sufficient for the obstruction

Let Q[:,2]=(p,z,w)^T. Suppose

    p e=e, z e=0, w e=0.                           (3)

The transferred column from C's positive construction satisfies (3):

    N0=(I-s1)(I+h)/4,
    p=I-N0, z=G N0, w=0,

because h commutes with s1 and N0 e=0. The rest of Q is arbitrary. In
particular, the theorem includes every ordinary completion with this same
last column, not merely the published high/low example.

The last column of L is the third basis vector. The Gaussian-two part of
L C U_native Q[:,2] e is therefore exactly

    E2[:,2] e=(U e,0,0)^T.                         (4)

For completeness, the two-source part from p is
(U Ps1 p,U Pt1 p,0)^T. All z and w terms disappear after multiplying e
by (3), and Ps1 e=e, Pt1 e=0. The remaining one-source terms have class one
and do not affect (4). Tensor-word class separation justifies this
component statement; extracting a Gaussian class is not an executable step.

## 3. The ordinary row annihilator is forced into one plus sector

Let (b0,b1,b2) be the row of O^-1 selecting the Gaussian-four endpoint in
(2). It annihilates the entire Gaussian-two component. Equation (4) gives

    b0 U e=0.                                     (5)

By (1) and commutation,

    U e=(M' U+M' U s1)/2.                          (6)

The two one-column word sets G U and G U s1, with G the finite group of
literal ordinary monomials, are disjoint even projectively. Otherwise
gU=g'Us1 up to a scalar phase would make U s1 U^-1 ordinary, contrary to
the literal source calculation. Adjoin all terms in b0 M' to the finite
catalogue and apply faithful tensor separation to (5)-(6). The two terms
cannot cancel each other. Since U is invertible,

    b0 M'=0, or b0=b0 P'.                          (7)

This is a source-specific ordinary annihilator theorem. It is stronger
than merely observing a physical subspace intersection at one width.

## 4. Two same-plus channels cannot encode the quartic bank

Only the four-source path through the first column of C can contribute to
the Gaussian-four component. Its two active entries are

    (a Ps a,a Pt a,0)^T.

The second entry is fixed on the left by P', because a Pt a=P' a^2.
The third output row has at most three source factors. Ordinary Gaussian
class extraction therefore gives, for every Q,

    E4[2,:]=0, P' E4[1,:]=E4[1,:].                 (8)

Let (c0,c1,c2)^T be the quartic encoder column O[:,0]. The row
F4 Iin[0,:] in (2) is surjective, so (8) implies

    c2=0, P' c1=c1.                                (9)

The actual inverse identity O^-1 O=I gives b0c0+b1c1=I. Using (7), the
ordinary column and row

    Cfree=(P' c0,c1)^T, Dfree=(b0,b1)

satisfy

    diag(P',P') Cfree=Cfree, Dfree Cfree=I.          (10)

Thus two identical plus sectors of a nonidentity ordinary involution would
contain a split free ordinary bank. At a faithful width the regular trace
of diag(P',P') is 1, while its augmentation rank is 2. The admitted
dimension/augmentation capacity theorem excludes equality with one free
bank. This contradicts (10), and proves that (2) is impossible under (3).

The contradiction uses the actual endpoint inverse supplied by (2); it
does not assume that a physical-rank-D projector is already a free bank.

## 5. A direct overlap for the particular high/low completion

C's Qhighlow has quartic image

    im((M' a^4,P' a^4,0)^T).

Equation (4) lies in this image, since P' U e=U Pt1 e=0. Hence its quartic
and quadratic images intersect in at least D/4 dimensions. This gives a
short direct exclusion of that particular Q. Sections 3-4 are stronger:
changing the other columns and the quartic image still cannot repair any
completion retaining (3).

## 6. A useful exact rank and the width-one coincidence

For the transferred column, the entire Gaussian-two last column is

    (U M0,U M1,-U z)^T,
    M0=Ps1 p-E1 z,
    M1=Pt1 p+(I-E1)z,
    E1=(I-s1)(I+t1)/4.

Its kernel is R1(I-N0), where R1=(I-s1)(I-t1)/4. Indeed z v=0 forces
N0 v=0 and hence p v=v; the remaining equations then say Ps1v=Pt1v=0.
The literal h also commutes with t1. Thus this kernel is the commuting
three-involution sector

    (I-s1)(I-t1)(I-h)/8.

The eight literal traces give the exact all-width rank

    dim ker(E2[:,2])=(D-2*8^V)/8,
    rank(E2[:,2])=7D/8+8^V/4.                      (11)

It is full rank at V=1 but has defect 16 at V=2. Likewise N0 equals R1 at
V=1 and differs from it at V=2. These small-width coincidences cannot be
used as all-width endpoint or kernel identities.

## 7. Consequence for the continuing construction

The transfer h,G,V0 and its primitive unit/inverse are correct; the prior
per-irrep coset comparison is genuinely resolved by that construction.
Its last column nevertheless fails the stronger independent-endpoint
obligation. A new column must alter its action on the plus/minus sector e
so that (3) no longer holds, or change the first interface. The sequential
first completion and shifted transfer covers remain separate questions.

Credit @CubeJerry, C's positive dyadic transfer and previous coset criterion,
the retained four-bit source, C's capacity theorem, B's independent endpoint
argument, and substantial OpenAI assistance. No new complete exponent or
supplier is claimed; all complete-cost and foundational obligations remain.
