# A native nine-port H provider with rank eight

**Positive source/readout component; independent admission pending. A one-dimensional paid complement is required. No complete global supplier or new kappa.**

This package constructs a physical9-by9 H642 signal map of rank8 with full common three-dimensional readouts at all36 geometric receivers, including all34 native receivers. It also supplies all three complete one-edit source tuples, all189 geometric and176 native source cuts, and three actual96-by96 early source bases. The retained ordinary additive identity target is used; donor10 and receiver80 are absent from this component.

The actual H642 donors are45,61,100. The physical D-port identifiers, in output order, are

    302,594,673,1089,1297,1509,1726,2230,3067.

This is a width3 component with nine selected exits. The remaining36 exits, a complementary width12 component, global H compatibility, D/K/facet continuation and the full physical invoice remain separate obligations.

## 1. General finite construction

Let E be the9-by3 linear evaluation matrix of the actual Desarguesian H642 chart, and E2 its9-by6 quadratic evaluation matrix. Let N be a full3-row annihilator of E2. For a receiver parameter r, put

    s=E r,           V(r)=diag(s) E.

The columns of V(r) lie in col(E2). At every actual receiver, exactly the three visible D ports have s_d=0. These facts are authenticated against the native atlas.

Choose m,n in row(N), with every coordinate of m,n,m+n nonzero. Put t=n/m, coordinatewise. Choose invertible row-basis changes so the first row of each of

    W0 = B0 N diag(1/(t+1)),
    W1 = B1 N,
    W2 = B2 N diag(1/t)

is the same row m. The first rows of B0 N,B1 N,B2 N are respectively m+n,m,n. The other two rows complete any bases; the package chooses the first available coordinate rows deterministically.

Choose a row p of length9 and set

    u = m p/(t+1),             v = m p/t.

Let G be the9-by9 matrix whose rows, in order, are

    m; u; u+v; W0[1]; W0[2]; W1[1]; W1[2]; W2[1]; W2[2].

Here row indices1,2 are the second and third rows. Let Q be the9-by9 map sending three input triples y0,y1,y2 to

    (0, y0_0+y1_0, y0_0+y2_0,
        y0_1,y0_2,y1_1,y1_2,y2_1,y2_2).

When G is invertible, define the physical provider

    P=G^(-1) Q.                                             (1)

Q has rank8 and kernel spanned by (1,0,0,1,0,0,1,0,0). Thus P has exactly rank8.

Define three3-by3 source pencils D_j(r). Their second and third rows are those of

    W0 diag(t) V(r),       W1 diag(t) V(r),       W2 V(r),

respectively. Replace their first rows by

    u V(r),               (m p) V(r),            v V(r),

respectively. All three pencils are linear in r. They arise by normalising the vanishing rows of a common-annihilator-row degeneration, but the proof below uses only finite identities and does not require a limit argument.

## 2. Exact common-readout identity

Put

    A(r) = [diag(t)V(r), V(r)],
    F(r) = [[D0(r),D0(r)], [D1(r),0], [0,D2(r)]].

Then

    G A(r)=Q F(r),             P F(r)=A(r).                  (2)

For the first row this uses m V(r)=n V(r)=0. For the next two rows it uses

    u t + m p=u,            (u+v)t=u.

The remaining rows follow from the quadratic annihilator identities: W0 annihilates diag(t+1)E2, W1 annihilates E2, and W2 annihilates diag(t)E2. These give the displayed blocks of F(r).

At the receiver's three visible ports, A(r) is zero. Restricting(2) to these rows gives

    P_visible,0 D0(r)=P_visible,1 D1(r)=P_visible,2 D2(r).     (3)

For the literal coefficient choice every D_j(r) and the common matrix in(3) is invertible at every one of the36 geometric receivers. Consequently those three physical port observations recover the sum of the three independent missing source coordinates. Equation(2) alone gives agreement; the explicit invertible minors are separately checked and are necessary.

## 3. Literal coefficients

All arithmetic is in GF64 with modulus x^6+x+1. The rows are

    m=(15,53,31,30,7,60,58,50,43),
    n=(43,63,36,47,6,25,20,57,16),
    p=(35,24,15,36,47,31,49,8,27).

They give t=(18,22,29,59,45,34,11,20,19). The stack of W0,W1,W2 has rank7, with their displayed common first row; G has rank9. The literal provider and all36 triples of source pencils are recorded in `LITERAL-PROVIDER.json`, and the checker regenerates them exactly from these rows and the native chart. The sample was found at deterministic seed1, but no random-search or generic-existence premise enters the theorem.

## 4. Complete one-edit sources and actual early bases

For each of the three donors, retain its27 geometric off-H642 quotients. Their whole inverse-H642 fibres have the form U_0(v) tensor I_3 and span an18-dimensional core. Extend each prescribed pencil D_j(r) to a3-by48 source map on that core and then choose the recorded deterministic free tail. The normalized fibre coordinate r is the actual binary-linear chart coordinate, so the prescribed pencil data have a consistent linear extension; the checker verifies every fibre rather than only the chosen core basis.

The central map is the only changed quotient. At views containing H642 its invertible pencil supplies the missing three dimensions. Other views are unchanged geometric views. The literal checker reconstructs all63 geometric views for each donor and all176 native views in total.

It also uses the actual native early quota at every source plane, preserving the designated H642 phase, and verifies three96-by96 early source bases at seed0. These are genuine source-phase matrices with the actual early owners. They do not make the rank-eight H provider itself invertible without its paid repair.

The four-edit protection theorem gives the stronger one-edit propagation bound27<45 for this width3 source, uniformly at every H/R pair. This is a source nonsaturation statement, not an extension theorem for other H centres.

## 5. The single missing coordinate is explicit

Let c select the first input coordinate of donor45. Then c is nonzero on the one-dimensional kernel of P, so

    rank [P;c]=9.

Eight independent actual rows of P followed by c form an invertible9-by9 basis. Removing c lowers the rank to8. Thus exactly one independent coordinate restores the provider's lost information. The separate `bit-paid-deficient-h-repair` compiler can account for this complement physically; this package supplies its literal rank hypothesis and does not re-price that compiler.

All fixed invertible minors and all identities persist over every finite extension of GF64. Repeating the component r times gives rank8r, complement dimension r, and full source/readout maps by tensoring with I_r. No claim is made about arbitrary source widths, a complementary width12 module, or a completed bank3840 word.

## 6. Replay

```sh
python -B research/moonshot-005-program/results/bit-shared-h-s031-construction/rank-eight-provider/check.py --repo . --out /tmp/s031-rank-eight-review
```

Expected receipt: `PASS_NATIVE_RANK_EIGHT_H642_COMPONENT`. The output contains literal full source maps, all whole fibres and receiver readouts, exact port ownership, independent output rows, the complement and the early-source receipts. A second implementation should reconstruct the finite matrices from the literal rows and raw native chart; the author executable is not an independent proof review.

Credit @CubeJerry, the retained native Desarguesian chart, S030 geometric source and quadratic-annihilator construction, and root's paid-complement compiler. Substantial OpenAI assistance. No new complete kappa.
