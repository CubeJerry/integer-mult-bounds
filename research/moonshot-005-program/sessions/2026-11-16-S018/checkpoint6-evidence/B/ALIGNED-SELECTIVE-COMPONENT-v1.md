# Exact ordinary alignment of complementary rank-four channels

**Positive component identity with a universal obstruction to completing this prefix to independent421.** All monomials below are literal root-four tables, and every scalar multiplying a collective tensor operator is external. This is not a full three-native caller or a new exponent claim.

## Source and endpoint equations

Use the pinned four-bit source A, its square-coordinate R2, the active-square swap J=R2^-1 SWAP_ab R2, and the literal spectator swap S=SWAP_ab in original coordinates. Put

    F=Z_a, H=A^-2 F A²,
    Fhat=A F A^-1, Fback=A^-1 H A,
    K=A J A² S A^-3, B2=A³ S A.

F,H,Fhat,Fback,J,S,K are root-four monomials. The sign controls are involutions. The exact source equations are

    K|a,b,c,d> = (-1)^(ad)|a,b xor ad,c xor ad,d>,
    K²=I, [K,Fhat]=0, [J,F]=0, [S,H]=0,
    A J A³=K B2,
    B2 Fback=Fhat B2, A⁴ Fback=Fhat A⁴.

B2 is Gaussian rank2; A⁴ and A J A² S A=K A⁴ are Gaussian rank4. The independent checks establish exact Gaussian gauges, not merely support cardinalities.

Take tensor lifts to any positive width V, writing a=A^tensor V and retaining the uppercase symbols for the corresponding collective monomial controls. Define

    P=(I+F)/2, T=(I+H)/2,
    Phat=(I+Fhat)/2, Pback=(I+Fback)/2,
    R(P)=[[I-P,P,0],[P,I-P,0],[0,0,I]].

The ordinary units and endpoint controls are

    C=diag(I,J,I) R(P),
    Q=diag(I,S,I) R(T) diag(I,S^-1,I),
    O=R(Phat) diag(I,K^-1,I), R=R(Pback).

Their inverses are obtained by reversing the displayed factors. R(P), R(T), R(Phat), R(Pback), and Q are involutions. In particular C's first column is (I-P,J P,0)^T, while Q's middle row is (S T,I-T,0).

For E=L C U Q L, write the four-source term as

    T4 = -(a C00 a, a C10 a, 0)^T a [Q10 a,Q11 a,0].

Exact multiplication and the two intertwining equations give

    T4=[[0,-(I-Phat)a⁴,0],[-Phat K a⁴,0,0],[0,0,0]],
    O T4 R=[[0,-a⁴,0],[0,0,0],[0,0,0]].

Thus the rank-four part has the full field rank D=16^V and admits an explicit ordinary input/output alignment, including every physical component. This is stronger than a nonzero or partial-rank witness.

The two apparent lower quartic terms vanish exactly:

    (I-Phat) B2 Pback=0,
    Phat B2 (I-Pback)=0.

Consequently the **entire four-source prefix is pure rank4**. Its first-column two-source prefix is pure rank2 and its three-source prefix is pure rank3. The universal pure-prefix image/cut theorem therefore excludes independent421 for every ordinary-unit completion preserving this first C column and middle Q row. It applies regardless of the remaining entries. The finite failed completion searches are not the reason for this conclusion.

## Literal ordinary forward and inverse words

For a collective monomial involution F, the shear y<-y+epsilon (I+F)x/2 is implemented chronologically by

    SCALE(x,epsilon/2), ADD(x,y), MONO_F(x), ADD(x,y),
    MONO_F(x), SCALE(x,2 epsilon).

The source x is restored because F²=I. Three shears E01(P), E10(-P), E01(P), followed by MONO_F on bank1 and the external SCALE(-1) on bank1 implement R(P). Each controlled swap costs 6 ADD, 7 SCALE, and 7 MONO calls; it is its own inverse. This identity uses the collective involution and does not replace an exterior -1 by a per-column phase.

Appending the displayed J/S/K services gives:

| Service, in either direction | ADD | SCALE | MONO |
|---|---:|---:|---:|
| C | 6 | 7 | 8 |
| Q | 6 | 7 | 9 |
| Output decoder O | 6 | 7 | 8 |
| Input decoder R | 6 | 7 | 7 |

The exact maximum bank row-sum bound during each listed primitive word is at most5. A forward use of all four services costs 24 ADD, 28 SCALE, 32 MONO, and their inverse services have the same invoice. There is no extra field owner. J is one coordinate swap and two Toffoli operations; S is one coordinate swap; K is two Toffoli operations plus one sign pass. Other tables may use the admitted fixed four-bit monomial compiler (at most105 three-control edges,630 negative-control X operations,one phase pass per service). Every service acts on and is paid for the full field volume, at least16^V. Precision, sources, native calls, ordinary passes, ownership and supplier obligations remain charged.

The exact eight primitive words and all one-column destination/phase tables are in root's reviewed `R/pure-prefix-review/ORDINARY-WORDS.json`. This package independently reconstructs A,J,H,Fhat,Fback,K and checks those words, their inverses, 48 omitted-ADD negative controls, prefix bounds, and the symbolic involution shear at both formal F eigensectors. The proof above tensors the multiplicative identities and then applies collective projector algebra, so width parity is retained correctly.

## Scope and pins

`PURE-PREFIX-IMAGE-GATE-v2.md` is the universal obstruction dependency; `INVERSE-CUT-SUPPORT-GATE-v2.md` is its cut dependency. The selective rank2/rank4 gauges for all six spectator GL2(F2) pullbacks are independently available in `SELECTIVE-RANK4-CONTROLS-RESULT.json`. The checker records the exact source/control file hashes and does not infer all-width claims from width-one numerical ranks. The component identity holds at every width; the no-completion theorem has the fixed-finite-template and sufficiently-large-faithful-width quantifier.

Credit: retained source and tensor-word frameworks, @CubeJerry, root's ordinary primitive compiler/review, and OpenAI-assisted Worker B derivation and independent replay. All unreviewed new assertions remain provisional.
