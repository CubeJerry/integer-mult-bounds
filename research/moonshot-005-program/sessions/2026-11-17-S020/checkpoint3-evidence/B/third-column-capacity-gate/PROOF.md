# A third-column capacity gate for conditional-rotation completions

**Scoped all-catalogue obstruction. This concerns Crot below, with completely
arbitrary ordinary Q. It does not concern the retained C_T completion, whose
third source column is (0,a,0)^T. No caller, supplier or new kappa is claimed.**

## 1. Exact hypotheses

Let a=A^(tensor V) be the pinned four-bit source, so that a,a^2,a^3 have exact
Gaussian ranks 1,2,3. Work in the retained fixed finite root-four collective
monomial interface, at sufficiently large faithful widths divisible by four.
Enlarge the finite proof catalogue to include every ordinary coefficient and
endpoint inverse used below. Distinct Gaussian classes then separate, and
ordinary multiplication preserves their component spaces.

Let T be an ordinary self-adjoint idempotent, N=I-T, and suppose

    T1=a^-1 T a, T2=a^-2 T a^2, Nj=I-Tj

are ordinary. Let G be a finite ordinary group containing their coefficient
supports. Assume in C[G] that

    tau_reg(N1)+tau_reg(N2)=1,
    rank epsilon(diag(N1,N2)) != 1.                 (1)

Here tau_reg is normalized regular trace, and epsilon sends each collective
monomial to 1 at widths divisible by four. The most relevant case is
tau_reg(N1)=tau_reg(N2)=1/2 with equal scalar augmentations, either both 0 or
both 1. The capacity theorem then says that diag(N1,N2) cannot contain a
split free ordinary bank: equality in regular dimension would force its
augmentation rank to be 1.

Set

    L=[[a,0,0],[I,a,0],[0,0,I]],
    U=[[a,-a^2,0],[0,a,0],[0,0,I]],
    Crot=[[T,0,-N],[0,I,0],[N,0,T]].                (2)

The ordinary unit Crot has inverse

    [[T,0,N],[0,I,0],[-N,0,T]].                     (3)

It is actually the three coefficient shears E20(N), E02(-N), E20(N), in
chronological order; the inverse reverses this word and negates its entries.
The coefficient sums and every source/scale/ADD restoration remain paid.

**Theorem.** No ordinary unit Q makes L Crot U Q L equivalent, by actual
ordinary invertible endpoint maps, to three independent Gaussian (4,2,1)
jobs. Q need not be block diagonal, triangular, or a rank-one-isolating
completion. All three banks and every entry of Q remain available.

## 2. The last native input column

Write Q[:,2]=(p,z,w)^T. The last column of L is e2, so the last output column
of E=L Crot U Q L is simply L Crot U (p,z,w)^T. Direct multiplication gives

    row0 = a^2 T1 p - a^3 T2 z - a N w,
    row1 = a T1 p + a^2 N2 z - N w,
    row2 = a N1 p - a^2 N2 z + T w.                (4)

Every coefficient to the right of a,a^2,a^3 is ordinary. In particular,
these displayed pieces have Gaussian classes 1,2,3 respectively; the last
two ordinary terms have class 0. This assertion uses the tensor-word class
decomposition, not a numerical rank assigned to a sum.

Independent (4,2,1) endpoints imply that E contains only these three classes.
The class-0 pieces in (4) give Nw=Tw=0, hence w=0. The class-3 piece gives
T2 z=0, hence z=N2 z. Therefore the exact Gaussian-two component of the
last output column is

    (a^2 T1 p, a^2 z, -a^2 z)^T.                   (5)

## 3. Endpoint independence creates an ordinary kernel constraint

For the Crot in (2), C10=0. Every lower output-row term in the whole word
has at most three source factors. Consequently its Gaussian-four component
is zero. The complete E4 is supported in output bank 0.

An independent Gaussian-four endpoint has rank D, where D=16^V. Since E4 is
contained in the D-dimensional top bank, its image is exactly that entire
bank. Independence of the endpoint jobs therefore implies

    im(E2) intersect (top bank) = {0}.              (6)

