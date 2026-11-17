# A paid ordinary compiler for removing one fixed source column

**Positive local compiler and exact native interface. No complete three-bank
endpoint, supplier, or new kappa. The distinguished-prefix representation is
explicitly larger than the old pure collective catalogue.**

## 1. The local source and the ordinary target

Use the pinned four-bit source A=C_b R, where

    C_b=((1+i)I+(1-i)X_b)/2,
    R:(a,b,c,d) -> (b,c,d,a), phase (-1)^(abd).

At tensor width V>=1 write p=A tensor I^(tensor(V-1)) and
b=I_16 tensor A^(tensor(V-1)). Then a=p b=b p. This note implements p and
p^-1 using only the declared ADD, nonzero dyadic-Gaussian SCALE, and root-four
MONO primitives, with one arbitrary borrowed bank restored exactly. No native
or Gaussian call is used to apply p.

The ordinary monomials inspect only bit b in the first four-bit column,
except R, which applies the displayed fixed permutation and phase to that
first column. Their address rules are fixed independently of V. A field-wide
pass is charged even though the monomial only changes a fixed prefix.

## 2. A within-bank elementary update from four cross-bank shears

Let u!=v be bits in {0,1}, E_uv=|u><v| on the distinguished b bit, and
P_v=|v><v|. The other three bits of the column, and all remaining columns,
carry identities. For any nonzero coefficient lambda, put

    P=lambda E_uv, Q=P_v.

Then PQ=lambda E_uv and QP=0. If E_ij(c) adds c times bank j into bank i,
the exact commutator identity is

    E_01(P) E_10(Q) E_01(-P) E_10(-Q)
       =diag(I+lambda E_uv,I).                         (1)

The chronological order is the reverse of the product in (1). This acts
only on the target bank after the full word and restores the arbitrary
borrowed bank. In particular, it is not a zero-workspace construction.

Both coefficient operators have literal two-monomial expansions:

    P=lambda (X_b+(-1)^u Z_b X_b)/2,
    Q=(I+(-1)^v Z_b)/2.                               (2)

Compile each coefficient term by applying its monomial to the source bank,
scaling by the nonzero coefficient, ADDing into the target bank, then undoing
the scale and monomial. Every intermediate source restoration is included.
There are two uses of each of P,Q. Thus (1), in either direction, costs

    8 ADD +16 SCALE +12 MONO.                         (3)

Replacing lambda by -lambda gives the inverse within-bank update. All
coefficients below and their reciprocals are Gaussian dyadics.

## 3. Three elementary updates compile C_b

Write d=(1-i)/2 and D_b=diag(1,i) on the distinguished bit. Direct two-by-two
multiplication gives

    C_b=U_01(-1) U_10(d) U_01(-i) D_b,
    U_uv(lambda)=I+lambda E_uv.                       (4)

Consequently the chronological source word is R, D_b, U_01(-i), U_10(d),
U_01(-1), with each U compiled by (1)-(2). Reverse that order, negate each
elementary coefficient, and invert D_b,R to implement p^-1. Both directions
have the complete local receipt

    24 ADD +48 SCALE +38 MONO.                        (5)

The checker records the largest exact Gaussian-l1 row sum over every primitive
prefix of both words. This is a uniform infinity-norm upper bound, including
temporary scales and the borrowed bank. Tensoring identities does not change
it. The resulting numerical bound and all literal words are retained in
RESULT.json and WORDS.json. This finite prefix bound is not a full caller
precision theorem.

## 4. The same two paid prefix controls normalize both native types

For either three-bank native L or U, define

    D_left=diag(p^-1,I,I), D_right=diag(I,p^-1,I).

Their exact two-active-bank identities are

    D_left [[a,0],[I,a]] D_right = [[b,0],[I,b]],
    D_left [[a,-a^2],[0,a]] D_right = [[b,-b^2],[0,b]]. (6)

The third bank remains an identity channel. Equation (6) follows from a=p b,
[p,b]=0; the off-diagonal a^2 loses one p from each side. Each of the two
controls in (6) is a complete instance of (5), with the third arbitrary bank
borrowed and restored. Therefore a normalized native instance requires the
local additional receipt

    48 ADD +96 SCALE +76 MONO.

For the three-native word L C U Q L, six copies of p^-1 suffice:

    144 ADD +288 SCALE +228 MONO,                     (7)

in addition to the original three native calls and every other interface.
Adjacent controls may be absorbed into the actual ordinary interfaces, but
(7) does not claim a saving from such absorption. The target heads can be
renormalized similarly; those endpoint copies must also be charged if used.

## 5. Scope and remaining work

This supplies an actual fixed-prefix implementation underlying the exploratory
model a=I_prefix tensor a_tail. It does not assume a nonmonomial prefix matrix
is a free one-bank operation, and does not consume the arbitrary third input.
Its literal primitive proof uses the declared local ordinary contract only.
The complete physical compiler, precision, source layout, ownership, erasure,
recursive invoice and strict supplier remain separate obligations.

The tail Gaussian rank of a normalized rank-r head is r(V-1), not rV.
Reattaching its actual p^r endpoint controls restores the exact original head;
one must retain those controls and their cost before using the old target
invoice. This note does not silently treat a missing prefix Gaussian layer
as a complete rV head.

The useful next question is an actual independent (4,2,1) endpoint identity
in this now explicitly compiled prefix model. Balanced plus-sector capacity
alone and finite-catalogue endpoint searches do not supply that identity.

Credit @CubeJerry, the retained four-bit source and primitive contract, the
distinguished-column same-plus construction, and substantial OpenAI assistance.
