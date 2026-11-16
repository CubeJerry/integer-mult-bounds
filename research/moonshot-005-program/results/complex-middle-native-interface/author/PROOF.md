# A middle-native interface for the four-bit three-call target

**Proved necessary conditions and an exact reconstruction criterion in the fixed
monomial tensor interface. No profitable caller or new kappa.**

Baseline: `3057acc9311101cfedfcfacf7f68fb0866507871`. This continues the actual
four-bit cubic source and the concentration construction, rather than treating
bounded caller searches as impossibility proofs.

## 1. Source, quantifiers, and the remaining construction

Let `A=C_b D_acd P` be the literal source of
`results/complex-four-bit-cubic-source/author/PROOF.md`, and let
`a=A^(tensor V)` on a bank of dimension `D=16^V`, for positive integer `V`.
The admitted source has pure Gaussian ranks 1, 2, and 4 for `a,a^2,a^4`,
and pure rank 1 for `a^-1`, with its actual phases. On three independent banks put

    L = [[a,0,0], [I,a,0], [0,0,I]],
    U = [[a,-a^2,0], [0,a,0], [0,0,I]].                 (1)

Let `O_V` be the tensor span of the full finite group of root-four-phase
monomial maps on the 16 one-column addresses. Every caller uses a fixed finite
template before `V` grows; its actual ordinary implementation and inverse are
still owed. Arbitrary invertible matrices in `M_3(O_V)` are permitted below.
They may mix all three banks. The finite tensor separation argument used by
the retained two-native proof gives ordinary-bimodule projections `pi_r` onto
the pure Gaussian-rank-r word classes, at all sufficiently large faithful
widths, retaining every scalar tensor phase. Non-Gaussian components are kept
separately, not assigned a Gaussian rank from support alone.

The current construction problem is an independent `(4,2,1)` endpoint `E`,
including its actual ordinary outer encodings, with

    E = L C U Q L,       C,Q invertible ordinary.       (2)

The last-interstage-only result already excludes `C=I` even with arbitrary
ordinary outer encodings. This note gives a different interface: peel the two
outer natives and inspect the desired endpoint itself,

    B = L^-1 E L^-1.                                  (3)

Finding `C,Q` is equivalent to realizing `B=C U Q`. The necessary tests below
do not fix output rows and do not sample a bounded ordinary basis.

## 2. Native flattening and relative nilpotency

**Theorem.** If `B=C U Q` with invertible ordinary `C,Q`, then:

1. Every component of `B` outside ranks 0, 1, and 2 vanishes.
2. With `B_r=pi_r(B)`, the three ranks are
   `rank B_0=D`, `rank B_1=2D`, `rank B_2=D`.
3. The flattened matrix `F=B_0+B_1` is invertible.
4. The actual matrices

       P=F^-1 B_0,       T=F^-1 B_2

   satisfy

       P^2=P, rank P=D, P is ordinary,
       T^2=0, rank T=D, PT=TP=0.                      (4)

   In particular the rank-two component must become a square-zero map after
   division by `F`; a component-rank census alone is insufficient.

**Proof.** Write `E_ij` for bank matrix units and put

    D_a=diag(a,a,I),       P_0=E_22,       T_0=-a E_01.

The rank components of `U` are `E_22`, `diag(a,a,0)`, and `-a^2 E_01`.
Projection commutes with ordinary multiplication on both sides. Therefore

    F=C D_a Q,
    F^-1 B_0=Q^-1 P_0 Q,
    F^-1 B_2=Q^-1 T_0 Q.                               (5)

All ranks, invertibility, ordinary membership, and identities in (4) follow.
Ordinary inverses belong to the finite-dimensional ordinary algebra; this
algebraic assertion does not supply a free physical inverse implementation.
The argument works for every sufficiently large width where the fixed word
catalogue is faithful. It is not an inference from a width-one matrix test.

The dual left-divided identities also hold, using `B_0 F^-1` and `B_2 F^-1`.
They provide the same conjugacy obstruction and need not be counted as an
independent theorem.

## 3. What is sufficient, and what is not

The necessary tests are not asserted sufficient. An exact constructive
criterion reduces the two missing ordinary matrices to one.

