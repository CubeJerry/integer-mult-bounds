# Exact fourth-power admission for every four-bit Boolean sign source

**Proved analytic classification with explicit normalizers. The earlier 65,536-table census is supplementary evidence, not the proof. No profitable caller or new kappa.**

## 1. Statement

Use input bits x=(a,b,c,d), output bits y=(u,v,w,z), P(a,b,c,d)=(b,c,d,a), C_b=alpha I+(1-i)X_b/2 with alpha=(1+i)/2, and A_f=C_b D_f P for an arbitrary Boolean function f on four bits. Write its algebraic normal form over F2, with coefficient c_T on squarefree monomial T. Let eta=c_abcd, equivalently the parity of its 16 truth-table values.

There are explicit actual monomial row/column gauges reducing A_f⁴ to

    W_eta(r,s)=alpha⁴ (-i)^[|r xor s|]
                   (-1)^[eta r_2 r_3 s_0 s_1].             (1)

Consequently eta=0 gives an exact rank4 Gaussian endpoint C_a C_b C_c C_d, whereas eta=1 does not. The respective dephased binary row ranks are 4 and 5. For every positive tensor width V they are4V and5V; the latter obstruction persists even under arbitrary global monomial maps on all 16^V addresses, without eventual tensor-word faithfulness.

Thus every sign of degree at most3 supplies a rank4 endpoint, and a nonzero quartic term is the exact obstruction for this fourth power. There are 32,768 functions on each side. This does not assert infinite projective order for every even table; that property is proved separately for the selected f=acd source.

The retained Boolean native admission supplies A_f,A_f² with ranks1,2, and the distinct-three-query/Fano argument supplies its cube with rank3. The eta=0 family therefore has admitted powers1,2,3,4. Every actual source, gauge and inverse recipe remains paid.

## 2. Unique-path kernel and the complete cross-term table

For j=3,2,1,0, let b_j=(1-j) modulo4. Start at x and process these j in descending order: evaluate f(P^-j current), then set bit b_j to the corresponding bit of y. Let F_f(y,x) be the XOR of the four sign evaluations. The queried bits are distinct, so

    (A_f⁴)_(y,x)=alpha⁴ (-i)^[|x xor y|] (-1)^[F_f(y,x)].   (2)

The dephased real sign exponent is

    E_f(y,x)=x dot y+F_f(y,x)+F_f(y,0)+F_f(0,x)+F_f(0,0).    (3)

Here F_f(0,0)=4f(0)=0, but retaining it specifies the phase convention. The dependence on f is linear over F2. Constants and linear monomials give only removable row/column phases. The complete nonzero cross-term table for E_f-x dot y is:

| Monomial in f | Cross contribution |
|---|---|
| ab | bu+dw+az |
| ac or bd | aw+bz |
| bc or ad or cd | bw |
| abc | adw+buw+abz |
| abd | bdw+buz+awz |
| acd or bcd | abw+bwz |
| abcd | abdw+abwz+buwz |

Each row follows by the four substitutions in(2), then(3). By linearity this proves the formula for every f. Define

    q=c_ab,    r=c_ac+c_bd,    s=c_bc+c_ad+c_cd,
    p=c_abc,   h=c_abd,        k=c_acd+c_bcd.

Then, in the Boolean ring,

    E_f=x dot y+q(bu+dw+az)+r(aw+bz)+s bw
        +p(adw+buw+abz)+h(bdw+buz+awz)+k(abw+bwz)
        +eta(abdw+abwz+buwz).                              (4)

## 3. Explicit triangular coordinate and phase formulas

Define the column permutation V by

    V_0=a+q b,
    V_1=b,
    V_2=c+q d+r a+s b+p ad+h bd+k ab+eta abd,
    V_3=d+q a+r b+p ab.                                    (5)

It is invertible by recovering b,a,d,c in that order. Define the row permutation U by

    U_0=u+h wz,
    U_1=v+p uw+h uz+(k+q h+eta q)wz+eta uwz,
    U_2=w,
    U_3=z.                                                (6)

It is invertible by recovering w,z,u,v. These are actual four-bit permutations for every choice of the seven coefficient bits, including eta=1.

Boolean expansion gives the polynomial identity

    E_f(y,x)=U(y) dot V(x)+eta U_2(y) U_3(y) V_0(x) V_1(x). (7)

