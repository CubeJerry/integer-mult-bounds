# A constructive ordinary compiler for split noncommuting control algebras

**Sufficient physical implementation theorem, pending independent review.** This extends the retained cyclic common-determinant compiler to an explicitly split finite noncommuting group algebra. It supplies actual recipes and counts; a group-algebra unit or its inverse is not a free service. No Gaussian endpoint or supplier follows.

## Fixed data and literal phases

Let G be a fixed finite group of admitted literal root-four monomial tables. Each g and g^-1 has a fixed-table ordinary service with all phase, layout, traversal, tape, precision and compiler costs retained. The multiplication table is literal, including central scalar matrices when present. At widthV the service is g^⊗V. A literal one-column iI acts as i^V I, whereas an exterior coefficient i in K=Q(i) acts as iI. Do not identify those objects using only widthone.

Work in R=K[G]. Supply an explicit K-basis of matrix units e^λ_ab, 1<=a,b<=d_λ, with fixed group coefficients, satisfying

    e^λ_ab e^μ_cd = δ_(λμ) δ_(bc) e^λ_ad,
    sum_(λ,a) e^λ_aa = 1,
    sum_λ d_λ² = |G|.

The multiplication relations, identity and coefficient-basis independence are finite exact certificate obligations. This supplies the identification R≅product_λ Mat_(d_λ)(K). No unavailable splitting field or Fourier oracle is assumed.

Fix n>=2 existing banks, independently ofV. For Q in Mat_n(R), let Q_λ be its explicit scalar component matrix of size m_λ=n d_λ. Suppose there is a nonzero fixed δ inK such that

    det Q_λ = δ^(d_λ) for everyλ.                         (1)

**Theorem.** Q and Q^-1 have finite ordinary words on these n banks, without an extra whole-field owner, valid at every positive tensor width. The primitives are unweighted ADD, fixed nonzero SCALE and actual monomial services/inverses. Every coefficient and word length is fixed independently ofV. Condition(1) is sufficient, not asserted necessary. Testing that every Q_λ is merely invertible is not this compiler's admission test.

## Scalar elimination and the common determinant

Let D_δ scale bank0 byδ. In componentλ its determinant isδ^(d_λ), so U=D_δ^-1 Q has U_λ in SL_(m_λ)(K). Compile U and then perform the one exterior bank scaling D_δ. No conditional spectral scaling is presumed.

A matrix A in SL_m(K) has an explicit factorization into at most F(m)=(m−1)(m+9) scalar elementary transvections, with F(1)=0. Gauss-Jordan elimination uses at mostm−1 signed pivot swaps (three transvections each), at mostm(m−1) row additions, and m−1 balanced diagonal scalings (six transvections each). The latter use

    diag_ij(t,t^-1)=w_ij(t) w_ij(−1),
    w_ij(t)=E_ij(t) E_ji(−t^-1) E_ij(t).

Reverse the elimination sequence and negate elementary coefficients for the forward word. Only fixed-size scalar matrices overK are inverted, never growing physical bank matrices. For Q^-1, reverse the algebraic shear sequence and negate each coefficient, reverse the exterior scaling position, and lower the inverse shears anew by the same physical recipe. An inverse unweighted ADD is not treated as free.

## Lift internal component operations to real bank shears

Index componentλ coordinates by(bank i, internal indexa). A transvection between different banks i≠j lifts directly to

    I+α E_ij tensor e^λ_ab.                              (2)

For a transvection within banki, a≠b. Choose another bankj and any internal indexc, and put

    X=α E_ij tensor e^λ_ac,   Y=E_ji tensor e^λ_cb.

Then X²=Y²=YX=0 and XY=α E_ii tensor e^λ_ab. Consequently

    (I+X)(I+Y)(I−X)(I−Y)=I+α E_ii tensor e^λ_ab.           (3)

Thus four cross-bank shears implement the internal transvection. The borrowed bank can contain arbitrary input and is restored by the full identity. Execute the factors right to left in chronological order. No projected field is initialized or copied.

Concatenate these lifts for each scalar component factorization. Different components commute algebraically, but every primitive is executed and charged. The resulting identity holds in Mat_n(R). Applying g↦g^⊗V proves it at everyV, even if a component has zero multiplicity at some width.

