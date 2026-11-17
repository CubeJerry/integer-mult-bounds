# An explicit dyadic transfer into the Klein kernel

**Constructive all-width second interface. The previous representation
comparison is resolved positively; the complete caller remains open.**

The original Klein completion required a coupled last column `(p,z,0)`
with `z=R2 z` and `P_H(s1-I)p=0`, where H is the monomial intersection
group for A^2. The standard choice `(I-R2,R2,0)` failed the latter condition.
This package supplies an explicit replacement that satisfies both, is
isometric, and has an actual three-bank unit completion with a dyadic
primitive word and inverse.

## 1. Literal ordinary operators

Retain `A=C_b Rsrc`, `Rsrc=D_(acd)P`, and the spectator involutions
`s=SWAP_cd`, `t=X_c X_d`. Define the ordinary backward transports

    s1=A^-1 s A=SWAP_ad,
    s2=A^-2 s A^2=SWAP_ab,
    t2=A^-2 t A^2.

For a basis vector indexed by bits `(a,b,c,d)`, let delta be the indicator
of `a=d`. Introduce the ordinary monomial h by

    c -> c xor delta,
    input phase i^((1-2c)*delta).

Thus h is Pauli Y on c when a=d, and identity otherwise. It is an
involution and commutes with s1. Its phase is essential. The phase exponent
can also be written modulo four as

    1-a-d-2c+2ad+2ac+2cd.

Its permutation is `X_c CNOT_a,c CNOT_d,c`, with the displayed input phase.
The exact independent checker verifies

    A^2 h A^-2 is a root-four monomial.               (1)

Consequently h belongs to H, the exact group used in the preceding
left-coset condition. Removing h's phases makes (1) false.

The second new ordinary monomial G has destination table

    [0,1,3,5,7,9,4,13,2,8,6,11,10,15,14,12],

with input phase -1 at indices 13 and 15 and phase +1 at every other
index. Its actual inverse is the inverse permutation with conjugated
phases. Exact matrix multiplication gives

    G s1 G^-1=s2, G h G^-1=s2 t2.                   (2)

No Gaussian operation is used to execute h, G, or either inverse. Their
literal monomial tables and the table in (1) accompany the checker.

## 2. A quarter-projector transfer with no extraction assumption

All following symbols denote collective tensor lifts at positive width V,
with projector sums and coefficients formed after lifting. Put

    N0=(I-s1)(I+h)/4, R2=(I-s2)(I-t2)/4.

Commutation and (2) imply

    G N0 G^-1=R2.                                   (3)

Indeed `(I-s2)(I+s2 t2)=(I-s2)(I-t2)`. Equation (3) is an equality of
actual ordinary idempotents at every width, not only an equality of their
dimensions or scalar characters.

The one-column traces of s1 and h are both eight; the product s1h has
trace zero. Hence

    rank(N0)=(16^V-8^V+8^V-0)/4=D/4.

R2 has the same rank. Both have regular trace 1/4 and ordinary augmentation
zero. Define

    V0=G N0.

Then exactly

    V0* V0=N0, V0 V0*=R2.                            (4)

Thus this is an explicit ordinary partial isometry, without treating a
projector image as a free bank or invoking an unimplemented spectral
inverse.

## 3. The previous coset condition is satisfied

Let `D0=P_H(s1-I)` and let N be its right-support projector, as in the
preceding coupled-column criterion. Since h belongs to H and commutes
with s1,

    D0 N0=D0.

For example `(s1-I)(I-s1)=2(s1-I)`, and multiplication by `(I+h)/2`
does not change P_H(s1-I). Therefore

    N<=N0,
    P_H(s1-I)(I-N0)=0.                              (5)

The previously unevaluated per-irrep condition `rank rho(N)<=rank rho(R2)`
now follows in every irreducible representation from (3) and (5). No
enumeration of the enormous ordinary group is needed.

The actual column

    (p,z,w)^T=(I-N0,G N0,0)^T                        (6)

is isometric by (4), satisfies `z=R2 z`, and obeys the stronger Gaussian-two
left-coset constraint (5). This is the promised positive escape from the
standard unrotated quarter-kernel route.

