# A genuinely three-bank column with actual ordinary endpoint units

**Positive exact one-column interface in the paid distinguished-prefix model.
The complete three-input caller is still open. This is not an independent
(4,2,1) supplier, and its unfixed two input columns cannot be ignored.**

## 1. Two fixed prefix bits and the literal source

Use the paid prefix normalization from distinguished-prefix-native-normalizer.
There are two distinguished bits sigma,tau in the normalized first column;
the other two prefix bits carry identities. Write a=I_prefix tensor A^(tensor W),
where W=V-1. The original head prefix must be restored and charged if an
exact original-width Gaussian head is required.

Let s0=SWAP_cd, s10=SWAP_ad, g0=SWAP_ac and retain
J0=R2^-1 SWAP_ab R2 and K0=A J0 s0 A^-1. Define

    S=Z_sigma tensor s0^(tensor W),
    S1=Z_sigma tensor s10^(tensor W),
    T=Z_tau tensor I, X=X_tau tensor I,
    J=I_prefix tensor J0^(tensor W),
    K=Z_sigma tensor K0^(tensor W),
    G=X_sigma tensor g0^(tensor W).

All these controls are actual ordinary root-four monomials. The source facts
and prefix anticommutation give

    a^-1 S a=S1,  K=a J S a^-1,  [J,S]=0,
    G S1 G^-1=-S,  XT=-TX.                           (1)

The remaining indicated prefix/tail operators commute. Put
P=(I+T)/2, N=(I-T)/2, Ps=(I+S)/2, Ns=I-Ps,
P1=(I+S1)/2, N1=I-P1, and c=(1+i)/2, d=(1-i)/2.
The sign in G S1 G^-1=-S is supplied by the distinguished sigma flip, so
it is valid at every W rather than only at odd tensor widths.

## 2. The first interface and a complete unit for the last column

Let Rot_ij(h) have block [[Ph,-Nh],[Nh,Ph]] on banks i,j. Use

    C=diag(I,J,I) Rot_01(S) Rot_02(T)
     =[[Ps P,-Ns,-Ps N],
       [J Ns P,J Ps,-J Ns N],
       [N,0,P]].                                     (2)

This is an ordinary unit, with its actual inverse given by the reversed
rotations and J^-1. Define

    p=N, z=X P N1, w=X G P P1.                       (3)

The three initial domain projectors N, P N1, P P1 are orthogonal and sum
to I. Hence p*p+z*z+w*w=I. Both z and w are nonzero; they use distinct
quarter-dimensional prefix sectors. Moreover

    Pz=0, S1 z=-z, Pw=0, S w=-w.                    (4)

Write Swap_ij(E) for a bank swap on projector E and identity on I-E. The
literal completion

    Q0=diag(I,X,XG) Swap_12(P N1) Swap_02(N)          (5)

has Q0[:,2]=(p,z,w)^T. Its factors are ordinary units; Q0^-1 is the reversed
word with the diagonal monomials inverted. All three banks are arbitrary.

## 3. An exact source-column identity, including every Gaussian class

Retain the actual native blocks

    L=[[a,0,0],[I,a,0],[0,0,I]],
    U=[[a,-a^2,0],[0,a,0],[0,0,I]].

Define the ordinary output gauge

    H=[[I,-K^-1,0],[I,K^-1,0],[0,0,I]].

Expanding L C U and using (1)-(4), the ENTIRE last column is

    H L C U (p,z,w)^T
      =(-a^2 z,-a^2 z,-a^2 z)^T + (-x,x,a p)^T,
    x=-K^-1 a z+a w=a(-S J z+w).                    (6)

There is no omitted ordinary or cubic term in (6). This is an operator
identity, not an instruction to project into Gaussian classes.

Now set

    O0=[[P,c N,-c N],
        [P X,c N,c N],
        [0,P+c N,N X]],
    ell=c^-1(-S J z+w)+X p.                          (7)

O0 is an actual ordinary three-bank unit. For c=1 its inverse is

    [[P,X P,0],
     [N/2,N/2,P],
     [-(N+X N)/2,(N-X N)/2,X N]].

The displayed O0 is this c=1 unit times
diag(I,P+cN,P+cN), whose inverse is explicit. Equations (6)-(7) give

    H L C U Q0 e2
      =O0 diag(a^4,a^2,a) (0,-c^-1 z,ell)^T.         (8)

