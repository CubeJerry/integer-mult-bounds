# A parity-uniform ordinary alignment retaining the lower quartic residue

**Exact positive component identity, not an independent421 caller.** This extends the frozen aligned-projector control by replacing one projector with an exterior-i coherent route. It works at every positive tensor width and uses no marked column.

Retain the literal controls F=Za, H=A^-2 F A², Fhat=A F A^-1, Fback=A^-1 H A, active-square swap J, spectator swap S=SWAP_ab, Kdec=A J A² S A^-3, and B2=A³ S A. They are the controls in `ALIGNED-SELECTIVE-COMPONENT-v1.md`; Kdec and all sign controls are involutions. All operators below denote collective tensor lifts except external scalars.

For an arbitrary ordinary unit G define

    R_G=[[ (I-G)/2,(I+G)/2,0],[(I+G)/2,(I-G)/2,0],[0,0,I]].

In the scalar symmetric/antisymmetric bank basis this is diag(I,-G), hence it is a unit with inverse R_(G^-1). This definition permits G=iH with the **exterior field scalar i**, which stays i at every width.

Take

    C=diag(I,J,I) R_F,
    Q=diag(I,S,I) R_(iH) diag(I,S^-1,I),
    O=R_Fhat diag(I,Kdec^-1,I).

Set T=(I+i Fback)/2. Since Fback²=I,

    T^-1=I-i Fback, (I-T)^-1=I+i Fback,
    T(I-T)=I/2.

Use the ordinary input unit

    D=diag(T^-1,(I-T)^-1,I), R=D R_Fback.

The source intertwiners and the same exact Kdec table give the entire four-source term of E=L C U Q L after these endpoints:

    O[-(a C00 a,a C10 a,0)^T a[Q10 a,Q11 a,0]]R
        =[[-B2,-a⁴,0],[0,0,0],[0,0,0]].

The first block is a full-field Gaussian rank2 operator; the second is a full-field Gaussian rank4 operator. Their one-column words have ranks2 and4 with exact Gaussian gauges. Tensoring preserves the multiplicative identities; projector/route algebra is applied afterward to collective operators. Thus this is a full-D rank4 alignment with a nonzero full-D lower quartic residue at every width. It is not merely a width-one rank observation.

## Paid forward and inverse operations

The retained projector C and output O words cost6 ADD,7 SCALE,8 MONO each per direction. For the coherent Q route, use the scalar bank matrix H2=[[1,1],[1,-1]]. It has the chronological word ADD(1,0), SCALE(1,-2), ADD(0,1); its inverse is the same word followed by scaling both banks by1/2. The identity

    R_(iH)=H2^-1 diag(I,-iH) H2

therefore gives Q and Q^-1 in4 ADD,5 SCALE,3 MONO each, including the surrounding S/S^-1. Inverse Q replaces -i by+i; no tensor phase substitution is used.

For D, put t=T^-1 and t^-1=T. The balanced-diagonal identity

    w(t)=E01(t) E10(-t^-1) E01(t),
    w(t)w(-1)=diag(t,t^-1),
    D=diag(I,2,I) diag(t,t^-1,I)

implements D by ordinary source-restoring shears. Each coefficient is an explicit sum of at most two terms in I,Fback. For a coefficient alpha times a monomial Fback, apply Fback to the source, SCALE(alpha), ADD, SCALE(alpha^-1), then Fback again; the source is restored. Identity terms omit the monomial calls. No conditional one-bank inverse is a free operation.

D costs9 ADD,13 SCALE,6 MONO; D^-1 costs9 ADD,17 SCALE,6 MONO. Adding the projector input route gives R costs15 ADD,20 SCALE,13 MONO and R^-1 costs15 ADD,24 SCALE,13 MONO. Overall, the four ordinary forward services C,Q,O,R cost31 ADD,39 SCALE,32 MONO; their inverse services cost31 ADD,43 SCALE,32 MONO. The conservative maximum bank row-sum prefix bounds are5 for C and O,14 for Q,145 for R and76 for R^-1. All eight literal words are emitted by the checker. Existing three banks hold arbitrary data throughout, with no extra field owner. Every monomial is the admitted fixed literal table and retains full-field-volume traversal, precision, tape and compiler costs.

## Exact limitation

The two-source prefix K=(a C00 a,a C10 a,0)^T is an isometry and O K has only its top bank nonzero. Therefore its image is ordinary, with projector O^-1 diag(I,0,0) O. K and K a are pure ranks2 and3. The generalized ordinary-prefix-image theorem in `PURE-PREFIX-IMAGE-GATE-v3.md` excludes independent421 for every completion preserving this first C column, even though the displayed quartic residue is nonzero. The positive result proves that lower residue can be retained and compiled; it does not overcome the ordinary-range obstruction.

The exterior-i distinction is essential: replacing i H^tensor V by (iH)^tensor V changes the scalar to i^V. At even V it can make T singular. The checker rejects that substitution explicitly and verifies the universal collective-involution identities in both Fback sectors.

All checks use exact Gaussian rationals, pin source dependencies, and separately verify Gaussian classes rather than infer them from support alone. Credit @CubeJerry, retained source/gauge and compiler work, root's generalized-image review, and OpenAI-assisted Worker B construction. No new exponent or supplier claim.
