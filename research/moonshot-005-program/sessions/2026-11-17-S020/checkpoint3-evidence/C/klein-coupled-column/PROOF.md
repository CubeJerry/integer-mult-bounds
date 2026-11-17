# Coupled last-column conditions for the original Klein completion

**An exact necessary representation condition and a scoped route exclusion.
The general Klein interface remains open. No complete (4,2,1) caller.**

This package concerns the reviewed first interface

    C=[[Ps,-E,-F],[Pt,I-E,0],[Pst,0,I-F]],
    Ps=(I+s)/2, Pt=(I+t)/2, Pst=(I+st)/2,
    E=e_-+, F=e_--,

with `s=SWAP_cd`, `t=X_c X_d`, and the literal source `a=A^tensor(V)`.
Projectors are formed after the collective tensor lift. It does not cover
different first columns or completions such as B's later sequential route.

## 1. Exact last-column constraints

Let `sj=a^-j s a^j`, `tj=a^-j t a^j` for j=1,2, and
`R2=(I-s2)(I-t2)/4`. These transported involutions are ordinary. Put

    K=(a Ps a,a Pt a,0)^T, W=(0,Ps,Pst)^T,
    Z2=(-a E a,a(I-E)a,0)^T, Z1=(0,-E a,0)^T,
    F1=(-a F,0,0)^T, F0=(0,-F,I-F)^T.

The exact native expansion is

    L C U=[K+Wa, -Ka-Wa^2+Z2+Z1, F1+F0].

For `Q[:,2]=(p,z,w)^T`, therefore,

    Efull[:,2]=(K+Wa)p+(-Ka-Wa^2+Z2+Z1)z+(F1+F0)w.   (1)

Use the admitted fixed-catalogue tensor-separation scope, including all
ordinary endpoint units and inverses, at sufficiently large faithful
widths divisible by four. The terms K,Z2,Wa^2 are pure Gaussian class two,
Ka is pure class three, Wa,Z1,F1 are pure class one, and F0 is ordinary.
The backward transports prove these statements without commuting arbitrary
Q entries past a source.

Independent (4,2,1) endpoints require absence of classes zero and three.
Equation (1) consequently gives

    z=R2 z, w=0.                                    (2)

The first follows from the exact Ka kernel. The second follows because
F0 is injective: its two nonzero components are complementary projectors.
Since epsilon(R2)=0 and epsilon(Q) is invertible,

    epsilon(z)=0, epsilon(p)!=0.

The Gaussian-two scalar image is forced to the line `(1,1,0)`, because
the last column of Phi_2 is `(1,1,0)^T epsilon(p)`. The Gaussian-one line
is similarly `(0,1,1)`. These two scalar lines do not by themselves exclude
an independent quartic image.

## 2. A left-coset quotient retains another necessary equation

Let G be the finite group of all one-column root-four monomial matrices,
modulo scalar fourth roots. This larger group is valid for necessary
conditions on any admitted finite ordinary catalogue. Set

    U=A^2, H={h in G: U h U^-1 is ordinary}, J=<H,s1>.

The Gaussian-two double coset GUG has a quotient that discards its left
ordinary factor and retains the right coset. It is the right permutation
module `C[H\G]`, equivalently `P_H C[G]`, where P_H is the finite subgroup
average. The quotient sends `U h` to `P_H h`. Left multiplication by an
ordinary block acts by scalar augmentation; right multiplication retains
the actual group-algebra action. Projective phases disappear at the chosen
width subsequence, and faithful tensor separation makes this a necessary
quotient of the actual source identities.

A single independent Gaussian-two bank whose scalar image is `(1,1,0)`
must have equal first and second rows in this quotient. Their difference
in the class-two part of (1) is

    a(Ps-Pt)a p+Ps a^2 z-a^2 z.

Equation (2) gives `Ps a^2 z=0`. Both s2 and t2 lie in H, so `P_H z=0`.
Also t1 lies in H because `A^2 t1 A^-2=A t A^-1` is ordinary. Hence the
row-difference equation is precisely

    P_H(s1-I)p=0.                                   (3)

Let N be the orthogonal right-support projector of `D0=P_H(s1-I)` in the
finite semisimple group algebra. Equation (3) is equivalent to

    N p=0, or p=(I-N)p.                              (4)

Q's last column therefore embeds one free ordinary bank in
`diag(I-N,R2)`. The appropriate row of Q inverse is its actual left inverse.

## 3. Representation capacity and a conditional construction

For every irreducible representation rho of G, the necessary condition is

    rank rho(N) <= rank rho(R2),
    rank rho(N)=dim(V_rho^H)-dim(V_rho^J).            (5)

For the second formula, `D0 D0*=2P_H-2P_H s1 P_H`. Its kernel on the
H-fixed subspace consists exactly of vectors also fixed by s1, namely
the J-fixed vectors. This proves the formula in every matrix block.

The literal identity

    A^2 s1 t2 s1 A^-2 is ordinary                    (6)

