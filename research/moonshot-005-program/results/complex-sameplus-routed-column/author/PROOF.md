# A changed same-plus source with a fully retained two-class endpoint column

**Positive ordinary units and an exact whole input-column identity. The two
other input columns and a complete independent (4,2,1) endpoint remain open.**

## 1. Paid prefix model and a literal source transport

Use the retained paid fixed-prefix normalization, so
a=I_prefix tensor A^(tensor W), with A=C_b R on sixteen letters. Here

    R:(a,b,c,d)->(b,c,d,a), phase (-1)^(abd),
    C_b=((1+i)I+(1-i)X_b)/2.

Only one distinguished prefix bit sigma is active below; every unused fixed
prefix bit is an identity. No prefix normalization or original-width target
restoration is free. Let

    S=Z_sigma tensor SWAP_cd^(tensor W),
    S1=a^-1 S a=Z_sigma tensor SWAP_ad^(tensor W),
    S2=a^-2 S a^2=Z_sigma tensor SWAP_ab^(tensor W),
    X=X_sigma tensor I,  R0=I_prefix tensor R^(tensor W).

The two S-transports are inherited. The additional literal transport is

    S a R0 = a R0 S2.                               (1)

For one column R^2 maps (a,b,c,d) to (c,d,a,b) with phase
(-1)^(ab(c+d)). That phase is invariant under SWAP_ab, while the output swap
is SWAP_cd. C_b commutes with SWAP_cd. Hence SWAP_cd A R=A R SWAP_ab,
which tensors to (1). The sigma factor commutes with a and R0.

Write P=(I+S)/2, N=I-P, P2=(I+S2)/2, N2=I-P2. The fixed prefix flip X
anticommutes with S and S2 at every W. Its collective replacement is not used.

## 2. A new first interface and actual input-column completion

Let Eij(c) add c times bank j into bank i. Set

    C=E10(I) Rot02(S)
     =[[P,0,-N],[P,I,-N],[N,0,P]].                  (2)

This is a genuine ordinary three-bank unit. Its inverse reverses the rotation
and applies E10(-I). Define the complete last column

    p=R0 N2,   z=X P2,   w=0.                      (3)

Its two initial projections N2 and P2 are orthogonal and sum to I. An actual
ordinary unit with this column is

    Q0=diag(R0,X,I) Swap12(P2) Swap02(N2).            (4)

Every bank is arbitrary. Equation (4) moves the N2 part of the third input
to bank0 and its P2 part to bank1; the two diagonal monomials finish (3).
Its inverse reverses the literal factors. No blank bank or erased input is used.

The source transports give

    P a p=0,   P a^2 z=0,   N a p=a p,   N a^2 z=a^2 z.  (5)

The first equality uses (1); the second uses a^2 P2=P a^2 and the fixed
prefix sign flip. Both are all-width identities, not class projections.

## 3. Exact full-column endpoint identity

Keep the literal three-native source

    L=[[a,0,0],[I,a,0],[0,0,I]],
    U=[[a,-a^2,0],[0,a,0],[0,0,I]],  E=L C U Q0 L.

Put H=E10(-I). Direct multiplication, followed by (5), gives the ENTIRE column

    H L C U (p,z,0)^T = (0,a^2 z,a p-a^2 z)^T.      (6)

There is no omitted ordinary or cubic term. The rightmost L fixes this input
bank, so it does not alter (6). Both p and z are nonzero and together retain
the entire original bank; they are not two copies of a half-bank input.

Define the actual independent endpoint units

    O=E10(I) E21(-I),
    I0=diag(I,X,R0) Swap12(P2).                      (7)

They have their literal reversed inverses, and I0 e2=(0,z,p)^T. Thus

    E e2 = O diag(a^4,a^2,a) I0 e2.                 (8)

This statement is an exact identity for one complete arbitrary input bank.
The quartic input component in this column is zero. It does not establish
the quartic job or the remaining two input columns of a full caller.

The source-class images here have ordinary whole-bank extensions without
the earlier fixed-column envelope contradiction: the quadratic encoder is
(0,I,-I)^T after H, the linear encoder is (0,0,I)^T, and their independent
quartic complement is (I,0,0)^T. These are actual unit columns in (7), not
merely images passing a numerical rank test.

## 4. Complete local primitive receipts

For an involution g, Swap_ij((I-g)/2) is H2^-1 diag(I,g) H2, where
H2=[[1,1],[1,-1]]. In chronological order H2 is ADD(i,j), SCALE(j,-2),
ADD(j,i); its inverse adds SCALE(i,1/2), SCALE(j,1/2). Each controlled swap
therefore costs four ADD, four SCALE and one MONO. Rot_ij(g) adds one MONO
on bank i; its inverse reverses those factors. Swap(P2) uses involution -S2.
A negative whole-bank shear costs one ADD plus two restored source SCALE(-1)
passes. Identity monomials are not charged.

| Actual unit | Forward ADD/SCALE/MONO | Inverse ADD/SCALE/MONO |
|---|---|---|
| C | 5/4/2 | 5/6/2 |
| Q0 | 8/8/4 | 8/8/4 |
| O | 2/2/0 | 2/2/0 |
| I0 | 4/4/3 | 4/4/3 |

The checker expands these words, replays every reduced-prefix/tail-one input
column, checks both inverse orders, and rejects every single-ADD omission.
It records a conservative all-width triangle-prefix bound for every word.
All prefix normalizers, source calls, original target-prefix restoration,
body costs, physical compiler, precision, ownership, erasure and recursive
work remain additional. These local receipts do not constitute a supplier
price or a new kappa.

## 5. Extension boundary and next task

The full matrices E and O diag(a^4,a^2,a) I0 differ on the other input columns;
the checker records a literal nonzero defect. The one-column identity is not
silently promoted to all columns. The finite search of a few simplest endpoint
complements has not supplied a full unit Q; that search failure is not a
universal obstruction.

After the ordinary gauge O^-1, the full middle source is exactly

    O^-1 L C U =
       [[a P a, -a P a^2, -a N],
        [P a,    N a^2,   -N],
        [a,      0,        S]].                     (9)

Any candidate complete endpoint must solve all three rows of (9), including
the quartic job. The established column fixes only the N/P split delivered
in (6). Ordinary unit changes on the unused complement are legitimate new
variables, but must be paid and checked on every input. Further source changes
also remain possible.

Reproduce with `python -B check.py --repo REPOSITORY_ROOT --out FRESH_OUTPUT`.
The source identities and actual words prove the all-width statement. Finite
exact replay and omission controls corroborate them. Credit @CubeJerry,
the retained source/prefix/controlled-swap constructions, S021 B, and
substantial OpenAI assistance. No new complete kappa or foundation discharge.
