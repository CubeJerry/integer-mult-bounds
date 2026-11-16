# Ordinary row ranges exclude the active-swap kernel; a spectator swap supplies two genuine kernel channels

**A universal scoped obstruction and an exact constructive source bridge. Independent review pending. No complete421 caller and no new κ.**

The component-augmentation gate already excludes the middle-oriented active-swap prefix. Here an ordinary range of dimension3D/4 excludes its opposite orientation as well. A literal spectator swap then avoids this obstruction and supplies both ordinary kernel interfaces, with a full-rank aligned quartic component. All ranks below are exact; the spectator-swap projector is not half-dimensional.

## 1. An ordinary row-range gate

Use the literal source a=A^tensor V on D=16^V coordinates and the retained native word E=L C U Q L, with C,Q arbitrary ordinary units in the fixed finite root-four tensor interface. Write s=C00,t=C10 and

    K=(a s a,a t a,0)^T.

Only the term `-K a [q10 a,q11 a,0]` in E can contain Gaussian rank4. Every other term has at most three source factors and one-column support at most8. At all sufficiently large faithful widths, exact Gaussian class extraction commutes with ordinary left multiplication.

Consequently, if an ordinary idempotent R fixes K and has rank strictly less thanD, then E cannot have an independent rank-D Gaussian4 endpoint. Indeed R fixes the full rank4 component E4, so `rank(E4)<=rank(R)<D`. This gate does not require K to be injective, pure rank2, or to have no ordinary kernel. The input/output endpoint interfaces remain arbitrary ordinary units, with their actual inverses included in the complete finite catalogue.

The idempotent here is a mathematical range certificate. The gate does not claim an uncharged physical implementation of an irreversible projector.

## 2. The active-swap family has only3D/4 of ordinary row capacity

Let

    F=Z_a, P=(I+F)/2, M=I-P,
    J=R2^-1 SWAP_ab R2,
    T0=SWAP_ab Z_c, T=(I+T0^tensor V)/2.

F commutes with J. The one-column involutions F,T0 generate D8, with

    z=(F T0)^2=Z_a Z_b,
    z²=I,  z central,  F T0=(T0 F)z.                 (1)

All seven nonidentity elements of this literal group have trace0. Thus H=complex^16 is two copies of its regular representation. At every positive width V, the collective action has character D at the identity and0 elsewhere, hence is D/8 copies of the regular representation. This all-width trace statement follows by taking tensor powers of the eight exact traces, not by extrapolating a numerical rank.

Write Zplus=(I+z^tensor V)/2 and Zminus=I-Zplus. The orthogonal range projectors of P T and M T are

    Rplus =P (Zminus+Zplus T),
    Rminus=M (Zminus+Zplus T).                       (2)

On the Zplus sector, F and T0 commute, so the product of their projectors is the range projector. On the Zminus sector they anticommute; there `P T P=P/2` and `M T M=M/2`, so P T and M T fill the P and M ranges respectively. This proves(2), including exact equality of their images. Expanding the eight group coefficients in(2), the identity coefficient is3/8. Therefore

    rank(Rplus)=rank(Rminus)=3D/8.                   (3)

For this actual source, exact literal matrices give two further ordinary monomials:

    Hout=A T0 A^-1,
    HoutJ=A J T0 J A^-1.                            (4)

Also A F A^-1=Fhat=Z_d. Hence both A Rplus A^-1 and A J Rminus J A^-1 are ordinary projectors: expand(2) using the conjugated ordinary generators in(4).

For the opposite prefix s=P T,t=J M T, the ordinary block projector

    R=diag(a Rplus a^-1, a J Rminus J a^-1, 0)        (5)

fixes K. Its rank is3D/4 by(3). Exchanging P and M gives the same rank bound for the middle-oriented prefix. Section1 therefore excludes BOTH orientations for arbitrary C20, arbitrary completions of C, and arbitrary ordinary Q. This closes the active-swap SZ_c continuation even though its square-transported ordinary Ka kernel is real.

The negative result is specific to the proved forward ordinary conjugates and the exact row-range bound. The next construction avoids those conjugates.

## 3. A literal spectator swap with two ordinary kernel channels

Let S_ab,S_ad,S_cd denote coordinate swaps in the ORIGINAL one-column coordinates, and now put

    Ts=S_cd, T=(I+Ts^tensor V)/2, N=I-T.

The checker reconstructs the literal source and proves the exact identities

    A^-1 Ts A=S_ad,
    A^-2 Ts A²=S_ab,
    A J Ts A^-1=Kdec,
    A Ts A³=B2=A³ S_ab A,                           (6)

where Kdec is the already retained ordinary involution

    (a,b,c,d)->(a,b xor ad,c xor ad,d),
    phase=(-1)^(ad).

Ts commutes with F and J; Kdec commutes with Fhat. In contrast to(4), both A Ts A^-1 and A J Ts J A^-1 are nonmonomial exact Gaussian rank2 operators. Thus the preceding ordinary row-range proof cannot be applied to Ts.

Use the opposite first-column orientation

    C[:,0]=(P T,J M T,N)^T.                          (7)