gives `N R2=0`. Indeed `P_H s1 t2=P_H s1`, while s2 and t2 commute, so
`P_H s1(I-s2)(I-t2)=0`. Together with `P_H R2=0` this gives D0 R2=0
and then N R2=0. The independent checker verifies every phase in (6).

Orthogonality does not settle (5): a coupled map may rotate one module
into an equivalent submodule of the other. Both coarse capacity tests
pass:

    tau(N)=1/|H|-1/|J| < 1/4=tau(R2),
    epsilon(N)=epsilon(R2)=0.

Here H contains a Klein subgroup of order four. Thus a no-go result would
need an individual irreducible block or additional caller equations. The
full comparison (5) has not been evaluated in this package.

Conversely, (5) is sufficient for this module embedding, although not for
the complete caller. It is equivalent to a partial isometry V0 with
`V0*V0=N` and `V0 V0*<=R2`. If an explicit V0 is supplied, set

    p=I-N, z=V0, w=0.

This is an isometric column satisfying (2)-(4), and its two-bank completion

    [[I-N,-V0*],[V0,I-V0 V0*]]

is the actual product of coefficient shears
`E10(V0), E01(-V0*), E10(V0)`. Reversing their order and signs gives its
inverse. Embedding it on banks 0,1 and exchanging input banks 0,2 puts
the column in the final input slot. An explicit V0, its permitted scalar
recipes and full charges remain necessary before this is a physical word.

After any particular Q0 last-column completion is chosen, all completions
with that same column have the algebraic form

    Q=Q0 [[W00,W01,0],[W10,W11,0],[z0,z1,I]],

with W an ordinary two-bank unit. The remaining z0,z1 are ordinary shear
coefficients. This preserves invertibility while exposing linear
cancellation equations for the remaining source components.

## 4. Literal return map and executable coupled example

Write `A=C_b Rsrc`, where `Rsrc=D_(acd)P`. The ordinary unit

    g=Rsrc^-1 X_b

satisfies the phase-sensitive identities

    A g A=Rsrc, A^2 g A=A Rsrc.                       (7)

Thus an ordinary middle direction can lower a three-source path to
Gaussian class one. Rsrc and g were absent as explicit directions in the
earlier finite discovery catalogue. Identity (7) holds at every width.

For E2=e_++(s2,t2), retain R2=e_--(s2,t2), and put

    P=I-R2, M=I-E2, T=I-E2-R2,
    Qexample=[[-R2,0,P],[T,E2 g,R2],[E2,-M g,0]].       (8)

For a projector B, let `J_B=[[I-B,-B],[B,I-B]]` on banks 0,1. Then

    Qexample=J_R2 SWAP02 diag(J_M diag(I,g),I).

Each J_B is three coefficient shears. Expanding M as I-E2 keeps all
temporary scalars and their inverses dyadic. The exact all-input receipts
are:

| Word | ADD | SCALE | MONO | Prefix magnitude bound |
|---|---:|---:|---:|---:|
| Qexample | 30 | 53 | 37 | 79 |
| Qexample inverse | 30 | 55 | 37 | 109 |

All MONO calls are charged full-field passes. Expanding s2t2 into two
generators and g into Rsrc inverse and X_b gives 50 generator passes per
direction. No zero bank, owner, or Gaussian invocation is added.

The quartic component is supported only in input column zero, with output

    -(1/2)(M'_t a^4,P'_t a^4,0)^T,

where P'_t=(I+A t A^-1)/2. Its rank is D. The exact identities are

    a e_+- a^3=M'_t(a^4+B2)/2,
    a e_-+ a^3=P'_t(a^4-B2)/2.

This example is not a caller. Forbidden ordinary and cubic terms remain,
and the fixed last column `(I-R2,R2,0)` already fails (3). Its Gaussian-two
left-coset vectors are exactly

    (1/2,1,0)^T and (1/2,0,0)^T,

on the distinct cosets of A^2 and A^2 s1. Their scalar rank is two, whereas
one whole-bank Gaussian-two output has left-coset image rank at most one.
No modification of Q's other columns can repair this fixed last column.

The obvious alternative `p=(I+s1)/2` satisfies (3), but its range together
with R2 has regular capacity only `1/2+1/4=3/4`, so it cannot form an
injective Q column. A successful replacement must meet both conditions.

## 5. Verification and remaining work

The checker imports only C's independently implemented exact Q(i) matrix
arithmetic. It verifies (6)-(8), the executable words and their inverses on
all three arbitrary inputs, literal monomial tables, complementary quartic
identities and the finite coset premises. The universal statements follow
from the written finite-group and tensor-separation arguments, not from
extrapolating small numerical widths.

The general Klein architecture remains open. Representation comparison,
an explicit partial isometry, all remaining class cancellations, independent
endpoint units and the complete supplier invoice remain unsupplied. No
strict supplier or new complete kappa is claimed.

Credit @CubeJerry, the retained source authors, B's original Klein unit,
root/C's capacity observation, the tensor-separation framework, and
substantial OpenAI assistance. Worker C derived the return map, the coupled
column criterion, the conditional completion and the independently checked
executable example with its scope obstruction.
