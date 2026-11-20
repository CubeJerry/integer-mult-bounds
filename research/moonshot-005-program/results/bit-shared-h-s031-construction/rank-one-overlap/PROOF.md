# Two protected H centres with a rank-one moving overlap

**Positive width3 component; independent admission pending. H642 needs one paid complement coordinate. No full bank3840 word or new kappa.**

A specialised rank-eight H642 provider permits a smaller moving-fibre construction than the earlier two-centre component. The first H fibre core has dimension22 instead of30. The two actual H centres remain H263 and H642, on donors0,61,62,45,100, with their same nine selected native ports.

The literal component passes all315 geometric and291 native source cuts, all72 complete geometric H fibre/readout checks, and five actual96-by96 early source bases at seed0. H263 uses an invertible rank9 provider. H642 uses a rank8 provider with an explicit one-dimensional information complement. All source tuples differ from their geometric bases at at most two quotients, giving the uniform propagation bound36<45 at the three two-edit donors and27<45 at the other two donors.

This is a nine-port width3 component only. The complementary width12 source component, all45 exits, full physical compiler/invoice, global common-H extension, later D/K/facet stages and the return target remain unbuilt here. In particular, smaller fibre-core dimension is not a claim that the third companion H now extends.

## 1. A specialised rank-eight second-centre provider

Use the general finite rank-eight construction proved in `rank-eight-provider`, now with the literal rows

    m=(43,44,10,45,49,17,7,29,1),
    n=(32,35,46,32,32,45,3,3,3),
    p=(4,53,11,7,10,60,62,9,47).

They give t=n/m=(38,44,58,17,6,60,55,28,3). The actual H642 chart and all9 port identifiers are unchanged. The checker reconstructs G,Q and P=G^(-1)Q from these rows and the actual linear/quadratic evaluation matrices. It verifies every source pencil on the transplanted common geometric fibre family.

For the shared donor61 pencil D_1(r), its second and third rows have one fixed right-kernel vector

    rho=(32,42,1)^T.

Thus at every actual H642 receiver i,

    D_1(r_i) rho = d_i e_0,

where d_i is nonzero because the complete3-by3 pencil is invertible. This fixed amplitude direction is what makes a rank-one source action possible. The complete provider still has rank8 and full three-port receiver readouts.

## 2. Source coordinates and the exact overlap prescription

Use the same common polynomial bank and node charts as the admitted two-centre construction. The first centre is node0 and the companion node is b=60. Its reflected actual source planes at the three first-centre donors are

| Donor | Companion plane |
| ---: | ---: |
| 0 | H116 |
| 61 | H642 |
| 62 | H643 |

Let U_a(v) be the normalized scalar geometric inverse-fibre polynomial from the retained Moore identity. Let S0 and Sb denote its six-dimensional scalar cores. Their intersection is span{1,z}.

At the20 receivers seeing both centres, prescribe the shared second-centre source map C_b by

    C_b (U_b(v_i) tensor I_3) = D_1(r_i),
    C_b (U_0(v_i) tensor I_3) = e_0 d_i lambda,
    lambda=(17,33,59).                                     (1)

The first prescription extends to every one of the36 H642 geometric receivers. The second is a rank-one map on the entire15-dimensional first-centre propagation through node b. The two prescriptions agree on their three-dimensional intersection, so they extend to one3-by48 source map. The emitted literal matrix certifies the extension exactly, including every prescribed column.

The unchanged first-centre central maps C_A,j annihilate the15-dimensional old companion propagation at receivers seeing both centres. Their restrictions on the old18-dimensional first-centre fibre core are the original invertible source pencils. All remaining source quotients are geometric evaluations, except that the same C_b is copied to the three reflected companion planes. The other two H642 donors receive the corresponding new rank-eight source pencils on the same companion core.

## 3. The new whole first-centre fibres have an explicit formula

At a receiver seeing both centres, define

    K_i' = U_0(v_i) tensor I_3
           + U_b(v_i) tensor (rho lambda).                 (2)

By(1), applying C_b to the first term gives e_0 d_i lambda; applying it to the second gives the same matrix. Their sum is zero in characteristic two. Every other visible off-H263 quotient is a geometric evaluation at a common zero of both scalar polynomials, so it also annihilates(2).

Each first-centre central map kills the correction term and has its original invertible pencil on the first term. Thus K_i' has dimension3, is the entire off-H263 inverse fibre, and retains the same common H263 readout. All three first-centre donors have this identical off-H map and identical whole uncertainty space. At a receiver not seeing the companion quotient, the whole inverse fibre remains U_0(v_i) tensor I_3.

For H642, the first-centre central map at donor61 still kills the old companion fibres. Hence the whole H642 fibre remains U_b(v_i) tensor I_3 at every receiver. Its new rank-eight provider gives the full common readout checked in Section1.

All new first-centre fibres lie in

    (S0 tensor F^3) + (Sb tensor span{rho}).                 (3)

The two summands have dimensions18 and6, and their intersection has dimension2. Therefore(3) has dimension22 over every coefficient extension. The literal fibres attain rank22, so this is the exact core dimension. Each of the20 affected fibres has a rank-one correction. The second-centre core remains dimension18.

The source cuts also follow by cases: unchanged views are geometric; views seeing only one edited centre use its invertible pencil; views seeing both centres have the same triangular source-coordinate block used in the earlier moving-fibres argument, with the rank-one lower off-diagonal term from(1). The checker independently reconstructs all315 actual geometric cuts instead of relying on these cases alone.

## 4. Costs and permitted scope

The H642 map has kernel spanned by (1,0,0,1,0,0,1,0,0). Selecting the first input coordinate is a rank-restoring complement. The separately reviewed paid-deficient-H compiler can account for that coordinate physically. No complement is omitted or called free here.

All fixed coefficient-field extensions preserve the explicit invertible minors, the rank-one prescription and the exact identities. Repeating r copies gives a first-centre core of dimension22r, a second-centre core of dimension18r, and complement dimension r. The noncommuting arbitrary-edit protection theorem applies to the fixed one/two-edit source tuples; the present provider construction itself is the explicit repeated component.

This local success does not resolve the continuation obstructions for frozen source/H data. Its value is a genuinely different two-centre fibre diagram with eight fewer core dimensions at the same bank width, coupled to a one-coordinate paid provider rather than the six-coordinate sum-only alternative.

## 5. Replay and literal evidence

```sh
python -B research/moonshot-005-program/results/bit-shared-h-s031-construction/rank-one-overlap/check.py --repo . --out /tmp/s031-rank-one-overlap-review
```

Expected receipt: `PASS_RANK_ONE_OVERLAP_TWO_H_COMPONENT`. `SOURCE-COEFFICIENTS.json.gz` contains every3-by48 source quotient and the second H word. `LITERAL-PROVIDER.json` contains the exact specialised rank-eight input. The emitted receipt includes all whole fibres, source counts, actual early bases, exact core ranks and the paid complement. The author checker does not serve as independent review.

Credit @CubeJerry, the retained S030 geometric/Desarguesian machinery, the S031 moving-fibres and rank-eight provider constructions, and the separately reviewed paid complement compiler. Substantial OpenAI assistance. No new complete kappa.
