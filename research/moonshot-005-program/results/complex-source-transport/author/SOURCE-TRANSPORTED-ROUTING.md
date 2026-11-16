# Source transport determines where the first routing can act

**Exact scoped obstruction and a constructive output decoder.** The obstruction
allows arbitrary ordinary outer encodings and an arbitrarily large fixed
diagonal second algebra. The decoder identifies a different placement of the
first clock that is not excluded by that argument. No profitable caller is
claimed.

## 1. Literal source and diagonal interface

Use the admitted four-bit source `A=C_b S`, `S=D_acd P`, and write
`a=A^(tensor V)`, `D=16^V`. The three natives are

    L=[[a,0,0],[I,a,0],[0,0,I]],
    U=[[a,-a^2,0],[0,a,0],[0,0,I]].

Let `D_V` denote the tensor span of **all** fixed one-column diagonal
root-four monomial tables. This is a finite fixed algebra before V grows.
It contains all joint quarter controls on all four source bits and all fixed
nonlinear sign/quarter-phase tables. Every operator in D_V is diagonal in
the physical address basis; actual implementation and inverse costs are not
silently waived. Let

    h_theta=(S^-1 D_b^theta)^(tensor V), theta in {0,1,2,3},
    R_b=sum_s P_(pi_s) tensor Pi_s(D_b^(tensor V)),

where each pi_s is any bank permutation of three banks. No phase sector is
fixed in advance, and all four sectors occur once V>=3.

We use the retained finite tensor separation principle at sufficiently large
faithful widths, including every actual root-four tensor phase. It separates
fixed one-column words that have different row-support sizes, even when a
word is non-Gaussian. The independent `(4,2,1)` requirement under arbitrary
ordinary outer encodings implies

    E has only pure Gaussian types1,2,4,
    rank(pi_1 E)=rank(pi_2 E)=rank(pi_4 E)=D.                  (1)

These necessary conditions do not fix the output rows.

## 2. A clock after the first conditional routing cannot work

**Theorem.** Let

    C=diag(I,h_theta,I) R_b,
    Q in M_3(D_V), with Q invertible.

Then `E=L C U Q L` cannot satisfy (1). This holds for every choice of the four
bank permutations, every clock exponent theta, arbitrary fixed coefficients
in the full diagonal algebra, and arbitrary invertible ordinary outer
encodings of the proposed independent Gaussian endpoint.

### Support facts used in the proof

For any one-column diagonal unit table d, each word `A^k d A`, k=1,2,3,
has exactly `2^(k+1)` nonzero entries in every row. Each of the first four
successive source flips acts on a different bit after rotation. Hence its
binary path choices have distinct destinations; inserting a nonzero diagonal
phase cannot cancel a path or change its support. The checker verifies the
finite support geometry, which proves the statement for every such table d.

In contrast,

    A (S^-1 D_b^theta) d A = C_b (D_b^theta d) C_b S          (2)

has at most two nonzero entries per row. Both C_b operators act within the
same b-pair and the middle table is diagonal. Any further right multiplication
by a diagonal table and A gives at most four entries per row. These bounds
include arbitrary nonlinear d; no Gaussian classification of (2) is assumed.

### The rank-four component forces the routing of its first column

All rank-four words must use the middle `-a^2 E_01` and an a from each outer
native. A word entering the clocked first-interstage row1 has at most eight
entries per one-column row by (2); a word entering row2 lacks the left a.
Thus pi_4(E) can have a nonzero block row only in output row0.

The entry `(R_b)_00` is a quarter-sector projector p. The exact transport
identity `a D_b^(tensor V)=D_a^(tensor V) a` moves p through the first a.
Consequently pi_4(E) factors on the left through p(D_a), so its rank is at
most rank(p). Condition (1) forces p=I. Each pi_s therefore fixes bank0,
and on banks1,2 it is either the identity or their swap. For a quarter-sector
projector f and g=I-f, the first interstage has the forced form

    C=[[I,0,0],[0,h_theta f,h_theta g],[0,g,f]].               (3)

This deduction uses full rank of the target, not a sampled routing catalogue.

### Forced zero pattern in the second interstage

Write q_ij for Q's diagonal entries. The first row of L C U is exactly
`(a^2,-a^3,0)`. Its products with Q L give

    E_01=a^2 q_01 a-a^3 q_11 a,
    E_02=a^2 q_02-a^3 q_12,
    E_00=a^2 q_00 a+a^2 q_01-a^3 q_10 a-a^3 q_11.

The eight-support words are forbidden by (1), and cannot cancel words of
support four or sixteen at faithful widths. Therefore

    q_01=q_12=0,             q_00 a=a q_11.                 (4)