An actual ordinary unit with this column is

    Cnew=diag(I,J,I) R01^-(F) R02^-(Ts),             (8)

where R_ij^-(G) has `(I+G)/2` on the two diagonal blocks and `(I-G)/2` on the off-diagonal blocks, and fixes the remaining bank. Each controlled route is an involution with an explicit primitive implementation. Multiplying(8) on the right by SWAP12 changes only the remaining two columns and meets the necessary scalar completion condition from the component-augmentation gate.

Let

    Kold=(a P a,a J M a,0)^T,
    K=(a P T a,a J M T a,0)^T.

Kold is an isometry and K=Kold a^-1 T a. A coordinate swap on four bits has trace8, so at every positive width

    rank(T)=rank(K)=(D+8^V)/2.                       (9)

This is strictly between D/2 andD. No half-rank approximation is used in the proof or invoice.

There is an actual ordinary output alignment. Put

    Drow=diag(I,Kdec^-1,I),
    O=R01^-(Fhat), H=O Drow.

Then identities(6) give

    H K=(a T a,0,0)^T.                              (10)

For example the second active row becomes `a Ts M T a=a M T a`, while the first is `a P T a`; O then combines their complementary Fhat output sectors into one whole bank.

Define the ordinary projectors

    R1minus=(I-S_ad^tensor V)/2,
    R2minus=(I-S_ab^tensor V)/2,
    Rjplus=I-Rjminus.

Equation(6) turns(10) into

    H K=(a² R1plus,0,0)^T,
    H K a=(a³ R2plus,0,0)^T.                        (11)

Thus for every operator column X, not only ordinary ones,

    K X=0  iff  X=R1minus X,
    K a X=0  iff X=R2minus X.                        (12)

Both kernel projectors are genuine ordinary coordinate-swap controls. Their exact ranks are `(D-8^V)/2`; they are nonzero at every positive width. Unlike the earlier JZa construction, neither kernel is merely a physical subspace inaccessible to ordinary operators.

The source columns K and Ka remain pure Gaussian rank2 and3. The verifier supplies full Gaussian monomial gauges for each literal word in the finite P/M,T combinations; it does not infer purity from support size alone.

## 4. The quartic component is full and ordinarily aligned

Apply H to the possible four-source column -K a². By(6) and(10), its only nonzero bank is

    -a T a³=-(a⁴+B2)/2.                             (13)

Here a⁴ is exact Gaussian rank4 and B2 exact Gaussian rank2, each unitary. Therefore the two class components of(13) each have rankD and occupy a whole ordinary input/output bank. Their sum has rank `(D+8^V)/2` by(9). This is a useful exact warning: class projection can increase rank, so the rank of K itself does not exclude the quartic endpoint.

The same source control is excluded by none of the following existing gates: the repeated-plus character multiplicity gate, the physical-injective ordinary-range gate, the ordinary-column injectivity argument, the middle-sector component-character gate, or the active-swap ordinary row-range certificate above. This statement only means that their hypotheses fail or that their necessary conditions are met; it is not evidence that the complete caller equations are solvable.

A first actual second-interface candidate is the controlled bank1/bank2 swap on R2minus:

    Qkernel=[[I,0,0],[0,R2plus,R2minus],[0,R2minus,R2plus]].  (14)

It is an ordinary involution with q12=R2minus nonzero, and so uses the legal channel required by the last-column rank3 equation. Equations(7)-(14) are a constructive bridge, not a full421 identity. In particular neither(8) nor its column-swapped version with(14) is asserted to have independent endpoints.

## 5. Cost, controls and the next equation

The verifier provides actual primitive words and inverses for Cnew, its column-swapped completion, Drow, O and Qkernel. All use the same three arbitrary banks, add no owner, and preserve arbitrary contents. New monomials Ts,S_ad,S_ab are coordinate swaps. J,Kdec and F/Fhat retain their pinned coordinate, Toffoli and phase recipes. Each MONO remains a charged full-field pass; the source construction and field volume have not been reduced.

Exact invoices, prefix bounds, omitted-ADD negative controls, Gaussian gauges, eight D8 traces, and source-conjugation tables accompany the proof. The row-range theorem is proved by(1)-(5); the finite matrix calculations verify the literal source hypotheses. The constructive all-width identities follow by tensoring literal equalities and forming the projectors after tensor lifting.

The optimistic three-native invoice remains `3[1]+6[7]+3[8]` against `[25]+[23]+[22]`, before all retained caller, owner, source, precision, compiler and recursive costs. No supplier admission or exponent improvement is claimed.

The next concrete obligation is to exploit BOTH ordinary kernels in(12): choose q12 through R2minus, allow q02 through R1minus when needed, and complete C,Q so the full rank2 residue in(13) moves to an independent output while an independent Gaussian1 job survives. The complete circuit, its endpoint interfaces and their actual inverse recipes must all be established before this bridge can supply a complex saving.

Credit @CubeJerry, the retained literal four-bit source and S018 coset/inverse-cut work, S019 complex construction and root review, and substantial OpenAI assistance. All five foundational assumptions remain.
