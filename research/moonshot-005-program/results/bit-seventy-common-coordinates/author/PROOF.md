# Seventy common coordinates with all foreign transfers invertible

## Result and scope

On the pinned balanced native source, with b=5,760 field records per role,
there is one causal linear programme over GF(2^30) for which all 6,470
foreign transfer matrices B_ij are invertible and `P B_ij=P`, where P is
the same first-70-coordinate projection at every donor and receiver.
Consequently all 111 receivers obtain those 70 original coordinates as
Y_i+X_i on arbitrary independent full-b inputs. Every original X is
restored at Hub, arbitrary Y is preserved by the actual preload gauge,
and the paid chart word is unchanged.

This strengthens the retained **69-coordinate mixed theorem**. The
separate 76-coordinate partial cache theorem is unchanged; it does not
assert this same all-block invertibility conclusion. The remaining 5,690
coordinates are not synchronized here. No complete supplier or new kappa.

## Exact invertible source-lifting lemma

Let T_e have size q-by-b, T_l size q-by-c, and R size q-by-b over any
field. Let pi project F^q onto `F^q/im(T_l)`. There exist an invertible
b-by-b E and a c-by-b L with `T_e E+T_l L=R` if and only if

    im(pi T_e) = im(pi R).

Necessity follows by applying pi and using invertibility of E. For
sufficiency call the common image W. Both A=pi T_e and B=pi R map F^b
surjectively onto W. Choose a basis of W, lifts under each map, and bases
of their kernels. These form two bases of F^b. The automorphism E taking
B's lift/kernel basis to A's corresponding basis satisfies `A E=B`.
Each column of `R-T_e E` then belongs to im(T_l); choose preimages to
obtain L.

In particular, full row rank of both `[T_e T_l]` and `[T_l R]` suffices:
both quotient images are the entire quotient. This is weaker than
requiring T_l itself to be row-surjective. The accompanying finite
controls compare the exact image criterion with enumeration of every
invertible E and every L in small binary examples, including a positive
case with nonsurjective T_l and a negative unequal-image case.

## Transfers and actual flow certificates

For donor j let d_j be its native orthogonal degree and c_j the number
of genuine late line visits. The source gives b actual early X holders
and c_j=4,320 or 4,500 actual late additions. Regard their b+c_j values
as independent formal source inputs. Let S_ij be their b-row transfer
to receiver i through proper paths, excluding the nine canonical
descents. Nonneighbor transfers vanish by proper containment.

All remaining chart coefficients, including terminal maps at F_i, are
indeterminates. Define

    T_j = stack_(i adjacent to j) P S_ij = [T_e,j T_l,j],
    R_j = stack of d_j copies of P.

Two witness families hold for k=70:

1. For every foreign pair (j,i), the actual two-wave graph routes b
   independent symbols to all b outputs at i and k symbols to the
   specified leading k outputs at every other neighbor. All 6,470
   targets `b+(d_j-1)k` are attained.
2. For each donor choose one neighbor r_j. Its c_j real late taps alone
   route k independent symbols to each of the other d_j-1 neighbors.
   All 111 targets `(d_j-1)k` are attained. Receiver r_j is still present
   in the desired common-row equations.

The checker reconstructs actual H, D, K-perp and F incidences from the
integer root table. It separates early and late copies and allows only
same-chart early-to-late snapshots. It introduces no extra movement,
source visit, virtual native role or reverse-time edge. Every directed
capacity and every conservation equation is checked in all 6,581 flows.
The graphs have at most 1,484 vertices and 15,443 positive physical arcs
before temporary source/terminal capacities are zeroed.

The flow table's uncompressed SHA256 is
`5532c3477c0154115836fba49ba7df148a2bbeca85ed8820e1db796c0777dd4d`.

## Nonzero minors over the same field

A mixed flow for (j,i) gives a nonzero maximal minor of the matrix
stacking S_ij and `P S_lj` for every other neighbor l. In particular the
common-row matrix T_j has full row rank at a joint specialization.

For the all-but-one late flow, select its k(d_j-1) routed late input
columns and the first k columns of R_j. They form a square d_j k minor
of `[T_l,j R_j]`. At the path specialization, the chosen late columns
are zero at receiver r_j and give a permutation matrix on the other
selected outputs. The R_j block at r_j is I_k. Ordering r_j first gives
a block triangular matrix with diagonal blocks I_k and that permutation,
so the minor is nonzero.

