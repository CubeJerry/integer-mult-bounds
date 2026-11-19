# A low-return target commuting with both native endpoint actions

**Algebraic construction pending separate review. No physical H/D/K word,
supplier, foundational discharge or new kappa.** This repairs the additional
two-sided Clifford compatibility condition without increasing the previous
target's return rank. Common inverse fibres and shared D/K demands remain open.

## 1. Exact statement

Let F be any field of characteristic two. Use the pinned 111 native roots,
foreign-contact matrix O and split 16-dimensional Clifford matrices gamma_i.
There is an explicit binary block matrix B on G^111, where

    G = F^60 tensor F^16 tensor F^4,    b=3840,
    Gamma_i = I_60 tensor gamma_i tensor I_4,

with the following properties:

1. Nonforeign blocks, including the diagonal, are zero; all 6,470 foreign
   blocks are invertible.
2. B_ij commutes with both Gamma_i and Gamma_j at every foreign pair.
3. rank(I+B)=9b+b/30=34688. Its repair rank relative to the retained
   canonical row code is also 128=b/30.
4. The block transport is irreducible: if W_i<=G and B_ij W_j<=W_i at
   every foreign pair, then all W_i=0 or all W_i=G.
5. There is no nonzero flat input system B_ij Z_j=Z_i and no nonzero flat
   output system P_i B_ij=P_j, allowing vertex-dependent rectangular maps.

Tensoring every block with I_t for a positive integer t preserves 1,2,3
with b=3840t and h=128t, and preserves 5. Replicated irreducibility is not
claimed. Every field and body copy remains a real paid record.

The all-field assertion follows from binary identities and one nonzero
binary determinant certificate. It is not extrapolated from size experiments.

## 2. Geometry and adapted spinor coordinates

Keep a=80 and d=10 from the preceding target. They are nonforeign, have
degrees 62 and 61, and beta(a,d)=1. Put A=gamma_a+I and C=gamma_d+I.
Then A^2=C^2=0 and AC+CA=I. The inherited explicit binary change of basis
identifies S=F^2 tensor F^8 with A=E_01 tensor I_8, C=E_10 tensor I_8.
Use those adapted coordinates, and put V=F^8 tensor F^4, of dimension 32.
Each of 60 banks is F^2 tensor V, of dimension 64.

The authenticated native graph is connected, K=I+O has rank 9, and its
restriction to columns outside N(a) union {d}, or outside {a} union N(d),
still has rank 9. These are the previous target's separation facts.

For j foreign to a, commutation with A gives
gamma_j=[[P_j,Q_j],[0,P_j]]. Consequently E_01 tensor T commutes with
gamma_j exactly when T commutes with P_j. For i foreign to d, the form
is [[P_i,0],[R_i,P_i]], with the corresponding E_10 condition. Adjoining
F^4 replaces each P by P tensor I_4. No new native root or owner is used.

## 3. Three matrices and a complete finite algebra certificate

Represent a binary 8-by-8 matrix by eight row bitmasks, column 0 being the
least significant bit. Define

    T8=(167,116,215,112,229,79,125,156),
    W8=(219,191,130,199,25,119,93,183),
    U8=(4,72,17,35,4,88,85,171).

Exact multiplication gives [T8,P_107]=[W8,P_109]=[U8,P_110]=0.
Let J4 have ones at (0,1),(1,2),(2,3), and E4 its sole one at (3,0). Set

    T=T8 tensor I4 + I8 tensor J4,
    W=W8 tensor I4 + I8 tensor E4,
    U=U8 tensor I4.

They satisfy the same respective commutators on V. WITNESS.json lists
1,024 words in T,W,U, including the empty word and words of length at most
10. Literal binary multiplication and elimination show their 1,024 flattened
1,024-bit rows have rank 1,024. Thus they form a basis of M_32(F2), and
remain a basis over every characteristic-two F: their binary determinant
maps to 1. The bounded search that found the three matrices has no proof role.

## 4. The complete native block assignment

For l=1,...,59 let F_l send bank l identically to bank 0 and vanish elsewhere;
let R_l=F_l^T. Each squares to zero and commutes with every Gamma_i.

Assign F_1,...,F_59 to the first 59 increasing donors of receiver 80. The
remaining donors 106,107,109 receive the following operators inside bank 0:

    E_01 tensor I32,   E_01 tensor T,   E_01 tensor W.       (R)

