# Independent phased-return and mixed-interface review

**PASS: exact source gauges, actual three-bank ordinary unit/inverse, all-width
D8 kernel, and the scoped exclusion of this fixed Cmix from a (4,2,1) endpoint.
No complete endpoint or supplier, improved kappa, or foundational discharge.**

Worker C, S020, 17 November 2026. Author package:
`workers/B/return-clock-source-interface`. Its four pinned files are recorded
in this review's manifest. No author algebra or compiler implementation is
imported by the independent checker.

## 1. Source convention and inherited return

The source is A=C_b S, with

    S|a,b,c,d> = (-1)^(abd)|b,c,d,a>,
    C_b=((1+i)I+(1-i)X_b)/2.

The checker reconstructs this product and all16 direct source columns, and
verifies their equality and unitarity. D_j denotes phase i^(bit j).
The return with s=SWAP_bc is inherited from S019's
`checkpoint3-evidence/C/s3-review`, including its explicit
`actual_return_monomial_A_Sbc_A` certificate. It is not newly discovered here.
The independent reconstruction fixes its literal form:

    A s A = r,       r|a,b,c,d> = |d,1-c,a,b>.

Indeed K=S s maps to (c,b,d,a) with phase (-1)^(acd), so it fixes b and
commutes with C_b. Since C_b^2=X_b, A s A=X_b S s S; the two cubic phases
cancel. Consequently A s A^j=r A^(j-1) for every j>=1.

## 2. New phased involution and exact gauges

Set

    h=s D_b D_c^-1,       ell=K D_b,
    R0=D_c D_d^-1,        R1=D_d D_a^-1,        R2=D_a D_b^-1.

The input phase of h is i^(b-c), which reverses on the second application,
so h^2=I. K commutes with both C_b and D_b. Exact two-by-two multiplication
gives C_b D_b C_b=D_b C_b D_b. Together with literal transport through S this
gives A h A=ell A R0. The further identities R0 A=A R1 and R1 A=A R2 give

    A h A^j = ell A^j R_(j-1),       j=1,2,3.

Every gauge is an actual root-four monomial, with its complete table recorded.
The interval j=1,2,3 is explicit; no next transport is presumed. Tensoring
the literal identities proves them at every collective tail width W. A fixed
identity prefix may also be attached, retaining any previously required price
of its native normalization.

The Gaussian ranks per source column are:

| Head g in A g A^j | j=1 | j=2 | j=3 |
|---|---:|---:|---:|
| I | 2 | 3 | 4 |
| h | 1 | 2 | 3 |
| s | 0 | 1 | 2 |
| s h | 2 | 3 | 4 |

For all12 entries, the independent checker constructs actual root-four
monomials L,R with A g A^j=L C_rank R, where C_rank is the product of standard
C butterflies on `rank` bits. It multiplies the three matrices and checks
every entry. Support counts alone are not used as Gaussian classification.
Complete support blocks are normalized by ((1+i)/2)^rank; cross phase
differences form binary Walsh characters. A character basis supplies row and
column permutations, and residual root-four phases supply L,R. Tensoring these
actual gauges proves the all-width classes, with rank multiplied by W.

## 3. Actual mixed interface and inverse

Write P_u=(I+u)/2, N_u=(I-u)/2, and

    Rot_ij(u)=[[P_u,-N_u],[N_u,P_u]].

The chronological rotations are Rot_01(h), then Rot_12(s), giving

    Cmix = [[P_h,       -N_h,        0],
            [P_s N_h,    P_s P_h,  -N_s],
            [N_s N_h,    N_s P_h,   P_s]].

No commutation between s and h is assumed. For B=[[1,1],[1,-1]], the word
X<-X+Y; Y<-(-2)Y; Y<-Y+X is B on arbitrary X,Y, at two ADDs and one unit
SCALE. Appending SCALE by1/2 on both banks implements B^-1, at two ADDs and
three SCALEs. Thus B diag(I,u) B^-1 is the controlled swap
[[P_u,N_u],[N_u,P_u]], at four ADDs, four SCALEs, and one MONO. Prepending
MONO(u) on the second bank gives Rot(u); appending it gives Rot(u)^-1.

Both directions of Cmix consequently cost **8 ADD + 8 SCALE + 4 MONO**.
The checker replays all48 independent input columns, compares the forward
result to the displayed blocks, and verifies both inverse products. All16
single-ADD omissions fail. All banks remain arbitrary; there is no zero
workspace, owner, erasure, or hidden Gaussian call. Erasing h's input clock
phase fails its proposed gauge, providing a separate phase control.