Multiply all these nonzero minors and the two pure-wave baseline
determinants. Each factor has its own specialization; those individual
specializations need not preserve wave invertibility or coincide.
The product is nevertheless a nonzero polynomial. There are 6,470 mixed
minors of order at most 10,030, 111 augmented late minors of order at
most 4,340, and two baseline determinants of order 111b. As in the
retained causal theorem, proper paths have degree at most ten. Hence
the total degree is at most

    10*(6470*10030 + 111*4340 + 2*111*5760)
    = 666,545,600 < 2^30.

The finite-grid polynomial lemma gives one common downstream assignment
over GF(2^30), without increasing the retained extension degree.

## Joint source choice and full foreign block invertibility

Fix that assignment and solve, independently for each donor,

    T_j F_j = R_j,       F_j = vertical concatenation of E_j and L_j.

Both T_j and `[T_l,j R_j]` have full row rank. The lifting lemma supplies
one solution with E_j invertible, so det(E_j) is a nonzero polynomial
on the affine solution space.

For each distinguished receiver i, the corresponding mixed minor makes
the larger system `S_ij F_j=I_b` and `P S_lj F_j=P` for all other l
row-surjective, hence solvable. This solution belongs to the common
affine space. Thus each det(S_ij F_j) is separately a nonzero polynomial
on that space. Its individual witness need not have invertible E_j.

The product of det(E_j) and these d_j foreign block determinants has
degree at most `(d_j+1)b <= 362,880 < 2^30`. Parameterizing the affine
space over the same field and applying the finite-grid lemma again
gives one F_j where every factor is nonzero. Doing this for all donors
makes every E_j and every B_ij=S_ij F_j invertible while maintaining
`P B_ij=P` simultaneously.

## Actual word and arbitrary input correctness

Before X_j leaves its source line, retain the stationary raw values
needed for its late parities. Apply E_j to its actual early X holders
and add L_j's rows at their actual late source-line visits. The pure
early downstream map is invertible; its paid inverse at Hub restores
all original X labels before any original Y leaves ground. Form and
descend the nine real canonical rows. The pure late map is invertible
too; its inverse is applied at ground to the full arbitrary Y bank
after adding the selected canonical contribution.

At each corrected coordinate the proper transfer supplies precisely
the foreign sum. The canonical row supplies the same sum plus the native
diagonal, so characteristic two gives Y_i+X_i. The equations involve
all b input columns; unselected coordinates do not contaminate the
corrected ones. This is not a Y=0-only argument.

Fixed finite field maps compile by binary whole-record ADD elimination.
Tensoring that finite word with the body identity works at every positive
body width. As in the retained mixed result, a numerical global
coefficient assignment has not been materialized; finite exhaustive
selection followed by exact linear algebra specifies one.

## Whole-system invoice

The retained bounds apply unchanged. With w=30, put
`M=111*b*w=19,180,800` and `C=9*b*w=1,555,200`. There are M public X and
M public Y binary records.

| Whole-system quantity | Bound or exact count |
| --- | ---: |
| ADD | `17 M^2+50 M+111 C = 6,254,353,638,547,200` |
| INIT | `5 M+C = 97,459,200` |
| Dirty CLEAR | `5 M+C = 97,459,200` |
| Peak public plus auxiliary records | `7 M+C = 135,820,800` |
| Gap-one MOVE | 96,141,600 |
| Gap-two MOVE | 77,900,400 |
| Gap-four MOVE | 4,147,200 |
| Gap-eight canonical MOVE | 1,555,200 |

The actual movement is the balanced profile
`(4451/8)[1]+(7213/16)[2]+24[4]+9[8]`, normalized by the entire b-bank
and paid on all 30 binary extension copies. It must not be renormalized
by the 70 useful coordinates. The ordinary count is a finite
implementation bound, not a closed caller exponent budget.

## Method ceiling and open questions

Donor 80 has 62 neighbors and 4,320 true late taps. A mixed witness
needs b+61k independent source inputs but only b+4,320 are available.
Thus these row-surjectivity witnesses require k<=70, since
`61*71=4,331>4,320`. This is a limitation of the witness method, not an
impossibility result for structured codes or full synchronization. The
exact quotient-image lemma remains valid when the transfer is deliberately
rank deficient.

The remaining 5,690 coordinates, a numerical global coefficient table,
tighter ordinary implementation, an admissible caller budget, both
complete suppliers and all five inherited foundations remain open.
Dependencies are in SOURCE-PINS.json. Credit @CubeJerry, the native
geometry and balanced-source authors, the retained mixed proof, and
S023 Worker A with substantial OpenAI assistance. No new kappa.
