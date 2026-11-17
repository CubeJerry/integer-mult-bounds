# Crot has a source-coset obstruction beyond same-plus capacity

**Universal scoped exclusion of the Crot first interface, including a fixed
finite distinguished prefix. It does not exclude the Klein or C_T interfaces.**

## Hypotheses

Let a be the retained collective source, or its tensor tail with a fixed
finite matrix prefix. The one-, two-, and three-source powers a,a^2,a^3 have
Gaussian ranks1,2,3 on the unbounded tail. Ordinary coefficients have a fixed
finite tail-monomial catalogue; arbitrary matrix coefficients on the fixed
prefix are allowed. Faithful tail tensor separation applies to the finitely
many source cosets used below.

Let T be an ordinary idempotent, N=I-T, and require both
T1=a^-1 T a and T2=a^-2 T a^2 to be ordinary. Assume T is nonzero. Use

    Crot=[[T,0,-N],[0,I,0],[N,0,T]],
    L=[[a,0,0],[I,a,0],[0,0,I]],
    U=[[a,-a^2,0],[0,a,0],[0,0,I]].

There is no regular-trace, augmentation, half-rank, involution-sign or
collective-only hypothesis on T in this theorem. Both Crot and its inverse
are the usual projector rotation.

Suppose Q is an ordinary three-bank unit and

    L Crot U Q L=O diag(F4,F2,F1) Iin                (1)

has actual ordinary endpoint units and inverses. The contradiction below
uses the whole Gaussian-one encoder image, not a numerical class rank.

## 1. The third ordinary row of Q is forced to have one unit entry

Direct multiplication gives

    B=L Crot U
      =[[a T a,-a T a^2,-a N],
        [T a,N a^2,-N],
        [N a,-N a^2,T]].                            (2)

Write Q=(qij), with indices0,1,2. The last input column of L is e2.
The ordinary component of (B Q L)[:,2] in output rows1,2 is
(-N q22,T q22)^T. Its vanishing forces q22=0.

Let K0 be the ordinary part of a q00 a. In input column0, the ordinary
component of the two lower rows is

    (T K0-N q21, N K0+T q21)^T.                     (3)

The remaining terms have nonzero Gaussian rank on the tail. In particular,
a^2 g a cannot be ordinary for any ordinary monomial g: otherwise a^2 g
would equal an ordinary multiple of a^-1, whose one-column support is that
of a Gaussian-one word, whereas a^2 g has Gaussian rank two. Prefix matrices
do not change this tail-coset comparison.

The coefficient matrix [[T,-N],[N,T]] in (3) is a unit, with inverse
[[T,N],[-N,T]]. Hence K0=q21=0. The third block row of Q is consequently
(q20,0,0). Since Q has an ordinary inverse, q20 has an ordinary right inverse
and is a unit in the finite-dimensional ordinary coefficient algebra.
Equivalently, at each faithful physical width this square block is onto and
therefore invertible.

## 2. One particular Gaussian-one coset already encodes a free bank

Consider the Gaussian-one component of input column0, and its left ordinary
coset represented by a. Let

    H=projection_B(a q01 a^-1),

where projection_B takes the ordinary part of this finite source-word sum.
It is a proof operation, not an executable service. Bimodularity is valid
by the fixed-catalogue tail separation.

The complete coefficient column of the left coset B a is

    K=(0, -N q20+T H, T q20+N H)^T.                 (4)

To check that no term is omitted, the two lower rows in (2) give their
q20 a terms directly; the a q01 terms contribute through H. Every a g a
or a^2 g a term with a further final a is disjoint from B a: canceling
that final a would make a g or a^2 g ordinary. The terms a^2 q11 are
Gaussian-two words, so cannot belong to B a. In the top row, a T a=a^2 T1
and a T a^2=a^3 T2; the corresponding terms have the same disjointness or
a different pure source rank. The sole one-source top term would involve
q21, which is zero. These assertions concern distinct literal tail words,
so matrix coefficients on a fixed prefix do not invalidate them.

The ordinary row

    D=(0,-q20^-1 N,q20^-1 T)

satisfies D K=I. Thus K is a split free bank, not merely a physical subspace
of a favorable dimension.

Let c1 be the Gaussian-one encoder column of O. Expanding the actual
factorization (1) in left source cosets shows im(K) is contained in im(c1).
Both have dimension one entire physical bank. Therefore their images are
equal at every sufficiently large faithful width. This argument may also
be stated as equality of two isomorphic free modules in the finite
ordinary coefficient algebra.

## 3. The last Gaussian-one column is transverse to that entire image

Put p=q02 and z=q12. Since q22=0, the whole Gaussian-one part of the last
input column is

    E1[:,2]=(0,T a p,N a p)^T.                      (5)

A vector K x lying in the subspace {(0,T y,N z)} must be zero. Indeed,
projecting its second coordinate by N gives -N q20 x=0, while projecting
its third coordinate by T gives T q20 x=0. Adding gives q20 x=0, hence
x=0. Since (5) belongs to im(c1)=im(K), it vanishes. Thus a p=0 and p=0.

The Gaussian-three part of the last input column is now

    (-a T a^2 z,0,0)^T.

Its required vanishing gives T2 z=0. But Q's last block column is now
(0,z,0)^T; invertibility of Q requires z to be injective on a whole bank.
That is impossible because its range lies in ker(T2) and T2 is nonzero.
This proves the exclusion.

## Scope and consequence

The distinguished-column same-plus unit remains a correct positive
interface. It removes the earlier augmentation contradiction, but it does
not repair Crot: the source-coset frame (4) supplies a different obstruction
that persists in the matrix-prefix algebra. A successful use of the new
representation must change the first interface, for example to a genuinely
coupled Klein completion, or change the target profile/source conditions.
The theorem does not apply to C_T, whose third source column is (0,a,0),
or to the Klein interface, whose two active first-column entries differ.

The checker verifies the literal rank facts and the block identities, and
checks the coefficient-frame inverse and transversality identities on
explicit noncommuting literal controls. It does not replace the faithful-coset argument or infer a
universal statement from a catalogue search. No new kappa, supplier or
foundational discharge is claimed.

Credit @CubeJerry, the retained four-bit source/native contract, the earlier
Crot capacity proof, and substantial OpenAI assistance.