Put B=`a h_theta f a`. The block E_11 now equals

    E_11=(B-a^2) q_11 a+a h_theta g q_21 a.                 (5)

Every word of `B q_11 a` has support at most four by (2), and every word of
the last term has support at most two. Every word of `a^2 q_11 a` has support
exactly eight. Its entire contribution is forbidden and cannot cancel the
other two terms. Thus `q_11=0`, and (4) gives `q_00=0`. We have forced

    Q=[[0,0,q_02],[q_10,0,0],[q_20,q_21,q_22]].             (6)

Invertibility of this square block matrix forces q_02,q_10,q_21 to be
invertible operators. This follows by a block permutation and triangular
factorization and does not need commutative determinant notation.

The ordinary component of E_20 is now exactly `f q_21`: its other terms are
`g a q_10 a` (four-support words) and `f q_20 a` (pure rank one).
Condition (1) excludes the ordinary component, so invertibility of q_21
forces f=0.

### The rank-two contradiction

With f=0, the relevant endpoint blocks are exactly

    E_00=-a^3 q_10 a,       E_02=a^2 q_02,
    E_20=a q_10 a,         E_22=0.

The first block has sixteen-support words and no rank-two component.
The second is an invertible pure rank-two component. Every word in E_20
has support four; the absence of non-Gaussian components in (1) forces this
whole invertible block to belong to the rank-two component as well.
Thus the rank-two component has an invertible `2D by 2D` block minor on
output banks0,2 and input banks2,0. Its rank is at least2D, contradicting
`rank(pi_2 E)=D`. This proves the theorem.

The statement is deliberately scoped. It does not exclude a dense coherent
first bank mixing, a first routing with a differently placed clock, or a
second interstage that permutes physical addresses. Giving the displayed
ordinary operations zero price would not remove this algebraic contradiction;
their actual costs certainly remain charged in any other construction.

## 3. An explicit decoder for a clock before the first routing

Consider instead the genuinely different order

    C=R_b diag(I,h_theta,I),

and suppose every pi_s sends bank0 into one of the two active banks0,1.
Let R_a be the same conditional bank permutation with its control transported
from D_b to D_a. This is an ordinary direct phase-table operation, with an
explicit inverse and its conditional scalar swap costs.

For Q in the joint Db,Dc quarter algebra, the exact rank-four component is

    pi_4(L C U Q L)
      = -R_a e_0 [a^3 q_10 a, a^3 q_11 a, 0].             (7)

The clock acts on first-interstage column1, while the rank-four path uses
column0, so it does not enter (7). The other paths contain at most three
heads. Transporting `a R_b e_0` through the two active rows uses the literal
identity `a Db=Da a`. The sixteen one-column words
`A^3 Db^u Dc^v A` are all pure rank four, including their exact phases; this
is checked exhaustively as a fixed source identity, not a width sample.

Consequently the known ordinary outer decoder `R_a^-1` concentrates the
entire rank-four component in output bank0. Its rank equals the rank of
`[q_10,q_11]`. In the sixteen joint quarter sectors this is full rank D
exactly when the pair `(q_10(s,t),q_11(s,t))` is nonzero in each occupied
sector. All sixteen sectors are occupied at V>=3. This gives a small exact
all-width condition for preserving the profitable rank-four job.

The two lower Gaussian components and their ordinary endpoint encodings
still have to be constructed. Equation (7) supplies a concrete decoder and
a correct transported control, rather than guessing the inverse R_b at the
output. The separate discovery script uses R_a^-1 explicitly and tests all
sixteen scalar unit blocks of Q. Finite failed samples remain only failed
samples.

## 4. Costs and scope

A four-sector conditional bank permutation has at most eight conditional
scalar swaps; its inverse has the same bound. The actual h_theta clock is
one separate fixed monomial service with its full retained tariff and inverse.
A joint-quarter Q can be applied directly by its sixteen scalar three-by-three
sector matrices. The conservative expanded bound per direction is96
unweighted ADD,240 SCALE and48 scalar SWAP passes, with zero conjugating
monomial adapters. All fixed-scalar precision, control, tape and ownership
charges remain. These are nonzero ordinary costs and do not replace the
three paid native calls or any common-body idle service.

The optimistic native-only `(4,2,1)` margin remains
`0.56059024897207293124...` at t=199/200. The obstruction above produces no
caller, and the transported decoder does not yet complete one. All five
foundations and both strict suppliers remain open. **No new complete kappa.**
Credit @CubeJerry and the retained source, finite tensor separation and
ordinary compiler contributors; Worker B with substantial OpenAI assistance.
Independent review is separate from the author checker.