## 4. Actual unit completions and inverses

The two-bank map

    T(V0)=[[I-N0,-V0*],[V0,I-R2]]

is an actual unit. Its chronological coefficient word is

    E10(V0), E01(-V0*), E10(V0).

The inverse reverses the order and signs. Embedding it on banks 0 and 1
and exchanging input banks 0 and 2 gives

    Qcolumn=[[0,-V0*,I-N0],[0,I-R2,V0],[I,0,0]],

whose last column is exactly (6). Both the ordinary unit and inverse act
on all three arbitrary bank inputs; no input is set to zero.

There is also a concrete extension preserving that last column while
creating a full quartic component. Let

    E2=(I+s2)(I+t2)/4, M=I-E2,
    g=Rsrc^-1 X_b,
    W=J_M diag(I,g), J_M=[[I-M,-M],[M,I-M]].

The literal return identities are `A g A=Rsrc` and `A^2 g A=A Rsrc`.
Define

    Qhighlow=Qcolumn diag(W,I).

Its explicit matrix is

    [[-V0* M, -V0* E2 g, I-N0],
     [(I-R2)M, E2 g, V0],
     [E2, -M g, 0]].

All factors have actual inverse words. In the native word L C U Qhighlow L,
the quartic component is supported only in input column zero and equals

    -(1/2)(M'_t a^4,P'_t a^4,0)^T,

where `P'_t=(I+A t A^-1)/2`, `M'_t=I-P'_t`. Its rank is D, and the two
ordinary complementary output sectors admit a charged ordinary route.
The proof is the same exact e_+-/e_-+ quartic decomposition already checked
in the preceding package. The changed q00 and q01 contain at most three
source factors and cannot create a Gaussian-four term.

This identifies the full quartic component; it does not state that the
remaining Gaussian classes cancel or that independent (4,2,1) endpoints
have been obtained.

## 5. Primitive receipts

V0 is the four-term ordinary sum

    (G-G s1+G h-G s1 h)/4.

Its adjoint is implemented with the inverse monomial tables. Each term
temporarily applies its monomial and dyadic coefficient to the source,
adds to the destination, then undoes both changes. Arbitrary source
contents are restored. The verified full-field primitive receipts are:

| Map | ADD | SCALE | MONO | Prefix magnitude bound |
|---|---:|---:|---:|---:|
| Qcolumn | 15 | 27 | 24 | 11 |
| Qcolumn inverse | 15 | 27 | 24 | 11 |
| Qhighlow | 30 | 53 | 43 | 79 |
| Qhighlow inverse | 30 | 55 | 43 | 109 |

Every MONO is a charged full-field pass with its literal table. No
Gaussian query, zero bank or new owner is added. Scalar expansions use
only nonzero dyadics, including the temporary inverses. The fixed catalogue
contains all displayed products and inverses.

These are complete receipts for these ordinary maps. Their compiler,
precision and recursive contributions remain part of the eventual full
supplier invoice; the retained optimistic Gaussian margin is not a
complete-budget certificate.

## 6. Independent verification and scope

The checker uses C's independently implemented Q(i) column arithmetic and
does not import B's discovery engine. It reconstructs the source, derives
the literal h table, checks all conjugacies including phases, proves the
finite partial-isometry identities, replays all four primitive words on
all arbitrary inputs, and checks both inverse products. Negative controls
remove h's phases and G's two signs and are rejected. The all-width proof
uses tensor multiplicativity and exterior projector sums, not a small-width
rank extrapolation.

This package supersedes only the earlier statement that the old Klein
last-column representation comparison was unevaluated. It does not alter
the earlier exclusion of `(I-R2,R2,0)`, and does not claim a complete caller.
Full class cancellation, independent endpoint units, and the full supplier
cost remain open. No strict supplier or new complete kappa is claimed.

Credit @CubeJerry, the retained source authors, B's Klein interface and
Fourier-fibre observation, the root/C capacity work, and substantial OpenAI
assistance. Worker C constructed h, G, the dyadic transfer, both actual
second-interface words and the independent exact verifier.