If zv=0 for a physical input vector v, (5) belongs to the top bank. By (6)
it must be zero, and a is invertible. Thus

    ker(z) is contained in ker(T1 p).              (7)

This argument does not extract a Gaussian class as a free operation. It is
a necessary consequence of the claimed independent endpoint identity.

## 4. A forbidden split ordinary bank

Consider the ordinary two-bank column

    F=(N1 p,z)^T.                                  (8)

It is injective. Indeed Fv=0 implies zv=0 and N1pv=0. Equation (7) then
gives T1pv=0, so pv=0 as well. Since w=0 and Q is invertible, Q[:,2]v=0
forces v=0.

At a faithful width, injectivity of (8) gives a left inverse in the finite
ordinary group algebra. Explicitly, F*F is invertible in C[G], and

    D=(F*F)^-1 F*,    DF=I.                        (9)

The inverse belongs to the same finite semisimple algebra: every irreducible
component is present in a faithful representation, and F*F is nonsingular
on each component. If the original coefficients are Gaussian-rational,
ordinary linear algebra supplies the inverse over that coefficient field.
This is an algebraic consequence, not a newly granted physical inverse.

Furthermore diag(N1,N2)F=F, by idempotence and z=N2z. Thus (8)-(9) split one
free ordinary bank inside diag(N1,N2). This contradicts (1) and the admitted
regular-dimension/augmentation capacity theorem. QED.

## 5. Literal covered instances and a width-one warning

Both spectator signs

    T=(I +/- SWAP_cd^(tensor V))/2

satisfy the theorem: the two transported monomials are SWAP_ad and SWAP_ab,
all are nonidentity involutions, and their complement augmentations agree.
For the plus choice the two complements have augmentation 0; for the minus
choice they both have augmentation 1. Their regular traces are 1/2.

A distinct covered control is g=SWAP_cd Z_c, of order four, with

    T=I/2+(1-i)g^(tensor V)/4+(1+i)(g^3)^(tensor V)/4.

This selects the collective eigenvalues 1 and i. It is an ordinary Hermitian
idempotent, with regular trace 1/2 and augmentation 1. Both first and second
backward conjugates of g are literal ordinary monomials. The checker retains
their phases. This projector is formed after tensor lifting; substituting
the tensor power of its one-column projector is false at width two.

For this C4 instance the three-shear recipe and its inverse each use
9 ADD, 18 SCALE and 12 MONO calls. A uniform prefix bound is 77/8: each
coefficient recipe restores its arbitrary source, the coefficient l1 sum
of N is at most 3/2, and the three target bounds are 5/2, 19/4, 77/8.
The smaller exact width-one prefix value 5/2 is retained only as a finite
control, not as an all-width precision bound.

The all-width ordinary conclusion cannot be replaced by a width-one rank
test. For the two plus spectator complements, the stack (P_ad,P_ab)^T is
physically injective when V=1: the common alternating S3 sector is absent.
At V=2 that sector has dimension 16. The regular capacity proof keeps all
representations at faithful widths and does not discard this sector.

## 6. Scope boundary and next question

The retained completion

    C_T=[[T,N,0],[0,I,I],[N,T,0]]

has third source column L C_T U e2=(0,a,0)^T. It therefore permits an
arbitrary Gaussian-one contribution from w=q22; equation w=0 is false for
that completion. This theorem neither extends the prior S3 obstruction from
its prescribed Q_R to arbitrary Q nor excludes the new Klein completion.
The surviving construction must retain such a third-source channel, or alter
the endpoint profile or the regular-capacity hypothesis.

Credit @CubeJerry, the retained literal four-bit source and S019 transports,
C's ordinary-module capacity theorem and correction of the C_T scope,
B's third-column argument, and substantial OpenAI assistance. The full
ordinary/compiler/precision/ownership/recursive obligations and all five
foundations remain; no new complete multiplication exponent is obtained.