Assign R_1,...,R_59 to the first 59 increasing receivers foreign to donor 10.
The remaining receivers 109,110 receive, inside bank 0:

    E_10 tensor I32,   E_10 tensor U.                       (C)

Call these 123 operators N_ij. Put B_ij=I+N_ij there, I at every other foreign
block and zero on nonforeign blocks. The stars are disjoint, and each
altered edge has an identity reverse orientation.

Every N_ij is square-zero; T,W,U themselves need not be nilpotent.
Thus (I+N_ij)^-1=I+N_ij. Transfers commute with all endpoint actions.
The internal row generators commute with Gamma80 by their E01 form and
with their actual donor actions by section 3 (the first is Gamma80+I).
The internal column generators satisfy the analogous statements. This
establishes both covariance identities on all 6,470 foreign blocks.

## 5. Full algebra and the flat exclusions

The first generators in (R),(C) give E01 tensor I32 and E10 tensor I32 in
bank 0, and their products give E00 tensor I32 and E11 tensor I32. Combining
these with the other internal generators produces all two-by-two matrix
units tensored with T,W,U. Section 3 therefore yields every 64-by-64 matrix
unit in bank 0. Reverse and forward bank transfers move these units to
every ordered bank pair, proving generation of M_3840(F).

For invariant W_i, invertibility in both orientations gives equal dimensions
on every native edge. Its identity orientation then gives W_i=W_j.
Connectivity and the full matrix algebra imply the asserted irreducibility.

Flat input maps Z_i also coincide along identity edges. The 59 row transfers
force their common image into bank 0; E01 tensor I32 and E10 tensor I32
have zero common kernel there. Hence Z=0. Flat output maps P_i likewise
coincide. Reverse transfers fill banks 1,...,59 and the two internal
operators' images fill bank 0, so P=0. These kernel/image arguments survive
arbitrary identity-body replication without claiming replicated irreducibility.

## 6. Exact return and the unchanged movement screen

Put Delta=B-O tensor I. The row star has image exactly bank 0 at receiver 80,
rank 64, since a forward transfer is onto that bank. The column star depends
on exactly bank 0 at donor 10, rank 64, since a reverse transfer is injective
there. Their native input supports and output supports are disjoint. Thus
rank Delta=128.

The two native rank-9 restrictions in section 2 give zero intersections of
row Delta and col Delta with the corresponding spaces of K tensor I.
The inherited rank-additivity lemma then gives

    rank(I+B)=9*3840+128=34688,
    rank([K tensor I;I+B])-9*3840=128.

This is the actual algebraic fitting rank, not proper-map rank. The source
bank identifies with End(F^16)^15 while retaining the same left spinor
factor: its right multiplicity dimension is 60*4=240=16*15. It is eight
copies of the literal bank-480 atlas.

The normalized movement profile remains

    Q=(4451/8)[1]+(7213/16)[2]+24[4]+(9+1/30)[8],
    [r]=r^(199/200).

The pinned exact predecessor certificate gives positive limiting room
0.01419847341495436895537249536059...; even m=870 first passes and 868 fails.
These are movement comparisons only. Source selection, actual H/D/K maps,
phase inverses, snapshots, ordinary and storage charges, both strict
suppliers and the recursive caller remain separate. No physical word is
claimed merely because the algebraic endpoint has the desired profile.

## 7. Verification, scope and next questions

The portable author checker reconstructs the actual graph/Clifford data,
all five internal endpoint commutators, square-zero identities, the 1,024-word
algebra basis, native support restrictions and inherited exact intervals.
It explicitly reuses and pins the preceding author's geometry code;
separate mathematical/code review must check the critical steps afresh.

Negative controls: replace T by a matrix unit failing the donor commutator;
omit both E10 internal generators, leaving the first spinor half invariant;
and use a diagonal unit, which makes I+N singular. These detect covariance,
irreducibility and invertibility failures separately.

Open next questions: choose actual compatible source inverse fibres for B;
realize shared D packets and the coupled K quotient/phase requirements;
then verify the complete physical return and ordinary invoice. Two-sided
endpoint commutation supplies none of those missing implications.

Credit @CubeJerry; retained native, Clifford, target, return-bank and budget
authors; S028 Worker C's dual-interface diagnosis; and the S028 orchestrator's
five-generator construction and exact certificate, with substantial OpenAI
assistance. All five foundations remain. No new complete kappa.