Thus O=H^-1 O0 is a genuine ordinary output endpoint unit for this column.
The actual quartic encoder has image (P-bank0) plus (P-bank1), of full
one-bank dimension. The two lower columns of O0 are independent complements;
they are not both graphs with an invertible third component.

## 4. A complete ordinary input endpoint for that column

The input vector in (8) also has a literal ordinary unit completion. Put

    B=N+c^-1 P,
    CG=N+P G,
    I0=E_21(SJ) diag(I,-X,X CG)
          Swap_12(P N1) diag(B^-1,I,B).              (9)

Here E_21(SJ) adds SJ times bank1 into bank2. CG is the ordinary monomial
that applies G on the tau-plus prefix sector and identity on tau-minus.
Direct multiplication gives

    I0 e2=(0,-c^-1 z,ell)^T.                         (10)

Every factor in (9) has its actual inverse. In particular, the nonmonomial
prefix scale B is not free: the paired diagonal is compiled as follows.
For any coefficient unit b,

    diag(b,b^-1)
       =E_02(b-I) E_20(I) E_02(b^-1-I) E_20(-b).

Apply this identity on banks0,2 with b=B^-1=N+cP. Expand b-I=-dP,
b^-1-I=-iP, and -b=-N-cP before compiling coefficient shears. All scalar
terms and their inverses are Gaussian dyadics. No auxiliary zero bank is
introduced; modifying the other endpoint columns is part of a unit endpoint.

Combining (8)-(10), the actual three-native word E=L C U Q0 L satisfies

    E e2=O diag(a^4,a^2,a) I0 e2.                   (11)

The last L fixes e2. Both endpoint units in (11) are physical ordinary words,
not merely retractions or numerical image-rank certificates.

## 5. Complete local primitive receipts

For h an ordinary involution, Swap_ij((I-h)/2) is
H2^-1 diag(I,h) H2, H2=[[1,1],[1,-1]]. The chronological H2 word has
two ADDs and SCALE(-2); H2^-1 adds SCALE(1/2) on each bank. A controlled
swap therefore uses4 ADD,4 SCALE,1 MONO, preserving arbitrary banks.

The conditional involutions needed here, N+P S1 and N+P G, are literal
root-four monomials: a fixed prefix bit selects between two specified tail
permutations/phases. They are fixed uniform monomial address rules. They
also have finite expansions in the declared prefix-matrix/tail catalogue.
No pass is removed because the selector is a prefix bit.

For O0, first permute the six bank/tau roles by
[(0,+),(0,-),(1,+),(1,-),(2,+),(2,-)] ->
[(0,+),(1,+),(2,+),(0,-),(2,-),(1,-)]. Then apply E_20(cN), followed on
the tau-minus sector by c[[1,-1],[1,1]] on banks0,1. The latter has the
chronological word E_01(-iN), E_10(dN), E_01(-N), followed by phase i on
bank1's tau-minus sector. WORDS.json gives every primitive and inverse.

| Unit | Forward ADD/SCALE/MONO | Inverse ADD/SCALE/MONO |
|---|---|---|
| C | 8 / 8 / 5 | 8 / 8 / 5 |
| Q0 | 8 / 8 / 4 | 8 / 8 / 4 |
| O0 | 20 / 28 / 15 | 20 / 28 / 15 |
| O=H^-1 O0 | 22 / 32 / 16 | 22 / 30 / 16 |
| I0 | 14 / 20 / 13 | 14 / 20 / 13 |

These are local ordinary receipts, additional to the paid prefix normalization,
three native calls, target-prefix restoration, and the complete source/body/
precision/compiler/ownership/erasure/recursive invoice. The checker supplies
uniform triangle-prefix bounds with every restored-source term included.

## 6. Scope and next exact obligation

The checker verifies the literal source relations, all three-bank unit words
and inverses on every reduced-prefix/tail-one input column, omitted-ADD controls,
and the exact whole-column identity (11). The all-width proof is (1)-(11),
with two fixed prefix bits and tensoring the tail source identities.

The displayed E is NOT equal to O diag(a^4,a^2,a) I0 on the other two input
banks. RESULT.json retains an exact nonzero defect entry. Consequently (11)
is a positive endpoint-compatible column and a concrete starting point for
coupled completion, not a supplier. The next task is to change the other two
columns through actual ordinary unit completions while preserving (11), or
to change the endpoint complements and prove the entire identity anew.

Credit @CubeJerry, the retained source and primitive contract, the paid prefix
normalizer and balanced-plus construction, and substantial OpenAI assistance.
