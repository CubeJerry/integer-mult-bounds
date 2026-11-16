# A unit first-pivot obstruction for coherent routing

**Exact additional obstruction in a declared diagonal interface.** This note
extends the source-support argument to coherent scalar-sector matrices. It
also removes a redundant lower-shear parameter from the constructive search.
It does not exclude arbitrary first interfaces or non-diagonal second ones.

Let `R_b=R(Db^(tensor V))` be any invertible three-by-three matrix over the
quarter-control algebra. Write R_a for the same coefficients evaluated at Da.
Use the literal source, natives L,U and h_theta of
`SOURCE-TRANSPORTED-ROUTING.md`. All coefficient templates are fixed before V
grows, and every tensor phase is retained.

## 1. The exact normalization

Suppose the first column of R_b is `(s_b,t_b,0)^T` and s_b is a unit in the
quarter algebra: all four scalar values s(i^j) are nonzero. Set

    G_b=[[s_b,0,0],[t_b,s_b,0],[0,0,I]],
    R'_b=G_b^-1 R_b=[[I,b,c],[0,d,e],[0,f,g]].

All entries remain diagonal ordinary operators, and the lower two-by-two
block of R'_b is invertible. The exact source transport `a Db=Da a` gives

    G_a^-1 L G_b=L_w,
    L_w=[[a,0,0],[w,a,0],[0,0,I]],
    w=s_a^-1 s_b.                                         (1)

Thus w is an ordinary diagonal unit. The parameter t cancels entirely from
(1). In particular a leading `E_10(v(Db))` can be transported through L as
`E_10(v(Da))`; it changes only the ordinary output encoding. Repeatedly
varying this parameter cannot change whether a caller exists.

Consider the first interface `C=R_b diag(I,h_theta,I)` and any invertible
second interface Q over the entire fixed diagonal root-four algebra. An
ordinary left factor G_a reduces its endpoint to

    E'=L_w C' U Q L,
    C'=[[I,bh_theta,c],[0,dh_theta,e],[0,fh_theta,g]].        (2)

Ordinary outer factors preserve the Gaussian-type component ranks used by
the retained interface test.

## 2. The three forced steps

Suppose E' had only Gaussian types1,2,4, with each corresponding component
of rank D. The first row of `L_w C' U` is

    (a^2, -a^3+X, a c),       X=a b h_theta a.

Each one-column word in X has support at most two: move b through S, then
the two C_b factors act on the same bit pair. As in the source-support
proof, eight-support words cannot cancel words of support at most four or
exactly sixteen at sufficiently large faithful widths. The top output row
therefore forces

    q_01=q_12=0,            q_00 a=a q_11.                  (3)

The second row of `L_w C' U` is

    (w a, -w a^2+Y, w c+a e),
    Y=w b h_theta a+a d h_theta a.

Every word in Y has support at most two. Consequently

    E'_11=-w a^2 q_11 a+Y q_11 a+(w c+a e)q_21 a.

Only the first term can contain eight-support words: the other two have
support at most four. Since w is invertible, (3) strengthens to

    q_00=q_01=q_11=q_12=0.                                (4)

Invertibility of Q now forces q_02,q_10,q_21 to be units, by the same block
triangular argument as in the preceding obstruction.

The third output row has

    E'_20=f h_theta a q_10 a+g q_20 a+g q_21,
    E'_22=g q_22.

Its ordinary component is exactly g q_21, so g=0. Invertibility of the
lower two-by-two block of R'_b then forces e and f to be units.

## 3. The rank-two contradiction and scope

We have

    pi_2(E'_02)=a^2 q_02,
    E'_20=f h_theta a q_10 a,
    E'_22=0.

The first block is an invertible rank-two component. The middle block is
invertible and consists of four-support words; absence of non-Gaussian
components forces the whole block into pi_2(E'). Thus pi_2(E') has a
triangular invertible `2D by 2D` minor on output banks0,2 and input banks2,0,
regardless of its remaining top-left block. Its rank is at least2D, contrary
to the required D.

**Therefore no independent `(4,2,1)` endpoint exists in this class.** The
first matrix may be coherent and dense, the first clock may have any even
or odd exponent, the second diagonal algebra may be arbitrarily large but
fixed, and ordinary outer encodings are unrestricted. The declared
conditions `R_20=0` and invertible R_00 are essential to this statement.

Within this transported-routing approach, the next constructive interface
must escape at least one of them, or use a second interstage that actually
permutes addresses. The current explicit
construction uses a nontrivial conditional swap B(Db) of the two active
banks followed by coherent scalar shears. Its first column alternates
between e_0 and e_1, so R_00 is a proper phase projector. All first
interfaces and inverses remain explicit; R(Da)^-1 is still the known output
decoder for the rank-four component. No claim is made that these remaining
interfaces succeed.

## 4. Accounting

Equation (1) is an algebraic normalization and does not make an ordinary
encoding free. R_b,G_a and their inverses use their actual four scalar-sector
recipes; w is an explicit unit diagonal function of the two phase controls.
The clock, three native calls, all common-body services, scalar precision,
retained tapes and all other ordinary transformations remain paid. The
obstruction cannot yield a strict supplier or new kappa. All five foundations
remain. Credit @CubeJerry and the retained source, finite tensor-separation
and ordinary compiler contributors; Worker B with substantial OpenAI
assistance. Independent review remains separate.
