# A four-bit nonlinear native source with an exact rank-four endpoint

**Proved source and endpoint construction, with retained conditional physical/compiler interfaces. No profitable caller, complete supplier, or new kappa.**

## 1. Literal source

Use four address bits(a,b,c,d), encoded a+2b+4c+8d. Let P rotate them to(b,c,d,a), let D_f have diagonal sign(-1)^f for f(a,b,c,d)=acd, and put

    alpha=(1+i)/2,
    C_j=alpha I+(1-i)X_j/2,
    S=D_f P,    A=C_b S.                                    (1)

Equivalently S applies the input sign(-1)^(abd) and then the displayed rotation. Its implementation must evaluate this input phase.

Define actual monomial maps on input bits:

    J_cd : (a,b,c,d) -> (a xor cd,b,c,d), phase i^(cd),
    R4   : (a,b,c,d) -> (a,b,c xor ab,d),
           phase i^[ab(1+2c+2d)],
    L4   : (a,b,c,d) -> (a,b xor cd,c,d),
           phase i^[cd(2a+2b-1)].                            (2)

Both L4 and R4 are involutions: the two phase exponents on each exchanged pair sum to a multiple of4. Set

    R2=J_cd S²=P² R4.                                      (3)

Then the exact phase-preserving identities are

    A²=C_a C_b R2,
    A⁴=L4 C_a C_b C_c C_d R4.                              (4)

Thus A,A²,A⁴ have pure Gaussian ranks1,2,4 with actual ordinary gauges. The retained arbitrary-Boolean family separately supplies a rank3 cube gauge, but neither the proof of(4) nor the proposed(4,2,1) caller relies on its normalization algorithm.

## 2. Native source admission and the shared square/fourth gauge

Since P sends X_b to X_a,

    S X_b S^-1=D_f X_a D_f=(-1)^(cd) X_a.

The sign is independent of a. The retained monomial admission calculation applies with g=cd, giving R2=J_cd S² and

    C_b S=A,
    S^-1 C_a R2=A,
    C_a C_b R2=A².                                         (5)

These are the source gauges for the actual native orientations

    N0(a_V)=[[a_V,0],[I,a_V]],
    N2(a_V)=[[a_V,-a_V²],[0,a_V]],    a_V=A^tensor V.         (6)

The original native ADD and boundary services remain paid. No new independent input, erased owner or nonordinary source coefficient is introduced.

Directly, S²=D_(acd+bcd) P². On original input(a,b,c,d), R2 has output(c xor ab,d,a,b) and phase i^[ab(1+2c+2d)], exactly P² R4. Let B0=C_a C_b P². Since P² exchanges the first and last pair of bits,

    B0²=C_a C_b C_c C_d,
    A²=B0 R4,
    B0 R4 B0^-1=L4.                                       (7)

The last relation follows from(4), using R4²=I. The square and fourth-power endpoints therefore share the identical actual right gauge R4 after the ordinary P² in the square.

## 3. Direct all-column proof of the fourth power

Write input x=(a,b,c,d) and output y=(u,v,w,z). Four Gaussian stages query four distinct bits, so there is one path per input/output pair. The cyclic permutations cancel because P⁴=I. The coefficient is

    (A⁴)_(y,x)=alpha⁴ (-i)^[(a xor u)+(b xor v)+(c xor w)+(d xor z)]
                 (-1)^[abd+abw+bwz+uwz].                  (8)

The signs are evaluated as abd before changing c, abw before changing d, bwz before changing a, and uwz before changing b. This derives(8) from the actual source without a Hadamard-classification assumption.

Define U(y)=(u,v xor wz,w,z) and V(x)=(a,b,c xor ab,d). Their binary dot product is

    U(y) dot V(x)=y dot x+abw+bwz.                          (9)

The remaining signs in(8) depend only on row(uwz) or column(abd). The four-Gaussian coefficient at row U(y),column V(x) is

    alpha⁴ (-i)^[|U(y)|+|V(x)|] (-1)^[U(y) dot V(x)].

Comparison with(8) supplies row phase i^[|U(y)|-|y|+2uwz] and column phase i^[|V(x)|-|x|+2abd]. The row map from input U(y) to output y is L4, and the column map is R4; their phases simplify to(2). This proves(4) for every column, retaining alpha⁴. Tensoring proves(3)--(7) for every positive V with each actual width phase.

## 4. Infinite projective order and the denominator-bearing trace

The cube satisfies

    tr(A³)=3(1-i)/2.                                       (10)

In A³ the Gaussian stages change b,a,d after P³. A diagonal path exists exactly when original b=c. For the eight triples(a,b,d), its amplitude is

    alpha³ (-i)^[(a xor d)+(b xor a)+(d xor b)] (-1)^(abd).

The000 and111 contributions cancel; the other six have two flips and positive sign, contributing -alpha³ each. Thus the sum is -6alpha³, as claimed.

Also det(A)=1: C_b has determinant i^8=1 on its eight fibers; D_f has two negative entries; and each coordinate SWAP in P exchanges four address pairs. If A^n=lambda I, its determinant gives lambda^16=1. Every eigenvalue of A would be a root of unity, making tr(A³) an algebraic integer. Equation(10) is not in Z[i], a contradiction. Thus A has infinite projective order.