Without the eta*q term in U_1, the residual is eta*a*b*w*z. Adding eta*q*w*z changes it to eta*(a+q b)*b*w*z, exactly the term in(7). The checker verifies(7) symbolically in the Boolean polynomial ring on all 15 variables; assignment enumeration is not needed for this identity.

For r=U(y), define actual monomial gauges

    L |r> = i^[|r|-|U^-1(r)|+2F_f(U^-1(r),0)] |U^-1(r)>,
    R |x> = i^[|V(x)|-|x|+2F_f(0,x)+2F_f(0,0)] |V(x)>.
                                                                    (8)

Then equations(2),(3),(7) prove

    A_f⁴=L W_eta R.                                       (9)

All phases and alpha⁴ are retained. For eta=0, W_0 is literally the four-coordinate Gaussian. Tensoring(9) supplies actual normalizers for every width and phase residue. Inverse normalizers are the actual inverse tables. Every gauge is a fixed four-bit monomial with a Z4 phase table, admitted by the retained general fixed-table compiler with its full constant and restored dirty work. No growing gather or free nonordinary coefficient is assumed.

## 4. The monomial-equivalence invariant and its tensor law

For a full matrix whose cross ratios are real signs, dephase at one chosen row and column, then replace +1,-1 by 0,1. Its **dephased binary row rank** means the F2 dimension of the span of these binary rows. This definition uses the actual full coefficient matrix, not a Clifford quotient or a rank inferred from support size.

For(1), the binary rows are

    ell_r(s)=r_0 s_0+r_1 s_1+r_2 s_2+r_3 s_3
              +eta r_2 r_3 s_0 s_1.                      (10)

When eta=0 they span four coordinate functions. When eta=1 they also span s_0 s_1, obtained by XORing rows e_2,e_3,e_2+e_3. These five functions are independent. The row ranks are therefore 4 and 5.

The invariant is unchanged by arbitrary row/column permutations and unit-modulus row/column phase multiplication. Phase factors cancel in cross-ratio dephasing. Changing the reference row translates the binary row set by one of its elements, leaving the span unchanged. Changing the reference column sends a row v to v+v(column)*1. This is injective on the old row span because every old row vanishes at the old reference column, so the all-one vector is absent. Column permutation merely permutes coordinates. A rank5 matrix therefore cannot be monomial-equivalent to the rank4 Walsh matrix, even with phases more general than Z4.

The kernel W_eta is unitary: if two row indices differ in coordinate2 or3, the corresponding last input coordinate gives a zero Walsh sum. If those two coordinates agree, the quartic terms cancel and the usual remaining Walsh sum gives orthogonality. Alternatively, unitarity follows from(9).

For V tensor factors, a binary sign row is a sum of V functions(10) on disjoint blocks of four variables. The zero row occurs in every factor, each summand space has no constants, and different variable blocks are independent. Hence the binary row rank adds, giving(4+eta)V. The Gaussian on4V bits has rank4V. Arbitrary global monomial reindexing and phases preserve this rank. Thus eta=1 cannot become a pure rank4V Gaussian by tensoring or changing phase convention. Adding a spectator identity only repeats the same full-support components and cannot remove their invariant. Additional paid nonordinary operations or general bank mixing are outside this endpoint-equivalence obstruction.

## 5. Compatibility and verification

The eta=0 family gives structural freedom to choose a nonlinear source while keeping a literal fourth-power Gaussian. Source square admission, cube gauges, inverse-native admission, table compilation and phases must still be checked for the selected caller. The acd inverse witness is not asserted for every f.

A hypothetical three-native(4,2,1) caller still has nine source and four endpoint monomial services. Fixed recipe constants depend on f; the 29-SWAP/6-Toffoli/13-phase bound belongs specifically to acd. The common-body Gaussian invoice remains[25]+[23]+[22]-3[1]-6[7]-3[8]>0 at t=199/200, with all three inactive body services paid. No family member is a profitable caller solely because this arithmetic is favorable.

The verifier checks the 16 basis-monomial cross contributions, symbolic identity(7), all 128 effective parameter permutations and phases, actual A_f⁴ normalizers on a stated finite control set, normal-form rank4/rank5, and tensor-rank controls. It separately reproduces the full 65,536-table census as finite evidence. The all-width result is the written kernel, triangular permutation and invariant proof.

Credit @CubeJerry; the Boolean source family and monomial admission work; the fixed-table nonlinear compiler; the specific four-bit cubic source; Worker B with substantial OpenAI assistance. The complete caller, uniform supplier admission, recursive accounting and all global foundational obligations remain. No new complete kappa.