## Lower each group-algebra shear and count it

For r=sum_g α_g g and i≠j,

    I+E_ij tensor r = product_g (I+α_g E_ij tensor g),     (4)

because E_ij²=0. Omit zero coefficients. For each remaining term execute:

    apply g to source bankj;
    SCALE(source j,α_g);
    ADD(destination i,source j);
    SCALE(source j,α_g^-1);
    apply g^-1 to source bankj.

The source is restored after each term. Identity g needs no service and unit coefficients may omit their SCALEs. This is the retained source-restoring monomial shear applied to explicit matrix-unit coefficients.

Set L=4 sum_λ F(n d_λ). Per forward or inverse application, a complete conservative bound is

    L|G| ADD,  2L|G|+1 SCALE,  2L(|G|−1) monomial services,
    zero extra whole-field owners and zero Gaussian queries.

These can be large fixed constants. Every monomial service retains the full-volume tariff O(N_field*((f log p)^tau+1)), with actual field volumeN_field, not tensor width. A finite compilation is not a profitable complete supplier invoice.

All monomials have norm1. Each scalar and its inverse are fixed, and every ADD has fixed amplification. Their finite product bounds every prefix independently ofV. A candidate must expose its actual coefficient heights and prefix bounds and retain the precision/tape invoice; no uniform conditioning promise is substituted.

## Concrete source-derived noncommuting control

Use the admitted source-square controls

    x=A^-2 D_a² A²,   y=A^-2 D_b² A²,
    t=R2^-1 SWAP_ab R2.

They are literal involutions, xy=yx and txt=y. The eight distinct tables x^u y^v t^e, u,v,e in{0,1}, formD8. Their tensor services supply a fixed noncommuting control algebra. The t table is exactly

    (a,b,c,d) -> (a,b,d xor ab,c xor ab), phase1,

implemented by one coordinate SWAP and two Toffolis. The x,y services use the admitted Boolean square recipes; every service and inverse is paid.

An explicit splitting of K[D8] has four scalar characters χ_(ε,η)(x)=χ_(ε,η)(y)=ε and χ_(ε,η)(t)=η, forε,η in{±1}, and one2×2 component

    ρ(x)=diag(1,−1), ρ(y)=diag(−1,1), ρ(t)=[[0,1],[1,0]].

Supply the matrix units as literal group coefficients

    e^λ_ab=(d_λ/8) sum_g ρ_λ(g^-1)_(b,a) g.

The checker verifies every product, the identity sum and eight-dimensional coefficient independence. Representation theory is not an unchecked physical premise for this example.

For the2×2 component,

    e11=(1+x−y−xy)/4,
    e12=(t+xt−yt−xyt)/4.

The single-bank nonmonomial unit Q_example=I+E_00 tensor e12 has determinant1 in every component and inverseI−E_00 tensor e12. Equation(3) with X=E_01 tensor e11 andY=E_10 tensor e12 gives an actual four-shear recipe on two existing banks. It changes only bank0 and restores bank1 for every arbitrary input. Fully lowering it uses16 ADD,32 SCALE and28 monomial services, without a new owner. The inverse has the same counts. The checker emits every primitive, verifies the exact group-algebra endpoint and inverse, and reconstructs the literal source/group tables. A second control exercises the general scalar-elimination and matrix-unit compiler on all five components.

## Provenance and remaining obligation

The cyclic common-determinant compiler is the predecessor: d_λ=1 reduces(1) to a commonδ. The new steps are the explicit noncommuting matrix-unit certificate, internal-coordinate four-shear lift, all-component determinant test and source-derivedD8 control. Earlier abstract semisimple factorization observations did not give these actual source-restoring recipes for internal component entries.

An arbitrary algebraic unit is still not automatically an admitted service. A candidate must supply its literal finite group, matrix units, coefficient field, determinant certificate, actual emitted word and complete cost/stability record. Root-four group phases remain literal at every width residue. Neither an independent421 endpoint nor a strict supplier, full recursion or any of the five foundations is established. Credit @CubeJerry, B's source controls, the retained cyclic/scalar/monomial compiler contributors, and this root extension, with substantial OpenAI assistance.
