# A concrete nonclean idle interface reduces421 to a two-bank42 endpoint

**Exact constructive interface and paid ordinary recipe, not a completed caller.**
This makes the actual remaining equation explicit after the clean-first gates.
Use the literal a and natives L,U. Let u,b,f be ordinary operators, f a unit,
and require beta=a^-1 b a ordinary. Put

    C=[[I,b,0],[0,I,I],[u,f+u b,0]],
    Q=[[p,q,0],[r,t,0],[-p-beta r,-q-beta t,I]],
    Q_A=[[p,q],[r,t]] an ordinary unit.                 (1)

All multiplication orders in(1) are literal. Neither u nor b must commute
with anything. C and Q are ordinary units. Define

    B=[[I,b],[u,f+u b]],
    L_A=[[a,0],[I,a]], U_A=[[a,-a²],[0,a]].

Then the middle output row of E=L C U Q L is EXACTLY(0,0,a), and the top
and bottom outputs on the first two inputs are

    M42=diag(a,I) B U_A Q_A L_A.                       (2)

Their last input column is zero. Consequently an ordinary equivalence
M42 ~ diag(G4,G2) supplies a genuine independent421 endpoint, using all
three input banks; the isolated third job is a, not an ordinary idle value.
The remaining equation is(2), with exact ordinary input/output gauges still
required. Merely getting component ranks16 at widthone would not solve it.

## Derivation and nonclean witness

The middle row of L C U is(a,b a,a)=a(I,beta,I). Equation(1) makes
(I,beta,I)Q=(0,0,I), and multiplication by the final L preserves that last
row. The top/bottom submatrix of L C U on columns0,1 is diag(a,I) B U_A;
its column2 is zero. This proves both claims directly.

The simplest case is b=0,f=I,u=S^-1D_b. This u is a literal monomial unit,
while A u A^-1 has support4 and is nonordinary. The first input really feeds
the idle output through u, escaping the clean-first-column obstruction.
A u A has rank1; the untwisted S^-1 instead gives A S^-1 A=X_b S ordinary.
These collapse identities can be used within Q_A, which must escape the
square-algebra gate. No positive Q_A or endpoint is asserted here.

A less restrictive family allows b=D_c or its powers: A^-1 D_c A=D_d is
ordinary, but D_c need not commute with u. Boolean sign tables also have
ordinary backward conjugates. Such b changes the active corner in(2) while
preserving the exact isolated rank1 row.

## Ordinary lowering and owner accounting

For monomial u,b,f,beta, the following fixed sequence implements C:

1. bank0 += b(bank1).
2. swap banks1,2.
3. bank1 += bank2.
4. apply f to bank2.
5. bank2 += u(bank0).

Each monomial shear uses one whole-field ADD and two actual monomial services
(apply to the source, ADD to the destination, inverse on the source), restoring
its source. Inverting the displayed sequence supplies C^-1. No clean or extra
whole-field owner is used. A conservative in-place SWAP uses3 ADD and3 sign
SCALE primitives. A negative ADD can be implemented by two extra sign SCALE operations on
its source. Therefore C costs at most6 ADD,9 SCALE,2 b-services,
2 u-services and1 f-service in each direction, including the inverse signs
and omitting identity/zero terms when appropriate. The corresponding ADD-prefix norm bound is at most64;
monomials and sign scales have norm1.

Q is diag(Q_A,I), followed by bank2 -= beta(bank1), then bank2 -= bank0.
Outside the still-uncompiled Q_A, this costs at most2 ADD,4 sign SCALE
and2 beta-services per direction, even with an unsigned ADD primitive. Its wrapper-prefix norm bound is at most4. The inverse
uses the reverse signed shears and the actual inverse of Q_A. An arbitrary
matrix inverse is not treated as a free physical service.

All monomial services use the admitted actual compact bridge on full physical
field volume, with their fixed coordinate/phase recipes and the inherited
O(volume*((f log p)^tau+1)) tariff. Constant one-column phases tensor to i^V,
not exterior i. The branch-free all-input algebra is valid for every positive
width; the necessary Gaussian-component gates additionally use faithful V0.

The three-native body invoice remains3[1]+6[7]+3[8], with target[25]+[23]+[22]
and optimistic gross difference about0.560590248972 at t=199/200 before the
ordinary/endpoint/precision/source expenses. A Q_A solving(2), its two exact
ordinary endpoint gauges, full compiler and inverse recipes, both strict
suppliers, precision and recursion are still missing. This interface produces
no new kappa or claimed saving. Credit @CubeJerry and retained native/source,
ordinary compiler, tensor and component contributors; OpenAI-assisted work.