Suppose the conditions defining `B_r,F` hold. There is a factorization
`B=C U Q` by invertible ordinary `C,Q` **if and only if** there is an
invertible ordinary `Q` satisfying

    F^-1 B_0=Q^-1 P_0 Q,
    F^-1 B_2=Q^-1 T_0 Q,
    C := F Q^-1 D_a^-1 is ordinary.                   (6)

Then the displayed formula constructs the required invertible `C`.
Indeed `B=F(I+F^-1 B_2)`, while
`C U Q=C D_a(I+T_0)Q=F(I+F^-1 B_2)`.
Conversely every source factorization gives (6) by (5).

The first equation in (6) is formally implied by the last ordinary-membership
condition and the reconstructed factorization, but retaining it as an
independently checkable filter is useful. Actual finite ordinary recipes,
inverse recipes and their costs remain separate requirements.

This criterion is useful for constructing an endpoint with mixed Gaussian
rows. It does not replace the unproved ordinary conjugacy by a component-rank
count or a modular unit at one width.

## 4. Two natural endpoints are excluded even with both interstages free

### 4.1 Keeping the literal concentrated pair

Let `g` be any fixed pure nonordinary Gaussian head of positive rank, with
its actual monomial gauges. Consider the endpoint

    E_g=[[0,-a^4,0], [a^2,0,0], [0,0,g]].              (7)

The inverse is `L^-1=[[a^-1,0,0],[-a^-2,a^-1,0],[0,0,I]]`.
Direct multiplication, valid in every associative coefficient algebra, gives

    L^-1 E_g L^-1=[[a,-a^2,0],[0,a,0],[0,0,g]].         (8)

Its ordinary component is zero. Theorem 2 requires ordinary-component rank
`D` for `C U Q`. Thus **no** invertible ordinary `C,Q` can realize (7).
This rules out merely retaining the exact concentrated `(4,2)` pair and
adding any independent nonordinary job on the previously idle role by
changing the two internal interstages. A successful three-call caller must
change its outer endpoint encodings as well.

This is a scoped statement about (7), not a general `(4,2,1)` impossibility.
Taking `g=I` is a sharp control: (8) becomes exactly `U`, and `C=Q=I`
recovers the admitted `LUL` endpoint.

### 4.2 The literal diagonal powers

For the different fixed boundary `E_d=diag(a^4,a^2,a)`, peeling gives

    B_d=[[a^2,0,0],[-a-a^-1,I,0],[0,0,a]].              (9)

The rank-zero-plus-rank-one part has a zero first block row. It is singular,
contradicting the flattening condition. Hence no invertible ordinary `C,Q`
realize this literal diagonal boundary either. This is not equivalent to
4.1 by simply absorbing arbitrary outer gauges: outer gauges cannot in
general move through the outer natives as ordinary operations.

## 5. A counterexample to rank-only admission

The all-width invertible matrix

    B_* = D_a + (1/2) a^2 E_00                         (10)

has exactly the native component ranks `(D,2D,D)` and invertible `F=D_a`.
It is invertible because its first diagonal block is
`a(I+a/2)` and `a` is unitary; the Neumann series proves `I+a/2` invertible.
Nevertheless `F^-1 pi_2(B_*)=(a/2)E_00` has square
`(a^2/4)E_00`, which is nonzero. It cannot equal `C U Q` for any ordinary
invertible `C,Q`. Thus even an exact all-width unit and correct component
ranks do not establish native factorization.

## 6. Cost and next construction

The existing optimistic three-native common-body `(4,2,1)` invoice stays

    Price=3[1]+6[7]+3[8],
    Target=[25]+[23]+[22],       [r]=r^(199/200),

with gross margin `0.56059024897207293124...` from the pinned source package.
The three idle body services remain paid. Every actual `C,Q`, outer gauge,
inverse-head wrapper, ordinary operation, storage/precision/tape expense and
recursive dependency must still be added. No cost is removed by peeling a
matrix algebraically.

The next constructive search varies actual ordinary endpoint encodings,
forms (3), and first enforces the exact word-type and conditions (4). A
surviving candidate must then solve (6) with real finite ordinary recipes.
The accompanying bounded searches are exploratory and are not proofs that
their unvisited or unsampled cases fail. Both strict suppliers, full recursion
and all five foundational assumptions remain open.

Credit: @CubeJerry; the retained four-bit source, concentration,
ordinary-coset and finite tensor-separation contributors; Worker B with
substantial OpenAI assistance. Independent review is separate from the
author's symbolic checks. **No new complete kappa.**