A conservative uniform primitive-prefix bound is14 in bank maximum norm:
one displayed rotation word has intermediate bound at most7 times its input
maximum by the triangle inequality, while the completed rotation has bound2
because P_u,N_u each have monomial coefficient norm at most1. The second
rotation therefore has bound14. The inverse has the same bound. This is not
asserted sharp; ordinary costs still belong in a full caller.

## 4. All-width active-column kernel

The active first column T=(P_h,P_s N_h)^T has

    ker T = ran N_h intersect ran N_s.

The first kernel equation gives N_h x=x; the second gives P_s x=0. The converse
is immediate. Put d0=s h=D_b D_c^-1. The literal relations d0^4=I and
s d0 s=d0^-1, with all eight monomials distinct, give D8. Since h=s d0,
the common-minus projector is

    Eminus=(I-s)(I+d0+d0^2+d0^3)/8.

The rotation average projects to d0=1 and commutes with s, so this is the
product of commuting Hermitian projectors with the claimed range. The checker
verifies its identities in the faithful eight-dimensional regular
representation, where its trace is1, and its zero width-one source image.

The four rotation traces are (16,8,0,8), and all four reflection traces are8.
Tensor-product traces imply, for every W>=1,

    dim ker T = (16^W-2*8^W)/8.

A fixed identity prefix of dimension p multiplies this by p. The dimensions
are0 at W=1,16 at W=2, and384 at W=3. Width-one injectivity must not be
extrapolated. This physical kernel alone does not establish cancellation
after a native Gaussian path.

## 5. Independently derived scoped (4,2,1) obstruction

Fix this Cmix and the retained native blocks

    L=[[a,0,0],[I,a,0],[0,0,I]],
    U=[[a,-a^2,0],[0,a,0],[0,0,I]].

For Q[:,2]=(p,z,w), the rightmost L leaves this column unchanged. Direct
multiplication of L Cmix U Q[:,2] gives in output0

    (a^2(p-z)+(a h a)(p+z)-a^3 z-(a h a^2)z)/2.      (1)

Use the retained uniform fixed finite ordinary collective-tail catalogue,
allowing fixed finite prefix-matrix coefficients. At sufficiently large
faithful widths, distinct Gaussian word classes have independent coefficient
spans. The tensor Gram argument establishes this: distinct projective
normalized one-column words have inner product magnitude strictly below1,
so a fixed finite catalogue becomes independent at large width. Projective
duplicates retain their actual phases. This is not a claim about every width,
a growing catalogue, or arbitrary new noncollective tails.

Only -a^3 z/2 has class3 in (1). A target using only classes1,2,4, including
ordinary invertible endpoint changes, has no class3, so z=0. The only ordinary
part of output1 is r(p+z)/4. Explicitly that output is

    P_h a p - P_h a^2 z - N_h a z
    + a P_s N_h a p - a P_s N_h a^2 z
    + a P_s P_h a z - a N_s w.

The first three terms have classes1 or2; the last has class1. Expanding the
remaining projector products gives heads I,h,s,sh. Section2 shows that only
their j=1 s heads are ordinary, contributing r p/4 and r z/4. Thus absence
of class0 forces p+z=0, hence p=0.

The remaining physical source column is (0,-a N_s w,P_s w). Its class0 part
forces P_s w=0, so w maps into the proper subspace N_s, whose dimension is
(16^W-8^W)/2, multiplied by a fixed prefix dimension if present. Therefore
(0,0,w) has no left inverse and cannot be a column of an invertible Q.

This excludes the fixed Cmix from (4,2,1) in the stated uniform catalogue,
including arbitrary ordinary Q and endpoint units. It uses class separation,
not a false all-width extrapolation of the width-one active kernel. Changed
first interfaces or different actual endpoint profiles remain open. The
source gauges, paid unit and inverse remain valid positive local results.

## Reproduction and independence

Run `python -B check.py --arithmetic PATH --out RESULT.json`. PATH is the
frozen C Gaussian-dyadic checker, SHA256
5a75913c9f2f9f55fe33174802e3fa40b8e1358ccb3966ce6638eaab9b4ffedb.
Only its Gaussian Fraction value type and generic primitive interpreter are
used. Source matrices, gauge reconstruction, rotation words and D8 geometry
are independently constructed. The finite replay verifies literal identities;
Sections2--5 provide all-width reasoning and explicit scope.

Credit B's phased involution and mixed-interface proposal, the retained source,
the historical S019 return, root's coordination, and substantial OpenAI
assistance. The multiplication exponent and all broader supplier and compiler
obligations are unchanged.
