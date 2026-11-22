# An exact diagonal-pencil readout at the actual receiver95

**A constructive advance on the forced four-space. No common entire fifth
receiver, complete supplier, new exponent or foundational discharge.**

The previous two-overlap construction raised an unrestricted common response
from rank2 to4, and the third overlap lowered its donor contrast to27. Neither
could provide eight actual receiver95 output rows: the native support has32
coordinates, so eight independent common rows require contrast rank at most24.
This package gives an explicit physical D matrix attaining rank24 and makes
all eight actual receiver95 outputs agree injectively on the fixed four-space K.

Its native common-decoder space has dimension8, while the intersection of the
retained48/73 row spaces has dimension2. Thus a proposed universal equality of
those spaces is false. The construction uses a different algebraic mechanism.

## 1. Pinned interfaces and the two scalar sectors

Use the exact S032 interpolation matrices at baseline
`44f09459f91f8c3e27fcd45f54be7d043e6493b7`. Let L be the fixed96-by-32 common
frame for receivers6,9,48,73, and write K=L W. The first two8-row blocks of W
are zero. For F=(4,5,7,8), exact matrices C48 and C73 satisfy

    W48 = T_old[O48,F] C48,
    W73 = T_old[O73,F] C73.

Let H0=C48+C73. The certificate verifies H0 invertible and

    C48 H0^(-1) = Dα = diag(53,53,58,58),
    C73 H0^(-1) = I + Dα.                              (2)

All numbers are GF64 polynomial-basis encodings with modulus x^6+x+1; the
addition sign denotes field addition, hence XOR. These are exact identities,
not floating point approximations.

## 2. A third inverse-section family

Choose nonzero field values d_p different from1 at every actual D input p.
Let Δ=diag(d_p), and enforce on the four special columns

    Δ_F = Dα (I+Dα)^(-1).                              (3)

Write G for the eight rows of the new D word at receiver48. Choose invertible
8-by-8 matrices M,N and place the retained73 and actual95 rows as

    T'[O73,:] = M G Δ,
    T'[O95,:] = Q = N G (I+Δ^(-1))^(-1).               (4)

The construction retains the original48/F and73/F rectangles and the complete
88-entry rectangle from the exact affine-family theorem. Every retained native
section G_Ij must be invertible. The explicit point also verifies all144
geometric D sections, both19/16 phase blocks and the full44 local systems.

Let P_j be any source-to-D map satisfying the four old common-frame identity
readouts for T'. Because K lies in L, its ingress B_j=P_j K is forced on K,
regardless of the free source extension. Equations(2)-(4) imply

    (B_j)_Ij H0^(-1)
      = G_Ij^(-1) G_F Dα
        + Δ_Ij^(-1) G_Ij^(-1) G_F Δ_F (I+Dα)
      = (I+Δ_Ij^(-1)) G_Ij^(-1) G_F Dα.

Therefore the actual receiver95 outputs are

    Q B_j = N G_F Dα H0                               (5)

for every native donor j. This common8-by-4 matrix has rank4: G_F has rank4,
and N,Dα,H0 are invertible. The actual eight-row receiver section is invertible
as well, because

    Q_Ij = N G_Ij (I+Δ_Ij^(-1))^(-1).

Thus the mechanism supplies a genuine injective common response at the eight
specified physical output rows, rather than only at a hypothetical decoder.
This conclusion is local to K and does not imply its off-D isolation.

## 3. Shared physical rows and chronology

Receiver48 and73 have actual shared rows10 and30, which also occur at95.
They cannot be assigned three unrelated values. The constructor chooses M
block diagonal with four early and four late rows. Its phase blocks are fixed
by the old F rectangles and(3). For each shared row let e be its unit row in
G and let m be the corresponding row of M. For every input column p impose

    (e + d_p m) G[:,p] = 0.                           (6)

These are linear column constraints and give the same shared row in G and
M G Δ. Select the corresponding row of N to be e+m. Then

    (e+m)G[:,p] d_p/(d_p+1) = e G[:,p],

so the95 row agrees as well. The rest of each four-row phase block of N is
completed to an invertible basis. The literal M and N are in the certificate.

Early G rows are zero at late input columns. Block diagonal M,N and column
scaling preserve those zeros. All other physical D coefficients are filled
within the same phase pattern, with the retained F rectangle fixed. The
chosen literal point has phase ranks19 and16 and all144 geometric sections
of rank8, including receiver95 at every native donor. No new owner, route or
D input is introduced by this matrix construction. A chronological binary
compilation and its costs are handled in the separate physical-source work.