At the prime1+i, (10) has valuation-1. A full invariant lattice over its valuation ring, even after a finite field extension, would make the cube trace integral. Such a lattice cannot exist. This genuinely escapes that retained finite-group invariant-lattice premise; it does not claim that all other source or caller obstructions have vanished.

## 4a. Fresh inverse witness for this source

Let Rev reverse the four coordinates(a,b,c,d)->(d,c,b,a), let Z_all be the parity sign(-1)^(a+b+c+d), and put T=Z_all Rev. These two ordinary factors commute, so T²=I. Direct conjugation gives

    Rev A^-1 Rev = P D_abd C_c^-1 = D_acd C_b^-1 P
                   = C_b^-1 D_acd P.

The last commutation is valid because acd is independent of b. Conjugating by Z_all, which commutes with D_acd and P, gives

    T A^-1 T=-i A.                                         (14)

This is a fresh four-bit proof. It does not transfer the old three-bit witness. At width V, a_V^-1=(-i)^V T_V a_V T_V. The literal native identities N0(a)^-1=J_bank N2(a^-1) J_bank and N2(a)^-1=J_bank N0(a^-1) J_bank therefore supply inverse-head natives with one opposite-orientation native and four paid T services, two quarter-phase scalar passes before fusion, and two bank-role swaps. Each T service is two coordinate SWAPs plus one parity-phase pass; no new nonlinear gate is required. These extra costs are **additional** to(11) whenever an inverse-head native is used.

The wrapped source keeps its fresh forward rank-seven body. A literal inverse of the complete body-times-head source additionally needs the ordinary translation on all seven body Gaussian coordinates on both active roles, as in the retained inverse-native accounting. A cancelled body cannot also be credited at the endpoint.

## 5. Paid physical recipes and optimistic Gaussian invoices

All nonlinear operations above are explicit Toffoli permutations and Z4 phases of degree at most3. The already admitted compact Toffoli/cubic-phase bridge applies directly; the general fixed-table compiler gives an alternative lowering. No new four-bit oracle or growing table service is assumed.

One native wrapper(5) uses S,R2,S^-1: three actual monomial services, with an uncompressed recipe bounded by eight coordinate SWAPs, one Toffoli and three phase passes. Four head coordinates are retained, including the inactive coordinates of each Gaussian call.

A hypothetical three-native(4,2,1) endpoint is normalized using L4^-1,R4^-1 on the first job, R2^-1 on the second, and S^-1 on the third. Source plus endpoint normalization totals thirteen monomial services, with explicit recipe bound

    29 coordinate SWAPs + 6 Toffoli gates + 13 phase passes.  (11)

Each SWAP may instead be three CNOTs. These are fixed recipe constants, and every pass pays its inherited movement/precision tariff. All actual interstage shears, role cycles, scalars, clocks, inverse wrappers and extra endpoint encodings must be added. Formula(11) is not a substitute for constructing that caller.

If each native introduces a fresh rank-seven body and all three independent roles receive all three bodies, the three inactive rank-seven services are paid. With [r]=r^t,

    P_G=3[1]+6[7]+3[8].                                    (12)

The ambient coordinate count is4+21=25. Spectators on lower-rank jobs remain in the common volume; no volume is dropped. The optimistic(4,2,1) target is

    T_421=[25]+[23]+[22].                                  (13)

At t=199/200, exact integer-root intervals in the checker enclose a positive margin near0.56059024897207293124164032535765. Profile(4,2,2) has credit[25]+2[23] and margin near1.54022086114340869169037199495069. These are complete Gaussian invoices for the stated native/idle counts. They do not include the missing caller's ordinary costs or prove complete supplier admission.

The substantive new option is that a profitable(4,2,1) target may retain one rank1 component; the former(3,2,2) interface had to remove all such components. At least one square-cross orientation is needed for a rank4 path in three calls. The extended two-native total-head gate remains applicable. A separate two-role/three-native(4,3) profile is also arithmetically positive if its actual rank3 endpoint and caller are supplied, with no third-role idles; this package makes no construction claim for it.

The inherited compiler tariff, native premises, uniformity, precision, source access, ownership and full recursive accounting remain obligations. No fixed ordinary constant is silently declared free.

## 6. Verification and boundaries

The exact checker verifies literal S,R2,L4,R4 tables, their inverse properties, equations(3)--(7), the cube trace and determinant factors, and full tensor-column controls at widths1 and2. It encloses the two displayed margins with integer arithmetic. Removing the source cubic phase, a fourth-power permutation correction, or its quarter phases is a negative control.

The separate exhaustive census of65,536 four-bit Boolean tables is finite classification evidence and is not used in this proof. No parity-classification theorem or general claim about powers of arbitrary Boolean sources is imported. The inverse admission used here is the separate explicit four-bit witness(14), with its full extra wrapper invoice.

Credit @CubeJerry; the retained native and exact monomial admission work; the Boolean source-family construction and compact nonlinear-control bridge; Worker B with substantial OpenAI assistance. All five global foundations remain. No complete new kappa.
