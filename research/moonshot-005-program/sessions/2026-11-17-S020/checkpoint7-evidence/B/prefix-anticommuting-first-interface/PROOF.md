# A changed first interface with exact kernels and a cancelling three-bank column

**Positive ordinary interface and exact cancellation of the last column's
ordinary/cubic terms. Independent Gaussian endpoint units and a complete
supplier remain open. This changes the first interface of the preceding gate.**

## 1. Literal source and first interface

Use the paid fixed-prefix model a=I_prefix tensor A^(tensor W). On two fixed
prefix bits put T=Z_tau, R=X_tau and S=Z_sigma tensor SWAP_cd^(tensor W).
Retain S1=a^-1 S a, S2=a^-2 S a^2 and
J=I_prefix tensor (R2^-1 SWAP_ab R2)^(tensor W). All are ordinary monomials.
TR=-RT, while S,S1,S2 commute with T,R. S1 and S2 are the literal SWAP_ad
and SWAP_ab transports, with the sigma sign retained.

Write P=(I+T)/2, N=I-P, U=(I+R)/2, V=I-U, A_s=(I+S)/2 and B_s=I-A_s.
Then P V P=P/2 and V P V=V/2. Let Rot_ij(h) mean
[[Ph,-Nh],[Nh,Ph]] on banks i,j. Root's changed interface is

    C'=diag(I,J,I) Rot_02(T) Rot_12(R) Rot_01(S).      (1)

This is an actual ordinary unit. Its inverse reverses the factors and inverts
each rotation. Each rotation is a controlled bank swap followed by one monomial;
the complete receipt is12 ADD +12 SCALE +7 MONO in each direction. The matrix
product order in (1) is opposite the chronological order of its rotations.

## 2. Exact source kernels

Its relevant entries are

    c00=P A_s-N V B_s,       c10=J U B_s,
    c20=N A_s+P V B_s,       c21=-N B_s+P V A_s,
    c22=P U,                c02=-N U.                 (2)

The active first-column Gram operator is exactly

    c00* c00+c10* c10=A_s P+B_s U+(1/2)B_s V.        (3)

The three displayed ranges are orthogonal; the missing range is A_s N.
Thus the active kernel is exactly A_s N, of dimension D/4. The inverse on
the support is A_s P+B_s U+2B_s V, an ordinary dyadic coefficient operator.
The one- and two-step backward kernels are P_S1 N and P_S2 N.

For the native word L C' U_native Q L and Q[:,2]=(p,z,w), the cubic last-column
part is precisely minus the active first-column path times a z. It vanishes iff

    z=P_S2 N z.                                      (4)

The ordinary part is (0,c02 w,c22 w), which vanishes iff U w=0, equivalently

    w=V w.                                          (5)

The literal source words A J A and A J A^2 have Gaussian ranks2 and3; their
accompanying S terms have the same ranks. No rank-one return is hidden in the
cubic path. Necessity of separate class cancellation uses the retained fixed
finite prefix-matrix/tail catalogue and faithful tensor class separation at
large widths. Sufficiency in (4)-(5) is an exact operator identity.

## 3. The old third-bank selector is absent

The first two third-row coefficients have the explicit ordinary right inverse

    (c20,c21)(A_s N+2B_s V P,-B_s N+2A_s V P)^T=I.    (6)

Indeed (c20,c21)=(N,P V) Rot_01(S), and
N N+P V(2 V P)=N+2P V P=I. Therefore no nonzero row operator on output bank2
annihilates both third-row source coefficients. This removes the exact
ordinary-plus-linear selector used by the preceding pi gate. It does not
exclude every possible multirow selector or other endpoint obstruction.

## 4. A paid complete unit with a cancelling last column

Let H_tau=c(T+R), c=(1+i)/2. This fixed-prefix Hadamard is unitary and
H_tau U H_tau^-1=P. Its paid implementation is H_tau=D_tau C_tau D_tau:
24 ADD +48 SCALE +39 MONO in either direction, with an arbitrary borrowed
bank restored. The checker imports and expands the pinned prefix-normalizer
word; this nonmonomial prefix action is not free.

Use

    p=U N_S2, z=(R H_tau) U P_S2, w=V.               (7)

Their initial projections U N_S2,U P_S2,V are orthogonal and sum to I.
Hence this is an isometric whole-bank column. The image of z is in N P_S2;
w has image V. Thus (4)-(5) hold, with ranks D/4,D/4,D/2 at every tail width.

An actual ordinary completion is

    Q0=diag(H_tau^-1,R,H_tau^-1)
         Swap_12(P P_S2) Swap_02(P N_S2)
         diag(I,I,H_tau).                            (8)

The last column of (8) is (7). Its two controlled swaps use the literal
monomial involutions N-P S2 and N+P S2. A fixed prefix bit selects identity
or the specified signed tail monomial. These have finite expansions in the
prefix-matrix/tail catalogue and fixed uniform address rules.

Three paid H_tau words, two controlled swaps and R give

    Q0 and Q0^-1: 80 ADD +152 SCALE +120 MONO.         (9)

Every inverse is an actual reversed factor word. Each imported prefix word
restores its borrowed bank before the next factor. All banks remain arbitrary;
there is no Gaussian query, new owner, zero bank, or erased input.

## 5. Exact remaining obligation

The entire last column consists only of Gaussian-one and Gaussian-two terms;
all ordinary and cubic terms cancel exactly. This is not yet an independent
endpoint factorization. Actual whole-bank encoder containment, both endpoint
units, the quartic job on the other inputs, and the complete source/body/
ordinary/precision/compiler/ownership/erasure/recursive invoice are open.

This changes one proved obstruction's premise and supplies a concrete larger
ordinary-cancelling channel. It does not prove a profitable caller exists.
Further work must test the complete endpoint identity, not just these kernels.

Credit @CubeJerry, root's changed-C proposal, the retained source and rotation
compiler, the paid prefix normalizer, and substantial OpenAI assistance.
No new kappa or foundational discharge is claimed.