## 4. Exact point and independent checks

`PENCIL-CANDIDATE.json.gz` records the whole35-by-35 D matrix, all d_p, M,N,
and one canonical protected source extension. It is deterministic seed22 of
the explicit constructor; no probability premise is retained.

For the native donors J, let V=union I_j, of size32, and

    Z = [B_j-B_61] over j in J other than61.

The exact certificate gives:

| Quantity | Value |
| --- | ---: |
| rank Z | 24 |
| rank[Z B_61] | 28 |
| Actual95 contrast response rank | 0 |
| Actual95 common response rank on K | 4 |
| Native common-decoder dimension | 8 |
| Intersection of retained48/73 native row spaces | 2 |
| Additional common-decoder dimensions beyond that intersection | 6 |
| Retained local interpolation systems | 44 |
| Geometric D sections of rank8 | 144 |
| Early/late D phase ranks | 19/16 |

`check.py` uses the separate GF64 arithmetic from the parent exact-family
checker. It imports no construction executable. It reconstructs actual D
owners from the raw balanced-atlas routes and the geometry from the root,
A2 and D4 tables, checks(2)-(6) against the literal point, all144 sections,
all44 prescribed source images and the exact rank counts. Corrupting an actual
receiver95 coefficient breaks commonness; corrupting a diagonal parameter
breaks the displayed pencil identity. The separate adversarial review uses
another arithmetic implementation and records its exact coverage explicitly.

Reproduce the explicit point and verify it from the repository root:

```sh
python3 -B research/moonshot-005-program/results/bit-coupled-fifth-s033/wave3/construct.py \
  --repo . --out /tmp/s033-pencil-construction
python3 -B research/moonshot-005-program/results/bit-coupled-fifth-s033/wave3/check.py \
  --repo . --out /tmp/s033-pencil-verification
```

The checker reports `PASS_ACTUAL95_DIAGONAL_PENCIL_FORCED_K_READOUT`.
The constructor reuses the pinned predecessor geometry/arithmetic; that replay
is not independent verification. The checker performs its own exact arithmetic
and physical index reconstruction from literal inputs.

## 5. The next obstacle is actual proper isolation

The fixed K has dimension4, while a complete receiver95 fibre must have
dimension8 per base bank. Equation(5) repairs its actual D output values but
says nothing about unwanted proper records outside D1509.

The separately checked physical H-to-proper maps still give nonzero off-D
responses on K for every donor except61. The four D-parent leak ranks are2
at donors0,45,62,100 and4 at32,35,38,68,69,90. At61 the rank is0. K is in the
span of the four retained frames, so those parent values are fixed by T' and
the retained identity readouts. Free source extensions outside that span cannot
remove these particular leaks. A global right-gauge lift can preserve full
source ranks and nonsaturation, but it does not change this parent-on-K fact.

For the next coupled D candidate, necessary equations are

    B95_off(j,h) sum_r M(j,h,r) S'(j,r)^(-1) W_r = 0

at each actual D parent h. Here B95_off is the real H-to-proper restriction to
records visible at95 outside D1509, and the sum runs over the four retained
receivers (only48 and73 contribute for this K). These exact extra equations
must be imposed alongside the actual common-readout identity. Alternatively,
change the H word, the retained common frames, the relevant source routing or
the isolation contract and account for that change explicitly.

Thus this candidate closes the specific actual readout deficiency on K and
supplies six common-decoder dimensions outside the overlap mechanism. It does
not solve the complete fifth receiver. The canonical local source extension
is not admitted as a full source; the separately constructed global lift has
its own proof, verification and cost ledger.

## 6. Open next questions and status

First determine whether the diagonal-pencil family can also satisfy the new
proper-isolation equations without losing its phases or sections. If it can,
construct the remaining four dimensions of the common whole receiver95 fibre
and all full source constraints. If it cannot, identify the necessary changed
H/source interface rather than returning to overlap-only decoder searches.

The identities in Sections1-3 persist over coefficient-field extensions and
under tensoring this exact construction with I_k. Arbitrary noncommuting new
pencil blocks are not asserted. Both complete strict suppliers, the full
H/D/K/facet word, paid return, recursive caller and all five foundational
assumptions remain open. No new complete κ.

Credit @CubeJerry; S031/S032 source/H/D contributors and independent reviewers;
S033 adversarial work identifying the stronger actual95 gate; inherited
geometry, atlas and compiler authors. Substantial OpenAI assistance, with
independent agent review distinct from independent human or kernel proof.
Apache-2.0.
